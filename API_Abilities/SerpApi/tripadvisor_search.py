"""
SerpApi - TripAdvisor Search
Search for businesses and reviews on TripAdvisor
REAL DATA ONLY - NO MOCK DATA
"""

import os
import requests
from typing import Dict

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def search_tripadvisor(query: str, location: str = None) -> Dict:
    """
    Search for businesses on TripAdvisor (useful for storage facilities, moving services)
    
    Args:
        query: The search query (e.g., "storage facilities", "moving services")
        location: Optional location to search in
        
    Returns:
        Dict with TripAdvisor business results including ratings, reviews
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "tripadvisor",
            "q": query,
            "api_key": SERPAPI_API_KEY
        }
        
        if location:
            params["location"] = location
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract business results
        businesses = []
        for item in data.get("organic_results", []):
            businesses.append({
                "business_name": item.get("title", ""),
                "tripadvisor_url": item.get("link", ""),
                "rating": item.get("rating"),
                "reviews_count": item.get("reviews"),
                "address": item.get("address", ""),
                "phone": item.get("phone", ""),
                "description": item.get("description", ""),
                "category": item.get("category", ""),
                "thumbnail": item.get("thumbnail", ""),
                "position": item.get("position", 0)
            })
        
        result = {
            "query": query,
            "location": location,
            "total_results": len(businesses),
            "businesses": businesses,
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


