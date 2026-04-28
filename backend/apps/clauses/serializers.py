from rest_framework import serializers


# 1. The "Conflict" object (nested inside the main clause)
class ConflictClauseSerializer(serializers.Serializer):
    clause_id = serializers.IntegerField()
    text = serializers.CharField()
    type = serializers.CharField()
    reason = serializers.CharField()


# 2. The "Similar Clause" object (nested inside the main clause)
class SimilarClauseSerializer(serializers.Serializer):
    clause_id = serializers.IntegerField()
    text = serializers.CharField()
    type = serializers.CharField()


# 3. The Main Clause Object
class ClauseAnalysisSerializer(serializers.Serializer):
    clause_id = serializers.IntegerField()
    text = serializers.CharField()
    type = serializers.CharField()

    # List of nested Conflict objects
    conflicts = serializers.ListField(
        child=ConflictClauseSerializer(), required=False, default=list
    )

    # List of nested Similar Clause objects
    similar_clauses = serializers.ListField(
        child=SimilarClauseSerializer(), required=False, default=list
    )
