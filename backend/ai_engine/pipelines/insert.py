from ai_engine.pipelines.clause_extractor import ClauseExtractor
from ai_engine.pipelines.classify_clause import ClauseClassifier

from ai_engine.dataclasses import DocumentInput, AnalysisResult

from ai_engine.utils.similarity_engine import SimilarityEngine
from ai_engine.utils.conflict_detector import ConflictDetector

from ai_engine.db.neo4j_connection import Neo4jConnection


def insert_document(
        doc: DocumentInput, 
        extractor: ClauseExtractor,
        classifier: ClauseClassifier,
        similarity_engine: SimilarityEngine,
        conflict_detector: ConflictDetector,
        db: Neo4jConnection
        ) -> AnalysisResult:
    
    """
    # Inserts a new document into the knowledge graph:
    
    Parameters:
    - (doc): document to be inserted
    - (extractor): the clause extractor used
    - (classifier): the clause classifier to use
    - (similarity_engine)
    - (conflict_detector)
    - (db): a Neo4j Connection object

    Pipeline:
    ---------
    1. Extract clauses from raw text
    2. Classify document type  (stubbed — wire to classifier.py in production)
    3. Embed all clauses
    4. Write Document + Clause nodes to Neo4j
    5. Compare against existing clauses → find similar pairs
    6. Write SIMILAR_TO edges
    7. Run conflict detection → write CONTRADICTS edges
    8. Return AnalysisResult
    
    Full pipeline: parse → embed → store → link → detect conflicts.
    Persists everything to Neo4j.
    """

    print(f'[insert] Processing document: {doc.document_id}')

    # 1. Classify
    doc_type = classifier.classify(doc.raw_text)

    # 2. Extract clauses
    clause_texts = extractor.extract(doc.raw_text)
    print(f'[insert] Extracted {len(clause_texts)} clauses')

    # 3. Embed all clauses in one batch (fast)
    embeddings = similarity_engine.embed(clause_texts)  # (N, 384)

    # 4. Write Document node
    db.create_document(
        doc_id         = doc.document_id,
        title          = doc.title,
        doc_type       = doc_type,
        file_extension = doc.file_extension,
        signed_at      = doc.signed_at
    )

    # 5. Write Clause nodes + HAS edges
    new_clauses = []
    for i, (text, emb) in enumerate(zip(clause_texts, embeddings)):
        clause_id = (doc.document_id * 1000) + i
        db.create_clause(
            clause_id   = clause_id,
            doc_id      = doc.document_id,
            text        = text,
            clause_type = 'general',   # wire clause type classifier here later
            embedding   = emb.tolist()
        )
        new_clauses.append({'id': clause_id, 'text': text, 'embedding': emb.tolist()})

    # 6. Get existing clauses (excluding this doc)
    existing_clauses = db.get_all_clauses(exclude_doc_id=doc.document_id)
    print(f'[insert] Comparing against {len(existing_clauses)} existing clauses')

    # 7. Find similar pairs
    similar_pairs = similarity_engine.find_similar(new_clauses, existing_clauses)
    print(f'[insert] Found {len(similar_pairs)} similar pairs')

    # 8. Write SIMILAR_TO edges
    for match in similar_pairs:
        db.create_similar_to(match.new_clause_id, match.existing_clause_id, match.score)

    # 9. Detect conflicts
    conflicts = conflict_detector.detect(similar_pairs)
    print(f'[insert] Detected {len(conflicts)} conflicts')

    # 10. Write CONTRADICTS edges
    for conflict in conflicts:
        db.create_contradicts(
            conflict.new_clause_id,
            conflict.existing_clause_id,
            conflict.reason
        )

    return AnalysisResult(
        document_id   = doc.document_id,
        doc_type      = doc_type,
        clauses       = [{'id': c['id'], 'text': c['text'], 'clause_type': 'general'} for c in new_clauses],
        similar_pairs = similar_pairs,
        conflicts     = conflicts
    )