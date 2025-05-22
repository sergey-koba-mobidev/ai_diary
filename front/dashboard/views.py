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
    response = requests.post(
        "http://langchain-api:8000/api/mood_graph/", json=query_obj
    )
    moods = response.json()["moods"]
    return render(
        request,
        "charts/mood_chart.html",
        {
            "data": [mood["mark"] for mood in moods],
            "categories": [mood["happened_at"] for mood in moods],
        },
    )
