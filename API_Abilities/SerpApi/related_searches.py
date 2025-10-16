"""
SerpApi Related Searches
Get related search queries
"""

import os
import requests
from typing import Dict, List

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def get_related_searches(query: str, location: str = None) -> Dict:
    """
    Get related search queries for a keyword
    
    Args:
        query: The search query to find related searches for
        location: Optional location for localized results
        
    Returns:
        Dict with related search queries
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "google",
            "q": query,
            "api_key": SERPAPI_API_KEY,
            "num": 10
        }
        
        if location:
            params["location"] = location
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract related searches
        related_searches_data = data.get("related_searches", [])
        related_searches = []
        
        for item in related_searches_data:
            related_searches.append({
                "query": item.get("query", ""),
                "link": item.get("link", "")
            })
        
        # Also get "people also search for" if available
        people_also_search = data.get("people_also_search_for", [])
        
        result = {
            "query": query,
            "location": location,
            "related_searches": related_searches,
            "people_also_search_for": people_also_search,
            "total_related": len(related_searches),
            "status": "success"
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

