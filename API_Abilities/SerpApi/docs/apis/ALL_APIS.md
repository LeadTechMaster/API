# SerpApi - Complete API Guide (Abilities, Endpoints, DB)

This guide documents all integrated APIs, what they do, example usage, backend endpoint, and where data is stored in the SQLite DB.

Notes
- All data is real from live APIs; caching window ~15 minutes unless `?refresh=true`.
- Each call is logged in `api_calls` with timestamps and response time.
- The HTML dashboard cards are noted per API.

Format
- Ability: name
- Endpoint: Flask route
- Example: request shape or query
- Returns: key fields
- DB Tables: where it is persisted
- Dashboard: where it appears

---

## Search & Rankings

1) Ability: Google Search
- Endpoint: `/api/google-search`
- Example: moving companies miami
- Returns: organic results, title/url/snippet, positions
- DB Tables: `api_calls`
- Dashboard: Overview (SERP snapshot)

2) Ability: Local Businesses (Google Maps)
- Endpoint: `/api/local-businesses`
- Example: q=moving companies, ll=@25.7617,-80.1918,15z, num=20
- Returns: business_name, rating, reviews_count, phone, address, latitude, longitude, hours, website
- DB Tables: `local_businesses`, `api_calls`
- Dashboard: 🏢 Top Movers, Map heatmap/clusters

3) Ability: SERP Analysis (features)
- Endpoint: `/api/serp-analysis`
- Example: moving companies miami
- Returns: features flags (ads, local pack, snippets, PAA, images, videos, shopping)
- DB Tables: `serp_features`, `api_calls`
- Dashboard: 📊 SERP Features Analysis

4) Ability: Keyword Difficulty
- Endpoint: `/api/keyword-difficulty`
- Example: moving companies miami
- Returns: difficulty_score (0-100), difficulty_level, serp_counts
- DB Tables: `keywords`, `api_calls`
- Dashboard: 🎯 Keyword Difficulty

5) Ability: Keyword Suggestions
- Endpoint: `/api/keyword-suggestions`
- Example: seed="moving companies"
- Returns: suggestions[], relevance
- DB Tables: `keyword_suggestions`, `api_calls`
- Dashboard: 💡 Keyword Suggestions

6) Ability: Related Searches
- Endpoint: `/api/related-searches`
- Example: moving companies miami
- Returns: related_searches[]
- DB Tables: `related_searches`, `api_calls`
- Dashboard: 🔗 Related Searches

7) Ability: People Also Ask
- Endpoint: `/api/people-also-ask`
- Example: moving companies miami FAQs
- Returns: questions[], answer preview, source
- DB Tables: `people_also_ask`, `api_calls`
- Dashboard: ❓ People Also Ask

---

## Volume, Trends & Geo

8) Ability: Search Trends (time series)
- Endpoint: `/api/search-trends`
- Example: keyword=moving companies miami
- Returns: points(date, interest), normalized 0-100
- DB Tables: `keyword_volume_history`, `api_calls`
- Dashboard: 📈 Volume & Trends (Chart)

9) Ability: Regional Interest
- Endpoint: `/api/regional-interest`
- Example: keyword=moving companies, type=GEO_MAP_0
- Returns: region, interest_value, rank
- DB Tables: `regional_interest`, `api_calls`
- Dashboard: 📈 Volume & Trends, Map heatmap composition

---

## Business Intelligence

10) Ability: Yelp Businesses
- Endpoint: `/api/yelp-businesses`
- Example: term=movers, location=Miami, FL
- Returns: business_name, rating, review_count, price_range, latitude, longitude, phone
- DB Tables: `yelp_businesses`, `api_calls`
- Dashboard: ⭐ Yelp Business Intelligence, Map heatmap composition

11) Ability: Local Pack Results
- Endpoint: `/api/local-pack`
- Example: city=Miami
- Returns: 3-pack businesses, positions, rating, review counts
- DB Tables: `local_pack_results`, `api_calls`
- Dashboard: Competitors view

---

## Content & Media

12) Ability: Image Search
- Endpoint: `/api/image-search`
- Example: moving companies miami branding
- Returns: title, thumbnail_url, image_url, source, position
- DB Tables: `images`, `api_calls`
- Dashboard: 🖼️ Visual Content

13) Ability: News Search
- Endpoint: `/api/news-search`
- Example: moving companies industry news 30d
- Returns: headline, source, date, link
- DB Tables: `news`, `api_calls`
- Dashboard: 📰 Industry News

