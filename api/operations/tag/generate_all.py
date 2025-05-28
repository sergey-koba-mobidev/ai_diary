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
            tags = []
            diary_record.tags = []
            self.session.commit()
            for llm_tag in diary_record.llm_response["tags"]:
                tag_title = llm_tag.lower()
                tag = self._get_or_create_tag(tag_title)
                if not tag_title in tags:
                    tags.append(tag_title)
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
