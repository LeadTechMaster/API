"""
SerpApi - Yelp Business Search
Search for business reviews and ratings on Yelp
REAL DATA ONLY - NO MOCK DATA
"""

import os
import requests
from typing import Dict, Optional

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def search_yelp_businesses(query: str, location: str, num_results: int = 10) -> Dict:
    """
    Search for businesses on Yelp
    
    Args:
        query: The business type or search query (e.g., "moving companies")
        location: The location to search in (e.g., "Miami, FL")
        num_results: Number of results to return (default: 10)
        
    Returns:
        Dict with Yelp business results including ratings, reviews, contact info
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "yelp",
            "find_desc": query,
            "find_loc": location,
            "api_key": SERPAPI_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract business results
        businesses = []
        for item in data.get("organic_results", [])[:num_results]:
            # Extract neighborhood/area
            neighborhoods = item.get("neighborhoods", [])
            neighborhood = neighborhoods[0] if neighborhoods else ""
            
            # Extract categories
            categories = [cat.get("title", "") for cat in item.get("categories", [])]
            
            businesses.append({
                "business_name": item.get("title", ""),
                "yelp_url": item.get("link", ""),
                "rating": item.get("rating"),
                "reviews_count": item.get("reviews"),
                "price_range": item.get("price", ""),
                "categories": categories,
                "address": item.get("address", ""),
                "neighborhood": neighborhood,
                "phone": item.get("phone", ""),
                "is_claimed": item.get("is_claimed", False),
                "snippet": item.get("snippet", ""),
                "position": item.get("position", 0)
            })
        
        result = {
            "query": query,
            "location": location,
            "total_results": len(businesses),
            "businesses": businesses,
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

def get_yelp_reviews(yelp_url: str, num_reviews: int = 10) -> Dict:
    """
    Get detailed reviews for a specific Yelp business
    
    Args:
        yelp_url: The Yelp business URL
        num_reviews: Number of reviews to fetch
        
    Returns:
        Dict with detailed reviews including text, ratings, dates
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "yelp_reviews",
            "url": yelp_url,
            "api_key": SERPAPI_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract reviews
        reviews = []
        for review in data.get("reviews", [])[:num_reviews]:
            user = review.get("user", {})
            
            reviews.append({
                "reviewer_name": user.get("name", ""),
                "reviewer_location": user.get("address", ""),
                "reviewer_friends": user.get("friends"),
                "reviewer_reviews": user.get("reviews"),
                "reviewer_photos": user.get("photos"),
                "rating": review.get("rating"),
                "review_date": review.get("date", ""),
                "review_text": review.get("comment", {}).get("text", ""),
                "helpful_count": review.get("comment", {}).get("votes", {}).get("useful", 0),
                "funny_count": review.get("comment", {}).get("votes", {}).get("funny", 0),
                "cool_count": review.get("comment", {}).get("votes", {}).get("cool", 0)
            })
        
        # Extract business info
        business_info = {}
        if "place_info" in data:
            place = data["place_info"]
            business_info = {
                "business_name": place.get("title", ""),
                "rating": place.get("rating"),
                "reviews_count": place.get("reviews"),
                "price_range": place.get("price", ""),
                "phone": place.get("phone", ""),
                "address": place.get("address", ""),
                "website": place.get("website", "")
            }
        
        result = {
            "business_info": business_info,
            "total_reviews": len(reviews),
            "reviews": reviews,
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


