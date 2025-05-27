from models import postgres_session, Sleep


class GetList:
    def __init__(self, start_date, end_date) -> None:
        self.session = postgres_session()
        self.start_date = start_date
        self.end_date = end_date

    def run(self):
        sleeps = (
            self.session.query(Sleep)
            .filter(Sleep.happened_at <= self.end_date)
            .filter(Sleep.happened_at >= self.start_date)
            .order_by(Sleep.happened_at)
            .all()
        )
        return [
            {
                "id": row.id,
                "deep_sleep_time": row.deep_sleep_time,
                "shallow_sleep_time": row.shallow_sleep_time,
                "rem_time": row.rem_time,
                "total_sleep_time": row.total_sleep_time,
                "wake_time": row.wake_time,
                "start_at": row.start_at,
                "stop_at": row.stop_at,
                "naps": row.naps,
                "happened_at": row.happened_at,
            }
            for row in sleeps
        ]
