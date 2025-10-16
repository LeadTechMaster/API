"""
SerpApi News Search
Search Google News results
"""

import os
import requests
from typing import Dict, Optional

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def search_news(query: str, location: str = None, date_range: str = None, num_results: int = 20) -> Dict:
    """
    Search for news articles on Google News
    
    Args:
        query: The news search query
        location: Optional location for localized news
        date_range: Optional date range (e.g., "qdr:d" for past day, "qdr:w" for week, "qdr:m" for month)
        num_results: Number of results to return (default: 20)
        
    Returns:
        Dict with news search results
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "google",
            "q": query,
            "api_key": SERPAPI_API_KEY,
            "tbm": "nws",  # News search
            "num": num_results
        }
        
        if location:
            params["location"] = location
        
        if date_range:
            params["tbs"] = date_range
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract news results
        news_results = []
        for item in data.get("news_results", []):
            news_results.append({
                "position": item.get("position", 0),
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "source": item.get("source", ""),
                "date": item.get("date", ""),
                "snippet": item.get("snippet", ""),
                "thumbnail": item.get("thumbnail", "")
            })
        
        result = {
            "query": query,
            "location": location,
            "date_range": date_range,
            "total_results": len(news_results),
            "news": news_results,
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

