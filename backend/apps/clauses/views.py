from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .services.clause_service import ClauseService


class ClauseAnalysisView(APIView):
    """
    Handles clause analysis retrieval.
    """

    permission_classes = [IsAuthenticated]

    def get(self, request, clause_id):
        """
        Route: GET /clauses/<int:clause_id>/analysis/
        Action: Retrieve detailed analysis for a clause, including
                conflicts and similar clauses.
        """
        result = ClauseService.get_clause_analysis(clause_id)

        if result is None:
            return Response(
                {"error": "Clause not found"},
                status=status.HTTP_404_NOT_FOUND,
            )

        return Response(result, status=status.HTTP_200_OK)
