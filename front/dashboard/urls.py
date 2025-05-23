from django.urls import path

from .views import dashboard, mood_chart, tags

urlpatterns = [path("", dashboard), path("mood_chart", mood_chart), path("tags", tags)]
