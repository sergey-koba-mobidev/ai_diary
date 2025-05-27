from datetime import date, datetime
from pydantic import BaseModel
from typing import List


class SleepsRequest(BaseModel):
    start_date: date
    end_date: date


class Sleep(BaseModel):
    id: int
    deep_sleep_time: int
    shallow_sleep_time: int
    rem_time: int
    total_sleep_time: int
    wake_time: int
    start_at: datetime
    stop_at: datetime
    naps: int
    happened_at: date


class SleepsAnswer(BaseModel):
    sleeps: List[Sleep]
