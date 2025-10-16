-- Enhanced SerpApi Database Schema
-- Comprehensive storage for all API data with validation, tagging, and timestamps
-- Created: October 16, 2025
-- Purpose: Market Intelligence for Miami Moving Companies

-- ============================================================================
-- CORE TABLES
-- ============================================================================

-- API Call Logs (Track all API calls for validation and cost monitoring)
CREATE TABLE IF NOT EXISTS api_calls (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    api_endpoint TEXT NOT NULL,
    query TEXT NOT NULL,
    location TEXT,
    status TEXT NOT NULL, -- 'success' or 'error'
    response_time_ms INTEGER,
    api_credits_used INTEGER DEFAULT 1,
    error_message TEXT,
    raw_response TEXT, -- JSON blob
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    validated_at TIMESTAMP,
    is_valid BOOLEAN DEFAULT 1
);

-- Tags for organizing searches
CREATE TABLE IF NOT EXISTS tags (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tag_name TEXT UNIQUE NOT NULL,
    description TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Search Sessions (Group related searches together)
CREATE TABLE IF NOT EXISTS search_sessions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    session_name TEXT NOT NULL,
    industry TEXT, -- e.g., 'moving_companies'
    location TEXT, -- e.g., 'Miami, FL'
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    completed_at TIMESTAMP
);

-- ============================================================================
-- GOOGLE SEARCH DATA
-- ============================================================================

-- Keyword Research Data (Enhanced)
CREATE TABLE IF NOT EXISTS keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    location TEXT,
    search_volume INTEGER,
    difficulty_score REAL,
    difficulty_level TEXT, -- 'Easy', 'Medium', 'Hard'
    cpc REAL,
    competition TEXT,
    session_id INTEGER,
    api_call_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(keyword, location),
    FOREIGN KEY (session_id) REFERENCES search_sessions(id),
    FOREIGN KEY (api_call_id) REFERENCES api_calls(id)
);

-- Keyword Suggestions
CREATE TABLE IF NOT EXISTS keyword_suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seed_keyword TEXT NOT NULL,
    suggested_keyword TEXT NOT NULL,
    relevance_score REAL,
    session_id INTEGER,
    api_call_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES search_sessions(id),
    FOREIGN KEY (api_call_id) REFERENCES api_calls(id)
);

-- Autocomplete Suggestions
CREATE TABLE IF NOT EXISTS autocomplete_suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    partial_keyword TEXT NOT NULL,
    suggestion TEXT NOT NULL,
    relevance INTEGER,
    location TEXT,
    session_id INTEGER,
    api_call_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES search_sessions(id),
    FOREIGN KEY (api_call_id) REFERENCES api_calls(id)
);

-- People Also Ask Questions
CREATE TABLE IF NOT EXISTS people_also_ask (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT,
    source_title TEXT,
    source_link TEXT,
    position INTEGER,
    session_id INTEGER,
    api_call_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES search_sessions(id),
    FOREIGN KEY (api_call_id) REFERENCES api_calls(id)
);

-- Search Results (Organic)
CREATE TABLE IF NOT EXISTS search_results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    location TEXT,
    position INTEGER,
    title TEXT,
    link TEXT,
    snippet TEXT,
    domain TEXT,
    rating REAL,
    reviews_count INTEGER,
    session_id INTEGER,
    api_call_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES search_sessions(id),
    FOREIGN KEY (api_call_id) REFERENCES api_calls(id)
);

-- SERP Features
CREATE TABLE IF NOT EXISTS serp_features (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    location TEXT,
    has_ads BOOLEAN DEFAULT 0,
    num_ads INTEGER DEFAULT 0,
    has_featured_snippet BOOLEAN DEFAULT 0,
    has_knowledge_graph BOOLEAN DEFAULT 0,
    has_local_results BOOLEAN DEFAULT 0,
    has_images BOOLEAN DEFAULT 0,
    has_videos BOOLEAN DEFAULT 0,
    has_shopping BOOLEAN DEFAULT 0,
    has_people_also_ask BOOLEAN DEFAULT 0,
    has_related_searches BOOLEAN DEFAULT 0,
    organic_results_count INTEGER,
    session_id INTEGER,
    api_call_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES search_sessions(id),
    FOREIGN KEY (api_call_id) REFERENCES api_calls(id)
);

