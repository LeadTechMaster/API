#!/usr/bin/env python3
"""
SerpApi Live Data Server
Flask backend that serves REAL API data to the HTML frontend
NO MOCK DATA - ALL REAL API CALLS
"""

import os
import sys
from flask import Flask, jsonify, send_from_directory
from flask_cors import CORS

# Add parent directory to path to import SerpApi modules
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Set API key
os.environ['SERPAPI_API_KEY'] = '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c'

# Import SerpApi modules
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

# Import NEW APIs (Priority 1)
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

# Import Enhanced Tracking
from keyword_volume_tracker import get_keyword_volume_history, get_multi_keyword_comparison, get_regional_interest

# Import NEW Search Engines & Analytics
from bing_search import search_bing, get_bing_autocomplete
from duckduckgo_search import search_duckduckgo, get_duckduckgo_instant_answers
from google_scholar import search_scholar, get_scholar_author
from google_finance import search_finance, get_market_trends
from marketing_analytics import get_marketing_analytics_summary

# Import Mapbox Miami Visualization
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '../Mapbox/SerpAPI_MAP'))
from miami_data_visualization import get_miami_map_data

# Import database manager
from DB.db_manager import get_db

app = Flask(__name__)
CORS(app)  # Enable CORS for frontend access

# Initialize database
db = get_db()
session_id = db.get_current_session("moving_companies", "Miami, FL")

# Miami moving companies constants
MIAMI_LOCATION = "Miami, FL"
MIAMI_KEYWORD = "moving companies miami"

# ============================================================================
# SMART CACHING WRAPPER
# ============================================================================

def smart_api_call(endpoint_name, api_function, *args, save_function=None, force_refresh=False, **kwargs):
    """
    Smart wrapper that checks cache first, then calls API if needed
    Automatically saves results to database with timestamps
    
    Args:
        endpoint_name: Name of the endpoint for logging
        api_function: The actual API function to call
        save_function: Optional DB save function
        force_refresh: If True, skip cache and call API
        *args, **kwargs: Arguments for the API function
        
    Returns:
        Dict with result data plus metadata (from_cache, cached_at, etc.)
    """
    from datetime import datetime
    import time
    
    # Extract query and location from args for cache check
    query = kwargs.get('query') or (args[0] if len(args) > 0 else MIAMI_KEYWORD)
    location = kwargs.get('location') or (args[1] if len(args) > 1 else MIAMI_LOCATION)
    
    # Check cache if not forcing refresh
    if not force_refresh:
        freshness = db.get_data_freshness(endpoint_name, query, location)
        if freshness['is_fresh']:
            # Return cached data
            cached = db.get_cached_data('api_calls', query, location, max_age_minutes=15)
            if cached and cached.get('data'):
                result = cached['data']
                result['from_cache'] = True
                result['cached_at'] = cached['cached_at']
                result['age_minutes'] = freshness['age_minutes']
                return result
    
    # Call API
    start_time = time.time()
    result = api_function(*args, **kwargs)
    elapsed_ms = int((time.time() - start_time) * 1000)
    
    # Log API call
    api_call_id = db.log_api_call(
        endpoint=endpoint_name,
        query=query,
        location=location,
        status=result.get('status', 'unknown'),
        response_time_ms=elapsed_ms,
        error_message=result.get('error'),
        raw_response=result
    )
    
    # Save to database if function provided and successful
    if save_function and result.get('status') == 'success':
        try:
            save_function(result, session_id, api_call_id)
        except Exception as e:
            print(f"Warning: Failed to save {endpoint_name} to DB: {e}")
    
    # Add metadata
    result['from_cache'] = False
    result['api_call_id'] = api_call_id
    result['response_time_ms'] = elapsed_ms
    
    return result

@app.route('/')
def index():
    """Serve the main HTML dashboard"""
    return send_from_directory('.', 'dashboard.html')

@app.route('/favicon.ico')
def favicon():
    """Return empty response for favicon to avoid 404 errors"""
    return '', 204

