"""
SerpApi - Google Patents Search
Search for patents (equipment innovations, moving technology)
REAL DATA ONLY - NO MOCK DATA
"""

import os
import requests
from typing import Dict

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def search_patents(query: str, num_results: int = 10) -> Dict:
    """
    Search for patents on Google Patents (moving equipment, packing technology)
    
    Args:
        query: The search query (e.g., "moving equipment", "packing materials")
        num_results: Number of results to return
        
    Returns:
        Dict with patent results including titles, inventors, dates
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "google_patents",
            "q": query,
            "api_key": SERPAPI_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract patent results
        patents = []
        for item in data.get("organic_results", [])[:num_results]:
            patents.append({
                "title": item.get("title", ""),
                "patent_id": item.get("patent_id", ""),
                "patent_url": item.get("link", ""),
                "inventor": item.get("inventor", ""),
                "assignee": item.get("assignee", ""),
                "publication_date": item.get("publication_date", ""),
                "filing_date": item.get("filing_date", ""),
                "abstract": item.get("snippet", ""),
                "thumbnail": item.get("thumbnail", ""),
                "position": item.get("position", 0)
            })
        
        result = {
            "query": query,
            "total_results": len(patents),
            "patents": patents,
            "status": "success",
            "search_metadata": data.get("search_metadata", {})
        }
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            "query": query,
            "status": "error",
            "error": str(e)
        }
    except Exception as e:
        return {
            "query": query,
            "status": "error",
            "error": f"Unexpected error: {str(e)}"
        }


