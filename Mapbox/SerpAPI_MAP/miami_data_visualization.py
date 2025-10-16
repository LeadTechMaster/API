#!/usr/bin/env python3
"""
Miami Data Visualization with Mapbox
Integrates SerpApi data with Mapbox for geographic visualization
"""

import os
import sys
import sqlite3
import json
from typing import Dict, List, Optional, Tuple
from datetime import datetime

# Add SerpApi path for database access
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../SerpApi'))

# Mapbox API key (you'll need to set this)
MAPBOX_ACCESS_TOKEN = os.getenv('MAPBOX_ACCESS_TOKEN', 'pk.eyJ1IjoiZGVmYXVsdCIsImEiOiJjbGV4YW1wbGUifQ.example')

# Miami coordinates
MIAMI_CENTER = {
    "lat": 25.7617,
    "lng": -80.1918,
    "zoom": 11
}

class MiamiDataVisualization:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(__file__), '../../SerpApi/DB/serpapi_data.db')
        self.miami_center = MIAMI_CENTER
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def get_business_locations(self) -> Dict:
        """
        Get all business locations from Google Maps data
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT business_name, rating, reviews_count, phone, address, 
                       latitude, longitude, hours, website
                FROM local_businesses 
                WHERE latitude IS NOT NULL AND longitude IS NOT NULL
                ORDER BY reviews_count DESC
            """)
            
            businesses = cursor.fetchall()
            conn.close()
            
            # Convert to GeoJSON format
            features = []
            for business in businesses:
                if business[5] and business[6]:  # lat and lng exist
                    features.append({
                        "type": "Feature",
                        "properties": {
                            "name": business[0],
                            "rating": business[1],
                            "reviews": business[2],
                            "phone": business[3],
                            "address": business[4],
                            "hours": business[7],
                            "website": business[8],
                            "marker-color": self._get_marker_color(business[1]),  # Color by rating
                            "marker-size": self._get_marker_size(business[2])     # Size by reviews
                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": [float(business[6]), float(business[5])]  # [lng, lat]
                        }
                    })
            
            return {
                "status": "success",
                "type": "FeatureCollection",
                "features": features,
                "total_businesses": len(features),
                "center": self.miami_center
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error getting business locations: {str(e)}"
            }
    
    def get_rating_heatmap_data(self) -> Dict:
        """
        Create comprehensive heatmap data with multiple data sources
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get business data with ratings and reviews
            cursor.execute("""
                SELECT latitude, longitude, rating, reviews_count, business_name
                FROM local_businesses 
                WHERE latitude IS NOT NULL AND longitude IS NOT NULL 
                AND rating IS NOT NULL
            """)
            
            businesses = cursor.fetchall()
            
            # Get keyword search volume data by location
            cursor.execute("""
                SELECT keyword, search_volume, difficulty_score
                FROM keywords 
                WHERE location LIKE '%Miami%' OR location LIKE '%FL%'
                ORDER BY search_volume DESC
                LIMIT 50
            """)
            
            keywords = cursor.fetchall()
            
            # Get regional interest data
            cursor.execute("""
                SELECT region, interest_value, rank
                FROM regional_interest 
                WHERE region = 'Florida'
                ORDER BY rank ASC
            """)
            
            regional_data = cursor.fetchall()
            
            # Get Yelp review data
            cursor.execute("""
                SELECT latitude, longitude, rating, review_count, business_name
                FROM yelp_businesses 
                WHERE latitude IS NOT NULL AND longitude IS NOT NULL
                LIMIT 100
            """)
            
            yelp_businesses = cursor.fetchall()
            
            conn.close()
            
            # Create comprehensive heatmap points
            heatmap_points = []
            
            # Business rating heatmap (weight: 40%)
            for business in businesses:
                if business[0] and business[1] and business[2]:
                    # Enhanced intensity calculation
                    rating_score = business[2] / 5.0  # Normalize to 0-1
                    review_score = min((business[3] or 0) / 1000.0, 1.0)  # Cap at 1000 reviews
                    popularity_score = (rating_score * 0.6) + (review_score * 0.4)
                    
                    heatmap_points.append({
                        "coordinates": [float(business[1]), float(business[0])],
                        "intensity": popularity_score,
                        "type": "business_rating",
                        "rating": business[2],
                        "reviews": business[3] or 0,
                        "name": business[4],
                        "weight": 0.4
                    })
            
            # Yelp review heatmap (weight: 30%)
            for yelp in yelp_businesses:
                if yelp[0] and yelp[1] and yelp[2]:
                    rating_score = yelp[2] / 5.0
                    review_score = min((yelp[3] or 0) / 500.0, 1.0)  # Cap at 500 reviews
                    yelp_score = (rating_score * 0.7) + (review_score * 0.3)
                    
                    heatmap_points.append({
                        "coordinates": [float(yelp[1]), float(yelp[0])],
                        "intensity": yelp_score,
                        "type": "yelp_reviews",
                        "rating": yelp[2],
                        "reviews": yelp[3] or 0,
                        "name": yelp[4],
                        "weight": 0.3
                    })
            
            # Keyword search volume heatmap (weight: 20%)
            # Distribute keyword intensity across Miami based on search volume
            miami_areas = [
                {"lat": 25.7743, "lng": -80.1937, "name": "Downtown"},
                {"lat": 25.7663, "lng": -80.1918, "name": "Brickell"},
                {"lat": 25.8011, "lng": -80.1994, "name": "Wynwood"},
                {"lat": 25.8054, "lng": -80.1918, "name": "Design District"},
                {"lat": 25.7286, "lng": -80.2374, "name": "Coconut Grove"},
                {"lat": 25.7907, "lng": -80.1300, "name": "South Beach"},
                {"lat": 25.9565, "lng": -80.1390, "name": "Aventura"},
                {"lat": 25.8195, "lng": -80.3553, "name": "Doral"}
            ]
            
            for i, keyword in enumerate(keywords[:20]):  # Top 20 keywords
                area = miami_areas[i % len(miami_areas)]
                search_intensity = min((keyword[1] or 0) / 10000.0, 1.0)  # Normalize search volume
                difficulty_factor = 1.0 - ((keyword[2] or 50) / 100.0)  # Lower difficulty = higher intensity
                
                heatmap_points.append({
                    "coordinates": [area["lng"], area["lat"]],
                    "intensity": search_intensity * difficulty_factor,
                    "type": "search_volume",
                    "keyword": keyword[0],
                    "search_volume": keyword[1] or 0,
                    "difficulty": keyword[2] or 0,
                    "area": area["name"],
                    "weight": 0.2
                })
            
            # Regional interest overlay (weight: 10%)
            if regional_data:
                florida_interest = regional_data[0][1] if regional_data else 50
                interest_intensity = florida_interest / 100.0
                
                # Add interest points across Miami
                for area in miami_areas:
                    heatmap_points.append({
                        "coordinates": [area["lng"], area["lat"]],
                        "intensity": interest_intensity * 0.5,  # Lower weight for regional data
                        "type": "regional_interest",
                        "interest_value": florida_interest,
                        "area": area["name"],
                        "weight": 0.1
                    })
            
            # Calculate statistics
            total_intensity = sum(point["intensity"] for point in heatmap_points)
            avg_intensity = total_intensity / len(heatmap_points) if heatmap_points else 0
            max_intensity = max(point["intensity"] for point in heatmap_points) if heatmap_points else 0
            
            return {
                "status": "success",
                "heatmap_data": heatmap_points,
                "total_points": len(heatmap_points),
                "statistics": {
                    "total_intensity": total_intensity,
                    "average_intensity": avg_intensity,
                    "max_intensity": max_intensity,
                    "business_points": len([p for p in heatmap_points if p["type"] == "business_rating"]),
                    "yelp_points": len([p for p in heatmap_points if p["type"] == "yelp_reviews"]),
                    "search_points": len([p for p in heatmap_points if p["type"] == "search_volume"]),
                    "regional_points": len([p for p in heatmap_points if p["type"] == "regional_interest"])
                },
                "center": self.miami_center
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error creating comprehensive heatmap: {str(e)}"
            }
    
    def get_regional_interest_map(self) -> Dict:
        """
        Create map showing regional interest data
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT region, interest_value, rank
                FROM regional_interest 
                ORDER BY rank ASC
                LIMIT 20
            """)
            
            regions = cursor.fetchall()
            conn.close()
            
            # Map state names to approximate coordinates for visualization
            state_coords = {
                "Florida": [25.7617, -80.1918],  # Miami
                "California": [34.0522, -118.2437],  # LA
                "New York": [40.7128, -74.0060],  # NYC
                "Texas": [29.7604, -95.3698],  # Houston
                "Illinois": [41.8781, -87.6298],  # Chicago
                "Pennsylvania": [39.9526, -75.1652],  # Philadelphia
                "Ohio": [39.9612, -82.9988],  # Columbus
                "Georgia": [33.7490, -84.3880],  # Atlanta
                "North Carolina": [35.2271, -80.8431],  # Charlotte
                "Michigan": [42.3314, -83.0458],  # Detroit
                "Virginia": [37.5407, -77.4360],  # Richmond
                "Washington": [47.6062, -122.3321],  # Seattle
                "Arizona": [33.4484, -112.0740],  # Phoenix
                "Massachusetts": [42.3601, -71.0589],  # Boston
                "Tennessee": [36.1627, -86.7816],  # Nashville
                "Indiana": [39.7684, -86.1581],  # Indianapolis
                "Missouri": [38.6270, -90.1994],  # St. Louis
                "Maryland": [39.2904, -76.6122],  # Baltimore
                "Wisconsin": [43.0731, -89.4012],  # Madison
                "Colorado": [39.7392, -104.9903]  # Denver
            }
            
            features = []
            for region in regions:
                region_name = region[0]
                if region_name in state_coords:
                    features.append({
                        "type": "Feature",
                        "properties": {
                            "region": region_name,
                            "interest": region[1],
                            "rank": region[2],
                            "marker-color": self._get_interest_color(region[1]),
                            "marker-size": self._get_interest_size(region[1])
                        },
                        "geometry": {
                            "type": "Point",
                            "coordinates": state_coords[region_name]
                        }
                    })
            
            return {
                "status": "success",
                "type": "FeatureCollection",
                "features": features,
                "total_regions": len(features),
                "center": self.miami_center
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error getting regional data: {str(e)}"
            }
    
    def get_market_density_analysis(self) -> Dict:
        """
        Analyze market density in different Miami areas
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT latitude, longitude, business_name, rating, reviews_count
                FROM local_businesses 
                WHERE latitude IS NOT NULL AND longitude IS NOT NULL
            """)
            
            businesses = cursor.fetchall()
            conn.close()
            
            # Define Miami neighborhoods/areas
            miami_areas = {
                "Downtown Miami": {"lat": 25.7743, "lng": -80.1937, "radius": 0.05},
                "Brickell": {"lat": 25.7663, "lng": -80.1918, "radius": 0.03},
                "Wynwood": {"lat": 25.8011, "lng": -80.1994, "radius": 0.04},
                "Design District": {"lat": 25.8054, "lng": -80.1918, "radius": 0.03},
                "Coconut Grove": {"lat": 25.7286, "lng": -80.2374, "radius": 0.04},
                "South Beach": {"lat": 25.7907, "lng": -80.1300, "radius": 0.05},
                "Aventura": {"lat": 25.9565, "lng": -80.1390, "radius": 0.04},
                "Doral": {"lat": 25.8195, "lng": -80.3553, "radius": 0.05}
            }
            
            area_stats = {}
            for area_name, area_data in miami_areas.items():
                businesses_in_area = []
                for business in businesses:
                    if business[0] and business[1]:  # lat and lng exist
                        distance = self._calculate_distance(
                            area_data["lat"], area_data["lng"],
                            float(business[0]), float(business[1])
                        )
                        if distance <= area_data["radius"]:
                            businesses_in_area.append(business)
                
                if businesses_in_area:
                    avg_rating = sum(b[3] for b in businesses_in_area if b[3]) / len([b for b in businesses_in_area if b[3]])
                    total_reviews = sum(b[4] or 0 for b in businesses_in_area)
                    area_stats[area_name] = {
                        "count": len(businesses_in_area),
                        "avg_rating": round(avg_rating, 2),
                        "total_reviews": total_reviews,
                        "coordinates": [area_data["lng"], area_data["lat"]],
                        "density_score": len(businesses_in_area) * avg_rating
                    }
            
            return {
                "status": "success",
                "area_analysis": area_stats,
                "total_areas": len(area_stats),
                "center": self.miami_center
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error analyzing market density: {str(e)}"
            }
    
    def get_competitor_clusters(self) -> Dict:
        """
        Identify competitor clusters in Miami
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("""
                SELECT business_name, latitude, longitude, rating, reviews_count, phone
                FROM local_businesses 
                WHERE latitude IS NOT NULL AND longitude IS NOT NULL
                ORDER BY reviews_count DESC
            """)
            
            businesses = cursor.fetchall()
            conn.close()
            
            # Simple clustering based on proximity
            clusters = []
            used_businesses = set()
            
            for i, business in enumerate(businesses):
                if i in used_businesses:
                    continue
                
                cluster = [business]
                used_businesses.add(i)
                
                # Find nearby businesses
                for j, other_business in enumerate(businesses[i+1:], i+1):
                    if j in used_businesses:
                        continue
                    
                    distance = self._calculate_distance(
                        float(business[1]), float(business[2]),
                        float(other_business[1]), float(other_business[2])
                    )
                    
                    if distance <= 0.02:  # Within ~2km
                        cluster.append(other_business)
                        used_businesses.add(j)
                
                if len(cluster) > 1:  # Only clusters with multiple businesses
                    clusters.append({
                        "center": self._calculate_cluster_center(cluster),
                        "businesses": cluster,
                        "size": len(cluster),
                        "avg_rating": sum(b[3] for b in cluster if b[3]) / len([b for b in cluster if b[3]]),
                        "total_reviews": sum(b[4] or 0 for b in cluster)
                    })
            
            return {
                "status": "success",
                "clusters": clusters,
                "total_clusters": len(clusters),
                "center": self.miami_center
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error finding clusters: {str(e)}"
            }
    
    def _get_marker_color(self, rating: float) -> str:
        """Get marker color based on rating"""
        if rating >= 4.5:
            return "#10b981"  # Green
        elif rating >= 4.0:
            return "#f59e0b"  # Yellow
        elif rating >= 3.5:
            return "#f97316"  # Orange
        else:
            return "#ef4444"  # Red
    
    def _get_marker_size(self, reviews: int) -> str:
        """Get marker size based on review count"""
        if reviews >= 1000:
            return "large"
        elif reviews >= 500:
            return "medium"
        else:
            return "small"
    
    def _get_interest_color(self, interest: int) -> str:
        """Get color based on interest level"""
        if interest >= 80:
            return "#10b981"  # Green
        elif interest >= 60:
            return "#f59e0b"  # Yellow
        elif interest >= 40:
            return "#f97316"  # Orange
        else:
            return "#ef4444"  # Red
    
    def _get_interest_size(self, interest: int) -> str:
        """Get size based on interest level"""
        if interest >= 80:
            return "large"
        elif interest >= 60:
            return "medium"
        else:
            return "small"
    
    def _calculate_distance(self, lat1: float, lng1: float, lat2: float, lng2: float) -> float:
        """Calculate distance between two points in degrees"""
        return ((lat1 - lat2) ** 2 + (lng1 - lng2) ** 2) ** 0.5
    
    def _calculate_cluster_center(self, businesses: List) -> List[float]:
        """Calculate center point of a cluster"""
        total_lat = sum(float(b[1]) for b in businesses if b[1])
        total_lng = sum(float(b[2]) for b in businesses if b[2])
        count = len(businesses)
        return [total_lng / count, total_lat / count]

