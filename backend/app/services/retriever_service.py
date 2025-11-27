from app.services.vector_service import vector_service
from app.services.llm_service import llm_service
from app.services.query_classifier import query_classifier
from app.services.web_search_service import web_search_service

class RetrieverService:
    def __init__(self):
        self.vector_service = vector_service
        self.llm_service = llm_service
        self.classifier = query_classifier
        self.web_search = web_search_service
    
    def retrieve_and_answer(self, query: str) -> dict:
        """
        Main entry point - routes query based on classification
        """
        # Classify the query
        query_type = self.classifier.classify_query(query)
        
        print(f"Query classified as: {query_type}")
        
        if query_type == "KNOWLEDGE":
            return self._handle_knowledge(query)
        elif query_type == "REALTIME":
            return self._handle_realtime(query)
        else:  # CASUAL
            return self._handle_casual(query)
    
    def _handle_casual(self, query: str) -> dict:
        """Handle casual conversational queries - direct LLM without context"""
        from langchain_core.prompts import ChatPromptTemplate
        from langchain_core.output_parsers import StrOutputParser
        
        prompt = f"""You are a friendly AI assistant. Respond naturally and conversationally to this message:

        User: {query}

        Keep your response concise and friendly."""
            
        try:
            # Direct LLM call without retrieval
            response = self.llm_service.llm.invoke(prompt)
            answer = response.content if hasattr(response, 'content') else str(response)
            
            return {
                "answer": answer,
                "sources": ["direct_response"],
                "type": "casual"
            }
        except Exception as e:
            print(f"Casual handler error: {e}")
            return {
                "answer": f"Sorry, I couldn't process that: {str(e)}",
                "sources": [],
                "type": "casual"
            }

    
    def _handle_realtime(self, query: str) -> dict:
        """Handle real-time queries - web search + LLM"""
        try:
            # Search the web
            search_results = self.web_search.search_web(query, num_results=3)
            
            if not search_results:
                return {
                    "answer": "I couldn't find current information about that. Try rephrasing your question.",
                    "sources": [],
                    "type": "realtime_no_results"
                }
            
            # Format search context
            context = self.web_search.format_search_context(search_results)
            
            # Generate answer using search results
            prompt = f"""Based on the following web search results, answer this question:

            Question: {query}

            {context}

            Provide a clear, factual answer based on the search results above."""
            
            answer = self.llm_service.answer_with_context(prompt, context="")
            
            # Extract URLs from results
            sources = [result["url"] for result in search_results]
            
            return {
                "answer": answer,
                "sources": sources,
                "type": "realtime"
            }
        except Exception as e:
            return {
                "answer": f"Error searching for real-time info: {str(e)}",
                "sources": [],
                "type": "realtime_error"
            }
    
    def _handle_knowledge(self, query: str) -> dict:
        """Handle knowledge-based queries - existing RAG pipeline"""
        try:
            # Retrieve relevant documents from vector DB
            search_results = self.vector_service.search(query, n_results=3)
            
            # Extract documents and metadata
            documents = search_results.get("documents", [])
            metadatas = search_results.get("metadatas", [])
            
            if not documents or not documents[0]:
                return {
                    "answer": "I don't have information about that in my knowledge base. Try asking about LangChain, FastAPI, ChromaDB, React, Groq, or Vercel.",
                    "sources": [],
                    "type": "knowledge_no_docs"
                }
            
            # Format context from retrieved documents
            context = "\n\n".join(documents[0]) if documents[0] else ""
            
            # Generate answer using context
            answer = self.llm_service.answer_with_context(query, context)

            # Defensive check
            if not isinstance(answer, str):
                # If it’s a dict or non-string, convert appropriately (or debug)
                answer = str(answer)
            
            # Extract source information
            sources = [meta.get("source", "unknown") for meta in metadatas[0]] if metadatas[0] else []
            
            return {
                "answer": answer,
                "sources": sources,
                "type": "knowledge"
            }
        except Exception as e:
            return {
                "answer": f"Error retrieving from knowledge base: {str(e)}",
                "sources": [],
                "type": "knowledge_error"
            }

# Global instance
retriever_service = RetrieverService()
