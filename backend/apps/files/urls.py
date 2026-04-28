# urls.py
from django.urls import path

from .views import DocumentViewSet

urlpatterns = [
    path(
        "documents/",
        DocumentViewSet.as_view({"get": "list", "post": "create"}),
        name="document-list",
    ),
    path(
        "documents/<int:pk>/",
        DocumentViewSet.as_view(
            {"get": "retrieve", "put": "update", "delete": "destroy"}
        ),
        name="document-detail",
    ),
]
