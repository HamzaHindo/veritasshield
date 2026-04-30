# urls.py
from django.urls import path

from .views import DocumentClausesView, DocumentViewSet

urlpatterns = [
    path(
        "documents/",
        DocumentViewSet.as_view({"get": "list"}),
        name="document-list",
    ),
    path(
        "documents/<int:pk>/",
        DocumentViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="document-detail",
    ),
    path(
        "documents/<int:doc_id>/clauses/",
        DocumentClausesView.as_view(),
        name="document-clauses",
    ),
]
