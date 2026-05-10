DROP TABLE IF EXISTS itinerary_items;
DROP TABLE IF EXISTS regions;
DROP TABLE IF EXISTS trips;
DROP TABLE IF EXISTS users;

CREATE TABLE users (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    public_id TEXT UNIQUE,
    first_name TEXT NOT NULL,
    last_name TEXT NOT NULL,
    email TEXT NOT NULL UNIQUE,
    phone_number TEXT,
    city TEXT,
    country TEXT,
    description TEXT,
    password_hash TEXT NOT NULL,
    photo_url TEXT,
    role TEXT NOT NULL DEFAULT 'user',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE trips (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_code TEXT NOT NULL UNIQUE,
    user_id INTEGER NOT NULL,
    trip_name TEXT NOT NULL,
    start_date DATE,
    end_date DATE,
    description TEXT,
    status TEXT NOT NULL DEFAULT 'draft',
    created_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (user_id) REFERENCES users (id) ON DELETE CASCADE
);

CREATE TABLE regions (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_id INTEGER NOT NULL,
    name TEXT NOT NULL,
    country TEXT,
    city TEXT,
    start_date DATE,
    end_date DATE,
    FOREIGN KEY (trip_id) REFERENCES trips (id) ON DELETE CASCADE
);

CREATE TABLE itinerary_items (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    trip_id INTEGER NOT NULL,
    region_id INTEGER,
    title TEXT NOT NULL,
    description TEXT,
    start_date DATE,
    end_date DATE,
    budget_amount NUMERIC,
    currency TEXT NOT NULL DEFAULT 'INR',
    FOREIGN KEY (trip_id) REFERENCES trips (id) ON DELETE CASCADE,
    FOREIGN KEY (region_id) REFERENCES regions (id) ON DELETE SET NULL
);
