import chromadb
from chromadb.utils import embedding_functions
import json
import os
from pathlib import Path

class RAGEngine:
    def __init__(self, db_path="./chroma_db", api_key=None):
        self.db_path = db_path
        self.client = chromadb.PersistentClient(path=db_path)
        
        if api_key:
            self.embedding_fn = embedding_functions.GoogleGenerativeAiEmbeddingFunction(
                api_key=api_key
            )
        else:
            # Fallback to default sentence transformer (runs locally)
            self.embedding_fn = embedding_functions.DefaultEmbeddingFunction()
            
        self.collection = self.client.get_or_create_collection(
            name="it_support_kb",
            embedding_function=self.embedding_fn
        )

    def ingest_json(self, json_path):
        """Read knowledge_base.json and add to vector db"""
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        documents = []
        metadatas = []
        ids = []
        
        idx = 0
        for category in data.get("categories", []):
            cat_name = category.get("name", "General")
            for faq in category.get("faqs", []):
                question = faq.get("question", "")
                answer = faq.get("answer", "")
                
                # We store the question + answer for better context retrieval
                text_to_embed = f"Question: {question}\nAnswer: {answer}"
                
                documents.append(text_to_embed)
                metadatas.append({
                    "category": cat_name,
                    "question": question,
                    "answer": answer
                })
                ids.append(f"faq_{idx}")
                idx += 1
                
        if documents:
            self.collection.upsert(
                documents=documents,
                metadatas=metadatas,
                ids=ids
            )
            return len(documents)
        return 0

    def query(self, user_query, n_results=3):
        """Search for relevant context"""
        results = self.collection.query(
            query_texts=[user_query],
            n_results=n_results
        )
        
        formatted_results = []
        if results['metadatas'] and results['metadatas'][0]:
            for i in range(len(results['metadatas'][0])):
                meta = results['metadatas'][0][i]
                distance = results['distances'][0][i] if 'distances' in results else 0
                formatted_results.append({
                    "question": meta['question'],
                    "answer": meta['answer'],
                    "category": meta['category'],
                    "score": 1 - distance # Approximate confidence
                })
        return formatted_results

if __name__ == "__main__":
    # Test block
    engine = RAGEngine()
    kb_path = Path(__file__).parent / "knowledge_base.json"
    count = engine.ingest_json(kb_path)
    print(f"Ingested {count} documents.")
    
    test_query = "ลืมรหัสผ่านทำไง"
    print(f"\nQuery: {test_query}")
    matches = engine.query(test_query)
    for m in matches:
        print(f"- [{m['category']}] {m['question']} (Score: {m['score']:.2f})")
