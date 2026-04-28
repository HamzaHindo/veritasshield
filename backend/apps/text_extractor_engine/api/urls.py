from django.urls import path

from .views import ContractUploadView

urlpatterns = [
    path("upload/", ContractUploadView.as_view()),
]
