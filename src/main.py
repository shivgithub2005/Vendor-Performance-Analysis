from pipelines.pipeline import run_pipeline
from utils.logger import setup_logger
import logging


def main():
    # Setup logging
    setup_logger()
    logging.info("Starting Vendor Performance ETL Pipeline")

    try:
        run_pipeline()
        logging.info("Pipeline executed successfully")
    except Exception as e:
        logging.error(f"Pipeline failed: {e}")
        raise


if __name__ == "__main__":
    main()