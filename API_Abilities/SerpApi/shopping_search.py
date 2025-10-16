"""
SerpApi Shopping Search
Search Google Shopping results
"""

import os
import requests
from typing import Dict, Optional

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def search_shopping(query: str, location: str = None, num_results: int = 20) -> Dict:
    """
    Search for shopping/product results on Google Shopping
    
    Args:
        query: The product search query
        location: Optional location for localized shopping results
        num_results: Number of results to return (default: 20)
        
    Returns:
        Dict with shopping results
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "google_shopping",
            "q": query,
            "api_key": SERPAPI_API_KEY,
            "num": num_results
        }
        
        if location:
            params["location"] = location
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract shopping results
        shopping_results = []
        for item in data.get("shopping_results", []):
            shopping_results.append({
                "position": item.get("position", 0),
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "product_link": item.get("product_link", ""),
                "product_id": item.get("product_id", ""),
                "source": item.get("source", ""),
                "price": item.get("price", ""),
                "extracted_price": item.get("extracted_price", 0),
                "rating": item.get("rating", 0),
                "reviews": item.get("reviews", 0),
                "thumbnail": item.get("thumbnail", ""),
                "delivery": item.get("delivery", ""),
                "extensions": item.get("extensions", [])
            })
        
        result = {
            "query": query,
            "location": location,
            "total_results": len(shopping_results),
            "products": shopping_results,
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

