from pydantic import BaseModel
from typing import List


class Tag(BaseModel):
    id: int
    title: str
    diary_records_count: int


class TagsAnswer(BaseModel):
    tags: List[Tag]
