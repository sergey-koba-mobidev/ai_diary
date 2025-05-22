from django.urls import path

from .views import dashboard, mood_chart

urlpatterns = [path("", dashboard), path("mood_chart", mood_chart)]
