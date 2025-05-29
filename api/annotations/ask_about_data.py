from pydantic import BaseModel


class AskAboutDataRequest(BaseModel):
    query: str


class AskAboutDataAnswer(BaseModel):
    answer: str
