from datetime import datetime

import pandas as pd


def transform_flights(api_response):
    """
    Transform raw AviationStack API response into a clean Pandas DataFrame.
    """

    if not api_response or "data" not in api_response:
        print("No data available for transformation.")
        return pd.DataFrame()

    flights = api_response["data"]

    transformed_data = []

    # Timestamp showing when THIS ETL execution happened
    etl_load_timestamp = datetime.now()

    for flight in flights:

        transformed_data.append({

            "flight_date": flight.get("flight_date"),
            "flight_status": flight.get("flight_status"),

            "airline_name": flight.get("airline", {}).get("name"),
            "airline_iata": flight.get("airline", {}).get("iata"),
            "airline_icao": flight.get("airline", {}).get("icao"),

            "flight_number": flight.get("flight", {}).get("number"),
            "flight_iata": flight.get("flight", {}).get("iata"),
            "flight_icao": flight.get("flight", {}).get("icao"),

            "departure_airport": flight.get("departure", {}).get("airport"),
            "departure_iata": flight.get("departure", {}).get("iata"),
            "departure_icao": flight.get("departure", {}).get("icao"),
            "departure_terminal": flight.get("departure", {}).get("terminal"),
            "departure_gate": flight.get("departure", {}).get("gate"),
            "departure_delay": flight.get("departure", {}).get("delay"),
            "scheduled_departure": flight.get("departure", {}).get("scheduled"),
            "estimated_departure": flight.get("departure", {}).get("estimated"),
            "actual_departure": flight.get("departure", {}).get("actual"),

            "arrival_airport": flight.get("arrival", {}).get("airport"),
            "arrival_iata": flight.get("arrival", {}).get("iata"),
            "arrival_icao": flight.get("arrival", {}).get("icao"),
            "scheduled_arrival": flight.get("arrival", {}).get("scheduled"),
            "estimated_arrival": flight.get("arrival", {}).get("estimated"),
            "actual_arrival": flight.get("arrival", {}).get("actual"),

            # ETL metadata
            "etl_load_timestamp": etl_load_timestamp

        })

    df = pd.DataFrame(transformed_data)

    df = df.drop_duplicates()

    df["flight_date"] = pd.to_datetime(
        df["flight_date"],
        errors="coerce"
    ).dt.date

    datetime_columns = [
        "scheduled_departure",
        "estimated_departure",
        "actual_departure",
        "scheduled_arrival",
        "estimated_arrival",
        "actual_arrival",
    ]

    for column in datetime_columns:
        df[column] = pd.to_datetime(
            df[column],
            errors="coerce",
            utc=True
        )

    print("Transformation completed successfully.")
    print(f"Total records transformed: {len(df)}")

    return df


if __name__ == "__main__":
    from extract import extract_flights

    raw_data = extract_flights("ATH")

    if raw_data:
        # Keep only the first 5 flights for testing
        raw_data["data"] = raw_data["data"][:5]

        transformed_df = transform_flights(raw_data)

        print("\nFirst five transformed records:\n")
        print(transformed_df)

        print("\nDataFrame Information:\n")
        transformed_df.info()