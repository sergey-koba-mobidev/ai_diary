from models import postgres_session, Tag, diary_records_tags_association
from sqlalchemy import func, desc


class GetAll:
    def __init__(self) -> None:
        self.session = postgres_session()

    def run(self):
        tags = (
            self.session.query(
                Tag,
                func.count(diary_records_tags_association.c.diary_record_id).label(
                    "total"
                ),
            )
            .join(diary_records_tags_association)
            .group_by(Tag)
            .order_by(desc("total"))
            .all()
        )
        return [
            {
                "id": row[0].id,
                "title": row[0].title,
                "diary_records_count": row[1],
            }
            for row in tags
        ]
