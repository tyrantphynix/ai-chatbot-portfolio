import chromadb
# Disable ChromaDB telemetry
os.environ["CHROMA_TELEMETRY_ENABLED"] = "false"
from pathlib import Path
import os

class VectorService:
    def __init__(self, data_path: str = "./chroma_data"):
        """Initialize ChromaDB with persistent storage using new API"""
        # Create data directory if it doesn't exist
        Path(data_path).mkdir(parents=True, exist_ok=True)
        
        # Initialize ChromaDB with new persistent client API
        self.client = chromadb.PersistentClient(path=data_path)
        self.collection = self._get_or_create_collection()
    
    def _get_or_create_collection(self):
        """Create or retrieve the knowledge base collection"""
        return self.client.get_or_create_collection(
            name="knowledge_base",
            metadata={"hnsw:space": "cosine"}
        )
    
    def add_documents(self, documents: list, metadatas: list = None, ids: list = None):
        """Add documents to the vector store"""
        if metadatas is None:
            metadatas = [{"source": f"doc_{i}"} for i in range(len(documents))]
        if ids is None:
            ids = [f"id_{i}" for i in range(len(documents))]
        
        self.collection.add(
            documents=documents,
            metadatas=metadatas,
            ids=ids
        )
        return len(documents)
    
    def search(self, query: str, n_results: int = 3):
        """Search for similar documents"""
        results = self.collection.query(
            query_texts=[query],
            n_results=n_results
        )
        
        # Format results
        return {
            "documents": results["documents"][0] if results["documents"] else [],
            "metadatas": results["metadatas"][0] if results["metadatas"] else [],
            "distances": results["distances"][0] if results["distances"] else []
        }
    
    def delete_all(self):
        """Clear all documents (for testing)"""
        self.client.delete_collection(name="knowledge_base")
        self.collection = self._get_or_create_collection()

# Initialize globally
vector_service = VectorService()
