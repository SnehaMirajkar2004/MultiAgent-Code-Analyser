from app.agents.base_agent import BaseAgent


class ComplexityAgent(BaseAgent):
    name = "Complexity Analysis Agent"

    def build_prompt(self, code: str) -> str:
        return f"""You are a Complexity Analysis Agent. Your ONLY job is to
estimate the time complexity and space complexity of the given Python code
using Big-O notation, and briefly explain your reasoning. Do NOT comment on
style, bugs, or optimizations — other agents handle that.

Respond with ONLY a valid JSON object in exactly this shape, no extra text:

{{
  "time_complexity": "e.g. O(n^2)",
  "space_complexity": "e.g. O(1)",
  "explanation": "brief reasoning for both estimates, referencing the loops/recursion/data structures involved"
}}

Python code to analyze:
```python
{code}
```"""
