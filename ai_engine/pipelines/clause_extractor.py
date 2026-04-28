import re



class ClauseExtractor:
    '''
    Splits raw contract text into individual clauses.
    
    Strategy (in priority order):
       1. Numbered sections:  "1." / "1)" / "(1)"
       2. Lettered sections:  "a." / "a)"
       3. ALL-CAPS headings:  "TERMINATION", "PAYMENT TERMS"
       4. Sentence fallback:  split on '. ' for unstructured text
    '''
    
    # Matches: "1." "2." "1)" "(1)" "Article 1" "Section 2"
    NUMBERED  = re.compile(r'(?:^|\n)\s*(?:Article|Section)?\s*(?:\(\d+\)|\d+[.)])\s+')
    # Matches: "a." "b)" at line start
    LETTERED  = re.compile(r'(?:^|\n)\s*[a-z][.)]\s+')
    # ALL-CAPS heading on its own line (≥3 words or known keywords)
    HEADINGS  = re.compile(r'\n([A-Z][A-Z\s]{4,})\n')

    MIN_CLAUSE_LENGTH = 20   # chars — ignore fragments shorter than this

    def extract(self, raw_text: str) -> list[str]:
        """
        Returns a list of clause strings extracted from raw_text.
        Automatically picks the best splitting strategy.
        """
        text = raw_text.strip()

        # Try numbered sections first (most reliable for formal contracts)
        clauses = self._split(text, self.NUMBERED)
        if len(clauses) >= 3:
            return clauses

        # Try lettered sub-sections
        clauses = self._split(text, self.LETTERED)
        if len(clauses) >= 3:
            return clauses

        # Try ALL-CAPS headings as delimiters
        clauses = self._split(text, self.HEADINGS)
        if len(clauses) >= 3:
            return clauses

        # Fallback: sentence splitting
        return self._split_sentences(text)

    def _split(self, text: str, pattern: re.Pattern) -> list[str]:
        parts = pattern.split(text)
        return [
            p.strip() for p in parts
            if p and len(p.strip()) >= self.MIN_CLAUSE_LENGTH
        ]

    def _split_sentences(self, text: str) -> list[str]:
        # Split on '. ' but keep sentences that are long enough to be meaningful
        raw = re.split(r'\.\s+', text)
        return [
            s.strip() for s in raw
            if len(s.strip()) >= self.MIN_CLAUSE_LENGTH
        ]