# apps/clauses/services/analysis_service.py
import os

from apps.files.models import Document
from apps.files.services.document_services import DocumentService

# Import your AI/OCR services here
from apps.text_extractor_engine.services.extract_text import ExtractTextService

from ai_engine.dataclasses import (
    DocumentInput,
)

text_extractor = ExtractTextService()
Document_service = DocumentService()


class AnalysisService:

    @staticmethod
    def inspect_uploaded_file(user, file_obj, title=None, lang="en"):
        """
        Main entry point for the /analyze endpoint.
        """

        # 1. Create Document Instance in DB
        # We reuse the DocumentService to handle validation and saving
        file_extension = os.path.splitext(file_obj.name)[1].lower()
        document = Document_service.create_document(
            user=user,
            file_data={
                "file": file_obj,
                "file_extension": file_extension,
                "title": title,
                "lang": lang,
            },
        )

        # 2. Extract Raw Text (OCR)
        raw_text = text_extractor.extract_text(document.file.path)

        # Update DB with extracted text
        document.raw_text = raw_text
        document.save()

        # 3. Create DocumentInput Dataclass
        doc_input = DocumentInput(
            document_id=document.id,
            raw_text=raw_text,
            title=document.title,
            file_extension=document.file_extension,
            language=document.lang,
            signed_at=document.signed_at.isoformat() if document.signed_at else None,
        )

        # 4. Call Inspection Logic
        result = Document_service.inspect_document(doc_input)

        return result

    @staticmethod
    def insert_uploaded_file(user, doc_id):
        """
        Main entry point for the /analyze endpoint.
        """

        # 1. Create Document Instance in DB
        # We reuse the DocumentService to handle validation and saving
        document = Document.objects.get(id=doc_id)

        if document.raw_text is None:
            raise ValueError(
                "Document must have raw_text before insertion. Call inspect first."
            )

        # 3. Create DocumentInput Dataclass
        doc_input = DocumentInput(
            document_id=document.id,
            raw_text=document.raw_text,
            title=document.title,
            file_extension=document.file_extension,
            language=document.lang,
            signed_at=document.signed_at.isoformat() if document.signed_at else None,
        )

        # 4. Call Insert Logic
        result = Document_service.insert_document(doc_input)

        return result
