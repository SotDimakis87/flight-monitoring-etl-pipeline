CREATE TABLE IF NOT EXISTS flights (
    id SERIAL PRIMARY KEY,

    flight_date DATE,
    flight_status TEXT,

    airline_name TEXT,
    airline_iata CHAR(2),
    airline_icao CHAR(3),

    flight_number TEXT,
    flight_iata TEXT,
    flight_icao TEXT,

    departure_airport TEXT,
    departure_iata CHAR(3),
    departure_icao CHAR(4),
    departure_terminal TEXT,
    departure_gate TEXT,
    departure_delay INTEGER,
    scheduled_departure TIMESTAMPTZ,
    estimated_departure TIMESTAMPTZ,
    actual_departure TIMESTAMPTZ,

    arrival_airport TEXT,
    arrival_iata CHAR(3),
    arrival_icao CHAR(4),
    scheduled_arrival TIMESTAMPTZ,
    estimated_arrival TIMESTAMPTZ,
    actual_arrival TIMESTAMPTZ,

    etl_load_timestamp TIMESTAMPTZ
);