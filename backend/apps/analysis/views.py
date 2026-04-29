from apps.files.models import Document
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .serializers import (
    AnalysisResultSerializer,
    DocumentSaveInputSerializer,
    DocumentUploadInputSerializer,
)
from .services.analysis_service import AnalysisService


class AnalyzeView(APIView):
    """
    Handles document analysis workflows.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Route: POST /api/analyze/
        Action: Upload file -> OCR -> Analyze -> Return Result
        """
        # 1. Validate Input using the new Serializer
        input_serializer = DocumentUploadInputSerializer(data=request.data)
        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        validated_data = input_serializer.validated_data
        file_obj = request.FILES.get("file")
        if not file_obj:
            return Response(
                {"error": "No file provided. Use multipart/form-data."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        title = request.data.get("title", file_obj.name)
        lang = request.data.get("language", "en")

        try:
            # Call the service to handle DB creation, OCR, and Inspection
            result = AnalysisService.inspect_uploaded_file(
                user=request.user, file_obj=file_obj, title=title, lang=lang
            )

            serializer = AnalysisResultSerializer(result)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Exception as e:
            return Response(
                {"error": "Analysis failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )


class AnalyzeSaveView(APIView):
    """
    Handles saving/inserting analysis for an existing document.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Route: POST /api/analyze/save/
        Body: { "doc_id": 123 }
        Action: Fetch Doc -> Validate Text -> Insert/Save Analysis
        """
        input_serializer = DocumentSaveInputSerializer(data=request.data)
        if not input_serializer.is_valid():
            return Response(input_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        doc_id = request.data.get("doc_id")
        try:
            # Call the service to handle fetching and insertion
            result = AnalysisService.insert_uploaded_file(
                user=request.user,  # Passed in case permissions need checking inside service
                doc_id=doc_id,
            )

            # Serialize the Dataclass result to JSON
            serializer = AnalysisResultSerializer(result)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except ValueError as e:
            # Handle specific business logic errors (e.g., missing raw_text)
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        except Document.DoesNotExist:
            return Response(
                {"error": "Document not found"}, status=status.HTTP_404_NOT_FOUND
            )
        except Exception as e:
            return Response(
                {"error": "Insertion failed", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
