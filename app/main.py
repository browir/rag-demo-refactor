from fastapi import FastAPI
from qdrant_client import QdrantClient
from .embeddings import EmbeddingService
from .storage import InMemoryDocumentStore, QdrantDocumentStore
from .workflow import RagWorkflow
from .api import create_router

app = FastAPI(title="Learning RAG Demo")

embedder = EmbeddingService()

# Choose storage backend
try:
    qdrant_client = QdrantClient("http://localhost:6333")
    store = QdrantDocumentStore(
        client=qdrant_client,
        collection="demo_collection",
        vector_size=embedder.VECTOR_SIZE,
    )
except Exception:
    store = InMemoryDocumentStore()

workflow = RagWorkflow(embedder, store)
router = create_router(workflow, embedder, store)

app.include_router(router)