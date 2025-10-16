"""
SerpApi Local Business Search
Search for local businesses via Google Maps
"""

import os
import requests
from typing import Dict, List

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def search_local_businesses(query: str, location: str, num_results: int = 20) -> Dict:
    """
    Search for local businesses in a specific area using Google Maps
    
    Args:
        query: The business type or search query (e.g., "restaurants", "plumbers")
        location: The location to search in (e.g., "New York, NY", "90210")
        num_results: Number of results to return (default: 20)
        
    Returns:
        Dict with local business results
    """
    try:
        url = "https://serpapi.com/search"
        
        # Use ll parameter with proper @ format for Google Maps
        params = {
            "engine": "google_maps",
            "q": query,
            "ll": "@25.7617,-80.1918,15z",  # Miami coordinates
            "api_key": SERPAPI_API_KEY,
            "type": "search",
            "num": num_results
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract local business results
        businesses = []
        for item in data.get("local_results", []):
            businesses.append({
                "position": item.get("position", 0),
                "title": item.get("title", ""),
                "place_id": item.get("place_id", ""),
                "data_id": item.get("data_id", ""),
                "rating": item.get("rating", 0),
                "reviews": item.get("reviews", 0),
                "price": item.get("price", ""),
                "type": item.get("type", ""),
                "types": item.get("types", []),
                "address": item.get("address", ""),
                "phone": item.get("phone", ""),
                "website": item.get("website", ""),
                "hours": item.get("hours", ""),
                "service_options": item.get("service_options", {}),
                "gps_coordinates": item.get("gps_coordinates", {}),
                "thumbnail": item.get("thumbnail", "")
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

