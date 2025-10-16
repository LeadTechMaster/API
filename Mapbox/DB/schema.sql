-- Mapbox Database Schema
-- Stores geocoding, routing, and map data

-- Geocoding Results
CREATE TABLE IF NOT EXISTS geocoding_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    address TEXT NOT NULL,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    place_name TEXT,
    place_type TEXT,
    confidence REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(address)
);

-- Reverse Geocoding Results
CREATE TABLE IF NOT EXISTS reverse_geocoding_cache (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    latitude REAL NOT NULL,
    longitude REAL NOT NULL,
    address TEXT NOT NULL,
    place_name TEXT,
    place_type TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    UNIQUE(latitude, longitude)
);

-- Routing Data
CREATE TABLE IF NOT EXISTS routes (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    origin_lat REAL NOT NULL,
    origin_lng REAL NOT NULL,
    dest_lat REAL NOT NULL,
    dest_lng REAL NOT NULL,
    profile TEXT NOT NULL,
    distance_meters REAL,
    duration_seconds REAL,
    geometry TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Isochrone Data
CREATE TABLE IF NOT EXISTS isochrones (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    center_lat REAL NOT NULL,
    center_lng REAL NOT NULL,
    minutes INTEGER NOT NULL,
    profile TEXT NOT NULL,
    geometry TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Distance Matrix
CREATE TABLE IF NOT EXISTS distance_matrix (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    origin_coords TEXT NOT NULL,
    destination_coords TEXT NOT NULL,
    distance_meters REAL,
    duration_seconds REAL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Indexes for faster searches
CREATE INDEX IF NOT EXISTS idx_geocoding_address ON geocoding_cache(address);
CREATE INDEX IF NOT EXISTS idx_reverse_coords ON reverse_geocoding_cache(latitude, longitude);
CREATE INDEX IF NOT EXISTS idx_routes_origin ON routes(origin_lat, origin_lng);
CREATE INDEX IF NOT EXISTS idx_isochrones_center ON isochrones(center_lat, center_lng);

