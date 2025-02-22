import os
from langchain_ollama import OllamaLLM
from constants import TEMPERATURE

OLLAMA_BASE_URL = os.getenv("OLLAMA_SERVER_URL", "http://ollama:11434")
OLLAMA_MODEL = os.getenv("OLLAMA_MODEL", "deepseek-r1:1.5b")


class DiaryLLM:
    def __init__(self) -> None:
        self.llm = OllamaLLM(
            model=OLLAMA_MODEL, base_url=OLLAMA_BASE_URL, temperature=TEMPERATURE
        )

    def get(self):
        return self.llm
