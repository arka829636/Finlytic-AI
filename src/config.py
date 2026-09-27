import os
from pathlib import Path

from dotenv import load_dotenv

PROJECT_ROOT = Path(__file__).resolve().parents[1]

load_dotenv(PROJECT_ROOT / ".env")

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "").strip()

OPENAI_MODEL = os.getenv(
    "OPENAI_MODEL",
    "gpt-5.6"
).strip()

MOCK_LLM = os.getenv(
    "MOCK_LLM",
    "true"
).strip().lower() == "true"


def is_llm_configured() -> bool:
    """Return True when live LLM configuration is available."""
    return bool(OPENAI_API_KEY)