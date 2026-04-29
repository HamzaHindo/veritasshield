from rest_framework import serializers

# ------------------------------------------------------------------
# 1. Nested Output Serializers (Matching Dataclasses)
# ------------------------------------------------------------------


class ClauseSerializer(serializers.Serializer):
    """
    Matches the Clause dataclass.
    Represents a single extracted clause.
    """

    id = serializers.IntegerField()
    text = serializers.CharField()
    clause_type = serializers.CharField()


class SimilarityMatchSerializer(serializers.Serializer):
    """
    Matches the SimilarityMatch dataclass.
    Represents a semantic match with an existing clause.
    """

    new_clause_id = serializers.IntegerField()
    new_clause_text = serializers.CharField()
    existing_clause_id = serializers.IntegerField()
    existing_clause_text = serializers.CharField()
    existing_doc_title = serializers.CharField()
    score = serializers.FloatField(min_value=0.0, max_value=1.0)


class ConflictSerializer(serializers.Serializer):
    """
    Matches the Conflict dataclass (inherits from SimilarityMatch + reason).
    Represents a detected logical contradiction.
    """

    new_clause_id = serializers.IntegerField()
    new_clause_text = serializers.CharField()
    existing_clause_id = serializers.IntegerField()
    existing_clause_text = serializers.CharField()
    existing_doc_title = serializers.CharField()
    score = serializers.FloatField(min_value=0.0, max_value=1.0)
    reason = serializers.CharField()


# ------------------------------------------------------------------
# 2. Main Result Serializer
# ------------------------------------------------------------------


class AnalysisResultSerializer(serializers.Serializer):
    """
    Matches the AnalysisResult dataclass.
    The main response object for the /analyze endpoint.
    """

    document_id = serializers.IntegerField()
    doc_type = serializers.CharField()

    # List of Clause objects
    clauses = ClauseSerializer(many=True)

    # List of SimilarityMatch objects
    similar_pairs = SimilarityMatchSerializer(many=True)

    # List of Conflict objects
    conflicts = ConflictSerializer(many=True)


# ------------------------------------------------------------------
# 3. Input Serializers (For Views)
# ------------------------------------------------------------------


class DocumentUploadInputSerializer(serializers.Serializer):
    """
    Validates the incoming multipart/form-data for /analyze/
    """

    file = serializers.FileField()
    title = serializers.CharField(required=False, allow_blank=True)
    language = serializers.CharField(required=False, default="en")


class DocumentSaveInputSerializer(serializers.Serializer):
    """
    Validates the incoming JSON body for /analyze/save/
    """

    doc_id = serializers.IntegerField()
