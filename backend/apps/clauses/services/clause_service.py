from ai_engine.repo.clause_repo import clause_repo


class ClauseService:

    @staticmethod
    def get_clause_analysis(clause_id: int):
        """
        Retrieve detailed analysis for a single clause, including
        conflicts and similar clauses.

        Args:
            clause_id (int): The ID of the clause.

        Returns:
            Dict | None: The clause details with conflicts and similarities,
                         or None if not found.
        """
        return clause_repo.get_clause_details(clause_id)
