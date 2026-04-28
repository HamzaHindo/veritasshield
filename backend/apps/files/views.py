from rest_framework import permissions
from rest_framework.viewsets import ModelViewSet

from .models import Document
from .serializers import DocumentSerializer


class DocumentViewSet(ModelViewSet):
    permission_classes = [permissions.IsAdminUser]
    queryset = Document.objects.all()
    serializer_class = DocumentSerializer
