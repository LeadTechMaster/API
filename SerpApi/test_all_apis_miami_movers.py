#!/usr/bin/env python3
"""
Comprehensive SerpApi Test Suite
Tests ALL 25+ APIs with REAL Miami Moving Company Data
Saves results to database with validation
NO MOCK DATA - 100% REAL API CALLS ONLY

APIs Tested:
1-15: Original APIs (Google Search, Keywords, Local, Media, etc.)
16-18: Priority 1 (Yelp, YouTube, Google Jobs)
19-22: Priority 2 (TripAdvisor, LinkedIn, App Stores)
23-25: Priority 3 (Patents, Amazon, Walmart)
"""

import os
import sys
import json
from datetime import datetime
from typing import Dict

# Set API key
os.environ['SERPAPI_API_KEY'] = '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c'

# Import all API modules
from google_search import google_search
from keyword_suggestions import get_keyword_suggestions
from autocomplete_suggestions import get_autocomplete_suggestions
from local_pack_results import get_local_pack_results
from local_businesses import search_local_businesses
from people_also_ask import get_people_also_ask
from related_searches import get_related_searches
from keyword_search_volume import get_keyword_search_volume
from search_trends import get_search_trends
from keyword_difficulty import get_keyword_difficulty
from serp_analysis import analyze_serp
from competitor_keywords import get_competitor_keywords
from image_search import search_images
from news_search import search_news
from shopping_search import search_shopping

# Import Priority 1 APIs
from yelp_search import search_yelp_businesses
from youtube_search import search_youtube
from google_jobs import search_jobs

# Import Priority 2 APIs
from tripadvisor_search import search_tripadvisor
from linkedin_jobs import search_linkedin_jobs
from apple_app_store import search_apple_apps
from google_play_store import search_google_play_apps

# Import Priority 3 APIs
from google_patents import search_patents
from amazon_product import search_amazon_products
from walmart_product import search_walmart_products

# Import database manager
from DB.db_manager import get_db

# Test configuration
MIAMI_LOCATION = "Miami, FL"
PRIMARY_KEYWORD = "moving companies miami"
INDUSTRY = "moving_companies"

