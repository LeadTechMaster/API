"""
SerpApi - Apple App Store Search
Search for apps on Apple App Store
REAL DATA ONLY - NO MOCK DATA
"""

import os
import requests
from typing import Dict

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def search_apple_apps(query: str, country: str = "us") -> Dict:
    """
    Search for apps on Apple App Store (e.g., moving calculator apps, booking apps)
    
    Args:
        query: The search query (e.g., "moving calculator", "moving cost estimator")
        country: Country code (default: "us")
        
    Returns:
        Dict with App Store results including ratings, reviews, prices
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "apple_app_store",
            "term": query,
            "country": country,
            "api_key": SERPAPI_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract app results
        apps = []
        for item in data.get("organic_results", []):
            apps.append({
                "app_name": item.get("title", ""),
                "app_id": item.get("product_id", ""),
                "developer": item.get("developer", ""),
                "app_store_url": item.get("link", ""),
                "rating": item.get("rating"),
                "reviews_count": item.get("reviews"),
                "price": item.get("price", "Free"),
                "description": item.get("description", ""),
                "category": item.get("category", ""),
                "thumbnail": item.get("thumbnail", ""),
                "version": item.get("version", ""),
                "size": item.get("size", ""),
                "age_rating": item.get("age_rating", ""),
                "position": item.get("position", 0)
            })
        
        result = {
            "query": query,
            "country": country,
            "total_results": len(apps),
            "apps": apps,
            "status": "success",
            "search_metadata": data.get("search_metadata", {})
        }
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            "query": query,
            "country": country,
            "status": "error",
            "error": str(e)
        }
    except Exception as e:
        return {
            "query": query,
            "country": country,
            "status": "error",
            "error": f"Unexpected error: {str(e)}"
        }


