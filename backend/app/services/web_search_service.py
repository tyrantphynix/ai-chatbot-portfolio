from googlesearch import search
import requests
from bs4 import BeautifulSoup

class WebSearchService:
    """Handles real-time web searches for current information"""
    
    def search_web(self, query: str, num_results: int = 3) -> list:
        """
        Search the web and return top results with snippets
        """
        results = []
        
        try:
            # Get top search result URLs
            urls = list(search(query, num_results=num_results, lang="en"))
            
            for url in urls[:num_results]:
                try:
                    # Fetch page content
                    response = requests.get(url, timeout=5)
                    soup = BeautifulSoup(response.content, 'html.parser')
                    
                    # Extract text snippet (first 200 chars of body text)
                    text = soup.get_text()
                    snippet = ' '.join(text.split())[:200] + "..."
                    
                    results.append({
                        'url': url,
                        'snippet': snippet
                    })
                except Exception as e:
                    print(f"Error fetching {url}: {e}")
                    continue
            
        except Exception as e:
            print(f"Search error: {e}")
        
        return results
    
    def format_search_context(self, search_results: list) -> str:
        """Format search results into context string for LLM"""
        if not search_results:
            return "No search results found."
        
        context = "Here is information from the web:\n\n"
        for idx, result in enumerate(search_results, 1):
            context += f"Source {idx} ({result['url']}):\n{result['snippet']}\n\n"
        
        return context

# Global instance
web_search_service = WebSearchService()
