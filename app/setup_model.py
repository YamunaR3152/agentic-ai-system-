from sentence_transformers import SentenceTransformer

print("🔄 Loading embedding model...")
EMBEDDING_MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
print("✅ Embedding model loaded")
