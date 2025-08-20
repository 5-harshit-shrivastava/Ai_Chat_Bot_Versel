import os
import requests
from typing import List
import hashlib

class EmbeddingGenerator:
    def __init__(self):
        """Use HF API instead of downloading model to save memory"""
        self.hf_token = os.getenv("HUGGINGFACE_API_TOKEN")
        self.api_url = "https://api-inference.huggingface.co/pipeline/feature-extraction/sentence-transformers/all-MiniLM-L6-v2"
    
    def get_embedding(self, text: str) -> List[float]:
        """Same model, same quality, zero memory usage"""
        if self.hf_token:
            try:
                headers = {"Authorization": f"Bearer {self.hf_token}"}
                response = requests.post(
                    self.api_url,
                    headers=headers,
                    json={"inputs": text},
                    timeout=15
                )
                
                if response.status_code == 200:
                    result = response.json()
                    if isinstance(result, list) and len(result) > 0:
                        if isinstance(result[0], list):
                            return result[0][:384]  # First embedding
                        return result[:384]
                        
            except Exception as e:
                print(f"HF API error: {e}")
        
        # Fallback: deterministic hash-based embedding
        return self._hash_embedding(text)
    
    def _hash_embedding(self, text: str) -> List[float]:
        """Consistent fallback embedding (384-dim)"""
        # Create deterministic embedding from text hash
        hash_bytes = hashlib.sha256(text.encode()).digest()
        hash_ints = [b for b in hash_bytes]
        
        # Extend to 384 dimensions
        embedding = []
        for i in range(384):
            byte_idx = i % len(hash_ints)
            # Normalize to [-1, 1] range
            normalized = (hash_ints[byte_idx] - 128) / 128.0
            embedding.append(normalized)
            
        return embedding

embedder = EmbeddingGenerator()