-- US Census Database Schema
-- Stores population, demographic, economic, and housing data

-- Population Data
CREATE TABLE IF NOT EXISTS population (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    geography_type TEXT NOT NULL,
    location_code TEXT NOT NULL,
    location_name TEXT,
    total_population INTEGER,
    male_population INTEGER,
    female_population INTEGER,
    median_age REAL,
    year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(geography_type, location_code, year)
);

-- Demographic Data
CREATE TABLE IF NOT EXISTS demographics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    geography_type TEXT NOT NULL,
    location_code TEXT NOT NULL,
    location_name TEXT,
    white_percent REAL,
    black_percent REAL,
    asian_percent REAL,
    hispanic_percent REAL,
    other_percent REAL,
    year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(geography_type, location_code, year)
);

-- Economic Data
CREATE TABLE IF NOT EXISTS economic_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    geography_type TEXT NOT NULL,
    location_code TEXT NOT NULL,
    location_name TEXT,
    median_income REAL,
    per_capita_income REAL,
    unemployment_rate REAL,
    poverty_rate REAL,
    gini_index REAL,
    year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(geography_type, location_code, year)
);

-- Housing Data
CREATE TABLE IF NOT EXISTS housing (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    geography_type TEXT NOT NULL,
    location_code TEXT NOT NULL,
    location_name TEXT,
    total_housing_units INTEGER,
    occupied_units INTEGER,
    owner_occupied_percent REAL,
    renter_occupied_percent REAL,
    median_home_value REAL,
    median_rent REAL,
    year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(geography_type, location_code, year)
);

-- Education Data
CREATE TABLE IF NOT EXISTS education (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    geography_type TEXT NOT NULL,
    location_code TEXT NOT NULL,
    location_name TEXT,
    high_school_grad_percent REAL,
    bachelors_degree_percent REAL,
    graduate_degree_percent REAL,
    year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(geography_type, location_code, year)
);

-- Business Patterns
CREATE TABLE IF NOT EXISTS business_patterns (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    geography_type TEXT NOT NULL,
    location_code TEXT NOT NULL,
    location_name TEXT,
    industry_code TEXT,
    industry_name TEXT,
    num_establishments INTEGER,
    num_employees INTEGER,
    annual_payroll REAL,
    year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Commute Data
CREATE TABLE IF NOT EXISTS commute_data (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    geography_type TEXT NOT NULL,
    location_code TEXT NOT NULL,
    location_name TEXT,
    mean_commute_time REAL,
    drive_alone_percent REAL,
    carpool_percent REAL,
    public_transit_percent REAL,
    walk_percent REAL,
    work_from_home_percent REAL,
    year INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(geography_type, location_code, year)
);

-- Indexes for faster searches
CREATE INDEX IF NOT EXISTS idx_population_location ON population(geography_type, location_code);
CREATE INDEX IF NOT EXISTS idx_demographics_location ON demographics(geography_type, location_code);
CREATE INDEX IF NOT EXISTS idx_economic_location ON economic_data(geography_type, location_code);
CREATE INDEX IF NOT EXISTS idx_housing_location ON housing(geography_type, location_code);
CREATE INDEX IF NOT EXISTS idx_education_location ON education(geography_type, location_code);
CREATE INDEX IF NOT EXISTS idx_business_location ON business_patterns(geography_type, location_code);
CREATE INDEX IF NOT EXISTS idx_commute_location ON commute_data(geography_type, location_code);