def get_miami_map_data() -> Dict:
    """
    Get comprehensive Miami map data for visualization
    """
    viz = MiamiDataVisualization()
    
    return {
        "status": "success",
        "timestamp": datetime.now().isoformat(),
        "miami_center": MIAMI_CENTER,
        "mapbox_token": MAPBOX_ACCESS_TOKEN,
        "data": {
            "business_locations": viz.get_business_locations(),
            "rating_heatmap": viz.get_rating_heatmap_data(),
            "regional_interest": viz.get_regional_interest_map(),
            "market_density": viz.get_market_density_analysis(),
            "competitor_clusters": viz.get_competitor_clusters()
        }
    }

if __name__ == "__main__":
    # Test the visualization
    print("=== Miami Data Visualization Test ===")
    
    data = get_miami_map_data()
    print(f"Status: {data['status']}")
    
    if data['status'] == 'success':
        business_data = data['data']['business_locations']
        print(f"Business locations: {business_data.get('total_businesses', 0)}")
        
        heatmap_data = data['data']['rating_heatmap']
        print(f"Heatmap points: {heatmap_data.get('total_points', 0)}")
        
        regional_data = data['data']['regional_interest']
        print(f"Regional points: {regional_data.get('total_regions', 0)}")
        
        density_data = data['data']['market_density']
        print(f"Market areas: {density_data.get('total_areas', 0)}")
        
        cluster_data = data['data']['competitor_clusters']
        print(f"Competitor clusters: {cluster_data.get('total_clusters', 0)}")
