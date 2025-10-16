"""
SerpApi - Walmart Product Search
Search for products on Walmart (moving supplies comparison)
REAL DATA ONLY - NO MOCK DATA
"""

import os
import requests
from typing import Dict

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def search_walmart_products(query: str) -> Dict:
    """
    Search for products on Walmart (moving boxes, packing supplies)
    
    Args:
        query: The search query (e.g., "moving boxes", "packing tape")
        
    Returns:
        Dict with Walmart product results including prices, ratings, availability
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "walmart",
            "query": query,
            "api_key": SERPAPI_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract product results
        products = []
        for item in data.get("organic_results", []):
            # Extract primary offer
            primary_offer = item.get("primary_offer", {})
            
            products.append({
                "product_name": item.get("title", ""),
                "product_id": item.get("us_item_id", ""),
                "product_url": item.get("product_page_url", ""),
                "rating": item.get("rating"),
                "reviews_count": item.get("reviews"),
                "price": primary_offer.get("offer_price"),
                "was_price": primary_offer.get("list_price"),
                "savings": primary_offer.get("savings"),
                "in_stock": primary_offer.get("in_stock", False),
                "shipping": primary_offer.get("shipping_options", ""),
                "thumbnail": item.get("thumbnail", ""),
                "seller": item.get("seller_name", "Walmart"),
                "position": item.get("position", 0)
            })
        
        result = {
            "query": query,
            "total_results": len(products),
            "products": products,
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


