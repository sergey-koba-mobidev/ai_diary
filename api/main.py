from fastapi import FastAPI
from typing import Any
from annotations.mood_graph import MoodGraphRequest, MoodGraphAnswer
from annotations.sleeps import SleepsRequest, SleepsAnswer
from annotations.tags import TagsAnswer, TagDetailsAnswer
from annotations.persons import PersonsAnswer, PersonDetailsAnswer
from annotations.ask_about_data import AskAboutDataRequest
from operations.mood.get_graph import GetGraph
from operations.sleep.get_list import GetList
from operations.tag.get_all import GetAll as GetAllTags
from operations.tag.get import Get as GetTag
from operations.person.get_all import GetAll as GetAllPersons
from operations.person.get import Get as GetPerson
from operations.text_to_sql.get_result import GetResult

app = FastAPI()


@app.get("/api/mood_graph/")
async def mood_graph(mood_request: MoodGraphRequest) -> MoodGraphAnswer:
    """
    Return array of moods for specified date range
    """
    moods = GetGraph(mood_request.start_date, mood_request.end_date).run()
    return MoodGraphAnswer(moods=moods)


@app.get("/api/sleeps/")
async def sleeps(sleeps_request: SleepsRequest) -> SleepsAnswer:
    """
    Return array of sleeps for specified date range
    """
    sleeps_list = GetList(sleeps_request.start_date, sleeps_request.end_date).run()
    return SleepsAnswer(sleeps=sleeps_list)


@app.get("/api/tags/")
async def tags() -> TagsAnswer:
    """
    Return array of tags
    """
    tags_list = GetAllTags().run()
    return TagsAnswer(tags=tags_list)


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
    persons_list = GetAllPersons().run()
    return PersonsAnswer(persons=persons_list)


@app.get("/api/persons/{person_id}")
async def person(person_id) -> PersonDetailsAnswer:
    """
    Return person with details
    """
    person_details = GetPerson(id=int(person_id)).run()
    return PersonDetailsAnswer(
        person=person_details["person"], actions=person_details["actions"]
    )


@app.post("/api/ask_about_data/")
async def ask_about_data(ask_about_data_request: AskAboutDataRequest) -> Any:
    """
    Return json with data of SQL query generated from user input
    """
    response = GetResult(user_input=ask_about_data_request.query).run()
    return response