@app.route('/api/status')
def api_status():
    """API health check with database stats"""
    recent_calls = db.get_recent_searches(5)
    
    return jsonify({
        'status': 'online',
        'message': 'SerpApi Complete Market Intelligence Platform - 35+ APIs',
        'api_key_set': bool(os.environ.get('SERPAPI_API_KEY')),
        'total_endpoints': 35,
        'database_connected': True,
        'session_id': session_id,
        'database_path': db.db_path,
        'recent_api_calls': recent_calls,
        'api_categories': {
            'search_rankings': 3,
            'keyword_research': 4,
            'competitive_intelligence': 3,
            'media_content': 3,
            'job_market': 3,
            'app_stores': 2,
            'ecommerce': 3,
            'innovation': 1,
            'reviews': 3
        },
        'features': {
            'smart_caching': True,
            'auto_db_save': True,
            'data_validation': True,
            'freshness_tracking': True
        }
    })

@app.route('/api/data-freshness')
def api_data_freshness():
    """Check freshness of all cached data"""
    endpoints = [
        'Google Search', 'Local Businesses (Maps)', 'Keyword Suggestions',
        'People Also Ask', 'Related Searches', 'Keyword Difficulty',
        'SERP Analysis', 'Image Search', 'News Search', 'Shopping Search',
        'Yelp Business Search', 'YouTube Search', 'Google Jobs',
        'Walmart Products'
    ]
    
    freshness_data = {}
    for endpoint in endpoints:
        freshness_data[endpoint] = db.get_data_freshness(
            endpoint, MIAMI_KEYWORD, MIAMI_LOCATION
        )
    
    return jsonify({
        'location': MIAMI_LOCATION,
        'keyword': MIAMI_KEYWORD,
        'session_id': session_id,
        'freshness': freshness_data,
        'cache_duration_minutes': 15
    })

@app.route('/api/google-search')
def api_google_search():
    """Get Google search results for Miami moving companies (with smart caching)"""
    from flask import request
    force_refresh = request.args.get('refresh', 'false').lower() == 'true'
    
    result = smart_api_call(
        "Google Search",
        google_search,
        MIAMI_KEYWORD,
        MIAMI_LOCATION,
        10,
        save_function=db.save_search_results,
        force_refresh=force_refresh
    )
    return jsonify(result)

@app.route('/api/keyword-suggestions')
def api_keyword_suggestions():
    """Get keyword suggestions"""
    result = get_keyword_suggestions(
        seed_keyword="moving companies miami",
        location="us"
    )
    return jsonify(result)

@app.route('/api/autocomplete')
def api_autocomplete():
    """Get autocomplete suggestions"""
    result = get_autocomplete_suggestions(
        partial_keyword="moving companies mia",
        location="us"
    )
    return jsonify(result)

@app.route('/api/local-pack')
def api_local_pack():
    """Get local 3-pack results"""
    result = get_local_pack_results(
        keyword="moving companies",
        location=MIAMI_LOCATION
    )
    return jsonify(result)

@app.route('/api/local-businesses')
def api_local_businesses():
    """Get local businesses from Google Maps (with smart caching)"""
    from flask import request
    force_refresh = request.args.get('refresh', 'false').lower() == 'true'
    
    result = smart_api_call(
        "Local Businesses (Maps)",
        search_local_businesses,
        "moving companies",
        MIAMI_LOCATION,
        10,
        save_function=db.save_local_businesses,
        force_refresh=force_refresh
    )
    return jsonify(result)

@app.route('/api/people-also-ask')
def api_people_also_ask():
    """Get People Also Ask questions"""
    result = get_people_also_ask(
        keyword=MIAMI_KEYWORD
    )
    return jsonify(result)

@app.route('/api/related-searches')
def api_related_searches():
    """Get related search queries"""
    result = get_related_searches(
        query=MIAMI_KEYWORD,
        location="United States"
    )
    return jsonify(result)

@app.route('/api/keyword-volume')
def api_keyword_volume():
    """Get keyword search volume"""
    result = get_keyword_search_volume(
        keyword=MIAMI_KEYWORD,
        location="United States"
    )
    return jsonify(result)

@app.route('/api/search-trends')
def api_search_trends():
    """Get Google Trends data"""
    result = get_search_trends(
        keyword="moving companies",
        location="US-FL",
        date_range="today 3-m"
    )
    return jsonify(result)

