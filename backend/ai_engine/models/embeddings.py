import os

# Perfect singelton wrapper around the embedding model
class Embedder:
    _instance = None

    _model_name = 'all-MiniLM-L6-v2'
    
    _current_dir = os.path.dirname(os.path.abspath(__file__))
    _cache_path = os.path.join(_current_dir, "cache", _model_name) # ai_engine/cache/all-MiniLM-L6-v2/

    def __new__(cls):
        if cls._instance is None:
            print(f"Downloading Embeddings Model: {cls._model_name}.....")

            cls._instance = super(Embedder, cls).__new__(cls)
            

            # Load the actual model onto the instance once
            cls._instance._model = cls._load_model()
            print("Model loaded into memory ✓")
        else:
            print("Embeddings Model found, continuing.")

        return cls._instance
    
    @classmethod
    def _load_model(cls):

        from sentence_transformers import SentenceTransformer
        
        if os.path.exists(cls._cache_path):
            return SentenceTransformer(cls._cache_path)
        else:
            model = SentenceTransformer(cls._model_name)

            os.makedirs(cls._cache_path, exist_ok=True)
            
            model.save(cls._cache_path)

            return model

    def __getattr__(self, name):
        """
        Delegates any method/attribute access not found in this class
        directly to the underlying SentenceTransformer model.
        """
        return getattr(self._model, name)