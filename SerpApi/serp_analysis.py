"""
SerpApi - SERP Analysis
Analyze search engine results page (SERP) features
"""

import os
import requests
from typing import Dict, Optional

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def analyze_serp(keyword: str, location: str = None) -> Dict:
    """
    Analyze SERP features (snippets, knowledge graph, ads, etc.)
    
    Args:
        keyword: The keyword to analyze SERP for
        location: Optional location for localized SERP analysis
        
    Returns:
        Dict with comprehensive SERP feature analysis
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "google",
            "q": keyword,
            "api_key": SERPAPI_API_KEY,
            "num": 100
        }
        
        if location:
            params["location"] = location
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Analyze SERP features
        features = {
            "has_ads": "ads" in data and len(data.get("ads", [])) > 0,
            "num_ads": len(data.get("ads", [])),
            "has_featured_snippet": "answer_box" in data or "featured_snippet" in data,
            "has_knowledge_graph": "knowledge_graph" in data,
            "has_local_results": "local_results" in data or "local_pack" in data,
            "has_image_results": "inline_images" in data,
            "has_video_results": "inline_videos" in data,
            "has_shopping_results": "shopping_results" in data,
            "has_people_also_ask": "related_questions" in data,
            "has_related_searches": "related_searches" in data,
            "has_top_stories": "top_stories" in data,
            "has_twitter_results": "twitter_results" in data
        }
        
        # Count organic results
        organic_count = len(data.get("organic_results", []))
        
        # Extract featured snippet if exists
        featured_snippet = None
        if data.get("answer_box"):
            featured_snippet = {
                "title": data["answer_box"].get("title", ""),
                "snippet": data["answer_box"].get("snippet", ""),
                "link": data["answer_box"].get("link", "")
            }
        
        # Extract knowledge graph if exists
        knowledge_graph = None
        if data.get("knowledge_graph"):
            kg = data["knowledge_graph"]
            knowledge_graph = {
                "title": kg.get("title", ""),
                "type": kg.get("type", ""),
                "description": kg.get("description", ""),
                "source": kg.get("source", {})
            }
        
        result = {
            "keyword": keyword,
            "location": location,
            "features": features,
            "organic_results_count": organic_count,
            "featured_snippet": featured_snippet,
            "knowledge_graph": knowledge_graph,
            "local_results_count": len(data.get("local_results", [])),
            "people_also_ask_count": len(data.get("related_questions", [])),
            "related_searches_count": len(data.get("related_searches", [])),
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

