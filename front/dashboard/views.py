import requests
from datetime import datetime
from django.shortcuts import render


def dashboard(request):
    return render(request, "dashboard.html", {})


def mood_chart(request):
    query_obj = {
        "start_date": "2020-01-01",
        "end_date": datetime.today().strftime("%Y-%m-%d"),
    }
    response = requests.get("http://langchain-api:8000/api/mood_graph/", json=query_obj)
    moods = response.json()["moods"]
    return render(
        request,
        "charts/mood_chart.html",
        {
            "data": [mood["mark"] for mood in moods],
            "categories": [mood["happened_at"] for mood in moods],
        },
    )


def tags(request):
    response = requests.get("http://langchain-api:8000/api/tags/", json={})
    tags_dict = response.json()["tags"]
    return render(
        request,
        "tags/list.html",
        {
            "tags": tags_dict,
        },
    )


def tag(request, tag_id):
    response = requests.get(f"http://langchain-api:8000/api/tags/{tag_id}", json={})
    tag_response = response.json()
    return render(
        request,
        "tags/show.html",
        {"tag": tag_response["tag"], "diary_records": tag_response["diary_records"]},
    )
