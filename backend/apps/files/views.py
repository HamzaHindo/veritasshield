from rest_framework import permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet

from .models import Document
from .serializers import DocumentSerializer
from .services.document_services import DocumentService


class DocumentViewSet(ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = DocumentSerializer

    def get_queryset(self):
        return Document.objects.filter(user=self.request.user)


class DocumentClausesView(APIView):
    """
    Handles retrieval of clauses for a specific document.
    """

    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, doc_id):
        """
        Route: GET /files/documents/<int:doc_id>/clauses/
        Action: Retrieve all clauses associated with a document.
        """
        service = DocumentService()
        clauses = service.get_document_clauses(doc_id)
        if clauses:
            return Response(clauses, status=status.HTTP_200_OK)
        else:
            return Response({"error": "Clauses not found"}, status=status.HTTP_404_NOT_FOUND)
