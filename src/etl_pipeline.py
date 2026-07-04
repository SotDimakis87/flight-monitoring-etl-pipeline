from extract import extract_flights
from transform import transform_flights
from load import load_data


def run_pipeline():
    print("🚀 Starting ETL pipeline...")

    # 1. Extract
    raw_data = extract_flights("ATH", limit=100)

    if not raw_data:
        print("❌ Extraction failed. Stopping pipeline.")
        return

    # 2. Transform (test with small subset optional here)
    transformed_df = transform_flights(raw_data)

    if transformed_df.empty:
        print("❌ Transformation failed or returned empty DataFrame.")
        return

    # 3. Load
    load_data(transformed_df)

    print("✅ ETL pipeline completed successfully!")


if __name__ == "__main__":
    run_pipeline()