from app.gemini_client import call_gemini_json


class BaseAgent:
    """
    Every specialized agent extends this class. Each agent only needs to
    define its own `name` and `build_prompt(code)` — the actual Gemini
    call and JSON handling is shared here.
    """

    name = "BaseAgent"

    def build_prompt(self, code: str) -> str:
        raise NotImplementedError

    def run(self, code: str) -> dict:
        prompt = self.build_prompt(code)
        result = call_gemini_json(prompt, self.name)
        return result
