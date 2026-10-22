"""
Thin wrapper around the Gemini API.

Every agent sends a system-style instruction + the user's code, and asks
Gemini to reply with ONLY a JSON object. This module takes care of:
  - calling the model with automatic multi-model fallback on rate-limits (429)
  - stripping markdown code fences if the model adds them anyway
  - safely parsing JSON (falling back to a readable error object instead
    of crashing the whole request)
"""

import json
import re
import time
import google.generativeai as genai

from app.config import GEMINI_API_KEY, GEMINI_MODEL

if GEMINI_API_KEY:
    genai.configure(api_key=GEMINI_API_KEY)

# List of models to try in sequence if a model hits free-tier rate limits / quota limits
FALLBACK_MODELS = [
    GEMINI_MODEL,
    "gemini-3.5-flash",
    "gemini-flash-latest",
    "gemini-3.1-flash-lite",
]


def _strip_code_fences(text: str) -> str:
    text = text.strip()
    # Try finding JSON wrapped inside ```json ... ``` code fence
    fence_match = re.search(r"```(?:json)?\s*(\{.*?\})\s*```", text, re.DOTALL)
    if fence_match:
        return fence_match.group(1).strip()
    # Fallback to finding the JSON object boundaries from first '{' to last '}'
    json_match = re.search(r"\{.*\}", text, re.DOTALL)
    if json_match:
        return json_match.group(0).strip()
    return text


def call_gemini_json(prompt: str, agent_name: str, retries: int = 1) -> dict:
    """
    Calls Gemini with the given prompt and expects a JSON object back.
    If a model hits 429 quota/rate limits, automatically fails over to
    backup Gemini models (e.g. gemini-3.5-flash, gemini-flash-latest).
    """
    if not GEMINI_API_KEY:
        return {
            "error": True,
            "message": f"{agent_name}: GEMINI_API_KEY is not configured on the backend."
        }

    last_error = None

    for model_name in FALLBACK_MODELS:
        try:
            model = genai.GenerativeModel(model_name)
            for attempt in range(retries + 1):
                try:
                    response = model.generate_content(
                        prompt,
                        generation_config={
                            "temperature": 0.2,
                            "response_mime_type": "application/json",
                        },
                    )
                    raw_text = response.text or ""
                    cleaned = _strip_code_fences(raw_text)
                    return json.loads(cleaned)

                except json.JSONDecodeError as e:
                    last_error = f"Could not parse JSON from model response: {e}"
                except Exception as e:
                    err_str = str(e)
                    last_error = err_str
                    # If 429 quota limit hit on current model, break to switch fallback model
                    if "429" in err_str or "Quota exceeded" in err_str or "ResourceExhausted" in err_str:
                        print(f"[{agent_name}] Rate limit on {model_name}. Switching fallback model...")
                        break

                time.sleep(1.0 * (attempt + 1))

        except Exception as model_err:
            last_error = str(model_err)

    if "429" in str(last_error) or "Quota exceeded" in str(last_error):
        friendly_msg = (
            f"{agent_name}: Free Tier Quota Limit reached (429). "
            "Please wait ~30 seconds before analyzing again, or check your Google AI Studio quota."
        )
    else:
        friendly_msg = f"{agent_name} failed: {last_error}"

    return {
        "error": True,
        "message": friendly_msg
    }
