from app.agents.base_agent import BaseAgent


class CodeReviewAgent(BaseAgent):
    name = "Code Review Agent"

    def build_prompt(self, code: str) -> str:
        return f"""You are a Code Review Agent. Your ONLY job is to review the
readability, naming, structure, maintainability and coding-practice quality
of the given Python code. Do NOT look for bugs or estimate complexity —
other agents handle that.

Respond with ONLY a valid JSON object in exactly this shape, no extra text:

{{
  "issues": [
    {{
      "title": "short title",
      "description": "what the issue is and where",
      "severity": "Low | Medium | High",
      "suggestion": "concrete suggested fix"
    }}
  ],
  "summary": "1-3 sentence overall code-quality summary"
}}

If there are no issues, return an empty "issues" list but still give a summary.

Python code to review:
```python
{code}
```"""
