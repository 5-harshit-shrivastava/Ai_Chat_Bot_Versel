import os
import json
import requests
import psycopg2
from typing import List, Dict, Any

# Database connection
NEON_URL = os.getenv("NEON_DATABASE_URL")
HF_TOKEN = os.getenv("HUGGINGFACE_API_TOKEN")

def get_embedding(text: str) -> List[float]:
    """Generate embedding using BAAI/bge-small-en-v1.5 model"""
    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }
    
    try:
        response = requests.post(
            "https://api-inference.huggingface.co/models/BAAI/bge-small-en-v1.5",
            headers=headers,
            json={"inputs": text},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            embedding = result[0] if isinstance(result[0], list) else result
            return embedding[:384]  # Ensure 384 dimensions
        else:
            print(f"❌ Embedding API error: {response.status_code}")
            print(f"Response: {response.text}")
            return None
            
    except Exception as e:
        print(f"❌ Embedding error: {e}")
        return None

def setup_database():
    """Create database table if not exists"""
    try:
        conn = psycopg2.connect(NEON_URL)
        cursor = conn.cursor()
        
        # Create table with vector extension
        cursor.execute("""
            CREATE EXTENSION IF NOT EXISTS vector;
            
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                embedding vector(384),
                doc_metadata JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
            
            CREATE INDEX IF NOT EXISTS idx_documents_embedding 
            ON documents USING ivfflat (embedding vector_cosine_ops);
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        print("✅ Database setup completed")
        
    except Exception as e:
        print(f"❌ Database setup error: {e}")

def clear_existing_data():
    """Clear existing documents from database"""
    try:
        conn = psycopg2.connect(NEON_URL)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM documents")
        conn.commit()
        
        cursor.close()
        conn.close()
        print("✅ Existing data cleared")
        
    except Exception as e:
        print(f"❌ Error clearing data: {e}")

def add_document(content: str, metadata: Dict[str, Any] = None):
    """Add a document to the database with embedding"""
    if not content.strip():
        print("❌ Empty content, skipping")
        return
    
    # Generate embedding
    embedding = get_embedding(content)
    if embedding is None:
        print(f"❌ Failed to generate embedding for: {content[:50]}...")
        return
    
    try:
        conn = psycopg2.connect(NEON_URL)
        cursor = conn.cursor()
        
        # Convert embedding to PostgreSQL array format
        embedding_str = "[" + ",".join(map(str, embedding)) + "]"
        
        cursor.execute("""
            INSERT INTO documents (content, embedding, doc_metadata)
            VALUES (%s, %s::vector, %s)
        """, (content, embedding_str, json.dumps(metadata or {})))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ Added: {content[:50]}...")
        
    except Exception as e:
        print(f"❌ Error adding document: {e}")

def ingest_navyakosh_data():
    """Ingest Navyakosh fertilizer data"""
    
    navyakosh_docs = [
        {
            "content": "Navyakosh is a specialized organic fertilizer designed specifically for sugarcane cultivation. It provides essential nutrients and improves soil health through natural organic matter.",
            "metadata": {"category": "fertilizer_info", "crop": "sugarcane", "type": "organic"}
        },
        {
            "content": "Navyakosh fertilizer application rate: Apply 25-30 kg per acre during planting season. For established sugarcane fields, apply 20-25 kg per acre before irrigation.",
            "metadata": {"category": "application_rate", "crop": "sugarcane", "season": "planting"}
        },
        {
            "content": "Navyakosh contains balanced NPK nutrients along with essential micronutrients. The organic composition helps improve soil structure and water retention capacity.",
            "metadata": {"category": "composition", "nutrients": "NPK", "benefits": "soil_health"}
        },
        {
            "content": "Best time to apply Navyakosh fertilizer for sugarcane: Apply during land preparation 15-20 days before planting. Second application can be done 45-60 days after planting.",
            "metadata": {"category": "timing", "crop": "sugarcane", "application_schedule": "multiple"}
        },
        {
            "content": "Navyakosh fertilizer benefits for sugarcane: Increases cane yield by 15-20%, improves sugar content, enhances root development, and reduces chemical fertilizer dependency.",
            "metadata": {"category": "benefits", "crop": "sugarcane", "yield_increase": "15-20%"}
        },
        {
            "content": "Mix Navyakosh fertilizer with soil or compost before application. Ensure proper moisture in soil during application. Do not apply during heavy rainfall periods.",
            "metadata": {"category": "application_method", "precautions": "moisture_rainfall"}
        },
        {
            "content": "Navyakosh is compatible with other organic fertilizers and bio-fertilizers. Can be used alongside vermicompost, neem cake, and beneficial microorganisms.",
            "metadata": {"category": "compatibility", "type": "organic_mix"}
        },
        {
            "content": "Storage instructions for Navyakosh: Store in cool, dry place away from direct sunlight. Use within 2 years of manufacture date for best results.",
            "metadata": {"category": "storage", "shelf_life": "2_years"}
        }
    ]
    
    print(f"📊 Starting ingestion of {len(navyakosh_docs)} Navyakosh documents...")
    
    for i, doc in enumerate(navyakosh_docs, 1):
        print(f"\n📝 Processing document {i}/{len(navyakosh_docs)}")
        add_document(doc["content"], doc["metadata"])

def test_search():
    """Test the search functionality"""
    test_query = "How to apply Navyakosh fertilizer for sugarcane?"
    
    print(f"\n🔍 Testing search with query: '{test_query}'")
    
    # Generate query embedding
    query_embedding = get_embedding(test_query)
    if query_embedding is None:
        print("❌ Failed to generate query embedding")
        return
    
    try:
        conn = psycopg2.connect(NEON_URL)
        cursor = conn.cursor()
        
        # Convert embedding to PostgreSQL array format
        embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"
        
        # Search for similar documents
        cursor.execute("""
            SELECT content, doc_metadata, 
                   1 - (embedding <=> %s::vector) as similarity
            FROM documents 
            WHERE embedding IS NOT NULL
            ORDER BY embedding <=> %s::vector 
            LIMIT 3
        """, (embedding_str, embedding_str))
        
        results = cursor.fetchall()
        
        print(f"\n📊 Found {len(results)} similar documents:")
        for i, (content, metadata, similarity) in enumerate(results, 1):
            print(f"\n{i}. Similarity: {similarity:.4f}")
            print(f"   Content: {content[:100]}...")
            print(f"   Category: {metadata.get('category', 'N/A')}")
        
        cursor.close()
        conn.close()
        
    except Exception as e:
        print(f"❌ Search test error: {e}")

if __name__ == "__main__":
    print("🚀 NAVYAKOSH DATA INGESTION - BAAI/bge-small-en-v1.5")
    print("=" * 60)
    
    # Setup database
    setup_database()
    
    # Clear existing data
    print("\n🗑️ Clearing existing data...")
    clear_existing_data()
    
    # Ingest new data
    print("\n📥 Ingesting Navyakosh data...")
    ingest_navyakosh_data()
    
    # Test search
    print("\n🧪 Testing search functionality...")
    test_search()
    
    print("\n✅ INGESTION COMPLETED!")
    print("Your RAG system is ready with BAAI/bge-small-en-v1.5 embeddings.")
