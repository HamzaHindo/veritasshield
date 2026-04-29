from django.urls import path

from .views import AnalyzeSaveView, AnalyzeView

urlpatterns = [
    path("analyze/", AnalyzeView.as_view(), name="analyze"),
    path("analyze/save/", AnalyzeSaveView.as_view(), name="analyze-save"),
]
