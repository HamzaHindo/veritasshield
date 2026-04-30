from rest_framework import serializers


class ClauseSerializer(serializers.Serializer):
    """
    Serializes the plain clause dict returned by clause_repo.
    """
    clause_id = serializers.IntegerField()
    clause_text = serializers.CharField()
    clause_type = serializers.CharField()


class SimilarityMatchSerializer(serializers.Serializer):
    """
    Matches the SimilarityMatch dataclass from ai_engine.
    """
    new_clause_id = serializers.IntegerField()
    new_clause_text = serializers.CharField()
    existing_clause_id = serializers.IntegerField()
    existing_clause_text = serializers.CharField()
    existing_doc_title = serializers.CharField()
    score = serializers.FloatField(min_value=0.0, max_value=1.0)


class ConflictSerializer(serializers.Serializer):
    """
    Matches the Conflict dataclass from ai_engine (SimilarityMatch + reason).
    """
    new_clause_id = serializers.IntegerField()
    new_clause_text = serializers.CharField()
    existing_clause_id = serializers.IntegerField()
    existing_clause_text = serializers.CharField()
    existing_doc_title = serializers.CharField()
    score = serializers.FloatField(min_value=0.0, max_value=1.0)
    reason = serializers.CharField()


class ClauseDetailsSerializer(serializers.Serializer):
    """
    Serializes the full payload returned by clause_repo.get_clause_details().

    Expected shape:
        {
            'Clause':       {'id': ..., 'text': ..., 'type': ...},
            'Conflicts':    [Conflict(...), ...],
            'Similarities': [SimilarityMatch(...), ...]
        }
    """
    Clause = ClauseSerializer()
    Conflicts = ConflictSerializer(many=True)
    Similarities = SimilarityMatchSerializer(many=True)
