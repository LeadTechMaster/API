#!/usr/bin/env python3
"""Quick test of Miami Map integration"""

import sys
import os

# Add paths
sys.path.insert(0, os.path.dirname(__file__))
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../../SerpApi'))

try:
    from miami_data_visualization import get_miami_map_data
    
    print("=" * 80)
    print("Testing Miami Map Data Visualization")
    print("=" * 80)
    
    data = get_miami_map_data()
    
    print(f"\nStatus: {data.get('status')}")
    print(f"Keys: {list(data.keys())}")
    
    if data['status'] == 'success':
        print("\n✅ SUCCESS!")
        print(f"Miami Center: {data.get('miami_center')}")
        
        if 'data' in data:
            print(f"\nData sections: {list(data['data'].keys())}")
            
            # Business locations
            if 'business_locations' in data['data']:
                bl = data['data']['business_locations']
                print(f"  - Business Locations: {bl.get('total_businesses', 0)} businesses")
            
            # Rating heatmap
            if 'rating_heatmap' in data['data']:
                rh = data['data']['rating_heatmap']
                print(f"  - Rating Heatmap: {rh.get('total_points', 0)} points")
            
            # Market density
            if 'market_density' in data['data']:
                md = data['data']['market_density']
                print(f"  - Market Density: {md.get('total_areas', 0)} areas")
            
            # Competitor clusters
            if 'competitor_clusters' in data['data']:
                cc = data['data']['competitor_clusters']
                print(f"  - Competitor Clusters: {cc.get('total_clusters', 0)} clusters")
            
            # Regional interest
            if 'regional_interest' in data['data']:
                ri = data['data']['regional_interest']
                print(f"  - Regional Interest: {ri.get('total_regions', 0)} regions")
    else:
        print("\n❌ ERROR!")
        print(f"Error: {data.get('error', 'Unknown error')}")
    
except Exception as e:
    print(f"\n❌ EXCEPTION: {e}")
    import traceback
    traceback.print_exc()


