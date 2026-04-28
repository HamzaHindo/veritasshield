from rest_framework import serializers

from .models import Contract


class ContractSerializer(serializers.ModelSerializer):
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Contract
        fields = [
            "id",
            "title",
            "file",
            "raw_text",
            "confidence",
            "created_at",
            "status",
        ]
        read_only_fields = [
            "created_at",
            "updated_at",
            "risk_score",
            "summary",
            "status",
        ]
