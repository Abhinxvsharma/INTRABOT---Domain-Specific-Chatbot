import os

# Base Directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
DATA_DIR = os.path.join(BASE_DIR, "data")
VECTORSTORE_DIR = os.path.join(BASE_DIR, "vectorstore")
CACHE_DIR = os.path.join(BASE_DIR, "cache")

# RAG Pipeline Configuration
CHUNK_SIZE = 300
CHUNK_OVERLAP = 45  # 15% of 300
MIN_CHUNK_SIZE = 5

EMBEDDING_MODEL = "sentence-transformers/all-MiniLM-L6-v2" 


# LLM Configuration
OLLAMA_BASE_URL = "http://localhost:11434"
LLM_MODEL = "tinyllama:latest"
TEMPERATURE = 0.7
MAX_TOKENS = 300
CONTEXT_WINDOW = 1000

# Retrieval Configuration
RETRIEVAL_TOP_K = 3
RERANK_TOP_K = 5
SIMILARITY_THRESHOLD = 0.4
