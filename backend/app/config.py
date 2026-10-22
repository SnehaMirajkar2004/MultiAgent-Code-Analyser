import os
from dotenv import load_dotenv

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
GEMINI_MODEL = os.getenv("GEMINI_MODEL", "gemini-3.6-flash")
DATABASE_URL = os.getenv("DATABASE_URL", "postgresql+pg8000://postgres:postgres@localhost:5432/code_analyzer")


if not GEMINI_API_KEY:
    print(
        "\n[WARNING] GEMINI_API_KEY is not set. "
        "Create a .env file in the backend folder (copy .env.example) "
        "and paste your Gemini API key there.\n"
    )
