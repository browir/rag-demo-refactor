from typing import Dict
from langgraph.graph import StateGraph, END
from .embeddings import EmbeddingService
from .storage import DocumentStore


class RagWorkflow:
    def __init__(self, embedder: EmbeddingService, store: DocumentStore):
        self.embedder = embedder
        self.store = store
        self._chain = self._build()

    def _retrieve(self, state: Dict) -> Dict:
        query = state["question"]
        vector = self.embedder.embed(query)
        state["context"] = self.store.search(query, vector)
        return state

    def _answer(self, state: Dict) -> Dict:
        ctx = state.get("context", [])
        if ctx:
            state["answer"] = f"I found this: '{ctx[0][:100]}...'"
        else:
            state["answer"] = "Sorry, I don't know."
        return state

    def _build(self):
        graph = StateGraph(dict)
        graph.add_node("retrieve", self._retrieve)
        graph.add_node("answer", self._answer)
        graph.set_entry_point("retrieve")
        graph.add_edge("retrieve", "answer")
        graph.add_edge("answer", END)
        return graph.compile()

    def run(self, question: str) -> Dict:
        return self._chain.invoke({"question": question})