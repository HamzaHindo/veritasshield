from ai_engine.pipelines.clause_extractor import ClauseExtractor
from ai_engine.pipelines.classify_clause import ClauseClassifier

from ai_engine.dataclasses import DocumentInput, AnalysisResult

from ai_engine.utils.similarity_engine import SimilarityEngine
from ai_engine.utils.conflict_detector import ConflictDetector

from ai_engine.db.neo4j_connection import Neo4jConnection

# Same pipeline as insert_document but NOTHING is written to Neo4j.
# Use this for: previewing conflicts before a user decides to save.

def inspect_document(
        doc: DocumentInput, 
        extractor: ClauseExtractor,
        classifier: ClauseClassifier,
        similarity_engine: SimilarityEngine,
        conflict_detector: ConflictDetector,
        db: Neo4jConnection
        ) -> AnalysisResult:
    """
    Read-only analysis. Compares document against the existing graph
    without persisting anything. Safe to call multiple times.

    Parameters:
    - (doc): document to be inserted
    - (extractor): the clause extractor used
    - (classifier): the clause classifier to use
    - (similarity_engine)
    - (conflict_detector)
    - (db): a Neo4j Connection object
    """
    print(f'[inspect] Analysing document: {doc.document_id} (no writes)')

    doc_type     = classifier.classify(doc.raw_text)
    clause_texts = extractor.extract(doc.raw_text)
    embeddings   = similarity_engine.embed(clause_texts)

    # Build temporary in-memory clause objects (never touch Neo4j)
    temp_clauses = [
        {'id': f'temp_{i}', 'text': text, 'embedding': emb.tolist()}
        for i, (text, emb) in enumerate(zip(clause_texts, embeddings))
    ]

    existing_clauses = db.get_all_clauses()  # everything in DB
    similar_pairs    = similarity_engine.find_similar(temp_clauses, existing_clauses)
    conflicts        = conflict_detector.detect(similar_pairs)

    print(f'[inspect] {len(clause_texts)} clauses | {len(similar_pairs)} similar | {len(conflicts)} conflicts')

    return AnalysisResult(
        document_id   = doc.document_id,
        doc_type      = doc_type,
        clauses       = [{'id': c['id'], 'text': c['text'], 'clause_type': 'general'} for c in temp_clauses],
        similar_pairs = similar_pairs,
        conflicts     = conflicts
    )