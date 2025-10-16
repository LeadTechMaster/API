#!/usr/bin/env python3
"""
SerpApi Database Manager
Handles all database operations for storing and retrieving API data
NO MOCK DATA - ALL REAL DATA WITH VALIDATION
"""

import sqlite3
import json
import os
from datetime import datetime
from typing import Dict, List, Optional, Any

class SerpApiDB:
    def __init__(self, db_path: str = None):
        if db_path is None:
            db_dir = os.path.dirname(os.path.abspath(__file__))
            db_path = os.path.join(db_dir, 'serpapi_data.db')
        
        self.db_path = db_path
        self.init_database()
    
    def init_database(self):
        """Initialize database with enhanced schema"""
        schema_path = os.path.join(os.path.dirname(__file__), 'enhanced_schema.sql')
        
        with open(schema_path, 'r') as f:
            schema_sql = f.read()
        
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        cursor.executescript(schema_sql)
        conn.commit()
        conn.close()
        
        print(f"✅ Database initialized: {self.db_path}")
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    # ========================================================================
    # SESSION MANAGEMENT
    # ========================================================================
    
    def create_session(self, session_name: str, industry: str, location: str) -> int:
        """Create a new search session"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT INTO search_sessions (session_name, industry, location)
            VALUES (?, ?, ?)
        """, (session_name, industry, location))
        
        session_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return session_id
    
    def get_current_session(self, industry: str, location: str) -> Optional[int]:
        """Get or create current session for industry/location"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Get most recent uncompleted session
        cursor.execute("""
            SELECT id FROM search_sessions
            WHERE industry = ? AND location = ? AND completed_at IS NULL
            ORDER BY created_at DESC
            LIMIT 1
        """, (industry, location))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            return result[0]
        else:
            # Create new session
            session_name = f"{industry} - {location} - {datetime.now().strftime('%Y-%m-%d %H:%M')}"
            return self.create_session(session_name, industry, location)
    
    # ========================================================================
    # API CALL LOGGING
    # ========================================================================
    
    def log_api_call(self, endpoint: str, query: str, location: str, 
                     status: str, response_time_ms: int = None, 
                     error_message: str = None, raw_response: Any = None) -> int:
        """Log an API call for tracking and validation"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        raw_json = json.dumps(raw_response) if raw_response else None
        
        cursor.execute("""
            INSERT INTO api_calls (
                api_endpoint, query, location, status, response_time_ms,
                error_message, raw_response, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (endpoint, query, location, status, response_time_ms, 
              error_message, raw_json, datetime.now()))
        
        api_call_id = cursor.lastrowid
        conn.commit()
        conn.close()
        
        return api_call_id
    
    # ========================================================================
    # GOOGLE SEARCH DATA
    # ========================================================================
    
    def save_search_results(self, data: Dict, session_id: int, api_call_id: int):
        """Save Google search results"""
        if data.get('status') != 'success':
            return
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        keyword = data.get('query', '')
        location = data.get('location', '')
        
        for result in data.get('organic_results', []):
            cursor.execute("""
                INSERT INTO search_results (
                    keyword, location, position, title, link, snippet, domain,
                    rating, reviews_count, session_id, api_call_id, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                keyword, location, result.get('position'), result.get('title'),
                result.get('link'), result.get('snippet'), 
                result.get('displayed_link', '').split('/')[0] if result.get('displayed_link') else None,
                result.get('rich_snippet', {}).get('top', {}).get('detected_extensions', {}).get('rating'),
                result.get('rich_snippet', {}).get('top', {}).get('detected_extensions', {}).get('reviews'),
                session_id, api_call_id, datetime.now()
            ))
        
        conn.commit()
        conn.close()
    
    def save_keyword_difficulty(self, data: Dict, session_id: int, api_call_id: int):
        """Save keyword difficulty analysis"""
        if data.get('status') != 'success':
            return
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            INSERT OR REPLACE INTO keywords (
                keyword, location, difficulty_score, difficulty_level,
                session_id, api_call_id, created_at, updated_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get('keyword'), data.get('location'),
            data.get('difficulty_score'), data.get('difficulty_level'),
            session_id, api_call_id, datetime.now(), datetime.now()
        ))
        
        conn.commit()
        conn.close()
    
    def save_keyword_suggestions(self, data: Dict, session_id: int, api_call_id: int):
        """Save keyword suggestions"""
        if data.get('status') != 'success':
            return
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        seed_keyword = data.get('seed_keyword', '')
        
        for suggestion in data.get('suggestions', []):
            cursor.execute("""
                INSERT INTO keyword_suggestions (
                    seed_keyword, suggested_keyword, relevance_score,
                    session_id, api_call_id, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (seed_keyword, suggestion, None, session_id, api_call_id, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def save_people_also_ask(self, data: Dict, session_id: int, api_call_id: int):
        """Save People Also Ask questions"""
        if data.get('status') != 'success':
            return
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        keyword = data.get('keyword', '')
        
        for i, q in enumerate(data.get('questions', []), 1):
            cursor.execute("""
                INSERT INTO people_also_ask (
                    keyword, question, answer, source_title, source_link, position,
                    session_id, api_call_id, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                keyword, q.get('question'), q.get('answer'),
                q.get('title'), q.get('link'), i,
                session_id, api_call_id, datetime.now()
            ))
        
        conn.commit()
        conn.close()
    
    def save_related_searches(self, data: Dict, session_id: int, api_call_id: int):
        """Save related searches"""
        if data.get('status') != 'success':
            return
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        keyword = data.get('query', '')
        
        for search in data.get('related_searches', []):
            cursor.execute("""
                INSERT INTO related_searches (
                    keyword, related_keyword, link, session_id, api_call_id, created_at
                ) VALUES (?, ?, ?, ?, ?, ?)
            """, (keyword, search.get('query'), search.get('link'), 
                  session_id, api_call_id, datetime.now()))
        
        conn.commit()
        conn.close()
    
    def save_serp_analysis(self, data: Dict, session_id: int, api_call_id: int):
        """Save SERP feature analysis"""
        if data.get('status') != 'success':
            return
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        features = data.get('features', {})
        
        cursor.execute("""
            INSERT INTO serp_features (
                keyword, location, has_ads, num_ads, has_featured_snippet,
                has_knowledge_graph, has_local_results, has_images, has_videos,
                has_shopping, has_people_also_ask, has_related_searches,
                organic_results_count, session_id, api_call_id, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            data.get('keyword'), data.get('location'),
            features.get('has_ads'), features.get('num_ads'),
            features.get('has_featured_snippet'), features.get('has_knowledge_graph'),
            features.get('has_local_results'), features.get('has_image_results'),
            features.get('has_video_results'), features.get('has_shopping_results'),
            features.get('has_people_also_ask'), features.get('has_related_searches'),
            data.get('organic_results_count'),
            session_id, api_call_id, datetime.now()
        ))
        
        conn.commit()
        conn.close()
    
    # ========================================================================
    # LOCAL BUSINESS DATA
    # ========================================================================
    
    def save_local_businesses(self, data: Dict, session_id: int, api_call_id: int):
        """Save local businesses from Google Maps"""
        if data.get('status') != 'success':
            return
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = data.get('query', '')
        location = data.get('location', '')
        
        for biz in data.get('businesses', []):
            cursor.execute("""
                INSERT OR REPLACE INTO local_businesses (
                    business_name, place_id, address, phone, website,
                    rating, reviews_count, latitude, longitude, hours,
                    type, types, price_range, service_options,
                    query, location, position, session_id, api_call_id, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                biz.get('title'), biz.get('place_id'), biz.get('address'),
                biz.get('phone'), biz.get('website'), biz.get('rating'),
                biz.get('reviews'), 
                biz.get('gps_coordinates', {}).get('latitude'),
                biz.get('gps_coordinates', {}).get('longitude'),
                biz.get('hours'), biz.get('type'),
                json.dumps(biz.get('types', [])),
                biz.get('price'), json.dumps(biz.get('service_options', {})),
                query, location, biz.get('position'),
                session_id, api_call_id, datetime.now()
            ))
        
        conn.commit()
        conn.close()
    
    def save_local_pack(self, data: Dict, session_id: int, api_call_id: int):
        """Save local pack (3-pack) results"""
        if data.get('status') != 'success':
            return
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        keyword = data.get('keyword', '')
        location = data.get('location', '')
        
        for biz in data.get('local_pack', []):
            cursor.execute("""
                INSERT INTO local_pack (
                    keyword, location, business_name, address, phone,
                    rating, reviews_count, position, place_id,
                    gps_latitude, gps_longitude, hours,
                    session_id, api_call_id, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                keyword, location, biz.get('title'), biz.get('address'),
                biz.get('phone'), biz.get('rating'), biz.get('reviews'),
                biz.get('position'), biz.get('place_id'),
                biz.get('gps_coordinates', {}).get('latitude'),
                biz.get('gps_coordinates', {}).get('longitude'),
                biz.get('hours'), session_id, api_call_id, datetime.now()
            ))
        
        conn.commit()
        conn.close()
    
    # ========================================================================
    # MEDIA & CONTENT
    # ========================================================================
    
    def save_images(self, data: Dict, session_id: int, api_call_id: int):
        """Save image search results"""
        if data.get('status') != 'success':
            return
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = data.get('query', '')
        
        for img in data.get('images', []):
            cursor.execute("""
                INSERT INTO images (
                    query, title, link, original_url, thumbnail_url,
                    source, source_link, position, session_id, api_call_id, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                query, img.get('title'), img.get('link'), img.get('original'),
                img.get('thumbnail'), img.get('source'), img.get('source_link'),
                img.get('position'), session_id, api_call_id, datetime.now()
            ))
        
        conn.commit()
        conn.close()
    
    def save_news(self, data: Dict, session_id: int, api_call_id: int):
        """Save news articles"""
        if data.get('status') != 'success':
            return
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = data.get('query', '')
        
        for article in data.get('news', []):
            cursor.execute("""
                INSERT INTO news_articles (
                    query, title, link, source, published_date, snippet,
                    thumbnail_url, position, session_id, api_call_id, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                query, article.get('title'), article.get('link'),
                article.get('source'), article.get('date'), article.get('snippet'),
                article.get('thumbnail'), article.get('position'),
                session_id, api_call_id, datetime.now()
            ))
        
        conn.commit()
        conn.close()
    
    def save_shopping(self, data: Dict, session_id: int, api_call_id: int):
        """Save shopping products"""
        if data.get('status') != 'success':
            return
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        query = data.get('query', '')
        
        for product in data.get('products', []):
            cursor.execute("""
                INSERT INTO shopping_products (
                    query, title, link, product_link, product_id, source,
                    price, extracted_price, rating, reviews_count,
                    thumbnail_url, delivery_info, position,
                    session_id, api_call_id, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                query, product.get('title'), product.get('link'),
                product.get('product_link'), product.get('product_id'),
                product.get('source'), product.get('price'),
                product.get('extracted_price'), product.get('rating'),
                product.get('reviews'), product.get('thumbnail'),
                product.get('delivery'), product.get('position'),
                session_id, api_call_id, datetime.now()
            ))
        
        conn.commit()
        conn.close()
    
    # ========================================================================
    # NEW API SAVE FUNCTIONS
    # ========================================================================
    
    def save_yelp_businesses(self, data: Dict, session_id: int, api_call_id: int):
        """Save Yelp business data"""
        if data.get('status') != 'success':
            return
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        for biz in data.get('businesses', []):
            cursor.execute("""
                INSERT OR REPLACE INTO yelp_reviews (
                    business_name, yelp_url, rating, reviews_count, price_range,
                    categories, address, phone, query, location, position,
                    session_id, api_call_id, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                biz.get('business_name'), biz.get('yelp_url'), biz.get('rating'),
                biz.get('reviews_count'), biz.get('price_range'),
                json.dumps(biz.get('categories', [])), biz.get('address'),
                biz.get('phone'), data.get('query'), data.get('location'),
                biz.get('position'), session_id, api_call_id, datetime.now()
            ))
        
        conn.commit()
        conn.close()
    
    def save_youtube_videos(self, data: Dict, session_id: int, api_call_id: int):
        """Save YouTube video results"""
        if data.get('status') != 'success':
            return
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        for video in data.get('videos', []):
            cursor.execute("""
                INSERT OR REPLACE INTO youtube_videos (
                    query, video_id, title, channel_name, video_url, thumbnail_url,
                    description, view_count, published_date, duration, position,
                    session_id, api_call_id, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get('query'), video.get('video_id'), video.get('title'),
                video.get('channel_name'), video.get('video_url'), video.get('thumbnail_url'),
                video.get('description'), video.get('views'), video.get('published_date'),
                video.get('duration'), video.get('position'),
                session_id, api_call_id, datetime.now()
            ))
        
        conn.commit()
        conn.close()
    
    def save_job_listings(self, data: Dict, session_id: int, api_call_id: int):
        """Save job listings"""
        if data.get('status') != 'success':
            return
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        for job in data.get('jobs', []):
            cursor.execute("""
                INSERT INTO job_listings (
                    query, location, job_title, company_name, job_url, description,
                    salary, posted_date, position, session_id, api_call_id, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                data.get('query'), data.get('location'), job.get('job_title'),
                job.get('company_name'), job.get('job_url'), job.get('description'),
                job.get('salary'), job.get('posted_date'), job.get('position'),
                session_id, api_call_id, datetime.now()
            ))
        
        conn.commit()
        conn.close()
    
    def save_keyword_volume_history(self, data: Dict, session_id: int, api_call_id: int):
        """Save detailed keyword volume history with time series data"""
        if data.get('status') != 'success':
            return
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        keyword = data.get('keyword', '')
        location = data.get('location', '')
        
        # Save each time period's data
        for period in data.get('historical_data', []):
            date_range = period.get('date_range', '')
            stats = period.get('statistics', {})
            timeline = period.get('timeline', [])
            
            # Save aggregate statistics
            cursor.execute("""
                INSERT INTO keyword_volume_history (
                    keyword, location, date_range, timeline_date,
                    interest_value, avg_interest, max_interest, min_interest,
                    trend_direction, volatility, session_id, api_call_id, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                keyword, location, date_range, None,
                stats.get('current_interest'), stats.get('avg_interest'),
                stats.get('max_interest'), stats.get('min_interest'),
                stats.get('trend'), stats.get('volatility'),
                session_id, api_call_id, datetime.now()
            ))
            
            # Save individual timeline points
            for point in timeline:
                timeline_date = point.get('date', '')
                values = point.get('values', [])
                if values and len(values) > 0:
                    interest_val = values[0].get('extracted_value', 0)
                    
                    cursor.execute("""
                        INSERT INTO keyword_volume_history (
                            keyword, location, date_range, timeline_date,
                            interest_value, session_id, api_call_id, created_at
                        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (
                        keyword, location, date_range, timeline_date,
                        interest_val, session_id, api_call_id, datetime.now()
                    ))
        
        conn.commit()
        conn.close()
    
    def save_regional_interest(self, data: Dict, session_id: int, api_call_id: int):
        """Save regional interest data"""
        if data.get('status') != 'success':
            return
        
        conn = self.get_connection()
        cursor = conn.cursor()
        
        keyword = data.get('keyword', '')
        country = data.get('country', '')
        
        for i, region in enumerate(data.get('all_regions', []), 1):
            cursor.execute("""
                INSERT INTO regional_interest (
                    keyword, country, region, interest_value, rank,
                    session_id, api_call_id, created_at
                ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                keyword, country, region.get('location', ''),
                region.get('extracted_value', 0), i,
                session_id, api_call_id, datetime.now()
            ))
        
        conn.commit()
        conn.close()
    
    def save_keyword_metrics_snapshot(self, keyword: str, location: str, 
                                     difficulty_data: Dict, serp_data: Dict,
                                     session_id: int):
        """Save a snapshot of keyword metrics for historical tracking"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        today = datetime.now().date()
        
        cursor.execute("""
            INSERT OR REPLACE INTO keyword_metrics_history (
                keyword, location, date_measured, difficulty_score, competition_level,
                num_ads, num_organic_results, has_local_pack, session_id, created_at
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            keyword, location, today,
            difficulty_data.get('difficulty_score'),
            difficulty_data.get('difficulty_level'),
            serp_data.get('features', {}).get('num_ads', 0),
            serp_data.get('organic_results_count', 0),
            serp_data.get('features', {}).get('has_local_results', False),
            session_id, datetime.now()
        ))
        
        conn.commit()
        conn.close()
    
    # ========================================================================
    # DATA RETRIEVAL WITH FRESHNESS CHECK
    # ========================================================================
    
    def get_cached_data(self, table: str, query: str, location: str, max_age_minutes: int = 15) -> Optional[Dict]:
        """
        Get cached data from database if fresh enough
        
        Args:
            table: Table name to query
            query: Search query
            location: Location filter
            max_age_minutes: Maximum age of data in minutes (default: 15)
            
        Returns:
            Dict with cached data or None if too old/doesn't exist
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        # Check last API call for this query
        cursor.execute("""
            SELECT created_at, raw_response
            FROM api_calls
            WHERE query = ? AND location = ? AND status = 'success'
            AND created_at > datetime('now', '-' || ? || ' minutes')
            ORDER BY created_at DESC
            LIMIT 1
        """, (query, location, max_age_minutes))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            created_at, raw_response = result
            return {
                'from_cache': True,
                'cached_at': created_at,
                'data': json.loads(raw_response) if raw_response else None
            }
        
        return None
    
    def get_market_summary(self, industry: str, location: str) -> Dict:
        """Get comprehensive market summary"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT * FROM v_market_snapshot
        """)
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            columns = [desc[0] for desc in cursor.description]
            return dict(zip(columns, result))
        return {}
    
    def get_recent_searches(self, limit: int = 10) -> List[Dict]:
        """Get recent API calls"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT api_endpoint, query, location, status, created_at
            FROM api_calls
            ORDER BY created_at DESC
            LIMIT ?
        """, (limit,))
        
        results = []
        for row in cursor.fetchall():
            results.append({
                'endpoint': row[0],
                'query': row[1],
                'location': row[2],
                'status': row[3],
                'created_at': row[4]
            })
        
        conn.close()
        return results
    
    def get_data_freshness(self, endpoint: str, query: str, location: str) -> Dict:
        """
        Check how fresh the data is for a specific endpoint
        
        Returns:
            Dict with freshness info: last_updated, age_minutes, is_fresh
        """
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT created_at, 
                   (julianday('now') - julianday(created_at)) * 24 * 60 as age_minutes
            FROM api_calls
            WHERE api_endpoint = ? AND query = ? AND location = ? AND status = 'success'
            ORDER BY created_at DESC
            LIMIT 1
        """, (endpoint, query, location))
        
        result = cursor.fetchone()
        conn.close()
        
        if result:
            last_updated, age_minutes = result
            return {
                'last_updated': last_updated,
                'age_minutes': int(age_minutes),
                'is_fresh': age_minutes < 15,  # Fresh if < 15 minutes
                'needs_refresh': age_minutes >= 15
            }
        
        return {
            'last_updated': None,
            'age_minutes': None,
            'is_fresh': False,
            'needs_refresh': True
        }
    
    def get_keyword_volume_timeline(self, keyword: str, location: str, date_range: str = "today 3-m") -> List[Dict]:
        """Get keyword volume timeline for graphing"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT timeline_date, interest_value
            FROM keyword_volume_history
            WHERE keyword = ? AND location = ? AND date_range = ? AND timeline_date IS NOT NULL
            ORDER BY timeline_date
        """, (keyword, location, date_range))
        
        timeline = []
        for row in cursor.fetchall():
            timeline.append({
                'date': row[0],
                'interest': row[1]
            })
        
        conn.close()
        return timeline
    
    def get_keyword_historical_stats(self, keyword: str, location: str) -> Dict:
        """Get historical statistics for a keyword"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT 
                date_measured,
                difficulty_score,
                competition_level,
                num_organic_results,
                has_local_pack
            FROM keyword_metrics_history
            WHERE keyword = ? AND location = ?
            ORDER BY date_measured DESC
            LIMIT 30
        """, (keyword, location))
        
        history = []
        for row in cursor.fetchall():
            history.append({
                'date': row[0],
                'difficulty': row[1],
                'competition': row[2],
                'organic_results': row[3],
                'has_local_pack': bool(row[4])
            })
        
        conn.close()
        return {
            'keyword': keyword,
            'location': location,
            'total_snapshots': len(history),
            'history': history
        }
    
    def get_top_regions(self, keyword: str, limit: int = 10) -> List[Dict]:
        """Get top regions by interest for a keyword"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("""
            SELECT region, interest_value, rank
            FROM regional_interest
            WHERE keyword = ?
            ORDER BY rank ASC
            LIMIT ?
        """, (keyword, limit))
        
        regions = []
        for row in cursor.fetchall():
            regions.append({
                'region': row[0],
                'interest': row[1],
                'rank': row[2]
            })
        
        conn.close()
        return regions

# Singleton instance
_db_instance = None

def get_db() -> SerpApiDB:
    """Get database instance"""
    global _db_instance
    if _db_instance is None:
        _db_instance = SerpApiDB()
    return _db_instance

