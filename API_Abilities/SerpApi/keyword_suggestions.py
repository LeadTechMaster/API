"""
SerpApi - Keyword Suggestions
Get keyword suggestions and related keywords
"""

import os
import requests
from typing import Dict, List, Optional

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def get_keyword_suggestions(seed_keyword: str, location: str = None) -> Dict:
    """
    Get keyword suggestions based on a seed keyword
    
    Args:
        seed_keyword: The seed keyword to get suggestions for
        location: Optional location for localized suggestions
        
    Returns:
        Dict with keyword suggestions
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "google_autocomplete",
            "q": seed_keyword,
            "api_key": SERPAPI_API_KEY
        }
        
        if location:
            params["gl"] = location
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract suggestions
        suggestions = data.get("suggestions", [])
        
        result = {
            "seed_keyword": seed_keyword,
            "location": location,
            "suggestions": [s.get("value") for s in suggestions if "value" in s],
            "total_suggestions": len(suggestions),
            "status": "success",
            "raw_data": data
        }
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            "seed_keyword": seed_keyword,
            "location": location,
            "status": "error",
            "error": str(e)
        }
    except Exception as e:
        return {
            "seed_keyword": seed_keyword,
            "location": location,
            "status": "error",
            "error": f"Unexpected error: {str(e)}"
        }

