#!/usr/bin/env python3
"""
DuckDuckGo Search API - Privacy-focused search engine
Provides alternative search results without tracking
"""

import requests
import os
from typing import Dict, List, Optional

# Get API key from environment or use hardcoded fallback
SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def search_duckduckgo(query: str, num_results: int = 10, location: str = "Miami, FL") -> Dict:
    """
    Search DuckDuckGo for results
    
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
            "engine": "duckduckgo",
            "q": query,
            "api_key": SERPAPI_API_KEY,
            "kl": "us-en",  # Language
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
        
        # Extract instant answers
        instant_answers = []
        if "answer_box" in data:
            instant_answers.append({
                "type": "answer_box",
                "answer": data["answer_box"].get("answer", ""),
                "source": data["answer_box"].get("source", "")
            })
        
        # Extract related searches
        related_searches = []
        if "related_searches" in data:
            for related in data["related_searches"]:
                related_searches.append({
                    "query": related.get("query", ""),
                    "link": related.get("link", "")
                })
        
        return {
            "status": "success",
            "query": query,
            "location": location,
            "total_results": len(organic_results),
            "organic_results": organic_results,
            "instant_answers": instant_answers,
            "related_searches": related_searches,
            "total_related": len(related_searches),
            "search_engine": "DuckDuckGo",
            "privacy_focused": True,
            "api_response_time": data.get("search_metadata", {}).get("total_time_taken", 0)
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error": f"Request failed: {str(e)}",
            "query": query,
            "search_engine": "DuckDuckGo"
        }
    except Exception as e:
        return {
            "status": "error", 
            "error": f"Unexpected error: {str(e)}",
            "query": query,
            "search_engine": "DuckDuckGo"
        }

def get_duckduckgo_instant_answers(query: str) -> Dict:
    """
    Get DuckDuckGo instant answers
    
    Args:
        query: Search query
    
    Returns:
        Dict with instant answers
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "duckduckgo",
            "q": query,
            "api_key": SERPAPI_API_KEY,
            "kl": "us-en"
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        answers = []
        if "answer_box" in data:
            answers.append({
                "type": "answer_box",
                "answer": data["answer_box"].get("answer", ""),
                "source": data["answer_box"].get("source", ""),
                "title": data["answer_box"].get("title", "")
            })
        
        return {
            "status": "success",
            "query": query,
            "instant_answers": answers,
            "total_answers": len(answers),
            "search_engine": "DuckDuckGo"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Error getting instant answers: {str(e)}",
            "query": query,
            "search_engine": "DuckDuckGo"
        }

if __name__ == "__main__":
    # Test the API
    result = search_duckduckgo("moving companies miami", 5)
    print(f"DuckDuckGo Search Results: {result['total_results']} found")
    
    answers = get_duckduckgo_instant_answers("moving companies")
    print(f"DuckDuckGo Instant Answers: {answers['total_answers']} found")

