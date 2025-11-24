from app.services.vector_service import vector_service
from app.services.llm_service import llm_service
from typing import List, Dict

class RetrieverService:
    def __init__(self):
        self.vector_service = vector_service
        self.llm_service = llm_service
    
    def retrieve_and_answer(self, question: str, n_results: int = 3) -> Dict:
        """Main RAG pipeline: retrieve context + generate answer"""
        
        # Step 1: Retrieve relevant documents
        search_results = self.vector_service.search(question, n_results=n_results)
        
        # Step 2: Generate answer using retrieved context
        if search_results["documents"]:
            answer = self.llm_service.answer_with_context(
                question=question,
                context=search_results["documents"]
            )
        else:
            answer = self.llm_service.answer_direct(question)
        
        return {
            "answer": answer,
            "sources": search_results["metadatas"],
            "retrieved_docs": search_results["documents"]
        }

# Initialize globally
retriever_service = RetrieverService()
