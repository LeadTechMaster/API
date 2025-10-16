#!/usr/bin/env python3
"""
Marketing Analytics - Data aggregation and insights
Combines data from multiple APIs to create marketing intelligence
"""

import os
import sqlite3
from typing import Dict, List, Optional
from datetime import datetime, timedelta

# Database path
DB_PATH = os.path.join(os.path.dirname(__file__), 'DB', 'serpapi_data.db')

class MarketingAnalytics:
    def __init__(self):
        self.db_path = DB_PATH
    
    def get_connection(self):
        """Get database connection"""
        return sqlite3.connect(self.db_path)
    
    def get_market_penetration_analysis(self) -> Dict:
        """
        Analyze market penetration across platforms
        Combines Google Maps, Yelp, and search data
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get businesses from Google Maps
            cursor.execute("""
                SELECT business_name, rating, reviews_count, phone, address
                FROM local_businesses 
                ORDER BY reviews_count DESC
                LIMIT 10
            """)
            google_businesses = cursor.fetchall()
            
            # Get Yelp businesses
            cursor.execute("""
                SELECT business_name, rating, reviews_count, phone
                FROM yelp_reviews 
                ORDER BY reviews_count DESC
                LIMIT 10
            """)
            yelp_businesses = cursor.fetchall()
            
            # Calculate market metrics
            total_google_reviews = sum(b[2] for b in google_businesses if b[2])
            total_yelp_reviews = sum(b[2] for b in yelp_businesses if b[2])
            avg_google_rating = sum(b[1] for b in google_businesses if b[1]) / len(google_businesses) if google_businesses else 0
            avg_yelp_rating = sum(b[1] for b in yelp_businesses if b[1]) / len(yelp_businesses) if yelp_businesses else 0
            
            # Find businesses on both platforms
            google_names = {b[0].lower() for b in google_businesses}
            yelp_names = {b[0].lower() for b in yelp_businesses}
            cross_platform = len(google_names.intersection(yelp_names))
            
            conn.close()
            
            return {
                "status": "success",
                "analysis_type": "market_penetration",
                "platforms": {
                    "google_maps": {
                        "businesses": len(google_businesses),
                        "total_reviews": total_google_reviews,
                        "avg_rating": round(avg_google_rating, 2),
                        "top_business": google_businesses[0][0] if google_businesses else "N/A"
                    },
                    "yelp": {
                        "businesses": len(yelp_businesses),
                        "total_reviews": total_yelp_reviews,
                        "avg_rating": round(avg_yelp_rating, 2),
                        "top_business": yelp_businesses[0][0] if yelp_businesses else "N/A"
                    }
                },
                "cross_platform_analysis": {
                    "businesses_on_both": cross_platform,
                    "google_only": len(google_names - yelp_names),
                    "yelp_only": len(yelp_names - google_names),
                    "market_coverage": round((cross_platform / max(len(google_names), len(yelp_names))) * 100, 1) if max(len(google_names), len(yelp_names)) > 0 else 0
                },
                "insights": [
                    f"Market leader: {google_businesses[0][0] if google_businesses else 'N/A'} with {google_businesses[0][2] if google_businesses else 0} reviews",
                    f"Cross-platform presence: {cross_platform} businesses on both Google and Yelp",
                    f"Market coverage: {round((cross_platform / max(len(google_names), len(yelp_names))) * 100, 1) if max(len(google_names), len(yelp_names)) > 0 else 0}% of businesses on both platforms"
                ]
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error in market penetration analysis: {str(e)}"
            }
    
    def get_competitive_intelligence(self) -> Dict:
        """
        Competitive intelligence from multiple data sources
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get top competitors by reviews
            cursor.execute("""
                SELECT business_name, rating, reviews_count, phone
                FROM local_businesses 
                WHERE reviews_count > 100
                ORDER BY reviews_count DESC
                LIMIT 5
            """)
            top_competitors = cursor.fetchall()
            
            # Get keyword difficulty data
            cursor.execute("""
                SELECT keyword, difficulty_score, organic_results, paid_ads
                FROM keywords 
                ORDER BY difficulty_score ASC
                LIMIT 5
            """)
            keyword_opportunities = cursor.fetchall()
            
            # Get recent news mentions
            cursor.execute("""
                SELECT title, source, date
                FROM news_articles 
                ORDER BY created_at DESC
                LIMIT 5
            """)
            recent_news = cursor.fetchall()
            
            conn.close()
            
            return {
                "status": "success",
                "analysis_type": "competitive_intelligence",
                "top_competitors": [
                    {
                        "name": comp[0],
                        "rating": comp[1],
                        "reviews": comp[2],
                        "phone": comp[3],
                        "market_share": f"{round((comp[2] / sum(c[2] for c in top_competitors)) * 100, 1)}%" if top_competitors else "0%"
                    } for comp in top_competitors
                ],
                "keyword_opportunities": [
                    {
                        "keyword": kw[0],
                        "difficulty": kw[1],
                        "organic_results": kw[2],
                        "paid_ads": kw[3],
                        "opportunity_level": "High" if kw[1] < 30 else "Medium" if kw[1] < 60 else "Low"
                    } for kw in keyword_opportunities
                ],
                "recent_news": [
                    {
                        "title": news[0],
                        "source": news[1],
                        "date": news[2]
                    } for news in recent_news
                ],
                "insights": [
                    f"Market leader: {top_competitors[0][0] if top_competitors else 'N/A'} with {top_competitors[0][2] if top_competitors else 0} reviews",
                    f"Best keyword opportunity: {keyword_opportunities[0][0] if keyword_opportunities else 'N/A'} (difficulty: {keyword_opportunities[0][1] if keyword_opportunities else 'N/A'})",
                    f"Recent industry news: {len(recent_news)} articles in database"
                ]
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error in competitive intelligence: {str(e)}"
            }
    
    def get_content_strategy_insights(self) -> Dict:
        """
        Content strategy insights from FAQ and related searches
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get People Also Ask questions
            cursor.execute("""
                SELECT question, answer
                FROM people_also_ask 
                ORDER BY created_at DESC
                LIMIT 10
            """)
            faq_data = cursor.fetchall()
            
            # Get related searches
            cursor.execute("""
                SELECT query
                FROM related_searches 
                ORDER BY created_at DESC
                LIMIT 15
            """)
            related_searches = cursor.fetchall()
            
            # Get keyword suggestions
            cursor.execute("""
                SELECT keyword, relevance_score
                FROM keyword_suggestions 
                ORDER BY relevance_score DESC
                LIMIT 10
            """)
            keyword_suggestions = cursor.fetchall()
            
            conn.close()
            
            # Analyze content opportunities
            content_opportunities = []
            for faq in faq_data:
                if faq[0] and len(faq[0]) > 10:  # Valid question
                    content_opportunities.append({
                        "type": "FAQ Article",
                        "title": faq[0],
                        "priority": "High",
                        "reason": "Featured snippet opportunity"
                    })
            
            for related in related_searches[:5]:
                if related[0] and len(related[0]) > 5:
                    content_opportunities.append({
                        "type": "Blog Post",
                        "title": f"Complete Guide to {related[0]}",
                        "priority": "Medium",
                        "reason": "User search intent"
                    })
            
            return {
                "status": "success",
                "analysis_type": "content_strategy",
                "content_opportunities": content_opportunities,
                "faq_questions": [{"question": faq[0], "answer": faq[1][:100] + "..." if faq[1] and len(faq[1]) > 100 else faq[1]} for faq in faq_data],
                "related_searches": [search[0] for search in related_searches],
                "top_keywords": [{"keyword": kw[0], "relevance": kw[1]} for kw in keyword_suggestions],
                "insights": [
                    f"Content opportunities: {len(content_opportunities)} identified",
                    f"FAQ questions: {len(faq_data)} for featured snippets",
                    f"Related searches: {len(related_searches)} for content ideas",
                    f"Top keyword: {keyword_suggestions[0][0] if keyword_suggestions else 'N/A'} (relevance: {keyword_suggestions[0][1] if keyword_suggestions else 'N/A'})"
                ]
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error in content strategy analysis: {str(e)}"
            }
    
    def get_pricing_intelligence(self) -> Dict:
        """
        Pricing intelligence from product data
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get shopping products
            cursor.execute("""
                SELECT product_name, price, rating, source
                FROM shopping_products 
                WHERE price IS NOT NULL AND price > 0
                ORDER BY price ASC
            """)
            products = cursor.fetchall()
            
            if not products:
                return {
                    "status": "success",
                    "analysis_type": "pricing_intelligence",
                    "message": "No product pricing data available"
                }
            
            # Calculate pricing metrics
            prices = [float(p[1]) for p in products if p[1]]
            avg_price = sum(prices) / len(prices) if prices else 0
            min_price = min(prices) if prices else 0
            max_price = max(prices) if prices else 0
            
            # Price ranges
            price_ranges = {
                "budget": len([p for p in prices if p < 10]),
                "mid_range": len([p for p in prices if 10 <= p < 50]),
                "premium": len([p for p in prices if p >= 50])
            }
            
            # Top products by rating
            top_rated = sorted(products, key=lambda x: x[2] or 0, reverse=True)[:5]
            
            conn.close()
            
            return {
                "status": "success",
                "analysis_type": "pricing_intelligence",
                "pricing_metrics": {
                    "total_products": len(products),
                    "average_price": round(avg_price, 2),
                    "price_range": f"${min_price:.2f} - ${max_price:.2f}",
                    "median_price": round(sorted(prices)[len(prices)//2], 2) if prices else 0
                },
                "price_distribution": price_ranges,
                "top_rated_products": [
                    {
                        "name": product[0],
                        "price": product[1],
                        "rating": product[2],
                        "source": product[3]
                    } for product in top_rated
                ],
                "insights": [
                    f"Average moving supply cost: ${avg_price:.2f}",
                    f"Price range: ${min_price:.2f} - ${max_price:.2f}",
                    f"Budget options: {price_ranges['budget']} products under $10",
                    f"Premium options: {price_ranges['premium']} products over $50"
                ]
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error in pricing intelligence: {str(e)}"
            }
    
    def get_trend_analysis(self) -> Dict:
        """
        Trend analysis from time-series data
        """
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            
            # Get recent volume data
            cursor.execute("""
                SELECT date_range, avg_interest, trend_direction, volatility
                FROM keyword_volume_history 
                WHERE timeline_date IS NOT NULL
                ORDER BY created_at DESC
                LIMIT 10
            """)
            volume_data = cursor.fetchall()
            
            # Get regional trends
            cursor.execute("""
                SELECT region, interest_value, rank
                FROM regional_interest 
                ORDER BY rank ASC
                LIMIT 10
            """)
            regional_data = cursor.fetchall()
            
            conn.close()
            
            if not volume_data:
                return {
                    "status": "success",
                    "analysis_type": "trend_analysis",
                    "message": "No trend data available yet"
                }
            
            # Analyze trends
            recent_avg = sum(v[1] for v in volume_data[:3] if v[1]) / 3 if volume_data[:3] else 0
            older_avg = sum(v[1] for v in volume_data[3:6] if v[1]) / 3 if len(volume_data) > 3 else 0
            
            trend_direction = "Growing" if recent_avg > older_avg else "Declining" if recent_avg < older_avg else "Stable"
            trend_percentage = abs((recent_avg - older_avg) / older_avg * 100) if older_avg > 0 else 0
            
            return {
                "status": "success",
                "analysis_type": "trend_analysis",
                "search_trends": {
                    "current_interest": round(recent_avg, 1),
                    "previous_interest": round(older_avg, 1),
                    "trend_direction": trend_direction,
                    "trend_percentage": round(trend_percentage, 1),
                    "volatility": round(sum(v[3] for v in volume_data if v[3]) / len(volume_data), 1) if volume_data else 0
                },
                "regional_trends": [
                    {
                        "region": region[0],
                        "interest": region[1],
                        "rank": region[2],
                        "market_potential": "High" if region[1] >= 60 else "Medium" if region[1] >= 40 else "Low"
                    } for region in regional_data
                ],
                "insights": [
                    f"Search interest: {trend_direction} by {trend_percentage:.1f}%",
                    f"Current interest level: {recent_avg:.1f}/100",
                    f"Top market: {regional_data[0][0] if regional_data else 'N/A'} (interest: {regional_data[0][1] if regional_data else 'N/A'})",
                    f"Market volatility: {round(sum(v[3] for v in volume_data if v[3]) / len(volume_data), 1) if volume_data else 0}/100"
                ]
            }
            
        except Exception as e:
            return {
                "status": "error",
                "error": f"Error in trend analysis: {str(e)}"
            }

def get_marketing_analytics_summary() -> Dict:
    """
    Get comprehensive marketing analytics summary
    """
    analytics = MarketingAnalytics()
    
    return {
        "status": "success",
        "analysis_type": "comprehensive_marketing_analytics",
        "timestamp": datetime.now().isoformat(),
        "analyses": {
            "market_penetration": analytics.get_market_penetration_analysis(),
            "competitive_intelligence": analytics.get_competitive_intelligence(),
            "content_strategy": analytics.get_content_strategy_insights(),
            "pricing_intelligence": analytics.get_pricing_intelligence(),
            "trend_analysis": analytics.get_trend_analysis()
        }
    }

if __name__ == "__main__":
    # Test the analytics
    analytics = MarketingAnalytics()
    
    print("=== Marketing Analytics Test ===")
    
    market = analytics.get_market_penetration_analysis()
    print(f"Market Penetration: {market.get('status', 'error')}")
    
    competitive = analytics.get_competitive_intelligence()
    print(f"Competitive Intelligence: {competitive.get('status', 'error')}")
    
    content = analytics.get_content_strategy_insights()
    print(f"Content Strategy: {content.get('status', 'error')}")
    
    pricing = analytics.get_pricing_intelligence()
    print(f"Pricing Intelligence: {pricing.get('status', 'error')}")
    
    trends = analytics.get_trend_analysis()
    print(f"Trend Analysis: {trends.get('status', 'error')}")

