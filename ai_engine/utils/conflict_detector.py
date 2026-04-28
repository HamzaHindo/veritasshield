import re
from ai_engine.dataclasses import SimilarityMatch, Conflict
from typing import Optional



class ConflictDetector:

    '''
    Runs on top of SimilarityMatch pairs.
    A conflict = two similar clauses that disagree on specifics.

    Rule 1 — Number mismatch:  "30 days" vs "60 days"
    Rule 2 — Negation flip:    "must" vs "must not" / "allowed" vs "prohibited"
    Rule 3 — Permission clash: "shall" vs "shall not"
    
    Each rule returns a reason string or None.
    '''

    # Extracts all integers and decimals from text
    _NUMBERS     = re.compile(r'\b(\d+(?:\.\d+)?)\b')

    # Negation pairs to check
    _NEGATIONS   = [
        (r'\bmust\b',       r'\bmust not\b'),
        (r'\bshall\b',      r'\bshall not\b'),
        (r'\bwill\b',       r'\bwill not\b'),
        (r'\ballowed\b',    r'\bprohibited\b'),
        (r'\bpermitted\b',  r'\bforbidden\b'),
        (r'\bcan\b',        r'\bcannot\b'),
    ]

    def detect(self, matches: list[SimilarityMatch]) -> list[Conflict]:
        """
        Given a list of similar clause pairs, return those that conflict.
        """
        conflicts = []
        for match in matches:
            reason = (
                self._rule_number_mismatch(match.new_clause_text, match.existing_clause_text)
                or self._rule_negation_flip(match.new_clause_text, match.existing_clause_text)
            )
            if reason:
                conflicts.append(Conflict(
                    new_clause_id        = match.new_clause_id,
                    new_clause_text      = match.new_clause_text,
                    existing_clause_id   = match.existing_clause_id,
                    existing_clause_text = match.existing_clause_text,
                    existing_doc_title   = match.existing_doc_title,
                    score                = match.score,
                    reason               = reason
                ))
        return conflicts

    def _rule_number_mismatch(self, text_a: str, text_b: str) -> Optional[str]:
        """
        Detects when two similar clauses mention different numbers.
        Example: '30 days' vs '60 days'
        """
        nums_a = set(self._NUMBERS.findall(text_a.lower()))
        nums_b = set(self._NUMBERS.findall(text_b.lower()))
        if nums_a and nums_b and nums_a != nums_b:
            return f'Number mismatch: {nums_a} vs {nums_b}'
        return None

    def _rule_negation_flip(self, text_a: str, text_b: str) -> Optional[str]:
        """
        Detects when one clause affirms what the other negates.
        Example: 'must pay' vs 'must not pay'
        """
        a, b = text_a.lower(), text_b.lower()
        for positive, negative in self._NEGATIONS:
            a_pos = bool(re.search(positive, a))
            a_neg = bool(re.search(negative, a))
            b_pos = bool(re.search(positive, b))
            b_neg = bool(re.search(negative, b))
            # One has the positive, other has the negative
            if (a_pos and not a_neg) and (b_neg and not b_pos):
                return f'Negation conflict: clause says "{positive.strip("\\b")}" but existing says "{negative.strip("\\b")}"'
            if (a_neg and not a_pos) and (b_pos and not b_neg):
                return f'Negation conflict: clause says "{negative.strip("\\b")}" but existing says "{positive.strip("\\b")}"'
        return None