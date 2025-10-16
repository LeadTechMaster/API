-- SerpApi Database Schema
-- Stores keyword data, search results, and local business information

-- Keyword Research Data
CREATE TABLE IF NOT EXISTS keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    location TEXT,
    search_volume INTEGER,
    difficulty_score REAL,
    cpc REAL,
    competition TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(keyword, location)
);

-- Keyword Suggestions
CREATE TABLE IF NOT EXISTS keyword_suggestions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    seed_keyword TEXT NOT NULL,
    suggested_keyword TEXT NOT NULL,
    relevance_score REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- People Also Ask Questions
CREATE TABLE IF NOT EXISTS people_also_ask (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    question TEXT NOT NULL,
    answer TEXT,
    position INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Local Pack Results (3-pack)
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
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
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- SERP Features
CREATE TABLE IF NOT EXISTS serp_features (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    location TEXT,
    feature_type TEXT,
    feature_data TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Competitor Keywords
CREATE TABLE IF NOT EXISTS competitor_keywords (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    competitor_domain TEXT NOT NULL,
    keyword TEXT NOT NULL,
    position INTEGER,
    search_volume INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Related Searches
CREATE TABLE IF NOT EXISTS related_searches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    related_keyword TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Search Trends
CREATE TABLE IF NOT EXISTS search_trends (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    keyword TEXT NOT NULL,
    location TEXT,
    trend_date DATE,
    interest_score INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for faster searches
CREATE INDEX IF NOT EXISTS idx_keywords_keyword ON keywords(keyword);
CREATE INDEX IF NOT EXISTS idx_keywords_location ON keywords(location);
CREATE INDEX IF NOT EXISTS idx_local_pack_keyword ON local_pack(keyword, location);
CREATE INDEX IF NOT EXISTS idx_search_results_keyword ON search_results(keyword);
CREATE INDEX IF NOT EXISTS idx_competitor_domain ON competitor_keywords(competitor_domain);
CREATE INDEX IF NOT EXISTS idx_people_also_ask ON people_also_ask(keyword);

