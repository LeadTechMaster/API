-- Google Places & GMB Database Schema
-- Stores business listings, reviews, GMB data, and insights

-- Places/Businesses
CREATE TABLE IF NOT EXISTS places (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    place_id TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,
    address TEXT,
    latitude REAL,
    longitude REAL,
    phone TEXT,
    website TEXT,
    business_type TEXT,
    price_level INTEGER,
    rating REAL,
    user_ratings_total INTEGER,
    is_gmb_verified BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Business Hours
CREATE TABLE IF NOT EXISTS business_hours (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    place_id TEXT NOT NULL,
    day_of_week INTEGER,
    open_time TEXT,
    close_time TEXT,
    is_closed BOOLEAN DEFAULT 0,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (place_id) REFERENCES places(place_id)
);

-- Reviews
CREATE TABLE IF NOT EXISTS reviews (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    place_id TEXT NOT NULL,
    author_name TEXT,
    rating INTEGER,
    review_text TEXT,
    review_date TIMESTAMP,
    relative_time TEXT,
    response_text TEXT,
    response_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (place_id) REFERENCES places(place_id)
);

-- Photos
CREATE TABLE IF NOT EXISTS photos (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    place_id TEXT NOT NULL,
    photo_reference TEXT,
    photo_url TEXT,
    width INTEGER,
    height INTEGER,
    attribution TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (place_id) REFERENCES places(place_id)
);

-- GMB Insights
CREATE TABLE IF NOT EXISTS gmb_insights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id TEXT NOT NULL,
    place_id TEXT,
    date DATE NOT NULL,
    views_search INTEGER,
    views_maps INTEGER,
    actions_website INTEGER,
    actions_phone INTEGER,
    actions_driving_directions INTEGER,
    photos_count INTEGER,
    photos_views INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- GMB Posts
CREATE TABLE IF NOT EXISTS gmb_posts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id TEXT NOT NULL,
    post_id TEXT UNIQUE,
    post_type TEXT,
    title TEXT,
    content TEXT,
    media_url TEXT,
    cta_type TEXT,
    cta_url TEXT,
    start_date DATE,
    end_date DATE,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- GMB Questions & Answers
CREATE TABLE IF NOT EXISTS gmb_qa (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id TEXT NOT NULL,
    question_id TEXT UNIQUE,
    question_text TEXT,
    answer_text TEXT,
    asked_date TIMESTAMP,
    answered_date TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- GMB Attributes
CREATE TABLE IF NOT EXISTS gmb_attributes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    location_id TEXT NOT NULL,
    attribute_type TEXT,
    attribute_value TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Search History
CREATE TABLE IF NOT EXISTS place_searches (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    search_query TEXT NOT NULL,
    location_lat REAL,
    location_lng REAL,
    radius INTEGER,
    place_type TEXT,
    results_count INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for faster searches
CREATE INDEX IF NOT EXISTS idx_places_name ON places(name);
CREATE INDEX IF NOT EXISTS idx_places_location ON places(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_places_type ON places(business_type);
CREATE INDEX IF NOT EXISTS idx_reviews_place ON reviews(place_id);
CREATE INDEX IF NOT EXISTS idx_reviews_rating ON reviews(rating);
CREATE INDEX IF NOT EXISTS idx_gmb_insights_location ON gmb_insights(location_id, date);
CREATE INDEX IF NOT EXISTS idx_place_searches_query ON place_searches(search_query);

