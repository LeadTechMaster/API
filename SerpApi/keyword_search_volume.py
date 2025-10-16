"""
SerpApi - Keyword Search Volume
Get search volume data for keywords
"""

import os
import requests
from typing import Dict, Optional

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def get_keyword_search_volume(keyword: str, location: str = "United States") -> Dict:
    """
    Get search volume for a keyword in a specific location
    
    Args:
        keyword: The keyword to analyze
        location: Location for search (default: "United States")
        
    Returns:
        Dict with search volume data
    """
    try:
        # SerpApi Google Trends endpoint for search volume
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "google_trends",
            "q": keyword,
            "api_key": SERPAPI_API_KEY,
            "data_type": "TIMESERIES",
            "geo": location
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract relevant volume data
        result = {
            "keyword": keyword,
            "location": location,
            "status": "success",
            "data": data
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

