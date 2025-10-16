"""
SerpApi Image Search
Search Google Images
"""

import os
import requests
from typing import Dict, List

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def search_images(query: str, num_results: int = 20) -> Dict:
    """
    Search for images on Google Images
    
    Args:
        query: The image search query
        num_results: Number of image results to return (default: 20)
        
    Returns:
        Dict with image search results
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "google_images",
            "q": query,
            "api_key": SERPAPI_API_KEY,
            "num": num_results
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract image results
        images = []
        for item in data.get("images_results", []):
            images.append({
                "position": item.get("position", 0),
                "title": item.get("title", ""),
                "link": item.get("link", ""),
                "original": item.get("original", ""),
                "thumbnail": item.get("thumbnail", ""),
                "source": item.get("source", ""),
                "source_link": item.get("source_link", "")
            })
        
        result = {
            "query": query,
            "total_images": len(images),
            "images": images,
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

