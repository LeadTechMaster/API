"""
SerpApi - LinkedIn Jobs Search
Search for job listings on LinkedIn
REAL DATA ONLY - NO MOCK DATA
"""

import os
import requests
from typing import Dict

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def search_linkedin_jobs(query: str, location: str, num_results: int = 10) -> Dict:
    """
    Search for job listings on LinkedIn (company sizing, hiring patterns)
    
    Args:
        query: The job search query (e.g., "mover", "moving company operations")
        location: The location to search in (e.g., "Miami, FL")
        num_results: Number of results to return
        
    Returns:
        Dict with LinkedIn job listings including company info, salary estimates
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "linkedin_jobs",
            "keywords": query,
            "location": location,
            "api_key": SERPAPI_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract job listings
        jobs = []
        for item in data.get("jobs", [])[:num_results]:
            jobs.append({
                "job_title": item.get("title", ""),
                "company_name": item.get("company", ""),
                "company_url": item.get("company_link", ""),
                "job_url": item.get("job_link", ""),
                "location": item.get("location", ""),
                "posted_date": item.get("posted_at", ""),
                "description_snippet": item.get("description", ""),
                "seniority_level": item.get("seniority_level", ""),
                "employment_type": item.get("employment_type", ""),
                "job_function": item.get("job_function", ""),
                "industries": item.get("industries", ""),
                "position": item.get("position", 0)
            })
        
        result = {
            "query": query,
            "location": location,
            "total_results": len(jobs),
            "jobs": jobs,
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


