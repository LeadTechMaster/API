"""
SerpApi - Amazon Product Search
Search for products on Amazon (moving supplies, equipment)
REAL DATA ONLY - NO MOCK DATA
"""

import os
import requests
from typing import Dict

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def search_amazon_products(query: str, domain: str = "amazon.com") -> Dict:
    """
    Search for products on Amazon (moving boxes, packing supplies, equipment)
    
    Args:
        query: The search query (e.g., "moving boxes", "furniture dollies")
        domain: Amazon domain (default: "amazon.com")
        
    Returns:
        Dict with Amazon product results including prices, ratings, Prime availability
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "amazon",
            "amazon_domain": domain,
            "q": query,
            "api_key": SERPAPI_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract product results
        products = []
        for item in data.get("organic_results", []):
            # Extract price info
            price_raw = item.get("price", {})
            price = price_raw.get("value") if isinstance(price_raw, dict) else price_raw
            
            products.append({
                "product_name": item.get("title", ""),
                "asin": item.get("asin", ""),
                "product_url": item.get("link", ""),
                "rating": item.get("rating"),
                "reviews_count": item.get("ratings_total"),
                "price": price,
                "currency": price_raw.get("currency") if isinstance(price_raw, dict) else "USD",
                "is_prime": item.get("is_prime", False),
                "delivery": item.get("delivery", ""),
                "thumbnail": item.get("thumbnail", ""),
                "bestseller_badge": item.get("is_best_seller", False),
                "position": item.get("position", 0)
            })
        
        result = {
            "query": query,
            "domain": domain,
            "total_results": len(products),
            "products": products,
            "status": "success",
            "search_metadata": data.get("search_metadata", {})
        }
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            "query": query,
            "domain": domain,
            "status": "error",
            "error": str(e)
        }
    except Exception as e:
        return {
            "query": query,
            "domain": domain,
            "status": "error",
            "error": f"Unexpected error: {str(e)}"
        }


