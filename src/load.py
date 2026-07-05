import os
import psycopg2
import pandas as pd
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(
        host=os.getenv("POSTGRES_HOST"),
        database=os.getenv("POSTGRES_DB"),
        user=os.getenv("POSTGRES_USER"),
        password=os.getenv("POSTGRES_PASSWORD"),
        port=os.getenv("POSTGRES_PORT", 5432),
    )


def load_data(df: pd.DataFrame):
    """
    Load transformed DataFrame into PostgreSQL.
    """

    conn = get_connection()
    cursor = conn.cursor()

    insert_query = """
    INSERT INTO flights (
        flight_date, flight_status,
        airline_name, airline_iata, airline_icao,
        flight_number, flight_iata, flight_icao,
        departure_airport, departure_iata, departure_icao,
        departure_terminal, departure_gate, departure_delay,
        scheduled_departure, estimated_departure, actual_departure,
        arrival_airport, arrival_iata, arrival_icao,
        scheduled_arrival, estimated_arrival, actual_arrival,
        etl_load_timestamp
    )
    VALUES (
        %s, %s, %s, %s, %s,
        %s, %s, %s,
        %s, %s, %s,
        %s, %s, %s,
        %s, %s, %s,
        %s, %s, %s,
        %s, %s, %s,
        %s
    )
    """

    for _, row in df.iterrows():
        clean_row = tuple(None if pd.isna(value) else value for value in row)
        cursor.execute(insert_query, clean_row)

    conn.commit()
    cursor.close()
    conn.close()

    print(f"Loaded {len(df)} records into PostgreSQL.")