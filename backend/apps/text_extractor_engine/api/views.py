# views.py
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.files.serializers import DocumentSerializer  # Import your serializer

from ..services.ocr_service import OCRService
from ..services.pdf_service import pdf_to_images


class ContractUploadView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # 1. Initialize serializer with request data and files
        serializer = DocumentSerializer(data=request.data, context={"request": request})

        # 2. Validate data
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # 3. Save the instance (creates the Document row in DB)
        # Note: We pass user here because 'user' is read_only in the serializer
        try:
            document = serializer.save(user=request.user)
        except Exception as e:
            return Response(
                {"error": "Failed to save document", "details": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # 4. Perform OCR Processing
        file_path = document.file.path

        try:
            if file_path.lower().endswith(".pdf"):
                images = pdf_to_images(file_path)

                full_text = []
                confidences = []

                for img in images:
                    result = OCRService.extract(img)
                    full_text.append(result["text"])
                    confidences.append(result["confidence"])

                text = "\n".join(full_text)
                confidence = sum(confidences) / len(confidences) if confidences else 0.0

            else:
                # Handle image files directly
                result = OCRService.extract(file_path)
                text = result["text"]
                confidence = result["confidence"]

            # 5. Update the document with OCR results
            document.raw_text = text
            document.confidence = confidence
            document.save()

        except Exception as e:
            # Optional: Decide if you want to delete the contract if OCR fails
            # contract.delete()
            return Response(
                {
                    "error": "OCR processing failed",
                    "details": str(e),
                    "document_id": document.id,
                },
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )

        # 6. Return the updated serialized data
        # We re-serialize the instance to include the newly saved raw_text and confidence
        response_serializer = DocumentSerializer(document)
        return Response(response_serializer.data, status=status.HTTP_201_CREATED)
