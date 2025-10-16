-- Brightlocal Database Schema
-- Stores local SEO data, citations, rankings, and reputation data

-- Business Listings
CREATE TABLE IF NOT EXISTS businesses (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_name TEXT NOT NULL,
    address TEXT,
    city TEXT,
    state TEXT,
    zip TEXT,
    phone TEXT,
    website TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Local Rankings
CREATE TABLE IF NOT EXISTS local_rankings (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_id INTEGER NOT NULL,
    keyword TEXT NOT NULL,
    location TEXT NOT NULL,
    rank_position INTEGER,
    search_engine TEXT DEFAULT 'Google',
    date DATE NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (business_id) REFERENCES businesses(id)
);

-- Keyword Rank History
CREATE TABLE IF NOT EXISTS rank_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_id INTEGER NOT NULL,
    keyword TEXT NOT NULL,
    location TEXT NOT NULL,
    date DATE NOT NULL,
    position INTEGER,
    previous_position INTEGER,
    change_value INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (business_id) REFERENCES businesses(id)
);

-- Citations
CREATE TABLE IF NOT EXISTS citations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_id INTEGER NOT NULL,
    directory_name TEXT NOT NULL,
    directory_url TEXT,
    listing_url TEXT,
    is_verified BOOLEAN DEFAULT 0,
    is_claimed BOOLEAN DEFAULT 0,
    nap_accuracy_score REAL,
    last_checked TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (business_id) REFERENCES businesses(id)
);

-- Reviews Aggregated
CREATE TABLE IF NOT EXISTS review_analytics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_id INTEGER NOT NULL,
    source TEXT NOT NULL,
    total_reviews INTEGER,
    average_rating REAL,
    five_star_count INTEGER,
    four_star_count INTEGER,
    three_star_count INTEGER,
    two_star_count INTEGER,
    one_star_count INTEGER,
    date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (business_id) REFERENCES businesses(id)
);

-- SEO Audit Results
CREATE TABLE IF NOT EXISTS seo_audits (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_id INTEGER NOT NULL,
    audit_date DATE NOT NULL,
    overall_score REAL,
    on_page_score REAL,
    citations_score REAL,
    reviews_score REAL,
    social_score REAL,
    issues_found TEXT,
    recommendations TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (business_id) REFERENCES businesses(id)
);

-- Competitor Analysis
CREATE TABLE IF NOT EXISTS competitor_analysis (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_id INTEGER NOT NULL,
    competitor_name TEXT NOT NULL,
    competitor_website TEXT,
    visibility_score REAL,
    citations_count INTEGER,
    avg_ranking REAL,
    reviews_count INTEGER,
    avg_rating REAL,
    analysis_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (business_id) REFERENCES businesses(id)
);

-- Reputation Score
CREATE TABLE IF NOT EXISTS reputation_scores (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_id INTEGER NOT NULL,
    date DATE NOT NULL,
    overall_score REAL,
    google_score REAL,
    facebook_score REAL,
    yelp_score REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (business_id) REFERENCES businesses(id)
);

-- Directory Presence
CREATE TABLE IF NOT EXISTS directory_scan (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    business_id INTEGER NOT NULL,
    scan_date DATE NOT NULL,
    total_directories_checked INTEGER,
    listings_found INTEGER,
    listings_verified INTEGER,
    missing_listings INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (business_id) REFERENCES businesses(id)
);

-- Indexes for faster searches
CREATE INDEX IF NOT EXISTS idx_businesses_name ON businesses(business_name);
CREATE INDEX IF NOT EXISTS idx_rankings_business ON local_rankings(business_id, keyword);
CREATE INDEX IF NOT EXISTS idx_rankings_date ON local_rankings(date);
CREATE INDEX IF NOT EXISTS idx_citations_business ON citations(business_id);
CREATE INDEX IF NOT EXISTS idx_reviews_business ON review_analytics(business_id);
CREATE INDEX IF NOT EXISTS idx_competitors ON competitor_analysis(business_id);