-- Related Searches
CREATE TABLE IF NOT EXISTS related_searches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    related_keyword TEXT NOT NULL,
    link TEXT,
    session_id INTEGER,
    api_call_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES search_sessions(id),
    FOREIGN KEY (api_call_id) REFERENCES api_calls(id)
);

-- ============================================================================
-- LOCAL BUSINESS DATA
-- ============================================================================

-- Local Businesses (Google Maps)
CREATE TABLE IF NOT EXISTS local_businesses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_name TEXT NOT NULL,
    place_id TEXT UNIQUE,
    address TEXT,
    phone TEXT,
    website TEXT,
    rating REAL,
    reviews_count INTEGER,
    latitude REAL,
    longitude REAL,
    hours TEXT, -- JSON or text format
    type TEXT, -- e.g., 'Mover'
    types TEXT, -- JSON array of all types
    price_range TEXT,
    service_options TEXT, -- JSON
    query TEXT, -- What search found this
    location TEXT, -- Search location
    position INTEGER,
    session_id INTEGER,
    api_call_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES search_sessions(id),
    FOREIGN KEY (api_call_id) REFERENCES api_calls(id)
);

-- Local Pack Results (3-pack from regular search)
CREATE TABLE IF NOT EXISTS local_pack (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    location TEXT NOT NULL,
    business_name TEXT,
    address TEXT,
    phone TEXT,
    rating REAL,
    reviews_count INTEGER,
    position INTEGER,
    place_id TEXT,
    gps_latitude REAL,
    gps_longitude REAL,
    hours TEXT,
    session_id INTEGER,
    api_call_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES search_sessions(id),
    FOREIGN KEY (api_call_id) REFERENCES api_calls(id)
);

-- ============================================================================
-- MEDIA & CONTENT
-- ============================================================================

-- Images
CREATE TABLE IF NOT EXISTS images (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,
    title TEXT,
    link TEXT,
    original_url TEXT,
    thumbnail_url TEXT,
    source TEXT,
    source_link TEXT,
    position INTEGER,
    session_id INTEGER,
    api_call_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES search_sessions(id),
    FOREIGN KEY (api_call_id) REFERENCES api_calls(id)
);

-- News Articles
CREATE TABLE IF NOT EXISTS news_articles (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,
    title TEXT NOT NULL,
    link TEXT,
    source TEXT,
    published_date TEXT,
    snippet TEXT,
    thumbnail_url TEXT,
    position INTEGER,
    session_id INTEGER,
    api_call_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES search_sessions(id),
    FOREIGN KEY (api_call_id) REFERENCES api_calls(id)
);

-- Shopping Products
CREATE TABLE IF NOT EXISTS shopping_products (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,
    title TEXT NOT NULL,
    link TEXT,
    product_link TEXT,
    product_id TEXT,
    source TEXT,
    price TEXT,
    extracted_price REAL,
    rating REAL,
    reviews_count INTEGER,
    thumbnail_url TEXT,
    delivery_info TEXT,
    position INTEGER,
    session_id INTEGER,
    api_call_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES search_sessions(id),
    FOREIGN KEY (api_call_id) REFERENCES api_calls(id)
);

-- ============================================================================
-- NEW APIS - YELP, YOUTUBE, JOBS
-- ============================================================================

