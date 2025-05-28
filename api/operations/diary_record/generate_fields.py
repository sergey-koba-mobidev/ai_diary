import json
from models import postgres_session, DiaryRecord


class GenerateFields:
    def __init__(self) -> None:
        self.session = postgres_session()

    def run(self):
        diary_records = (
            self.session.query(DiaryRecord)
            .filter(DiaryRecord.llm_response != None)
            .all()
        )
        for diary_record in diary_records:
            llm_response = diary_record.llm_response
            illness = llm_response["illness"]
            if isinstance(illness, dict) or hasattr(illness, "__len__"):
                illness = json.dumps(illness)
            diary_record.mood = llm_response["mood"]
            diary_record.mood_mark = llm_response["mood_mark"]
            diary_record.health = llm_response["health"]
            diary_record.health_mark = llm_response["health_mark"]
            diary_record.health_reason = llm_response["health_reason"]
            diary_record.weather = llm_response["weather"]
            diary_record.illness = illness
            diary_record.summary = llm_response["summary"]
            self.session.commit()
