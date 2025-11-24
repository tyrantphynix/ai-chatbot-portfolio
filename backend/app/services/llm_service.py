from langchain_groq import ChatGroq
from langchain.prompts import ChatPromptTemplate
from langchain_core.output_parsers import StrOutputParser
from app.core.config import settings
from typing import List, Dict

class LLMService:
    def __init__(self):
        # Initialize Groq LLM
        self.llm = ChatGroq(
            api_key=settings.GROQ_API_KEY,
            model="llama-3.3-70b-versatile",
            temperature=0.7,
            max_tokens=1024
        )
    
    def create_rag_prompt(self):
        """Create a prompt template for RAG"""
        template = """You are a helpful AI assistant. Answer the user's question based on the provided context.

        Context:
        {context}

        Question: {question}

        If the context doesn't contain relevant information, politely say so.
        Provide a clear, concise answer."""
        
        return ChatPromptTemplate.from_template(template)
    
    def answer_with_context(self, question: str, context: List[str]) -> str:
        """Generate answer using RAG"""
        # Format context
        context_str = "\n".join([f"- {doc}" for doc in context])
        
        # Create prompt and chain
        prompt = self.create_rag_prompt()
        chain = prompt | self.llm | StrOutputParser()
        
        # Generate answer
        answer = chain.invoke({
            "context": context_str,
            "question": question
        })
        
        return answer
    
    def answer_direct(self, question: str) -> str:
        """Generate answer without context (for general questions)"""
        messages = [
            ("system", "You are a helpful AI assistant."),
            ("human", question)
        ]
        
        answer = self.llm.invoke(messages)
        return answer.content

# Initialize globally
llm_service = LLMService()
