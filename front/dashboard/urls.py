from django.urls import path

from .views import dashboard, mood_chart, tags, tag, persons, person

urlpatterns = [
    path("", dashboard),
    path("mood_chart", mood_chart),
    path("tags", tags),
    path("tags/<int:tag_id>", tag),
    path("persons", persons),
    path("persons/<int:person_id>", person),
]
