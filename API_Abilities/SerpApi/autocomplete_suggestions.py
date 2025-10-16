"""
SerpApi - Autocomplete Suggestions
Get Google autocomplete/suggest keywords
"""

import os
import requests
from typing import Dict, List

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def get_autocomplete_suggestions(partial_keyword: str, location: str = None) -> Dict:
    """
    Get Google autocomplete suggestions as user types
    
    Args:
        partial_keyword: The partial keyword to get suggestions for
        location: Optional location code (e.g., "us", "uk")
        
    Returns:
        Dict with autocomplete suggestions
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "google_autocomplete",
            "q": partial_keyword,
            "api_key": SERPAPI_API_KEY
        }
        
        if location:
            params["gl"] = location
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract suggestions
        suggestions_data = data.get("suggestions", [])
        suggestions = [s.get("value", "") for s in suggestions_data if "value" in s]
        
        result = {
            "partial_keyword": partial_keyword,
            "location": location,
            "suggestions": suggestions,
            "total_suggestions": len(suggestions),
            "status": "success",
            "raw_data": data
        }
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            "partial_keyword": partial_keyword,
            "location": location,
            "status": "error",
            "error": str(e)
        }
    except Exception as e:
        return {
            "partial_keyword": partial_keyword,
            "location": location,
            "status": "error",
            "error": f"Unexpected error: {str(e)}"
        }

