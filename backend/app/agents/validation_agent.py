import json
from app.gemini_client import call_gemini_json

VALIDATION_AGENT_NAME = "Validation Agent"


def build_validation_prompt(code: str, review: dict, bugs: dict, complexity: dict, performance: dict) -> str:
    findings_json = json.dumps(
        {
            "code_review": review,
            "bug_detection": bugs,
            "complexity_analysis": complexity,
            "performance_optimization": performance,
        },
        indent=2,
    )

    return f"""You are the Validation Agent in a multi-agent code-analysis
system. Four specialized agents (Code Review, Bug Detection, Complexity
Analysis, Performance Optimization) have already analyzed the Python code
below and produced the findings shown in FINDINGS_JSON.

Your job:
1. Check the findings against the actual code (does the reported bug
   really exist in this code? does the complexity estimate look right?
   are the optimization suggestions actually valid?).
2. Check whether the four agents' outputs are internally consistent with
   each other (e.g. a bug the Performance Agent relies on but the Bug
   Detection Agent didn't mention).
3. Classify EACH bug finding and EACH optimization suggestion as one of:
   "Confirmed" (clearly correct on inspection), "Likely" (plausible but not
   fully certain), or "Unsupported" (doesn't hold up against the code).
4. Give an overall confidence level for the whole report.

Respond with ONLY a valid JSON object in exactly this shape, no extra text:

{{
  "bug_validations": [
    {{"description": "short reference to the bug", "verdict": "Confirmed | Likely | Unsupported", "note": "why"}}
  ],
  "optimization_validations": [
    {{"description": "short reference to the suggestion", "verdict": "Confirmed | Likely | Unsupported", "note": "why"}}
  ],
  "consistency_notes": "any contradictions found between agents, or 'No contradictions found.'",
  "overall_confidence": "High | Medium | Low",
  "validated_summary": "2-4 sentence final summary for the developer, written after cross-checking everything above"
}}

Python code:
```python
{code}
```

FINDINGS_JSON:
{findings_json}
"""


def run_validation_agent(code: str, review: dict, bugs: dict, complexity: dict, performance: dict) -> dict:
    prompt = build_validation_prompt(code, review, bugs, complexity, performance)
    return call_gemini_json(prompt, VALIDATION_AGENT_NAME)