-- Yelp Reviews
CREATE TABLE IF NOT EXISTS yelp_reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_name TEXT NOT NULL,
    yelp_id TEXT,
    yelp_url TEXT,
    rating REAL,
    reviews_count INTEGER,
    price_range TEXT,
    categories TEXT, -- JSON array
    address TEXT,
    phone TEXT,
    website TEXT,
    latitude REAL,
    longitude REAL,
    hours TEXT, -- JSON
    is_claimed BOOLEAN,
    is_closed BOOLEAN,
    query TEXT,
    location TEXT,
    position INTEGER,
    session_id INTEGER,
    api_call_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES search_sessions(id),
    FOREIGN KEY (api_call_id) REFERENCES api_calls(id)
);

-- Individual Yelp Review Details
CREATE TABLE IF NOT EXISTS yelp_review_details (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_id INTEGER,
    reviewer_name TEXT,
    rating REAL,
    review_text TEXT,
    review_date TEXT,
    helpful_count INTEGER,
    session_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (business_id) REFERENCES yelp_reviews(id),
    FOREIGN KEY (session_id) REFERENCES search_sessions(id)
);

-- YouTube Videos
CREATE TABLE IF NOT EXISTS youtube_videos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,
    video_id TEXT UNIQUE,
    title TEXT NOT NULL,
    channel_name TEXT,
    channel_id TEXT,
    video_url TEXT,
    thumbnail_url TEXT,
    description TEXT,
    view_count INTEGER,
    like_count INTEGER,
    comment_count INTEGER,
    duration TEXT,
    published_date TEXT,
    position INTEGER,
    session_id INTEGER,
    api_call_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES search_sessions(id),
    FOREIGN KEY (api_call_id) REFERENCES api_calls(id)
);

-- Google Jobs
CREATE TABLE IF NOT EXISTS job_listings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    query TEXT NOT NULL,
    location TEXT,
    job_title TEXT NOT NULL,
    company_name TEXT,
    company_url TEXT,
    job_url TEXT,
    description TEXT,
    salary TEXT,
    salary_min REAL,
    salary_max REAL,
    salary_period TEXT, -- hourly, weekly, monthly, yearly
    job_type TEXT, -- full-time, part-time, contract
    posted_date TEXT,
    is_remote BOOLEAN DEFAULT 0,
    position INTEGER,
    session_id INTEGER,
    api_call_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES search_sessions(id),
    FOREIGN KEY (api_call_id) REFERENCES api_calls(id)
);

-- ============================================================================
-- COMPETITIVE INTELLIGENCE
-- ============================================================================

-- Competitor Domains
CREATE TABLE IF NOT EXISTS competitors (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    domain TEXT UNIQUE NOT NULL,
    company_name TEXT,
    industry TEXT,
    location TEXT,
    is_active BOOLEAN DEFAULT 1,
    notes TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Competitor Keywords
CREATE TABLE IF NOT EXISTS competitor_keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    competitor_id INTEGER,
    competitor_domain TEXT NOT NULL,
    keyword TEXT NOT NULL,
    position INTEGER,
    search_volume INTEGER,
    url TEXT,
    title TEXT,
    snippet TEXT,
    session_id INTEGER,
    api_call_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (competitor_id) REFERENCES competitors(id),
    FOREIGN KEY (session_id) REFERENCES search_sessions(id),
    FOREIGN KEY (api_call_id) REFERENCES api_calls(id)
);

-- Search Trends (Time Series)
CREATE TABLE IF NOT EXISTS search_trends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    location TEXT,
    trend_date DATE,
    interest_score INTEGER,
    rising_queries TEXT, -- JSON
    top_queries TEXT, -- JSON
    session_id INTEGER,
    api_call_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES search_sessions(id),
    FOREIGN KEY (api_call_id) REFERENCES api_calls(id)
);

-- Keyword Volume History (Detailed Time Series)
CREATE TABLE IF NOT EXISTS keyword_volume_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    location TEXT NOT NULL,
    date_range TEXT NOT NULL, -- e.g., "today 1-m", "today 3-m"
    timeline_date TEXT, -- Specific date from timeline
    interest_value INTEGER,
    avg_interest REAL,
    max_interest INTEGER,
    min_interest INTEGER,
    trend_direction TEXT, -- 'rising', 'falling', 'stable'
    volatility REAL,
    session_id INTEGER,
    api_call_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES search_sessions(id),
    FOREIGN KEY (api_call_id) REFERENCES api_calls(id)
);

