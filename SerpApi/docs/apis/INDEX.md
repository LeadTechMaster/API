# SerpApi APIs - Complete Index

This document lists every API integrated, its purpose, example query, backend endpoint, database tables, and the HTML card where it appears in `html/dashboard.html`.

> All data is real; responses are persisted to SQLite with timestamps and validation.

## Legend
- Endpoint: Flask route under `api_server.py`
- Tables: SQLite tables in `DB/enhanced_schema.sql`
- Card: Section title in the dashboard

---

## Core Search & Intelligence
- Google Search
  - Endpoint: `/api/google-search`
  - Tables: `api_calls`
  - Card: 📊 SERP Features Analysis / 🎯 Market Snapshot
- Local Businesses (Google Maps)
  - Endpoint: `/api/local-businesses`
  - Tables: `local_businesses`, `api_calls`
  - Card: 🏢 Top 20 Movers
- Keyword Difficulty
  - Endpoint: `/api/keyword-difficulty`
  - Tables: `keywords`, `api_calls`
  - Card: 🎯 Keyword Difficulty
- SERP Analysis (features)
  - Endpoint: `/api/serp-analysis`
  - Tables: `serp_features`, `api_calls`
  - Card: 📊 SERP Features Analysis
- Keyword Suggestions
  - Endpoint: `/api/keyword-suggestions`
  - Tables: `keyword_suggestions`, `api_calls`
  - Card: 💡 Keyword Suggestions
- Related Searches
  - Endpoint: `/api/related-searches`
  - Tables: `related_searches`, `api_calls`
  - Card: 🔗 Related Searches
- People Also Ask
  - Endpoint: `/api/people-also-ask`
  - Tables: `people_also_ask`, `api_calls`
  - Card: ❓ People Also Ask

## Content & Media
- Image Search
  - Endpoint: `/api/image-search`
  - Tables: `images`, `api_calls`
  - Card: 🖼️ Visual Content
- News Search
  - Endpoint: `/api/news-search`
  - Tables: `news`, `api_calls`
  - Card: 📰 Industry News
- YouTube Search
  - Endpoint: `/api/youtube-search`
  - Tables: `youtube_videos`, `api_calls`
  - Card: Appears in Media and Marketing Analytics views

## Business Intelligence
- Yelp Businesses
  - Endpoint: `/api/yelp-businesses`
  - Tables: `yelp_businesses`, `api_calls`
  - Card: ⭐ Yelp Business Intelligence
- Local Pack Results
  - Endpoint: `/api/local-pack`
  - Tables: `local_pack_results`, `api_calls`
  - Card: Competitors view

## Jobs & Hiring
- Google Jobs
  - Endpoint: `/api/google-jobs`
  - Tables: `jobs`, `api_calls`
  - Card: Competitors / Marketing Analytics
- LinkedIn Jobs
  - Endpoint: `/api/linkedin-jobs`
  - Tables: `linkedin_jobs`, `api_calls`
  - Card: Marketing Analytics

## Trends & Volumes
- Search Trends
  - Endpoint: `/api/search-trends`
  - Tables: `keyword_volume_history`, `api_calls`
  - Card: 📈 Volume & Trends
- Regional Interest
  - Endpoint: `/api/regional-interest`
  - Tables: `regional_interest`, `api_calls`
  - Card: 📈 Volume & Trends

## E‑commerce & Products
- Google Shopping
  - Endpoint: `/api/shopping-search`
  - Tables: `shopping`, `api_calls`
  - Card: Competitors / Marketing Analytics
- Amazon Products
  - Endpoint: `/api/amazon-products`
  - Tables: `amazon_products`, `api_calls`
  - Card: Marketing Analytics
- Walmart Products
  - Endpoint: `/api/walmart-products`
  - Tables: `walmart_products`, `api_calls`
  - Card: Marketing Analytics

## Apps & Stores
- Apple App Store
  - Endpoint: `/api/apple-apps`
  - Tables: `app_store_apple`, `api_calls`
  - Card: Marketing Analytics
- Google Play Store
  - Endpoint: `/api/google-play-apps`
  - Tables: `app_store_google`, `api_calls`
  - Card: Marketing Analytics

## Research & Finance
- Google Scholar
  - Endpoint: `/api/google-scholar`
  - Tables: `scholar_papers`, `api_calls`
  - Card: Marketing Analytics
- Google Patents
  - Endpoint: `/api/patents`
  - Tables: `patents`, `api_calls`
  - Card: Marketing Analytics
- Google Finance
  - Endpoint: `/api/google-finance`
  - Tables: `finance_news`, `stocks`, `api_calls`
  - Card: Marketing Analytics

## Alternative Search
- Bing Search
  - Endpoint: `/api/bing-search`
  - Tables: `api_calls`
  - Card: Marketing Analytics
- DuckDuckGo Search
  - Endpoint: `/api/duckduckgo-search`
  - Tables: `api_calls`
  - Card: Marketing Analytics

## Aggregations & Maps
- Marketing Analytics (aggregation)
  - Endpoint: `/api/marketing-analytics`
  - Tables: `analytics_snapshots`, `api_calls`
  - Card: 📊 Marketing Analytics
- Miami Map (Mapbox/OpenStreetMap)
  - Endpoint: `/api/miami-map-data`
  - Tables: `local_businesses`, `yelp_businesses`, `keywords`, `regional_interest`
  - Card: 🗺️ Miami Map

---

## How the Dashboard Gets Data
1. Frontend calls Flask `/api/*` endpoints.
2. Each endpoint uses `smart_api_call` (caching, validation) or specialized handlers.
3. Results are saved to SQLite with timestamps (`api_calls`) and domain tables.
4. Dashboard shows freshness badges (cached vs fresh) and response times.

