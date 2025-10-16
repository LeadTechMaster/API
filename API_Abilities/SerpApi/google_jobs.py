"""
SerpApi - Google Jobs Search
Search for job listings on Google Jobs
REAL DATA ONLY - NO MOCK DATA
"""

import os
import requests
from typing import Dict

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def search_jobs(query: str, location: str, num_results: int = 10) -> Dict:
    """
    Search for job listings on Google Jobs
    
    Args:
        query: The job search query (e.g., "mover", "moving company")
        location: The location to search in (e.g., "Miami, FL")
        num_results: Number of results to return (default: 10)
        
    Returns:
        Dict with job listings including salary, company, requirements
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "google_jobs",
            "q": query,
            "location": location,
            "api_key": SERPAPI_API_KEY,
            "hl": "en"
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract job listings
        jobs = []
        for item in data.get("jobs_results", [])[:num_results]:
            # Extract salary info
            detected_extensions = item.get("detected_extensions", {})
            salary = detected_extensions.get("salary", "")
            schedule = detected_extensions.get("schedule_type", "")
            
            jobs.append({
                "job_title": item.get("title", ""),
                "company_name": item.get("company_name", ""),
                "location": item.get("location", ""),
                "description": item.get("description", ""),
                "thumbnail": item.get("thumbnail", ""),
                "extensions": item.get("extensions", []),
                "salary": salary,
                "schedule_type": schedule,
                "posted_at": item.get("detected_extensions", {}).get("posted_at", ""),
                "work_from_home": detected_extensions.get("work_from_home", False),
                "job_highlights": item.get("job_highlights", []),
                "related_links": item.get("related_links", []),
                "job_id": item.get("job_id", ""),
                "apply_options": item.get("apply_options", [])
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

def get_job_details(job_id: str) -> Dict:
    """
    Get detailed information for a specific job listing
    
    Args:
        job_id: The Google Jobs job ID
        
    Returns:
        Dict with detailed job information
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "google_jobs_listing",
            "q": job_id,
            "api_key": SERPAPI_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract detailed job info
        apply_options = []
        for option in data.get("apply_options", []):
            apply_options.append({
                "title": option.get("title", ""),
                "link": option.get("link", "")
            })
        
        result = {
            "job_title": data.get("title", ""),
            "company_name": data.get("company_name", ""),
            "location": data.get("location", ""),
            "description": data.get("description", ""),
            "highlights": data.get("job_highlights", []),
            "apply_options": apply_options,
            "related_jobs": data.get("related_jobs_link", ""),
            "status": "success"
        }
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error": str(e)
        }
    except Exception as e:
        return {
            "status": "error",
            "error": f"Unexpected error: {str(e)}"
        }


