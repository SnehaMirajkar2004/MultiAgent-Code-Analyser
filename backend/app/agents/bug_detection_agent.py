from app.agents.base_agent import BaseAgent


class BugDetectionAgent(BaseAgent):
    name = "Bug Detection Agent"

    def build_prompt(self, code: str) -> str:
        return f"""You are a Bug Detection Agent. Your ONLY job is to find
syntax errors, logical bugs, edge-case failures and potential runtime
errors in the given Python code. Do NOT comment on style/naming or
complexity — other agents handle that. Be conservative: only report a bug
if you are reasonably confident it is a real issue, since false positives
hurt the system's precision.

Respond with ONLY a valid JSON object in exactly this shape, no extra text:

{{
  "bugs": [
    {{
      "type": "syntax | logical | runtime | edge-case",
      "description": "what the bug is, and why it's a bug",
      "severity": "Low | Medium | High",
      "location_hint": "line number or code snippet where it occurs"
    }}
  ],
  "summary": "1-3 sentence overall bug-risk summary"
}}

If there are no bugs, return an empty "bugs" list but still give a summary.

Python code to analyze:
```python
{code}
```"""
