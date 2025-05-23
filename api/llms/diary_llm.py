import os
from constants import TEMPERATURE
from langchain_google_genai import ChatGoogleGenerativeAI

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY", "")
MODEL = "gemini-2.5-flash-preview-05-20"  # gemini-2.5-flash-preview-05-20 has unsolved bug https://github.com/langchain-ai/langchain-google/issues/936


class DiaryLLM:
    def __init__(self) -> None:
        os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
        self.llm = ChatGoogleGenerativeAI(
            model=MODEL,
            temperature=0,
            max_tokens=None,
            timeout=None,
            max_retries=2,
        )

    def get(self):
        return self.llm
