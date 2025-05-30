from typing import List, Dict, Any
from rag_utils.custom_utils import query_vector_db

def search_relevant_articles(query: str, n_results: int = 3) -> List[Dict[str, Any]]:
    """Tool to search and retrieve relevant articles from the vector database based on a query.
    
    Args:
        query: The search query string.
        n_results: The number of relevant documents to retrieve.
        
    Returns:
        A list of dictionaries, where each dictionary contains the 'text', 'source', 
        and 'page_number' of a retrieved document chunk.
    """
    print(f"--- Tool: search_relevant_articles (Query: '{query}', N Results: {n_results}) ---")
    if not query:
        # It's good for tools to return structured error information if ADK handles it, 
        # or raise an exception if that's the preferred ADK pattern.
        # For now, returning a list with an error message as part of the data.
        print("Error: Query cannot be empty for search_relevant_articles.")
        return [{"error": "Query cannot be empty", "text": ""}]

    retrieved_documents = query_vector_db(query_texts=[query], n_results=n_results)
    
    if not retrieved_documents:
        return [{"text": "No relevant documents found for the query.", "source": "system", "page_number": 0}]
        
    return retrieved_documents 