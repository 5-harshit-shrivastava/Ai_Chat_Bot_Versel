import os
import requests
import psycopg2
import json
from typing import List, Dict

def get_embedding(text):
    """Generate embedding using BAAI/bge-small-en-v1.5 model"""
    headers = {
        'Authorization': f'Bearer {os.getenv("HUGGINGFACE_API_TOKEN")}',
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.post(
            'https://api-inference.huggingface.co/models/BAAI/bge-small-en-v1.5',
            headers=headers,
            json={'inputs': text},
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            embedding = result[0] if isinstance(result[0], list) else result
            return embedding[:384]  # Ensure 384 dimensions
        else:
            print(f"Embedding API error: {response.status_code}: {response.text}")
            return None
            
    except Exception as e:
        print(f"Embedding error: {e}")
        return None

def setup_database():
    """Initialize database with required tables and extensions"""
    try:
        db_url = os.getenv('NEON_DATABASE_URL')
        
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        # Enable vector extension
        cursor.execute("CREATE EXTENSION IF NOT EXISTS vector;")
        
        # Create documents table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id SERIAL PRIMARY KEY,
                content TEXT NOT NULL,
                embedding vector(384),
                doc_metadata JSONB,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)
        
        # Create index for vector similarity search
        cursor.execute("""
            CREATE INDEX IF NOT EXISTS documents_embedding_idx 
            ON documents USING ivfflat (embedding vector_cosine_ops)
            WITH (lists = 100);
        """)
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Database setup complete!")
        return True
        
    except Exception as e:
        print(f"❌ Database setup error: {e}")
        return False

def clear_database():
    """Clear all documents from database"""
    try:
        db_url = os.getenv('NEON_DATABASE_URL')
        
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        cursor.execute("DELETE FROM documents;")
        cursor.execute("ALTER SEQUENCE documents_id_seq RESTART WITH 1;")
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print("✅ Database cleared!")
        return True
        
    except Exception as e:
        print(f"❌ Database clear error: {e}")
        return False

def ingest_document(content: str, metadata: Dict = None):
    """Add a single document to the database"""
    try:
        # Generate embedding
        embedding = get_embedding(content)
        if not embedding:
            print(f"❌ Failed to generate embedding for: {content[:50]}...")
            return False
        
        # Store in database
        db_url = os.getenv('NEON_DATABASE_URL')
        
        conn = psycopg2.connect(db_url)
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO documents (content, embedding, doc_metadata)
            VALUES (%s, %s, %s)
        """, (content, embedding, json.dumps(metadata or {})))
        
        conn.commit()
        cursor.close()
        conn.close()
        
        print(f"✅ Added: {content[:50]}...")
        return True
        
    except Exception as e:
        print(f"❌ Ingest error: {e}")
        return False

def ingest_navyakosh_data():
    """Ingest Navyakosh fertilizer data"""
    
    documents = [
        {
            "content": "Navyakosh is a specialized organic fertilizer designed specifically for sugarcane cultivation. It contains essential nutrients and organic matter that improve soil health and crop yield.",
            "metadata": {"type": "product_info", "crop": "sugarcane"}
        },
        {
            "content": "Navyakosh fertilizer application rate: Apply 25-30 kg per acre during planting. For ratoon crops, apply 20-25 kg per acre after each harvest.",
            "metadata": {"type": "application_rate", "crop": "sugarcane"}
        },
        {
            "content": "Navyakosh timing for sugarcane: Apply at the time of planting or within 30 days of planting. For ratoon crops, apply immediately after harvesting the previous crop.",
            "metadata": {"type": "timing", "crop": "sugarcane"}
        },
        {
            "content": "Navyakosh benefits for sugarcane: Improves soil structure, increases organic matter content, enhances nutrient availability, promotes beneficial microbial activity, and increases sugar content in cane.",
            "metadata": {"type": "benefits", "crop": "sugarcane"}
        },
        {
            "content": "Navyakosh contains NPK (Nitrogen, Phosphorus, Potassium) in balanced proportions along with organic carbon, calcium, magnesium, and trace elements essential for sugarcane growth.",
            "metadata": {"type": "composition", "crop": "sugarcane"}
        },
        {
            "content": "Navyakosh application method: Broadcast the fertilizer uniformly over the field and incorporate into soil through cultivation. Can be applied through furrow placement during planting.",
            "metadata": {"type": "application_method", "crop": "sugarcane"}
        },
        {
            "content": "Navyakosh storage: Store in a cool, dry place away from direct sunlight. Keep away from moisture and ensure proper ventilation. Use within 2 years of manufacturing date.",
            "metadata": {"type": "storage", "product": "navyakosh"}
        },
        {
            "content": "Navyakosh compatibility: Can be mixed with other organic fertilizers. Compatible with most chemical fertilizers but conduct a small test before large-scale mixing.",
            "metadata": {"type": "compatibility", "product": "navyakosh"}
        }
    ]
    
    print("🚀 Starting Navyakosh data ingestion...")
    
    success_count = 0
    for doc in documents:
        if ingest_document(doc["content"], doc["metadata"]):
            success_count += 1
    
    print(f"\n📊 Ingestion Summary:")
    print(f"✅ Successfully added: {success_count}/{len(documents)} documents")
    print(f"🎯 Model used: BAAI/bge-small-en-v1.5")
    print(f"📏 Embedding dimensions: 384")

if __name__ == "__main__":
    print("🔧 RAG System Data Ingestion")
    print("=" * 40)
    
    # Setup database
    if setup_database():
        # Clear existing data
        if clear_database():
            # Ingest new data with BAAI model
            ingest_navyakosh_data()
            print("\n✅ Data ingestion complete!")
        else:
            print("❌ Failed to clear database")
    else:
        print("❌ Failed to setup database")
