from fastapi import FastAPI
from annotations.mood_graph import MoodGraphRequest, MoodGraphAnswer
from operations.mood.get_graph import GetGraph

app = FastAPI()


@app.post("/api/mood_graph/")
async def mood_graph(moodRequest: MoodGraphRequest) -> MoodGraphAnswer:
    """
    Return array of moods for specified date range
    """
    moods = GetGraph(moodRequest.start_date, moodRequest.end_date).run()
    return MoodGraphAnswer(moods=moods)
