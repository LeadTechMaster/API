"""
Google My Business - Listing Information
Get GMB listing details and profile information
"""

import os
import requests
from typing import Dict

GOOGLE_PLACES_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY', 'AIzaSyAzyKYxbA7HWHTU9UV9Z-ELGRQTTeN9dkw')

def get_gmb_listing_info(place_id: str) -> Dict:
    """
    Get complete GMB listing information using Google Places API
    
    Args:
        place_id: The Google Place ID of the business
        
    Returns:
        Dict with complete business listing information
    """
    try:
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        
        params = {
            "place_id": place_id,
            "fields": "name,formatted_address,formatted_phone_number,international_phone_number,website,url,rating,user_ratings_total,price_level,opening_hours,geometry,photos,types,business_status,reviews,editorial_summary",
            "key": GOOGLE_PLACES_API_KEY
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        if data.get("status") != "OK":
            return {
                "place_id": place_id,
                "status": "error",
                "error": data.get("status", "Unknown error")
            }
        
        result_data = data.get("result", {})
        
        # Extract comprehensive listing info
        result = {
            "place_id": place_id,
            "name": result_data.get("name", ""),
            "address": result_data.get("formatted_address", ""),
            "phone": result_data.get("formatted_phone_number", ""),
            "international_phone": result_data.get("international_phone_number", ""),
            "website": result_data.get("website", ""),
            "google_maps_url": result_data.get("url", ""),
            "rating": result_data.get("rating", 0),
            "total_ratings": result_data.get("user_ratings_total", 0),
            "price_level": result_data.get("price_level", 0),
            "business_status": result_data.get("business_status", ""),
            "types": result_data.get("types", []),
            "location": result_data.get("geometry", {}).get("location", {}),
            "opening_hours": result_data.get("opening_hours", {}),
            "photos_count": len(result_data.get("photos", [])),
            "reviews_count": len(result_data.get("reviews", [])),
            "editorial_summary": result_data.get("editorial_summary", {}).get("overview", ""),
            "status": "success",
            "raw_data": result_data
        }
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            "place_id": place_id,
            "status": "error",
            "error": str(e)
        }
    except Exception as e:
        return {
            "place_id": place_id,
            "status": "error",
            "error": f"Unexpected error: {str(e)}"
        }

