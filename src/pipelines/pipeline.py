import logging
from ingestion.extract import extract_data
from transformation.transform import transform_data
from loading.load import load_data


def run_pipeline():
    try:
        logging.info("Pipeline started")

        # Step 1: Extract
        df = extract_data()
        logging.info("Data extraction completed")

        # Step 2: Transform
        df = transform_data(df)
        logging.info("Data transformation completed")

        # Step 3: Load (CSV + PostgreSQL handled inside load.py)
        load_data(df)
        logging.info("Data loading completed")

    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        raise