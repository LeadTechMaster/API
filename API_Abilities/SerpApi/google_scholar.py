#!/usr/bin/env python3
"""
Google Scholar API - Academic research and papers
Provides scholarly articles and research data
"""

import requests
import os
from typing import Dict, List, Optional

# Get API key from environment or use hardcoded fallback
SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def search_scholar(query: str, num_results: int = 10, year_start: Optional[int] = None, year_end: Optional[int] = None) -> Dict:
    """
    Search Google Scholar for academic papers
    
    Args:
        query: Search query
        num_results: Number of results to return
        year_start: Start year for publication date filter
        year_end: End year for publication date filter
    
    Returns:
        Dict with scholarly results and metadata
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "google_scholar",
            "q": query,
            "api_key": SERPAPI_API_KEY,
            "num": num_results
        }
        
        if year_start:
            params["as_ylo"] = year_start
        if year_end:
            params["as_yhi"] = year_end
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract organic results (papers)
        papers = []
        if "organic_results" in data:
            for result in data["organic_results"]:
                papers.append({
                    "title": result.get("title", ""),
                    "link": result.get("link", ""),
                    "snippet": result.get("snippet", ""),
                    "position": result.get("position", 0),
                    "authors": result.get("publication_info", {}).get("authors", []),
                    "year": result.get("publication_info", {}).get("summary", ""),
                    "citations": result.get("inline_links", {}).get("cited_by", {}).get("total", 0),
                    "pdf_link": result.get("inline_links", {}).get("serpapi_scholar_link", ""),
                    "journal": result.get("publication_info", {}).get("summary", "").split(" - ")[-1] if result.get("publication_info", {}).get("summary") else ""
                })
        
        # Extract related queries
        related_queries = []
        if "related_searches" in data:
            for related in data["related_searches"]:
                related_queries.append({
                    "query": related.get("query", ""),
                    "link": related.get("link", "")
                })
        
        return {
            "status": "success",
            "query": query,
            "total_papers": len(papers),
            "papers": papers,
            "related_queries": related_queries,
            "total_related": len(related_queries),
            "search_engine": "Google Scholar",
            "academic_focus": True,
            "year_range": f"{year_start}-{year_end}" if year_start and year_end else "All years",
            "api_response_time": data.get("search_metadata", {}).get("total_time_taken", 0)
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error": f"Request failed: {str(e)}",
            "query": query,
            "search_engine": "Google Scholar"
        }
    except Exception as e:
        return {
            "status": "error", 
            "error": f"Unexpected error: {str(e)}",
            "query": query,
            "search_engine": "Google Scholar"
        }

def get_scholar_author(author_name: str, num_results: int = 10) -> Dict:
    """
    Search for a specific author on Google Scholar
    
    Args:
        author_name: Name of the author
        num_results: Number of results to return
    
    Returns:
        Dict with author's papers and profile
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "google_scholar_profiles",
            "mauthors": author_name,
            "api_key": SERPAPI_API_KEY,
            "num": num_results
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        profiles = []
        if "profiles" in data:
            for profile in data["profiles"]:
                profiles.append({
                    "name": profile.get("name", ""),
                    "affiliation": profile.get("affiliations", ""),
                    "interests": profile.get("interests", []),
                    "citations": profile.get("cited_by", {}).get("total", 0),
                    "h_index": profile.get("cited_by", {}).get("table", [{}])[0].get("h_index", 0),
                    "i10_index": profile.get("cited_by", {}).get("table", [{}])[0].get("i10_index", 0),
                    "profile_link": profile.get("link", "")
                })
        
        return {
            "status": "success",
            "author_name": author_name,
            "total_profiles": len(profiles),
            "profiles": profiles,
            "search_engine": "Google Scholar"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Error searching author: {str(e)}",
            "author_name": author_name,
            "search_engine": "Google Scholar"
        }

if __name__ == "__main__":
    # Test the API
    result = search_scholar("moving companies logistics", 5, 2020, 2025)
    print(f"Scholar Papers: {result['total_papers']} found")
    
    author = get_scholar_author("logistics management", 3)
    print(f"Scholar Authors: {author['total_profiles']} found")

