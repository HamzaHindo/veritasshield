from apps.files.serializers import DocumentCreateSerializer

from ai_engine.dataclasses import DocumentInput
from ai_engine.db.neo4j_connection import Neo4jConnection
from ai_engine.pipelines.classify_clause import ClauseClassifier
from ai_engine.pipelines.clause_extractor import ClauseExtractor
from ai_engine.pipelines.insert import insert_document as insert
from ai_engine.pipelines.inspect import inspect_document as inspect
from ai_engine.utils.conflict_detector import ConflictDetector
from ai_engine.utils.similarity_engine import SimilarityEngine
from ai_engine.repo.clause_repo import clause_repo
import dotenv
dotenv.load_dotenv()


class DocumentService:
    def __init__(self):
        self.similarity_engine = SimilarityEngine()
        self.conflict_detector = ConflictDetector()
        self.extractor = ClauseExtractor()
        self.classifier = ClauseClassifier()
        self.db = Neo4jConnection()

    def insert_document(self, doc: DocumentInput):
        """
        Service method to insert a new document into the knowledge graph.

        Args:
            doc (DocumentInput): The document to be inserted.
            extractor (ClauseExtractor): The clause extractor used.
            classifier (ClauseClassifier): The clause classifier to use.
            similarity_engine (SimilarityEngine): The similarity engine for embedding and comparisons.
            conflict_detector (ConflictDetector): The conflict detector for identifying contradictions.
            db (Neo4jConnection): A Neo4j Connection object.

        Returns:
            AnalysisResult: The result of the analysis after insertion.
        """
        return insert(
            doc,
            self.extractor,
            self.classifier,
            self.similarity_engine,
            self.conflict_detector,
            self.db,
        )

    def inspect_document(self, doc: DocumentInput):
        """
        Service method to inspect a document and retrieve its analysis results.

        Args:
            doc_id (int): The ID of the document to inspect.
        Returns:
            AnalysisResult: The result of the analysis for the specified document.
        """
        return inspect(
            doc,
            self.extractor,
            self.classifier,
            self.similarity_engine,
            self.conflict_detector,
            self.db,
        )

    def upload_document(self, doc: DocumentInput):
        """
        Service method to upload a new document.

        Args:
            doc (DocumentInput): The document to be uploaded.

        Returns:
            Document: The uploaded document.
        """
        return insert(
            doc,
            self.extractor,
            self.classifier,
            self.similarity_engine,
            self.conflict_detector,
            self.db,
        )

    def create_document(self, user, file_data: dict):
        """
        Creates a document using the Serializer.

        Args:
            user: The User instance.
            file_data: A dictionary containing 'file', 'title', 'lang', etc.
                    Usually request.data or request.FILES combined.

        Returns:
            Document: The saved instance.

        Raises:
            ValidationError: If data is invalid.
        """
        # 1. Initialize Serializer with data
        # Note: In DRF, files usually come in request.FILES, other data in request.data.
        # You might need to merge them if calling this outside a View.
        serializer = DocumentCreateSerializer(data=file_data)

        # 2. Validate
        serializer.is_valid(raise_exception=True)

        # 3. Save (Pass user explicitly because it's not in the input data)
        # serializer.save() calls the ModelSerializer's create() method
        document = serializer.save(user=user)

        return document

    def get_document_clauses(self, doc_id: int):
        """
        Retrieve all clauses associated with a specific document.

        Args:
            doc_id (int): The ID of the document.

        Returns:
            List[Dict]: A list of clause dictionaries.
        """
        return clause_repo.get_clauses_from_document(doc_id)

