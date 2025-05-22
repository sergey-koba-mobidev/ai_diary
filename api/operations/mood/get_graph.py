from models import postgres_session, DiaryRecord


class GetGraph:
    def __init__(self, start_date, end_date) -> None:
        self.session = postgres_session()
        self.start_date = start_date
        self.end_date = end_date

    def run(self):
        diary_records = (
            self.session.query(DiaryRecord)
            .filter(DiaryRecord.llm_response != None)
            .filter(DiaryRecord.happened_at <= self.end_date)
            .filter(DiaryRecord.happened_at >= self.start_date)
            .order_by(DiaryRecord.happened_at)
            .all()
        )
        return [
            {
                "mark": row.llm_response["mood_mark"],
                "description": row.llm_response["mood"],
                "happened_at": row.happened_at,
            }
            for row in diary_records
        ]
