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


class DocumentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Document
        # Fields that the client CAN send
        fields = ["id", "file", "title", "lang", "file_extension", "uploaded_at"]

        # Fields that are Read-Only (Client cannot send these, but they appear in response)
        read_only_fields = [
            "id",
            "uploaded_at",
            "user",
            "raw_text",
            "confidence",
            "signed_at",
        ]

    def validate_file(self, value):
        """Optional: Add custom file validation here"""
        if not value.name.endswith((".pdf", ".jpg", ".png", ".jpeg")):
            raise serializers.ValidationError("Unsupported file type.")
        return value

    def create(self, validated_data):
        """
        Override create to handle any custom logic before saving.
        Note: 'user' is not in validated_data because it's read_only/excluded.
        We will pass it via save() in the view.
        """
        return super().create(validated_data)