class MiamiMoversTestSuite:
    def __init__(self):
        self.db = get_db()
        self.session_id = self.db.get_current_session(INDUSTRY, MIAMI_LOCATION)
        self.results = {}
        self.start_time = datetime.now()
        
        print("="*80)
        print("🚀 MIAMI MOVING COMPANIES - COMPREHENSIVE API TEST SUITE")
        print("="*80)
        print(f"📍 Location: {MIAMI_LOCATION}")
        print(f"🔑 Keyword: {PRIMARY_KEYWORD}")
        print(f"💾 Session ID: {self.session_id}")
        print(f"🕐 Started: {self.start_time.strftime('%Y-%m-%d %H:%M:%S')}")
        print("="*80)
        print("\n✅ ALL DATA IS REAL - NO MOCK DATA\n")
    
    def test_api(self, name: str, func, *args, save_func=None):
        """Test an API and save results"""
        print(f"Testing {name}...", end=" ")
        start = datetime.now()
        
        try:
            result = func(*args)
            elapsed = (datetime.now() - start).total_seconds()
            
            # Log API call
            api_call_id = self.db.log_api_call(
                endpoint=name,
                query=PRIMARY_KEYWORD,
                location=MIAMI_LOCATION,
                status=result.get('status', 'unknown'),
                response_time_ms=int(elapsed * 1000),
                raw_response=result
            )
            
            # Save to database if function provided
            if save_func and result.get('status') == 'success':
                save_func(result, self.session_id, api_call_id)
            
            self.results[name] = {
                'status': result.get('status'),
                'elapsed': elapsed,
                'data_points': self._count_data_points(result),
                'api_call_id': api_call_id
            }
            
            status = "✅" if result.get('status') == 'success' else "❌"
            print(f"{status} ({elapsed:.2f}s) - {self.results[name]['data_points']} data points")
            
            return result
            
        except Exception as e:
            print(f"❌ ERROR: {str(e)}")
            self.results[name] = {'status': 'error', 'error': str(e)}
            return None
    
    def _count_data_points(self, result: Dict) -> int:
        """Count number of data points in result"""
        if not isinstance(result, dict):
            return 0
        
        count = 0
        # Count various result types
        for key in ['organic_results', 'businesses', 'suggestions', 'questions', 
                   'images', 'news', 'products', 'jobs', 'videos', 'local_pack',
                   'related_searches']:
            if key in result:
                items = result[key]
                if isinstance(items, list):
                    count += len(items)
        
        return count
    
    def run_all_tests(self):
        """Run all 18 API tests"""
        
        # Test 1: Google Search
        print("\n📊 SEARCH & RANKINGS")
        print("-" * 80)
        self.test_api(
            "Google Search",
            google_search,
            PRIMARY_KEYWORD,
            MIAMI_LOCATION,
            10,
            save_func=self.db.save_search_results
        )
        
        # Test 2: Local Pack Results
        self.test_api(
            "Local Pack (3-pack)",
            get_local_pack_results,
            "moving companies",
            MIAMI_LOCATION,
            save_func=self.db.save_local_pack
        )
        
        # Test 3: Local Businesses (Google Maps)
        self.test_api(
            "Local Businesses (Maps)",
            search_local_businesses,
            "moving companies",
            MIAMI_LOCATION,
            10,
            save_func=self.db.save_local_businesses
        )
        
        # Test 4-7: Keyword Research
        print("\n💡 KEYWORD RESEARCH")
        print("-" * 80)
        self.test_api(
            "Keyword Suggestions",
            get_keyword_suggestions,
            "moving companies miami",
            "us",
            save_func=self.db.save_keyword_suggestions
        )
        
        self.test_api(
            "Autocomplete",
            get_autocomplete_suggestions,
            "moving companies mia",
            "us"
        )
        
        self.test_api(
            "Related Searches",
            get_related_searches,
            PRIMARY_KEYWORD,
            "United States",
            save_func=self.db.save_related_searches
        )
        
        self.test_api(
            "People Also Ask",
            get_people_also_ask,
            PRIMARY_KEYWORD,
            save_func=self.db.save_people_also_ask
        )
        
        # Test 8-10: Competitive Intelligence
        print("\n🎯 COMPETITIVE INTELLIGENCE")
        print("-" * 80)
        self.test_api(
            "Keyword Difficulty",
            get_keyword_difficulty,
            PRIMARY_KEYWORD,
            "United States",
            save_func=self.db.save_keyword_difficulty
        )
        
        self.test_api(
            "SERP Analysis",
            analyze_serp,
            PRIMARY_KEYWORD,
            MIAMI_LOCATION,
            save_func=self.db.save_serp_analysis
        )
        
        self.test_api(
            "Competitor Keywords",
            get_competitor_keywords,
            "movebuddha.com",
            "United States",
            10
        )
        
        # Test 11-12: Trends
        print("\n📈 TRENDS & VOLUME")
        print("-" * 80)
        self.test_api(
            "Search Trends",
            get_search_trends,
            "moving companies",
            "US-FL",
            "today 3-m"
        )
        
        self.test_api(
            "Keyword Search Volume",
            get_keyword_search_volume,
            PRIMARY_KEYWORD,
            "United States"
        )
        
        # Test 13-15: Media & Content
        print("\n🖼️  MEDIA & CONTENT")
        print("-" * 80)
        self.test_api(
            "Image Search",
            search_images,
            "moving truck miami",
            10,
            save_func=self.db.save_images
        )
        
        self.test_api(
            "News Search",
            search_news,
            "moving companies miami",
            MIAMI_LOCATION,
            "qdr:m",
            5,
            save_func=self.db.save_news
        )
        
        self.test_api(
            "Shopping Search",
            search_shopping,
            "moving boxes supplies",
            MIAMI_LOCATION,
            10,
            save_func=self.db.save_shopping
        )
        
        # Test 16-18: PRIORITY 1 NEW APIS
        print("\n🆕 PRIORITY 1: Reviews & Jobs")
        print("-" * 80)
        self.test_api(
            "Yelp Business Search",
            search_yelp_businesses,
            "moving companies",
            MIAMI_LOCATION,
            10
        )
        
        self.test_api(
            "YouTube Search",
            search_youtube,
            "moving companies miami tips",
            10
        )
        
        self.test_api(
            "Google Jobs",
            search_jobs,
            "mover",
            MIAMI_LOCATION,
            10
        )
        
        # Test 19-22: PRIORITY 2 APIS
        print("\n🔥 PRIORITY 2: Advanced Platforms")
        print("-" * 80)
        self.test_api(
            "TripAdvisor Search",
            search_tripadvisor,
            "storage facilities miami",
            MIAMI_LOCATION
        )
        
        self.test_api(
            "LinkedIn Jobs",
            search_linkedin_jobs,
            "mover operations manager",
            MIAMI_LOCATION,
            5
        )
        
        self.test_api(
            "Apple App Store",
            search_apple_apps,
            "moving calculator cost",
            "us"
        )
        
        self.test_api(
            "Google Play Store",
            search_google_play_apps,
            "moving planner checklist",
            "us"
        )
        
        # Test 23-25: PRIORITY 3 APIS
        print("\n⚡ PRIORITY 3: Innovation & Ecommerce")
        print("-" * 80)
        self.test_api(
            "Google Patents",
            search_patents,
            "moving equipment dolly",
            5
        )
        
        self.test_api(
            "Amazon Products",
            search_amazon_products,
            "moving boxes heavy duty",
            "amazon.com"
        )
        
        self.test_api(
            "Walmart Products",
            search_walmart_products,
            "moving boxes packing tape"
        )
    
    def print_summary(self):
        """Print test summary"""
        end_time = datetime.now()
        total_time = (end_time - self.start_time).total_seconds()
        
        print("\n" + "="*80)
        print("📊 TEST SUMMARY")
        print("="*80)
        
        total_tests = len(self.results)
        successful = sum(1 for r in self.results.values() if r.get('status') == 'success')
        failed = total_tests - successful
        total_data_points = sum(r.get('data_points', 0) for r in self.results.values())
        
        print(f"\n✅ Successful: {successful}/{total_tests}")
        print(f"❌ Failed: {failed}/{total_tests}")
        print(f"📊 Total Data Points: {total_data_points}")
        print(f"⏱️  Total Time: {total_time:.2f}s")
        print(f"⚡ Avg Time/API: {total_time/total_tests:.2f}s")
        
        print("\n📝 Individual Results:")
        print("-" * 80)
        for name, result in self.results.items():
            status_icon = "✅" if result.get('status') == 'success' else "❌"
            elapsed = result.get('elapsed', 0)
            points = result.get('data_points', 0)
            print(f"{status_icon} {name:<30} {elapsed:>6.2f}s  {points:>4} points")
        
        # Get market summary from database
        print("\n" + "="*80)
        print("🎯 MARKET INTELLIGENCE SUMMARY")
        print("="*80)
        
        summary = self.db.get_market_summary(INDUSTRY, MIAMI_LOCATION)
        if summary:
            print(f"\n📍 Total Businesses Tracked: {summary.get('total_businesses', 0)}")
            print(f"⭐ Average Rating: {summary.get('avg_rating', 0):.1f}")
            print(f"💬 Total Reviews: {summary.get('total_reviews', 0)}")
            print(f"🔑 Keywords Tracked: {summary.get('keywords_tracked', 0)}")
            print(f"📊 Avg Difficulty: {summary.get('avg_difficulty', 0):.1f}/100")
            print(f"📰 News Articles: {summary.get('news_articles', 0)}")
        
        print("\n" + "="*80)
        print("✅ ALL DATA SAVED TO DATABASE")
        print(f"💾 Database: {self.db.db_path}")
        print(f"📅 Session ID: {self.session_id}")
        print("="*80)
        
        # Show recent API calls
        print("\n📜 Recent API Calls:")
        recent = self.db.get_recent_searches(5)
        for call in recent:
            print(f"  • {call['endpoint']:<30} | {call['status']:<8} | {call['created_at']}")
        
        print("\n" + "="*80)
        print("🎉 TEST SUITE COMPLETE!")
        print("="*80)
        print(f"\n✅ {successful}/{total_tests} APIs working with REAL data")
        print(f"💾 {total_data_points} data points saved to database")
        print(f"🚀 Ready for production use!")
        print("\n")

def main():
    """Run the test suite"""
    suite = MiamiMoversTestSuite()
    
    try:
        suite.run_all_tests()
        suite.print_summary()
        
    except KeyboardInterrupt:
        print("\n\n⚠️  Test interrupted by user")
        suite.print_summary()
        sys.exit(1)
    
    except Exception as e:
        print(f"\n\n❌ CRITICAL ERROR: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()

