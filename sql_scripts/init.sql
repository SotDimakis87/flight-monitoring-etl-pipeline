CREATE TABLE IF NOT EXISTS flights (
    id SERIAL PRIMARY KEY,

    flight_date DATE,
    flight_status TEXT,

    airline_name TEXT,
    airline_iata TEXT,
    airline_icao TEXT,

    flight_number TEXT,
    flight_iata TEXT,
    flight_icao TEXT,

    departure_airport TEXT,
    departure_iata TEXT,
    departure_icao TEXT,
    departure_terminal TEXT,
    departure_gate TEXT,
    departure_delay INTEGER,
    scheduled_departure TIMESTAMP,
    estimated_departure TIMESTAMP,
    actual_departure TIMESTAMP,

    arrival_airport TEXT,
    arrival_iata TEXT,
    arrival_icao TEXT,
    scheduled_arrival TIMESTAMP,
    estimated_arrival TIMESTAMP,
    actual_arrival TIMESTAMP,

    etl_load_timestamp TIMESTAMP
);