import time
from fastapi import APIRouter, HTTPException
from .models import QuestionRequest, DocumentRequest
from .workflow import RagWorkflow
from .embeddings import EmbeddingService
from .storage import DocumentStore


def create_router(
    workflow: RagWorkflow,
    embedder: EmbeddingService,
    store: DocumentStore,
):
    router = APIRouter()

    @router.post("/ask")
    def ask(req: QuestionRequest):
        start = time.time()
        try:
            result = workflow.run(req.question)
            return {
                "question": req.question,
                "answer": result["answer"],
                "context_used": result.get("context", []),
                "latency_sec": round(time.time() - start, 3),
            }
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.post("/add")
    def add(req: DocumentRequest):
        try:
            vector = embedder.embed(req.text)
            doc_id = store.add(req.text, vector)
            return {"id": doc_id, "status": "added"}
        except Exception as e:
            raise HTTPException(status_code=500, detail=str(e))

    @router.get("/status")
    def status():
        return {
            "in_memory_docs_count": store.count(),
            "graph_ready": True,
        }

    return router