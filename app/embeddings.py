import random
from typing import List


class EmbeddingService:
    VECTOR_SIZE = 128

    def embed(self, text: str) -> List[float]:
        # Deterministic fake embedding
        random.seed(abs(hash(text)) % 10000)
        return [random.random() for _ in range(self.VECTOR_SIZE)]