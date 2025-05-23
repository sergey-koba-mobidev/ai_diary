from datetime import date
from pydantic import BaseModel, Json
from typing import Any, List


class Tag(BaseModel):
    id: int
    title: str
    diary_records_count: int


class TagsAnswer(BaseModel):
    tags: List[Tag]


class DiaryRecord(BaseModel):
    id: int
    summary: str
    happened_at: date
    # llm_response: Json[Any]


class TagDetailsAnswer(BaseModel):
    tag: Tag
    diary_records: List[DiaryRecord]