@app.route('/api/keyword-difficulty')
def api_keyword_difficulty():
    """Get keyword difficulty analysis"""
    result = get_keyword_difficulty(
        keyword=MIAMI_KEYWORD,
        location="United States"
    )
    return jsonify(result)

@app.route('/api/serp-analysis')
def api_serp_analysis():
    """Get SERP feature analysis"""
    result = analyze_serp(
        keyword=MIAMI_KEYWORD,
        location=MIAMI_LOCATION
    )
    return jsonify(result)

@app.route('/api/competitor-keywords')
def api_competitor_keywords():
    """Get competitor keyword analysis"""
    result = get_competitor_keywords(
        competitor_domain="movebuddha.com",
        location="United States",
        num_results=10
    )
    return jsonify(result)

@app.route('/api/image-search')
def api_image_search():
    """Get image search results"""
    result = search_images(
        query="moving truck miami",
        num_results=10
    )
    return jsonify(result)

@app.route('/api/news-search')
def api_news_search():
    """Get news articles"""
    result = search_news(
        query="moving companies miami",
        location=MIAMI_LOCATION,
        date_range="qdr:m",
        num_results=5
    )
    return jsonify(result)

@app.route('/api/shopping-search')
def api_shopping_search():
    """Get shopping results for moving supplies"""
    result = search_shopping(
        query="moving boxes supplies",
        location=MIAMI_LOCATION,
        num_results=10
    )
    return jsonify(result)

@app.route('/api/yelp-businesses')
def api_yelp_businesses():
    """Get Yelp business listings (with DB save)"""
    from flask import request
    force_refresh = request.args.get('refresh', 'false').lower() == 'true'
    
    result = smart_api_call(
        "Yelp Business Search",
        search_yelp_businesses,
        "moving companies",
        MIAMI_LOCATION,
        10,
        save_function=db.save_yelp_businesses,
        force_refresh=force_refresh
    )
    return jsonify(result)

@app.route('/api/youtube-videos')
def api_youtube_videos():
    """Get YouTube video search results (with DB save)"""
    from flask import request
    force_refresh = request.args.get('refresh', 'false').lower() == 'true'
    
    result = smart_api_call(
        "YouTube Search",
        search_youtube,
        "moving companies miami tips",
        10,
        save_function=db.save_youtube_videos,
        force_refresh=force_refresh
    )
    return jsonify(result)

@app.route('/api/job-listings')
def api_job_listings():
    """Get Google Jobs listings (with DB save)"""
    from flask import request
    force_refresh = request.args.get('refresh', 'false').lower() == 'true'
    
    result = smart_api_call(
        "Google Jobs",
        search_jobs,
        "mover",
        MIAMI_LOCATION,
        10,
        save_function=db.save_job_listings,
        force_refresh=force_refresh
    )
    return jsonify(result)

@app.route('/api/tripadvisor')
def api_tripadvisor():
    """Get TripAdvisor business listings (storage facilities)"""
    result = search_tripadvisor(
        query="storage facilities miami",
        location=MIAMI_LOCATION
    )
    return jsonify(result)

@app.route('/api/linkedin-jobs')
def api_linkedin_jobs():
    """Get LinkedIn job listings"""
    result = search_linkedin_jobs(
        query="mover operations",
        location=MIAMI_LOCATION,
        num_results=10
    )
    return jsonify(result)

@app.route('/api/apple-apps')
def api_apple_apps():
    """Get Apple App Store apps (moving calculators)"""
    result = search_apple_apps(
        query="moving calculator cost estimator",
        country="us"
    )
    return jsonify(result)

@app.route('/api/google-play-apps')
def api_google_play_apps():
    """Get Google Play Store apps (moving planners)"""
    result = search_google_play_apps(
        query="moving planner checklist",
        country="us"
    )
    return jsonify(result)

@app.route('/api/patents')
def api_patents():
    """Get Google Patents (moving equipment innovations)"""
    result = search_patents(
        query="moving equipment packing innovation",
        num_results=10
    )
    return jsonify(result)

@app.route('/api/amazon-products')
def api_amazon_products():
    """Get Amazon products (moving supplies)"""
    result = search_amazon_products(
        query="moving boxes supplies",
        domain="amazon.com"
    )
    return jsonify(result)

