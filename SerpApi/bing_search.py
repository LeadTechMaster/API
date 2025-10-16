#!/usr/bin/env python3
"""
Bing Search API - Microsoft's search engine results
Provides alternative search results to compare with Google
"""

import requests
import os
from typing import Dict, List, Optional

# Get API key from environment or use hardcoded fallback
SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def search_bing(query: str, num_results: int = 10, location: str = "Miami, FL") -> Dict:
    """
    Search Bing for results
    
    Args:
        query: Search query
        num_results: Number of results to return
        location: Geographic location for search
    
    Returns:
        Dict with search results and metadata
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "bing",
            "q": query,
            "api_key": SERPAPI_API_KEY,
            "count": num_results,
            "location": location
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract organic results
        organic_results = []
        if "organic_results" in data:
            for result in data["organic_results"]:
                organic_results.append({
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                    "snippet": result.get("snippet", ""),
                    "position": result.get("position", 0),
                    "domain": result.get("displayed_link", "").split("/")[0] if result.get("displayed_link") else ""
                })
        
        # Extract ads
        ads = []
        if "ads" in data:
            for ad in data["ads"]:
                ads.append({
                    "title": ad.get("title", ""),
                    "link": ad.get("link", ""),
                    "snippet": ad.get("snippet", ""),
                    "position": ad.get("position", 0)
                })
        
        return {
            "status": "success",
            "query": query,
            "location": location,
            "total_results": len(organic_results),
            "organic_results": organic_results,
            "ads": ads,
            "total_ads": len(ads),
            "search_engine": "Bing",
            "api_response_time": data.get("search_metadata", {}).get("total_time_taken", 0)
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error": f"Request failed: {str(e)}",
            "query": query,
            "search_engine": "Bing"
        }
    except Exception as e:
        return {
            "status": "error", 
            "error": f"Unexpected error: {str(e)}",
            "query": query,
            "search_engine": "Bing"
        }

def get_bing_autocomplete(query: str, location: str = "Miami, FL") -> Dict:
    """
    Get Bing autocomplete suggestions
    
    Args:
        query: Search query
        location: Geographic location
    
    Returns:
        Dict with autocomplete suggestions
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "bing_autocomplete",
            "q": query,
            "api_key": SERPAPI_API_KEY,
            "location": location
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        suggestions = []
        if "suggestions" in data:
            suggestions = [s.get("value", "") for s in data["suggestions"]]
        
        return {
            "status": "success",
            "query": query,
            "suggestions": suggestions,
            "total_suggestions": len(suggestions),
            "search_engine": "Bing"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Error getting autocomplete: {str(e)}",
            "query": query,
            "search_engine": "Bing"
        }

if __name__ == "__main__":
    # Test the API
    result = search_bing("moving companies miami", 5)
    print(f"Bing Search Results: {result['total_results']} found")
    
    autocomplete = get_bing_autocomplete("moving companies")
    print(f"Bing Autocomplete: {autocomplete['total_suggestions']} suggestions")

