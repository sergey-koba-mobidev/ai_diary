from models import postgres_session, DiaryRecord, Tag


class GenerateAll:
    def __init__(self) -> None:
        self.session = postgres_session()

    def run(self):
        diary_records = (
            self.session.query(DiaryRecord)
            .filter(DiaryRecord.llm_response != None)
            .all()
        )
        for diary_record in diary_records:
            diary_record.tags = []
            self.session.commit()
            for llm_tag in diary_record.llm_response["tags"]:
                tag = self._get_or_create_tag(llm_tag.lower())
                diary_record.tags.append(tag)
                self.session.commit()

    def _get_or_create_tag(self, title):
        tag = self.session.query(Tag).filter_by(title=title).first()
        if tag:
            return tag
        else:
            tag = Tag(title=title)
            self.session.add(tag)
            return tag
