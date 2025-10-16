"""
SerpApi Search Trends
Get Google search trends and related searches
"""

import os
import requests
from typing import Dict, Optional

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def get_search_trends(keyword: str, location: str = "US", date_range: str = "today 12-m") -> Dict:
    """
    Get search trends for a keyword using Google Trends
    
    Args:
        keyword: The keyword to analyze trends for
        location: Location code (e.g., "US", "GB", "CA") - default: "US"
        date_range: Date range for trends (e.g., "today 12-m", "today 3-m", "today 1-m")
        
    Returns:
        Dict with search trend data
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "google_trends",
            "q": keyword,
            "api_key": SERPAPI_API_KEY,
            "data_type": "TIMESERIES",
            "geo": location,
            "date": date_range
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract interest over time
        interest_over_time = data.get("interest_over_time", {})
        timeline_data = interest_over_time.get("timeline_data", [])
        
        # Extract related queries
        related_queries = data.get("related_queries", {})
        
        result = {
            "keyword": keyword,
            "location": location,
            "date_range": date_range,
            "interest_over_time": timeline_data,
            "related_queries_rising": related_queries.get("rising", []),
            "related_queries_top": related_queries.get("top", []),
            "status": "success",
            "search_metadata": data.get("search_metadata", {})
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

