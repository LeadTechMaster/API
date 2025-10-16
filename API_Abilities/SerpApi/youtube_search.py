"""
SerpApi - YouTube Search
Search for videos on YouTube
REAL DATA ONLY - NO MOCK DATA
"""

import os
import requests
from typing import Dict

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def search_youtube(query: str, num_results: int = 10) -> Dict:
    """
    Search for videos on YouTube
    
    Args:
        query: The search query (e.g., "moving companies miami")
        num_results: Number of results to return (default: 10)
        
    Returns:
        Dict with YouTube video results including views, likes, engagement
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "youtube",
            "search_query": query,
            "api_key": SERPAPI_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract video results
        videos = []
        for item in data.get("video_results", [])[:num_results]:
            # Extract channel info
            channel = item.get("channel", {})
            
            # Extract view count (parse from string like "1.2M views")
            views_str = item.get("views", "0")
            
            videos.append({
                "video_id": item.get("link", "").split("v=")[-1] if "v=" in item.get("link", "") else "",
                "title": item.get("title", ""),
                "video_url": item.get("link", ""),
                "thumbnail_url": item.get("thumbnail", {}).get("static", ""),
                "channel_name": channel.get("name", ""),
                "channel_url": channel.get("link", ""),
                "channel_thumbnail": channel.get("thumbnail", ""),
                "channel_verified": channel.get("verified", False),
                "description": item.get("description", ""),
                "views": views_str,
                "published_date": item.get("published_date", ""),
                "duration": item.get("length", ""),
                "position": item.get("position", 0)
            })
        
        result = {
            "query": query,
            "total_results": len(videos),
            "videos": videos,
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