-- Regional Interest (Geographic Distribution)
CREATE TABLE IF NOT EXISTS regional_interest (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    country TEXT NOT NULL,
    region TEXT NOT NULL, -- State, province, or city
    interest_value INTEGER,
    rank INTEGER,
    session_id INTEGER,
    api_call_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES search_sessions(id),
    FOREIGN KEY (api_call_id) REFERENCES api_calls(id)
);

-- Keyword Metrics Over Time (Aggregated Statistics)
CREATE TABLE IF NOT EXISTS keyword_metrics_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    location TEXT,
    date_measured DATE NOT NULL,
    search_volume INTEGER,
    difficulty_score REAL,
    cpc REAL,
    competition_level TEXT,
    num_ads INTEGER,
    num_organic_results INTEGER,
    has_local_pack BOOLEAN,
    avg_position REAL,
    session_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(keyword, location, date_measured),
    FOREIGN KEY (session_id) REFERENCES search_sessions(id)
);

-- ============================================================================
-- DATA VALIDATION & QUALITY
-- ============================================================================

-- Data Quality Checks
CREATE TABLE IF NOT EXISTS data_validation (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    table_name TEXT NOT NULL,
    record_id INTEGER NOT NULL,
    validation_type TEXT NOT NULL, -- 'completeness', 'accuracy', 'freshness'
    is_valid BOOLEAN NOT NULL,
    validation_message TEXT,
    validated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Market Intelligence Summaries
CREATE TABLE IF NOT EXISTS market_summaries (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    industry TEXT NOT NULL,
    location TEXT NOT NULL,
    summary_date DATE NOT NULL,
    total_competitors INTEGER,
    avg_rating REAL,
    total_reviews INTEGER,
    keyword_opportunities INTEGER,
    market_difficulty_score REAL,
    top_keywords TEXT, -- JSON
    summary_data TEXT, -- JSON blob with all insights
    session_id INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (session_id) REFERENCES search_sessions(id)
);

-- ============================================================================
-- INDEXES FOR PERFORMANCE
-- ============================================================================

-- Core indexes
CREATE INDEX IF NOT EXISTS idx_api_calls_endpoint ON api_calls(api_endpoint, created_at);
CREATE INDEX IF NOT EXISTS idx_api_calls_query ON api_calls(query, location);
CREATE INDEX IF NOT EXISTS idx_api_calls_status ON api_calls(status);

-- Keyword indexes
CREATE INDEX IF NOT EXISTS idx_keywords_keyword ON keywords(keyword);
CREATE INDEX IF NOT EXISTS idx_keywords_location ON keywords(location);
CREATE INDEX IF NOT EXISTS idx_keywords_difficulty ON keywords(difficulty_score);
CREATE INDEX IF NOT EXISTS idx_keywords_session ON keywords(session_id);

-- Business indexes
CREATE INDEX IF NOT EXISTS idx_local_businesses_place ON local_businesses(place_id);
CREATE INDEX IF NOT EXISTS idx_local_businesses_name ON local_businesses(business_name);
CREATE INDEX IF NOT EXISTS idx_local_businesses_rating ON local_businesses(rating);
CREATE INDEX IF NOT EXISTS idx_local_pack_keyword ON local_pack(keyword, location);

-- Search results indexes
CREATE INDEX IF NOT EXISTS idx_search_results_keyword ON search_results(keyword);
CREATE INDEX IF NOT EXISTS idx_search_results_position ON search_results(position);
CREATE INDEX IF NOT EXISTS idx_search_results_domain ON search_results(domain);

-- Media indexes
CREATE INDEX IF NOT EXISTS idx_images_query ON images(query);
CREATE INDEX IF NOT EXISTS idx_news_query ON news_articles(query);
CREATE INDEX IF NOT EXISTS idx_shopping_query ON shopping_products(query);

-- New API indexes
CREATE INDEX IF NOT EXISTS idx_yelp_business ON yelp_reviews(business_name, location);
CREATE INDEX IF NOT EXISTS idx_youtube_query ON youtube_videos(query);
CREATE INDEX IF NOT EXISTS idx_jobs_query ON job_listings(query, location);

-- Competitor indexes
CREATE INDEX IF NOT EXISTS idx_competitors_domain ON competitors(domain);
CREATE INDEX IF NOT EXISTS idx_competitor_keywords_domain ON competitor_keywords(competitor_domain);
CREATE INDEX IF NOT EXISTS idx_people_also_ask ON people_also_ask(keyword);

-- Session indexes
CREATE INDEX IF NOT EXISTS idx_sessions_industry ON search_sessions(industry, location);
CREATE INDEX IF NOT EXISTS idx_sessions_created ON search_sessions(created_at);

-- ============================================================================
-- VIEWS FOR EASY QUERYING
-- ============================================================================

-- Comprehensive competitor view
CREATE VIEW IF NOT EXISTS v_competitor_overview AS
SELECT 
    c.domain,
    c.company_name,
    COUNT(DISTINCT ck.keyword) as total_keywords,
    AVG(ck.position) as avg_position,
    COUNT(DISTINCT lb.id) as local_listings,
    AVG(lb.rating) as avg_rating,
    SUM(lb.reviews_count) as total_reviews
FROM competitors c
LEFT JOIN competitor_keywords ck ON c.id = ck.competitor_id
LEFT JOIN local_businesses lb ON c.domain LIKE '%' || REPLACE(lb.website, 'http://', '') || '%'
GROUP BY c.id, c.domain, c.company_name;

-- Keyword opportunity view
CREATE VIEW IF NOT EXISTS v_keyword_opportunities AS
SELECT 
    k.keyword,
    k.location,
    k.difficulty_score,
    k.difficulty_level,
    k.search_volume,
    COUNT(DISTINCT sr.id) as current_ranking_urls,
    AVG(sr.position) as avg_position,
    k.created_at as last_checked
FROM keywords k
LEFT JOIN search_results sr ON k.keyword = sr.keyword
WHERE k.difficulty_level IN ('Easy', 'Medium')
GROUP BY k.id, k.keyword
ORDER BY k.difficulty_score ASC, k.search_volume DESC;

-- Market summary view
CREATE VIEW IF NOT EXISTS v_market_snapshot AS
SELECT 
    'Miami Moving Companies' as market_name,
    COUNT(DISTINCT lb.business_name) as total_businesses,
    AVG(lb.rating) as avg_rating,
    SUM(lb.reviews_count) as total_reviews,
    COUNT(DISTINCT k.keyword) as keywords_tracked,
    AVG(k.difficulty_score) as avg_difficulty,
    COUNT(DISTINCT n.id) as news_articles,
    MAX(api_calls.created_at) as last_updated
FROM local_businesses lb
CROSS JOIN keywords k
CROSS JOIN news_articles n
CROSS JOIN api_calls
WHERE api_calls.status = 'success';

-- ============================================================================
-- INITIAL DATA
-- ============================================================================

-- Insert default tags
INSERT OR IGNORE INTO tags (tag_name, description) VALUES
    ('moving_companies', 'Moving and relocation services'),
    ('miami', 'Miami, Florida market'),
    ('local_seo', 'Local SEO research'),
    ('competitor_analysis', 'Competitive intelligence'),
    ('keyword_research', 'Keyword and content research'),
    ('market_research', 'General market research');

-- Insert Miami Moving Companies session
INSERT OR IGNORE INTO search_sessions (session_name, industry, location) VALUES
    ('Miami Moving Companies - Initial Research', 'moving_companies', 'Miami, FL');


