from sentence_transformers import SentenceTransformer
import numpy as np

class EmbeddingGenerator:
    def __init__(self):
        self.model = SentenceTransformer('all-MiniLM-L6-v2')
    
    def get_embedding(self, text: str) -> list[float]:
        embedding = self.model.encode(text)
        return embedding.tolist()

embedder = EmbeddingGenerator()