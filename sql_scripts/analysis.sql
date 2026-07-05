--Total number of records
SELECT COUNT(*) AS total_records
FROM flights;

--Number of records per ETL execution
SELECT etl_load_timestamp,
        COUNT(*) AS records_loaded
FROM flights
GROUP BY etl_load_timestamp
ORDER BY etl_load_timestamp DESC;

--Flights by flight status
SELECT flight_status,
        COUNT(*) AS total_flights
FROM flights
GROUP BY flight_status
ORDER BY total_flights DESC;

--Flights by airline
SELECT airline_iata,
        airline_icao,
        airline_name,
        COUNT(*) AS total_flights
FROM flights
GROUP BY airline_name, airline_iata, airline_icao
ORDER BY total_flights DESC;

--Top 10 destinations from ATH
SELECT arrival_iata,
        arrival_airport,
        COUNT(*) AS total_flights
FROM flights
GROUP BY arrival_iata, arrival_airport
ORDER BY total_flights DESC
LIMIT 10;

--Scheduled departures by hour (UTC)
SELECT EXTRACT(HOUR FROM scheduled_departure AT TIME ZONE 'UTC') AS scheduled_departure_hour_utc,
        COUNT(*) AS total_flights
FROM flights
WHERE scheduled_departure IS NOT NULL
GROUP BY scheduled_departure_hour_utc
ORDER BY total_flights desc;

--Scheduled departures by hour (Athens local time)
SELECT EXTRACT(HOUR FROM scheduled_departure AT TIME ZONE 'Europe/Athens') AS scheduled_departure_hour_local,
        COUNT(*) AS total_flights
FROM flights
WHERE scheduled_departure IS NOT NULL
GROUP BY scheduled_departure_hour_local
ORDER BY total_flights desc;




-- ================================================================================================================================
-- Delay Analysis Queries
-- These queries are useful when the dataset contains active or landed flights with populated actual_departure or departure_delay.
-- With the free-tier data, these may return few or no rows.
-- ================================================================================================================================

--Check delay data availability
SELECT COUNT(*) AS total_records,
        COUNT(departure_delay) AS records_with_delay,
        ROUND(COUNT(departure_delay)::NUMERIC / NULLIF(COUNT(*), 0) * 100, 2) AS delay_data_availability_pct
FROM flights;


--Average departure delay by airline
SELECT airline_iata,
        airline_icao,
        airline_name,
        ROUND(AVG(departure_delay), 2) AS avg_departure_delay_minutes,
        COUNT(*) AS delayed_records
FROM flights
WHERE departure_delay IS NOT NULL
GROUP BY airline_name, airline_iata, airline_icao
ORDER BY avg_departure_delay_minutes DESC;


--Flights delayed more than 15 minutes
SELECT flight_date,
        airline_name,
        flight_iata,
        flight_icao,
        departure_iata,
        arrival_iata,
        scheduled_departure,
        actual_departure,
        departure_delay
FROM flights
WHERE departure_delay > 15
ORDER BY departure_delay DESC;


--Delay distribution by destination
SELECT arrival_iata,
        arrival_airport,
        COUNT(*) AS records_with_delay,
        ROUND(AVG(departure_delay), 2) AS avg_departure_delay_minutes,
        MAX(departure_delay) AS max_departure_delay_minutes
FROM flights
WHERE departure_delay IS NOT NULL
GROUP BY arrival_iata, arrival_airport
ORDER BY avg_departure_delay_minutes DESC;
