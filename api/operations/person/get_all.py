from models import postgres_session, Person, Action
from sqlalchemy import func, desc


class GetAll:
    def __init__(self) -> None:
        self.session = postgres_session()

    def run(self):
        persons = (
            self.session.query(
                Person,
                func.count(Action.person_id).label("total"),
            )
            .join(Action)
            .group_by(Person)
            .order_by(desc("total"))
            .all()
        )
        return [
            {
                "id": row[0].id,
                "name": row[0].name,
                "actions_count": row[1],
            }
            for row in persons
        ]
