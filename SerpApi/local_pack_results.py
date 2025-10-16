"""
SerpApi - Local Pack Results
Get local pack (3-pack) results for keywords
"""

import os
import requests
from typing import Dict, List

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def get_local_pack_results(keyword: str, location: str) -> Dict:
    """
    Get the local 3-pack results for a keyword and location
    
    Args:
        keyword: The keyword to search for
        location: The location to search in (e.g., "New York, NY")
        
    Returns:
        Dict with local pack results
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "google",
            "q": keyword,
            "location": location,
            "api_key": SERPAPI_API_KEY,
            "num": 10
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract local pack results
        local_results = data.get("local_results", [])
        
        businesses = []
        for item in local_results:
            businesses.append({
                "position": item.get("position", 0),
                "title": item.get("title", ""),
                "place_id": item.get("place_id", ""),
                "address": item.get("address", ""),
                "phone": item.get("phone", ""),
                "rating": item.get("rating", 0),
                "reviews": item.get("reviews", 0),
                "type": item.get("type", ""),
                "hours": item.get("hours", ""),
                "service_options": item.get("service_options", {}),
                "gps_coordinates": item.get("gps_coordinates", {})
            })
        
        result = {
            "keyword": keyword,
            "location": location,
            "total_results": len(businesses),
            "local_pack": businesses,
            "status": "success"
        }
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            "keyword": keyword,
            "location": location,
            "status": "error",
            "error": str(e)
        }
    except Exception as e:
        return {
            "keyword": keyword,
            "location": location,
            "status": "error",
            "error": f"Unexpected error: {str(e)}"
        }

