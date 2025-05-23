from fastapi import FastAPI
from annotations.mood_graph import MoodGraphRequest, MoodGraphAnswer
from annotations.tags import TagsAnswer, TagDetailsAnswer
from operations.mood.get_graph import GetGraph
from operations.tag.get_all import GetAll
from operations.tag.get import Get

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
    tags = GetAll().run()
    return TagsAnswer(tags=tags)


@app.get("/api/tags/{tag_id}")
async def tag(tag_id) -> TagDetailsAnswer:
    """
    Return tag with details
    """
    tag_details = Get(id=int(tag_id)).run()
    return TagDetailsAnswer(
        tag=tag_details["tag"], diary_records=tag_details["diary_records"]
    )
