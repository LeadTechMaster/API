#!/usr/bin/env python3
"""
Google Finance API - Financial data and market information
Provides stock prices, market trends, and financial news
"""

import requests
import os
from typing import Dict, List, Optional

# Get API key from environment or use hardcoded fallback
SERPAPI_API_KEY = os.getenv('SERPAPI_API_KEY', '850faf17d2e379f54ffdd1e300daaa7bdb1dee8abdc2536f1de3430d137e563c')

def search_finance(query: str, num_results: int = 10) -> Dict:
    """
    Search Google Finance for financial information
    
    Args:
        query: Search query (company name, ticker, etc.)
        num_results: Number of results to return
    
    Returns:
        Dict with financial data and news
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "google_finance",
            "q": query,
            "api_key": SERPAPI_API_KEY,
            "num": num_results
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract market summary
        market_summary = {}
        if "market_summary" in data:
            market_summary = {
                "market_status": data["market_summary"].get("market_status", ""),
                "market_time": data["market_summary"].get("market_time", ""),
                "market_change": data["market_summary"].get("market_change", ""),
                "market_change_percent": data["market_summary"].get("market_change_percent", "")
            }
        
        # Extract news
        news = []
        if "news" in data:
            for article in data["news"]:
                news.append({
                    "title": article.get("title", ""),
                    "link": article.get("link", ""),
                    "snippet": article.get("snippet", ""),
                    "date": article.get("date", ""),
                    "source": article.get("source", "")
                })
        
        # Extract stock data
        stocks = []
        if "stocks" in data:
            for stock in data["stocks"]:
                stocks.append({
                    "name": stock.get("name", ""),
                    "ticker": stock.get("ticker", ""),
                    "price": stock.get("price", ""),
                    "change": stock.get("change", ""),
                    "change_percent": stock.get("change_percent", ""),
                    "market_cap": stock.get("market_cap", ""),
                    "volume": stock.get("volume", "")
                })
        
        return {
            "status": "success",
            "query": query,
            "market_summary": market_summary,
            "news": news,
            "total_news": len(news),
            "stocks": stocks,
            "total_stocks": len(stocks),
            "search_engine": "Google Finance",
            "financial_focus": True,
            "api_response_time": data.get("search_metadata", {}).get("total_time_taken", 0)
        }
        
    except requests.exceptions.RequestException as e:
        return {
            "status": "error",
            "error": f"Request failed: {str(e)}",
            "query": query,
            "search_engine": "Google Finance"
        }
    except Exception as e:
        return {
            "status": "error", 
            "error": f"Unexpected error: {str(e)}",
            "query": query,
            "search_engine": "Google Finance"
        }

def get_market_trends(category: str = "transportation") -> Dict:
    """
    Get market trends for a specific category
    
    Args:
        category: Market category (transportation, logistics, etc.)
    
    Returns:
        Dict with market trend data
    """
    try:
        url = "https://serpapi.com/search"
        
        params = {
            "engine": "google_finance",
            "q": f"{category} stocks market trends",
            "api_key": SERPAPI_API_KEY,
            "num": 20
        }
        
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()
        
        # Extract trending stocks
        trending_stocks = []
        if "stocks" in data:
            for stock in data["stocks"][:10]:  # Top 10 trending
                trending_stocks.append({
                    "name": stock.get("name", ""),
                    "ticker": stock.get("ticker", ""),
                    "price": stock.get("price", ""),
                    "change_percent": stock.get("change_percent", ""),
                    "volume": stock.get("volume", ""),
                    "market_cap": stock.get("market_cap", "")
                })
        
        return {
            "status": "success",
            "category": category,
            "trending_stocks": trending_stocks,
            "total_trending": len(trending_stocks),
            "search_engine": "Google Finance"
        }
        
    except Exception as e:
        return {
            "status": "error",
            "error": f"Error getting market trends: {str(e)}",
            "category": category,
            "search_engine": "Google Finance"
        }

if __name__ == "__main__":
    # Test the API
    result = search_finance("moving companies transportation", 5)
    print(f"Finance Results: {result['total_news']} news articles, {result['total_stocks']} stocks")
    
    trends = get_market_trends("transportation")
    print(f"Market Trends: {trends['total_trending']} trending stocks")

