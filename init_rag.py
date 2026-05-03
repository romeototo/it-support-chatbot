from rag_engine import RAGEngine
import os
from pathlib import Path

def init():
    print("Initializing RAG Database...")
    
    # Check for API Key (Optional)
    api_key = os.getenv("GOOGLE_API_KEY") or ""
    if not api_key:
        print("Warning: GOOGLE_API_KEY not found. Using local embedding model.")
    
    engine = RAGEngine(api_key=api_key)
    
    kb_path = Path(__file__).parent / "knowledge_base.json"
    if not kb_path.exists():
        print(f"Error: {kb_path} not found!")
        return
        
    count = engine.ingest_json(kb_path)
    print(f"Successfully ingested {count} FAQs into ChromaDB.")
    print("📁 Database location: ./chroma_db")

if __name__ == "__main__":
    init()
