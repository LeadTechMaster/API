"""
SerpApi - Keyword Difficulty
Analyze keyword competition and difficulty
"""

import os
import requests
from typing import Dict, Optional

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def get_keyword_difficulty(keyword: str, location: str = None) -> Dict:
    """
    Get keyword difficulty score and competition level by analyzing SERP results
    
    Args:
        keyword: The keyword to analyze
        location: Optional location for localized analysis
        
    Returns:
        Dict with keyword difficulty metrics based on SERP analysis
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
        
        # Analyze competition based on SERP features
        organic_results = data.get("organic_results", [])
        ads = data.get("ads", [])
        
        # Calculate difficulty indicators
        has_ads = len(ads) > 0
        num_ads = len(ads)
        has_featured_snippet = "answer_box" in data
        has_knowledge_graph = "knowledge_graph" in data
        has_local_results = "local_results" in data
        
        # Extract domain authorities (simplified - based on well-known domains)
        high_authority_domains = [
            "wikipedia.org", "amazon.com", "youtube.com", "facebook.com",
            "linkedin.com", "twitter.com", "instagram.com", "reddit.com"
        ]
        
        high_authority_count = 0
        for result in organic_results[:10]:
            link = result.get("link", "")
            if any(domain in link for domain in high_authority_domains):
                high_authority_count += 1
        
        # Calculate difficulty score (0-100)
        difficulty_score = 0
        difficulty_score += num_ads * 5  # Each ad increases difficulty
        difficulty_score += 20 if has_featured_snippet else 0
        difficulty_score += 15 if has_knowledge_graph else 0
        difficulty_score += high_authority_count * 7
        difficulty_score = min(difficulty_score, 100)
        
        # Determine difficulty level
        if difficulty_score < 30:
            difficulty_level = "Easy"
        elif difficulty_score < 60:
            difficulty_level = "Medium"
        else:
            difficulty_level = "Hard"
        
        result = {
            "keyword": keyword,
            "location": location,
            "difficulty_score": difficulty_score,
            "difficulty_level": difficulty_level,
            "metrics": {
                "total_organic_results": len(organic_results),
                "num_ads": num_ads,
                "has_featured_snippet": has_featured_snippet,
                "has_knowledge_graph": has_knowledge_graph,
                "has_local_results": has_local_results,
                "high_authority_domains_in_top10": high_authority_count
            },
            "status": "success"
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

