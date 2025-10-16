"""
SerpApi - Enhanced Keyword Volume Tracker
Track keyword search volume over time with date ranges
Get detailed statistics and historical trends
REAL DATA ONLY - NO MOCK DATA
"""

import os
import requests
from typing import Dict, List
from datetime import datetime, timedelta

SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def get_keyword_volume_history(keyword: str, location: str = "US", date_ranges: List[str] = None) -> Dict:
    """
    Get keyword search volume over multiple time periods
    
    Args:
        keyword: The keyword to track
        location: Location code (e.g., "US", "US-FL")
        date_ranges: List of date ranges (e.g., ["today 1-m", "today 3-m", "today 12-m"])
        
    Returns:
        Dict with historical volume data, trends, and statistics
    """
    if date_ranges is None:
        date_ranges = ["today 1-m", "today 3-m", "today 12-m"]
    
    all_data = []
    
    try:
        for date_range in date_ranges:
            url = "https://serpapi.com/search"
            
            params = {
                "engine": "google_trends",
                "q": keyword,
                "api_key": SERPAPI_API_KEY,
                "data_type": "TIMESERIES",
                "geo": location,
                "date": date_range
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            # Extract timeline data
            interest_over_time = data.get("interest_over_time", {})
            timeline_data = interest_over_time.get("timeline_data", [])
            
            # Calculate statistics
            values = [point.get("values", [{}])[0].get("extracted_value", 0) for point in timeline_data]
            
            stats = {}
            if values:
                stats = {
                    "avg_interest": sum(values) / len(values),
                    "max_interest": max(values),
                    "min_interest": min(values),
                    "current_interest": values[-1] if values else 0,
                    "trend": "rising" if len(values) > 1 and values[-1] > values[0] else "falling",
                    "volatility": max(values) - min(values) if values else 0
                }
            
            all_data.append({
                "date_range": date_range,
                "timeline": timeline_data,
                "data_points": len(timeline_data),
                "statistics": stats
            })
        
        # Compare periods
        comparison = {}
        if len(all_data) >= 2:
            recent = all_data[0]["statistics"].get("avg_interest", 0)
            older = all_data[1]["statistics"].get("avg_interest", 0)
            
            if older > 0:
                change_pct = ((recent - older) / older) * 100
                comparison = {
                    "recent_vs_older": {
                        "change_percent": round(change_pct, 2),
                        "direction": "up" if change_pct > 0 else "down",
                        "recent_avg": round(recent, 2),
                        "older_avg": round(older, 2)
                    }
                }
        
        result = {
            "keyword": keyword,
            "location": location,
            "periods_analyzed": len(all_data),
            "historical_data": all_data,
            "comparison": comparison,
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

def get_multi_keyword_comparison(keywords: List[str], location: str = "US", date_range: str = "today 3-m") -> Dict:
    """
    Compare search volume for multiple keywords
    
    Args:
        keywords: List of keywords to compare (max 5)
        location: Location code
        date_range: Date range to analyze
        
    Returns:
        Dict with comparison data and rankings
    """
    try:
        # Combine keywords for comparison
        query = ",".join(keywords[:5])  # Google Trends max 5 keywords
        
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "google_trends",
            "q": query,
            "api_key": SERPAPI_API_KEY,
            "data_type": "TIMESERIES",
            "geo": location,
            "date": date_range
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract timeline for each keyword
        interest_over_time = data.get("interest_over_time", {})
        timeline_data = interest_over_time.get("timeline_data", [])
        
        # Calculate average interest for each keyword
        keyword_stats = {}
        for i, kw in enumerate(keywords[:5]):
            values = []
            for point in timeline_data:
                keyword_values = point.get("values", [])
                if i < len(keyword_values):
                    values.append(keyword_values[i].get("extracted_value", 0))
            
            if values:
                keyword_stats[kw] = {
                    "avg_interest": round(sum(values) / len(values), 2),
                    "max_interest": max(values),
                    "min_interest": min(values),
                    "current_interest": values[-1] if values else 0,
                    "data_points": len(values)
                }
        
        # Rank keywords by average interest
        ranked = sorted(keyword_stats.items(), key=lambda x: x[1]["avg_interest"], reverse=True)
        
        result = {
            "keywords": keywords,
            "location": location,
            "date_range": date_range,
            "timeline": timeline_data,
            "keyword_statistics": keyword_stats,
            "ranking": [{"keyword": k, "avg_interest": v["avg_interest"]} for k, v in ranked],
            "status": "success"
        }
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            "keywords": keywords,
            "location": location,
            "status": "error",
            "error": str(e)
        }
    except Exception as e:
        return {
            "keywords": keywords,
            "location": location,
            "status": "error",
            "error": f"Unexpected error: {str(e)}"
        }

def get_regional_interest(keyword: str, country: str = "US") -> Dict:
    """
    Get regional/geographic interest breakdown for a keyword
    
    Args:
        keyword: The keyword to analyze
        country: Country code (default: "US")
        
    Returns:
        Dict with interest by state/region
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "google_trends",
            "q": keyword,
            "api_key": SERPAPI_API_KEY,
            "data_type": "GEO_MAP_0",  # Changed from GEO_MAP
            "geo": country,
            "date": "today 12-m"
        }
        
        response = requests.get(url, params=params, timeout=30)
        response.raise_for_status()
        
        data = response.json()
        
        # Extract regional data
        interest_by_region = data.get("interest_by_region", [])
        
        # Sort by interest level
        regions_sorted = sorted(interest_by_region, key=lambda x: x.get("extracted_value", 0), reverse=True)
        
        result = {
            "keyword": keyword,
            "country": country,
            "total_regions": len(regions_sorted),
            "top_regions": regions_sorted[:10],  # Top 10 regions
            "all_regions": regions_sorted,
            "status": "success"
        }
        
        return result
        
    except requests.exceptions.RequestException as e:
        return {
            "keyword": keyword,
            "country": country,
            "status": "error",
            "error": str(e)
        }
    except Exception as e:
        return {
            "keyword": keyword,
            "country": country,
            "status": "error",
            "error": f"Unexpected error: {str(e)}"
        }

