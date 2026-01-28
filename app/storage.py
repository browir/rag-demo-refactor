from abc import ABC, abstractmethod
from typing import List
from qdrant_client import QdrantClient
from qdrant_client.models import PointStruct, VectorParams, Distance


class DocumentStore(ABC):
    @abstractmethod
    def add(self, text: str, vector: List[float]) -> int:
        pass

    @abstractmethod
    def search(self, query: str, vector: List[float], limit: int = 2) -> List[str]:
        pass

    @abstractmethod
    def count(self) -> int:
        pass

class InMemoryDocumentStore(DocumentStore):
    def __init__(self):
        self._docs: List[str] = []

    def add(self, text: str, vector: List[float]) -> int:
        self._docs.append(text)
        return len(self._docs) - 1

    def search(self, query: str, vector: List[float], limit: int = 2) -> List[str]:
        matches = [d for d in self._docs if query.lower() in d.lower()]
        if not matches and self._docs:
            matches = [self._docs[0]]
        return matches[:limit]

    def count(self) -> int:
        return len(self._docs)
    
class QdrantDocumentStore(DocumentStore):
    def __init__(self, client: QdrantClient, collection: str, vector_size: int):
        self.client = client
        self.collection = collection

        self.client.recreate_collection(
            collection_name=collection,
            vectors_config=VectorParams(size=vector_size, distance=Distance.COSINE),
        )

    def add(self, text: str, vector: List[float]) -> int:
        doc_id = hash(text)
        self.client.upsert(
            collection_name=self.collection,
            points=[
                PointStruct(
                    id=doc_id,
                    vector=vector,
                    payload={"text": text},
                )
            ],
        )
        return doc_id

    def search(self, query: str, vector: List[float], limit: int = 2) -> List[str]:
        hits = self.client.search(
            collection_name=self.collection,
            query_vector=vector,
            limit=limit,
        )
        return [hit.payload["text"] for hit in hits]

    def count(self) -> int:
        info = self.client.get_collection(self.collection)
        return info.points_count or 0