@app.route('/api/walmart-products')
def api_walmart_products():
    """Get Walmart products (moving supplies comparison)"""
    result = search_walmart_products(
        query="moving boxes packing supplies"
    )
    return jsonify(result)

@app.route('/api/keyword-volume-history')
def api_keyword_volume_history():
    """Get keyword volume history across multiple time periods"""
    result = get_keyword_volume_history(
        keyword=MIAMI_KEYWORD,
        location="US-FL",
        date_ranges=["today 1-m", "today 3-m", "today 12-m"]
    )
    
    # Save to database
    if result.get('status') == 'success':
        api_call_id = db.log_api_call(
            endpoint="Keyword Volume History",
            query=MIAMI_KEYWORD,
            location="US-FL",
            status='success',
            raw_response=result
        )
        db.save_keyword_volume_history(result, session_id, api_call_id)
    
    return jsonify(result)

@app.route('/api/keyword-comparison')
def api_keyword_comparison():
    """Compare multiple moving-related keywords"""
    keywords = [
        "moving companies miami",
        "movers miami",
        "miami moving services",
        "long distance movers miami"
    ]
    
    result = get_multi_keyword_comparison(
        keywords=keywords,
        location="US-FL",
        date_range="today 3-m"
    )
    return jsonify(result)

@app.route('/api/regional-interest')
def api_regional_interest():
    """Get regional interest breakdown for moving companies"""
    result = get_regional_interest(
        keyword="moving companies",
        country="US"
    )
    
    # Save to database
    if result.get('status') == 'success':
        api_call_id = db.log_api_call(
            endpoint="Regional Interest",
            query="moving companies",
            location="US",
            status='success',
            raw_response=result
        )
        db.save_regional_interest(result, session_id, api_call_id)
    
    return jsonify(result)

@app.route('/api/keyword-timeline')
def api_keyword_timeline():
    """Get cached timeline data for graphing"""
    from flask import request
    keyword = request.args.get('keyword', MIAMI_KEYWORD)
    location = request.args.get('location', 'US-FL')
    date_range = request.args.get('range', 'today 3-m')
    
    timeline = db.get_keyword_volume_timeline(keyword, location, date_range)
    
    return jsonify({
        'keyword': keyword,
        'location': location,
        'date_range': date_range,
        'timeline': timeline,
        'total_points': len(timeline)
    })

@app.route('/api/all-data')
def api_all_data():
    """Get ALL data at once (25+ APIs - may take 30-60 seconds)"""
    data = {
        # CORE SEARCH & RANKINGS (3)
        'google_search': google_search(MIAMI_KEYWORD, MIAMI_LOCATION, 5),
        'local_pack': get_local_pack_results("moving companies", MIAMI_LOCATION),
        'local_businesses': search_local_businesses("moving companies", MIAMI_LOCATION, 5),
        
        # KEYWORD RESEARCH (4)
        'keyword_suggestions': get_keyword_suggestions("moving companies miami", "us"),
        'autocomplete': get_autocomplete_suggestions("moving companies mia", "us"),
        'related_searches': get_related_searches(MIAMI_KEYWORD, "United States"),
        'people_also_ask': get_people_also_ask(MIAMI_KEYWORD),
        
        # COMPETITIVE INTELLIGENCE (3)
        'keyword_difficulty': get_keyword_difficulty(MIAMI_KEYWORD, "United States"),
        'serp_analysis': analyze_serp(MIAMI_KEYWORD, MIAMI_LOCATION),
        'competitor_keywords': get_competitor_keywords("movebuddha.com", "United States", 5),
        
        # MEDIA & CONTENT (3)
        'image_search': search_images("moving truck miami", 5),
        'news_search': search_news("moving companies miami", MIAMI_LOCATION, "qdr:m", 3),
        'shopping_search': search_shopping("moving boxes", MIAMI_LOCATION, 5),
        
        # JOB MARKET INTELLIGENCE (3)
        'google_jobs': search_jobs("mover", MIAMI_LOCATION, 5),
        'linkedin_jobs': search_linkedin_jobs("mover operations", MIAMI_LOCATION, 5),
        'search_trends': get_search_trends("moving companies", "US-FL", "today 3-m"),
        
        # REVIEW PLATFORMS (3)
        'yelp_businesses': search_yelp_businesses("moving companies", MIAMI_LOCATION, 5),
        'tripadvisor': search_tripadvisor("storage facilities miami", MIAMI_LOCATION),
        'keyword_volume': get_keyword_search_volume(MIAMI_KEYWORD, "United States"),
        
        # APP STORES (2)
        'apple_apps': search_apple_apps("moving calculator", "us"),
        'google_play_apps': search_google_play_apps("moving planner", "us"),
        
        # ECOMMERCE & PRICING (3)
        'amazon_products': search_amazon_products("moving boxes"),
        'walmart_products': search_walmart_products("moving boxes"),
        'youtube_videos': search_youtube("moving companies miami tips", 5),
        
        # INNOVATION TRACKING (1)
        'patents': search_patents("moving equipment innovation", 5)
    }
    return jsonify(data)