14) Ability: YouTube Search
- Endpoint: `/api/youtube-search`
- Example: moving companies miami
- Returns: title, channel, views, published_at, url
- DB Tables: `youtube_videos`, `api_calls`
- Dashboard: Media, Marketing Analytics

---

## Jobs & Hiring

15) Ability: Google Jobs
- Endpoint: `/api/google-jobs`
- Example: movers miami
- Returns: title, company, location, salary, posted_at, url
- DB Tables: `jobs`, `api_calls`
- Dashboard: Competitors, Marketing Analytics

16) Ability: LinkedIn Jobs
- Endpoint: `/api/linkedin-jobs`
- Example: moving companies miami
- Returns: title, company, seniority, location, posted_at, url
- DB Tables: `linkedin_jobs`, `api_calls`
- Dashboard: Marketing Analytics

---

## E‑commerce & Pricing

17) Ability: Shopping Search (Google)
- Endpoint: `/api/shopping-search`
- Example: moving boxes
- Returns: product, price, retailer, link
- DB Tables: `shopping`, `api_calls`
- Dashboard: Marketing Analytics

18) Ability: Amazon Products
- Endpoint: `/api/amazon-products`
- Example: moving boxes
- Returns: product, price, rating, reviews, url
- DB Tables: `amazon_products`, `api_calls`
- Dashboard: Marketing Analytics

19) Ability: Walmart Products
- Endpoint: `/api/walmart-products`
- Example: moving boxes
- Returns: product, price, rating, reviews, url
- DB Tables: `walmart_products`, `api_calls`
- Dashboard: Marketing Analytics

---

## App Stores

20) Ability: Apple App Store
- Endpoint: `/api/apple-apps`
- Example: moving
- Returns: app_name, developer, rating, price, url
- DB Tables: `app_store_apple`, `api_calls`
- Dashboard: Marketing Analytics

21) Ability: Google Play Store
- Endpoint: `/api/google-play-apps`
- Example: moving
- Returns: app_name, developer, rating, installs, url
- DB Tables: `app_store_google`, `api_calls`
- Dashboard: Marketing Analytics

---

## Research & Finance

22) Ability: Google Scholar
- Endpoint: `/api/google-scholar`
- Example: logistics moving
- Returns: title, authors, year, citations, url
- DB Tables: `scholar_papers`, `api_calls`
- Dashboard: Marketing Analytics

23) Ability: Google Patents
- Endpoint: `/api/patents`
- Example: moving equipment
- Returns: title, assignee, year, abstract, url
- DB Tables: `patents`, `api_calls`
- Dashboard: Marketing Analytics

24) Ability: Google Finance
- Endpoint: `/api/google-finance`
- Example: transportation category
- Returns: news(title,source,date), trending stocks(name,ticker,price,change,volume)
- DB Tables: `finance_news`, `stocks`, `api_calls`
- Dashboard: Marketing Analytics

---

## Alternative Search

25) Ability: Bing Search
- Endpoint: `/api/bing-search`
- Example: moving companies miami
- Returns: organic results (title/url/snippet)
- DB Tables: `api_calls`
- Dashboard: Marketing Analytics

26) Ability: DuckDuckGo Search
- Endpoint: `/api/duckduckgo-search`
- Example: moving companies miami
- Returns: organic results, instant answers
- DB Tables: `api_calls`
- Dashboard: Marketing Analytics

---

## Aggregations & Map

27) Ability: Marketing Analytics (aggregation)
- Endpoint: `/api/marketing-analytics`
- Example: default aggregation over current dataset
- Returns: market_penetration, competitive_intelligence, content_strategy, pricing_intelligence, trend_analysis
- DB Tables: `analytics_snapshots`, `api_calls`
- Dashboard: 📊 Marketing Analytics

28) Ability: Miami Map (Mapbox/OSM)
- Endpoint: `/api/miami-map-data`
- Example: default
- Returns: business_locations(GeoJSON), rating_heatmap(points with intensities), competitor_clusters, market_density
- DB Tables: `local_businesses`, `yelp_businesses`, `keywords`, `regional_interest`
- Dashboard: 🗺️ Miami Map

---

## Freshness & Caching
- Each endpoint supports `?refresh=true` to bypass cache and call the external API.
- Responses include: `from_cache`, `age_minutes`, `response_time_ms`, `saved_to_db`.

