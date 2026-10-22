from app.agents.base_agent import BaseAgent


class PerformanceAgent(BaseAgent):
    name = "Performance Optimization Agent"

    def build_prompt(self, code: str) -> str:
        return f"""You are a Performance Optimization Agent. Your ONLY job is
to identify genuine efficiency problems (unnecessary loops, redundant
computation, inefficient data structures, avoidable O(n^2)+ patterns) in the
given Python code, and suggest optimizations. Follow the principle of
SELECTIVE intervention: do NOT suggest a change unless it produces a real,
justified improvement in execution performance and/or algorithmic
complexity. If the code is already efficient, say so instead of inventing
an unnecessary change.

Respond with ONLY a valid JSON object in exactly this shape, no extra text:

{{
  "suggestions": [
    {{
      "issue": "what is inefficient and why",
      "suggestion": "concrete optimization to apply",
      "expected_improvement": "e.g. 'O(n^2) -> O(n)' or 'reduces redundant recomputation'"
    }}
  ],
  "is_already_efficient": true or false,
  "summary": "1-3 sentence overall performance summary"
}}

If no genuine optimization opportunity exists, return an empty "suggestions"
list and set "is_already_efficient" to true.

Python code to analyze:
```python
{code}
```"""
