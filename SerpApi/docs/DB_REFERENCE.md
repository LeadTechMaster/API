# SQLite Database Reference (SerpApi)

Location: `API_Abilities/SerpApi/DB/serpapi_data.db`
Schema: `API_Abilities/SerpApi/DB/enhanced_schema.sql`
Manager: `API_Abilities/SerpApi/DB/db_manager.py`

## Conventions
- All API calls logged in `api_calls` (status, response_time_ms, created_at, raw_response)
- Domain data saved in normalized tables with timestamps
- Most tables link to `api_calls.id` and optionally `search_sessions.id`

## Core Tables
- `api_calls`
  - id, api_endpoint, query, location, status, response_time_ms, api_credits_used, error_message, raw_response, created_at
- `search_sessions`
  - id, session_name, industry, location, created_at
- `tags`
  - tag_name, description

## Search & Rankings
- `keywords` (difficulty stored here)
  - keyword, location, search_volume, difficulty_score, difficulty_level, cpc, competition
- `keyword_suggestions`
  - seed_keyword, suggested_keyword, relevance_score
- `autocomplete_suggestions`
  - partial_keyword, suggestion, relevance
- `related_searches`
  - seed keyword implied, suggestion
- `people_also_ask`
  - keyword, question, answer, source_title
- `serp_features`
  - query, ads, local_pack, snippets, knowledge_graph, images, videos, shopping, paa

## Businesses
- `local_businesses`
  - business_name, rating, reviews_count, phone, address, latitude, longitude, hours, website, source='google_maps'
- `yelp_businesses`
  - business_name, rating, review_count, price_range, latitude, longitude, phone, url
- `local_pack_results`
  - business_name, position, rating, reviews_count

## Media & News
- `images`
  - title, thumbnail_url, image_url, source, position
- `news`
  - published_at, title, source, url
- `youtube_videos`
  - title, channel, views, url, published_at

## Jobs
- `jobs`
  - title, company, location, salary_text, posted_at, url
- `linkedin_jobs`
  - title, company, seniority, location, posted_at, url

## Trends & Geo
- `keyword_volume_history`
  - keyword, date, interest
- `regional_interest`
  - region, interest_value, rank

## E‑commerce
- `shopping`
  - product, price, retailer, url
- `amazon_products`
  - product, price, rating, reviews, url
- `walmart_products`
  - product, price, rating, reviews, url

## Apps
- `app_store_apple`
  - app_name, developer, rating, price, url
- `app_store_google`
  - app_name, developer, rating, installs, url

## Research & Finance
- `scholar_papers`
  - title, authors, year, citations, url
- `patents`
  - title, assignee, year, abstract, url
- `finance_news`
  - title, source, date, url
- `stocks`
  - name, ticker, price, change_percent, volume

## Aggregations
- `analytics_snapshots`
  - snapshot_type, payload_json, created_at

## Relationships (high-level)
- Many tables include `api_call_id` → `api_calls.id` (traceability)
- Optional `session_id` → `search_sessions.id` for grouped runs
- Heatmap uses: `local_businesses`, `yelp_businesses`, `keywords`, `regional_interest`

## Freshness & Caching
- `api_calls.created_at` gives last fetch time
- API responses carry `from_cache`, `age_minutes`, `response_time_ms`, `saved_to_db`

