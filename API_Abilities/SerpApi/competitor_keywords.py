"""
SerpApi - Competitor Keywords
Find keywords competitors are ranking for
"""

import os
import requests
from typing import Dict, List

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def get_competitor_keywords(competitor_domain: str, location: str = "United States", num_results: int = 100) -> Dict:
    """
    Get keywords that a competitor domain ranks for by analyzing their visible content
    
    Args:
        competitor_domain: The competitor domain to analyze
        location: Location for search context
        num_results: Number of results to analyze
        
    Returns:
        Dict with competitor keyword analysis
    """
    try:
        # Search for the domain to see what they rank for
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "google",
            "q": f"site:{competitor_domain}",
            "location": location,
            "api_key": SERPAPI_API_KEY,
            "num": num_results
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract organic results from the competitor
        results = []
        for item in data.get("organic_results", []):
            title = item.get("title", "")
            snippet = item.get("snippet", "")
            link = item.get("link", "")
            
            # Extract potential keywords from title and snippet
            results.append({
                "url": link,
                "title": title,
                "snippet": snippet,
                "position": item.get("position", 0)
            })
        
        result = {
            "competitor_domain": competitor_domain,
            "location": location,
            "total_pages_found": len(results),
            "pages": results,
            "status": "success",
            "search_metadata": data.get("search_metadata", {})
        }
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            "competitor_domain": competitor_domain,
            "location": location,
            "status": "error",
            "error": str(e)
        }
    except Exception as e:
        return {
            "competitor_domain": competitor_domain,
            "location": location,
            "status": "error",
            "error": f"Unexpected error: {str(e)}"
        }

