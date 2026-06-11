"""Initialize RAG database from knowledge base."""
import os
import logging
from pathlib import Path
from rag_engine import RAGEngine

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO, format='%(asctime)s [%(levelname)s] %(message)s')

def initialize_rag_database():
    """Ingest knowledge base into ChromaDB vector database."""
    logger.info("Initializing RAG Database...")
    
    api_key = os.getenv("GOOGLE_API_KEY") or ""
    if not api_key:
        logger.warning("GOOGLE_API_KEY not found. Using local embedding model.")
    
    engine = RAGEngine(api_key=api_key)
    
    kb_path = Path(__file__).parent / "knowledge_base.json"
    if not kb_path.exists():
        logger.error(f"Knowledge base not found: {kb_path}")
        return
        
    count = engine.ingest_json(kb_path)
    logger.info(f"Successfully ingested {count} FAQs into ChromaDB.")
    logger.info("Database location: ./chroma_db")

if __name__ == "__main__":
    initialize_rag_database()
