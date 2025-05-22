from datetime import date
from pydantic import BaseModel
from typing import List


class MoodGraphRequest(BaseModel):
    start_date: date
    end_date: date


class Mood(BaseModel):
    mark: int
    description: str
    happened_at: date


class MoodGraphAnswer(BaseModel):
    moods: List[Mood]
