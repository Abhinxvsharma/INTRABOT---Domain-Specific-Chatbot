from langchain_huggingface import HuggingFaceEmbeddings
from app.utils.config import EMBEDDING_MODEL

_embeddings_instance = None

def get_embeddings():
    """ Returns a singleton instance of HuggingFaceEmbeddings to save memory. """
    global _embeddings_instance
    if _embeddings_instance is None:
        print(f"--- Loading Shared Embedding Model: {EMBEDDING_MODEL} ---")
        _embeddings_instance = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={'device': 'cpu'},
            encode_kwargs={'normalize_embeddings': True}
        )
    return _embeddings_instance