# NEW SEARCH ENGINES & ANALYTICS ENDPOINTS

@app.route('/api/bing-search')
def api_bing_search():
    """Get Bing search results"""
    from flask import request
    force_refresh = request.args.get('refresh', 'false').lower() == 'true'
    
    result = smart_api_call(
        "Bing Search",
        search_bing,
        "moving companies miami",
        10,
        MIAMI_LOCATION,
        force_refresh=force_refresh
    )
    return jsonify(result)

@app.route('/api/duckduckgo-search')
def api_duckduckgo_search():
    """Get DuckDuckGo search results"""
    from flask import request
    force_refresh = request.args.get('refresh', 'false').lower() == 'true'
    
    result = smart_api_call(
        "DuckDuckGo Search",
        search_duckduckgo,
        "moving companies miami",
        10,
        MIAMI_LOCATION,
        force_refresh=force_refresh
    )
    return jsonify(result)

@app.route('/api/google-scholar')
def api_google_scholar():
    """Get Google Scholar academic papers"""
    from flask import request
    force_refresh = request.args.get('refresh', 'false').lower() == 'true'
    
    result = smart_api_call(
        "Google Scholar",
        search_scholar,
        "moving companies logistics",
        10,
        2020,
        2025,
        force_refresh=force_refresh
    )
    return jsonify(result)

@app.route('/api/google-finance')
def api_google_finance():
    """Get Google Finance data"""
    from flask import request
    force_refresh = request.args.get('refresh', 'false').lower() == 'true'
    
    result = smart_api_call(
        "Google Finance",
        search_finance,
        "moving companies transportation",
        10,
        force_refresh=force_refresh
    )
    return jsonify(result)

@app.route('/api/marketing-analytics')
def api_marketing_analytics():
    """Get comprehensive marketing analytics"""
    from flask import request
    force_refresh = request.args.get('refresh', 'false').lower() == 'true'
    
    result = smart_api_call(
        "Marketing Analytics",
        get_marketing_analytics_summary,
        force_refresh=force_refresh
    )
    return jsonify(result)

@app.route('/api/market-trends')
def api_market_trends():
    """Get market trends for transportation industry"""
    from flask import request
    force_refresh = request.args.get('refresh', 'false').lower() == 'true'
    
    result = smart_api_call(
        "Market Trends",
        get_market_trends,
        "transportation",
        force_refresh=force_refresh
    )
    return jsonify(result)

@app.route('/api/miami-map-data')
def api_miami_map_data():
    """Get Miami map visualization data with SerpApi integration"""
    try:
        result = get_miami_map_data()
        return jsonify(result)
    except Exception as e:
        return jsonify({
            "status": "error",
            "error": f"Error getting Miami map data: {str(e)}"
        }), 500

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🚀 SerpApi Live Data Server Starting...")
    print("="*80)
    print(f"📍 Location: {MIAMI_LOCATION}")
    print(f"🔑 API Key: ...{os.environ.get('SERPAPI_API_KEY', '')[-20:]}")
    print(f"🌐 Server: http://localhost:5001")
    print(f"📊 Dashboard: http://localhost:5001/")
    print("="*80)
    print("\n✅ Server is running. Press CTRL+C to stop.\n")
    
    app.run(debug=True, host='0.0.0.0', port=5001)

