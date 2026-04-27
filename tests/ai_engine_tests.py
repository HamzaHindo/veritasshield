import os
from dotenv import load_dotenv

# Database and Models
from ai_engine.db.neo4j_connection import get_db
from ai_engine.models.embeddings import Embedder

# Pipelines and Utils
from ai_engine.pipelines.clause_extractor import ClauseExtractor
from ai_engine.pipelines.classify_clause import ClauseClassifier
from ai_engine.utils.similarity_engine import SimilarityEngine
from ai_engine.utils.conflict_detector import ConflictDetector

from ai_engine.pipelines.insert import insert_document
from ai_engine.pipelines.inspect import inspect_document
from ai_engine.dataclasses import DocumentInput


def main():
    # 1. Load environment variables for Neo4j
    load_dotenv()
    
    print("Initializing VeritasShield Components...\n")

    # 2. Initialize Singletons & Services
    try:
        db = get_db()
        embedder = Embedder() # Forces the model to download/load into memory
        
        extractor = ClauseExtractor()
        classifier = ClauseClassifier()
        similarity_engine = SimilarityEngine()
        conflict_detector = ConflictDetector()
        
    except Exception as e:
        print(f"❌ Initialization Failed: {e}")
        return

    # 3. Clean slate for testing
    print("\nWiping existing graph for a clean test state...")
    db.clear_all()

    # 4. Create Mock Documents
    # Designed to trigger _rule_number_mismatch and _rule_negation_flip
    doc1_text = """
    TERMINATION
    The employee must give 30 days notice prior to resigning from the company.
    
    EQUIPMENT
    The company will provide a laptop to the employee for remote work.
    """

    doc2_text = """
    TERMINATION
    The employee must give 60 days notice prior to resigning from the company.
    
    EQUIPMENT
    The company will not provide a laptop to the employee under any circumstances.
    """

    doc_input_1 = DocumentInput(
        document_id="doc_001",
        raw_text=doc1_text,
        title="Standard Employment Contract v1",
        file_extension="txt"
    )

    doc_input_2 = DocumentInput(
        document_id="doc_002",
        raw_text=doc2_text,
        title="Standard Employment Contract v2",
        file_extension="txt"
    )

    # 5. Execute Pipeline: Insert Document 1
    print(f"\n{'='*50}\n▶ Running Pipeline: INSERT Document 1\n{'='*50}")
    result_1 = insert_document(
        doc=doc_input_1,
        extractor=extractor,
        classifier=classifier,
        similarity_engine=similarity_engine,
        conflict_detector=conflict_detector,
        db=db
    )
    result_1.summary()

    # 6. Execute Pipeline: Inspect Document 2 (Read-only Preview)
    print(f"\n{'='*50}\n▶ Running Pipeline: INSPECT Document 2 (Dry Run)\n{'='*50}")
    result_inspect = inspect_document(
        doc=doc_input_2,
        extractor=extractor,
        classifier=classifier,
        similarity_engine=similarity_engine,
        conflict_detector=conflict_detector,
        db=db
    )
    result_inspect.summary()

    # 7. Execute Pipeline: Insert Document 2 (Persistence)
    print(f"\n{'='*50}\n▶ Running Pipeline: INSERT Document 2\n{'='*50}")
    result_2 = insert_document(
        doc=doc_input_2,
        extractor=extractor,
        classifier=classifier,
        similarity_engine=similarity_engine,
        conflict_detector=conflict_detector,
        db=db
    )
    result_2.summary()

    # 8. Verify the Database State directly
    print(f"\n{'='*50}\n▶ Verifying Neo4j State directly\n{'='*50}")
    persisted_conflicts = db.get_conflicts_for_document("doc_002")
    print(f"Total conflict edges found in DB for doc_002: {len(persisted_conflicts)}")
    for c in persisted_conflicts:
        print(f"\n  Clause : {c['clause_text'][:70]}...")
        print(f"  Clashes: {c['conflict_text'][:70]}...")
        print(f"  Reason : {c['reason']}")

    # 9. Cleanup
    db.close()
    print("\n✅ Test completed successfully. Connection closed.")

if __name__ == "__main__":
    main()