from fastapi import FastAPI
from annotations.mood_graph import MoodGraphRequest, MoodGraphAnswer
from annotations.tags import TagsAnswer, TagDetailsAnswer
from annotations.persons import PersonsAnswer, PersonDetailsAnswer
from operations.mood.get_graph import GetGraph
from operations.tag.get_all import GetAll as GetAllTags
from operations.tag.get import Get as GetTag
from operations.person.get_all import GetAll as GetAllPersons
from operations.person.get import Get as GetPerson

app = FastAPI()


@app.get("/api/mood_graph/")
async def mood_graph(moodRequest: MoodGraphRequest) -> MoodGraphAnswer:
    """
    Return array of moods for specified date range
    """
    moods = GetGraph(moodRequest.start_date, moodRequest.end_date).run()
    return MoodGraphAnswer(moods=moods)


@app.get("/api/tags/")
async def tags() -> TagsAnswer:
    """
    Return array of tags
    """
    tags = GetAllTags().run()
    return TagsAnswer(tags=tags)


@app.get("/api/tags/{tag_id}")
async def tag(tag_id) -> TagDetailsAnswer:
    """
    Return tag with details
    """
    tag_details = GetTag(id=int(tag_id)).run()
    return TagDetailsAnswer(
        tag=tag_details["tag"], diary_records=tag_details["diary_records"]
    )


@app.get("/api/persons/")
async def persons() -> PersonsAnswer:
    """
    Return array of persons
    """
    persons = GetAllPersons().run()
    return PersonsAnswer(persons=persons)


@app.get("/api/persons/{person_id}")
async def person(person_id) -> PersonDetailsAnswer:
    """
    Return person with details
    """
    person_details = GetPerson(id=int(person_id)).run()
    return PersonDetailsAnswer(
        person=person_details["person"], actions=person_details["actions"]
    )
