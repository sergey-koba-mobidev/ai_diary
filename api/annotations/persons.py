from datetime import date
from pydantic import BaseModel
from typing import List


class Person(BaseModel):
    id: int
    name: str
    actions_count: int


class PersonsAnswer(BaseModel):
    persons: List[Person]


class Action(BaseModel):
    id: int
    description: str
    diary_record_id: int
    happened_at: date


class PersonDetailsAnswer(BaseModel):
    person: Person
    actions: List[Action]
