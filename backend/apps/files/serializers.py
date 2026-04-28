from rest_framework import serializers

from .models import Document


class DocumentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        # List all fields you want to expose in the API
        fields = [
            "id",
            "file",
            "user",
            "file_extension",
            "uploaded_at",
            "signed_at",
            "lang",
            "raw_text",
            "confidence",
            "title",
        ]
        read_only_fields = [
            "id",
            "user",  # User should be set in the View/ViewSet, not by the client
            "file_extension",  # Typically derived from the file name/type
            "uploaded_at",  # Auto-set by Django
            "confidence",  # Typically calculated by backend logic
            "raw_text",  # Typically extracted by backend logic
        ]
