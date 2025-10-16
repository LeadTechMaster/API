"""
SerpApi Google Search
General Google search results
"""

import os
import requests
from typing import Dict, Optional

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def google_search(query: str, location: str = None, num_results: int = 10) -> Dict:
    """
    Perform Google search and get results
    
    Args:
        query: The search query
        location: Optional location for localized results
        num_results: Number of results to return (default: 10)
        
    Returns:
        Dict with search results including organic results, ads, featured snippets
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "google",
            "q": query,
            "api_key": SERPAPI_API_KEY,
            "num": num_results
        }
        
        if location:
            params["location"] = location
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract organic results
        organic_results = []
        for item in data.get("organic_results", []):
            organic_results.append({
                "position": item.get("position", 0),
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "displayed_link": item.get("displayed_link", ""),
                "snippet": item.get("snippet", ""),
                "date": item.get("date", "")
            })
        
        # Extract ads
        ads = []
        for item in data.get("ads", []):
            ads.append({
                "position": item.get("position", 0),
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "displayed_link": item.get("displayed_link", ""),
                "snippet": item.get("snippet", "")
            })
        
        result = {
            "query": query,
            "location": location,
            "total_results": len(organic_results),
            "organic_results": organic_results,
            "ads": ads,
            "featured_snippet": data.get("answer_box", {}),
            "knowledge_graph": data.get("knowledge_graph", {}),
            "status": "success",
            "search_metadata": data.get("search_metadata", {})
        }
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            "query": query,
            "location": location,
            "status": "error",
            "error": str(e)
        }
    except Exception as e:
        return {
            "query": query,
            "location": location,
            "status": "error",
            "error": f"Unexpected error: {str(e)}"
        }

