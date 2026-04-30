import logging
from sqlalchemy import create_engine
from utils.config import DB_URL, OUTPUT_PATH


def load_data(df):
    try:
        # Save to CSV
        df.to_csv(OUTPUT_PATH, index=False)
        logging.info("Data successfully saved to CSV")

        # Save to PostgreSQL
        engine = create_engine(DB_URL)
        df.to_sql(
            name="vendor_performance",
            con=engine,
            if_exists="replace",
            index=False
        )
        logging.info("Data successfully loaded to PostgreSQL")

    except Exception as e:
        logging.error(f"Error in loading step: {e}")
        raise