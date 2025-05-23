import json
from models import postgres_session, Tag


class Get:
    def __init__(self, id) -> None:
        self.session = postgres_session()
        self.id = id

    def run(self):
        tag = self.session.query(Tag).filter(Tag.id == self.id).first()
        diary_records = sorted(
            tag.diary_records, key=lambda item: item.happened_at, reverse=True
        )
        return {
            "tag": {
                "id": tag.id,
                "title": tag.title,
                "diary_records_count": len(diary_records),
            },
            "diary_records": [
                {
                    "id": row.id,
                    "summary": row.llm_response["summary"],
                    "happened_at": row.happened_at,
                    # "llm_response": json.dumps(row.llm_response),
                }
                for row in diary_records
            ],
        }
