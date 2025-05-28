from pydantic import BaseModel


class AskAboutDataRequest(BaseModel):
    query: str
