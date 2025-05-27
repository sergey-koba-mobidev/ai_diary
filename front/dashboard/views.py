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
    moods_response = requests.get(
        "http://langchain-api:8000/api/mood_graph/", json=query_obj
    )
    moods = moods_response.json()["moods"]
    sleeps_response = requests.get(
        "http://langchain-api:8000/api/sleeps/", json=query_obj
    )
    sleeps = sleeps_response.json()["sleeps"]
    return render(
        request,
        "charts/mood_chart.html",
        {
            "moods_data": [
                {"y": mood["mark"], "x": mood["happened_at"]} for mood in moods
            ],
            "sleeps_data": [
                {"y": sleep["total_sleep_time"] / 60, "x": sleep["happened_at"]}
                for sleep in sleeps
            ],
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


def persons(request):
    response = requests.get("http://langchain-api:8000/api/persons/", json={})
    persons_dict = response.json()["persons"]
    return render(
        request,
        "persons/list.html",
        {
            "persons": persons_dict,
        },
    )


def person(request, person_id):
    response = requests.get(
        f"http://langchain-api:8000/api/persons/{person_id}", json={}
    )
    person_response = response.json()
    return render(
        request,
        "persons/show.html",
        {"person": person_response["person"], "actions": person_response["actions"]},
    )
