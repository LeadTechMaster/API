"""
Google Places - Place Details
Get detailed information about a specific place
"""

import os
import requests
from typing import Dict

GOOGLE_PLACES_API_KEY = os.getenv('GOOGLE_PLACES_API_KEY', 'AIzaSyAzyKYxbA7HWHTU9UV9Z-ELGRQTTeN9dkw')

def get_place_details(place_id: str) -> Dict:
    """
    Get detailed information for a place
    
    Args:
        place_id: The Google Place ID
        
    Returns:
        Dict with place details
    """
    try:
        url = "https://maps.googleapis.com/maps/api/place/details/json"
        
        params = {
            "place_id": place_id,
            "fields": "name,formatted_address,geometry,rating,opening_hours,formatted_phone_number,website,photos,types,price_level,user_ratings_total",
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
        
        result = {
            "place_id": place_id,
            "name": result_data.get("name", ""),
            "address": result_data.get("formatted_address", ""),
            "phone": result_data.get("formatted_phone_number", ""),
            "website": result_data.get("website", ""),
            "rating": result_data.get("rating", 0),
            "total_ratings": result_data.get("user_ratings_total", 0),
            "price_level": result_data.get("price_level", 0),
            "types": result_data.get("types", []),
            "location": result_data.get("geometry", {}).get("location", {}),
            "opening_hours": result_data.get("opening_hours", {}),
            "photos": [photo.get("photo_reference", "") for photo in result_data.get("photos", [])],
            "status": "success"
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

