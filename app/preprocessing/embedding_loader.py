from sentence_transformers import SentenceTransformer

# Shared embedding model (used by Analyzer)
EMBEDDING_MODEL = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)
