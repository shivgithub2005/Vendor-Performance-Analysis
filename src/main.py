import logging
from sqlalchemy import engine
from extract import extract_data
from transform import transform_data

logging.basicConfig(
    filename='logs/project.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

def main():
    logging.info("Project Started")

    df,engine = extract_data()
    logging.info("Data Extracted")

    df = transform_data(df)
    logging.info("Data Transformed")

    print(df.info())

    # Save for Power BI
    df.to_csv("data/final_data.csv", index=False)
    logging.info("Data Saved")

    df.to_sql(
        name = "final_data",
        con = engine,
        if_exists = "replace",
        index = False
    )

    logging.info("Project Completed")

if __name__ == "__main__":
    main()
