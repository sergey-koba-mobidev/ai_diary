from models import postgres_session, DiaryRecord, Person, Action


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
            diary_record.actions = []
            self.session.commit()
            for llm_person in diary_record.llm_response["subjects"]:
                if isinstance(llm_person, dict):
                    if "name" in llm_person:
                        name = llm_person["name"].lower()
                        actions = llm_person["actions"]
                    else:
                        key = list(llm_person.keys())[0]
                        name = key.lower()
                        actions = llm_person[key]
                else:
                    name = llm_person[0].lower()
                    actions = llm_person[1]
                person = self._get_or_create_person(name)
                for llm_action in actions:
                    action = Action(
                        diary_record_id=diary_record.id,
                        person_id=person.id,
                        name=llm_action,
                    )
                    self.session.add(action)
                self.session.commit()

    def _get_or_create_person(self, name):
        person = self.session.query(Person).filter_by(name=name).first()
        if person:
            return person
        else:
            person = Person(name=name)
            self.session.add(person)
            return person
