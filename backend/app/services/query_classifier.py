from app.services.llm_service import llm_service

class QueryClassifier:
    """Classifies user queries to determine appropriate response strategy"""
    
    CLASSIFICATION_PROMPT = """Classify the following user query into ONE category:

Categories:
1. CASUAL - Greetings, small talk, how are you, thanks, bye (no specific information needed)
2. REALTIME - Questions about current events, weather, sports scores, stock prices, news (requires internet search)
3. KNOWLEDGE - Questions that can be answered from existing documentation or knowledge base

Query: {query}

Respond with ONLY one word: CASUAL, REALTIME, or KNOWLEDGE"""

    def classify_query(self, query: str) -> str:
        """
        Classify query type
        Returns: 'CASUAL', 'REALTIME', or 'KNOWLEDGE'
        """
        prompt = self.CLASSIFICATION_PROMPT.format(query=query)
        
        # Use LLM to classify
        response = llm_service.llm.invoke(prompt)
        classification = response.content.strip().upper()
        
        # Validate response
        if classification not in ['CASUAL', 'REALTIME', 'KNOWLEDGE']:
            # Default to knowledge-based if unclear
            return 'CASUAL'
        
        return classification

# Global instance
query_classifier = QueryClassifier()
