from django.urls import path

from .views import ClauseAnalysisView

urlpatterns = [
    path(
        "<int:clause_id>/",
        ClauseAnalysisView.as_view(),
        name="clause-analysis",
    ),
]
