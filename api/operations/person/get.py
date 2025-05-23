from models import postgres_session, Person


class Get:
    def __init__(self, id) -> None:
        self.session = postgres_session()
        self.id = id

    def run(self):
        person = self.session.query(Person).filter(Person.id == self.id).first()
        actions = sorted(
            person.actions, key=lambda item: item.diary_record.happened_at, reverse=True
        )
        return {
            "person": {
                "id": person.id,
                "name": person.name,
                "actions_count": len(actions),
            },
            "actions": [
                {
                    "id": row.id,
                    "description": row.name,
                    "diary_record_id": row.diary_record.id,
                    "happened_at": row.diary_record.happened_at,
                }
                for row in actions
            ],
        }
