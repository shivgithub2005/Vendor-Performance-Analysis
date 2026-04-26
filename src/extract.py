import  os
from dotenv import load_dotenv
load_dotenv()

import pandas as pd
from sqlalchemy import create_engine
from urllib.parse import quote_plus

def extract_data():

    # Database connection details
    user = "postgres"
    password = quote_plus(os.getenv("DB_PASSWARD"))   # replace if needed
    host = "localhost"
    port = "5432"
    dbname = "Data Science Projects"

    # Create connection
    engine = create_engine(
        f"postgresql://{user}:{password}@{host}:{port}/{dbname}"
    )

    # SQL Query (your full summary query)
    query = """
    WITH FreightSummary AS (
        SELECT
            "VendorNumber",
            SUM("Freight") AS "FreightCost"
        FROM vendor_invoice
        GROUP BY "VendorNumber"
    ),

    PurchaseSummary AS (
        SELECT
            p."VendorNumber",
            p."VendorName",
            p."Brand",
            p."Description",
            p."PurchasePrice",
            pp."Price" AS "ActualPrice",
            pp."Volume",
            SUM(p."Quantity") AS "TotalPurchaseQuantity",
            SUM(p."Dollars") AS "TotalPurchaseDollars"
        FROM purchases p
        JOIN purchase_prices pp
            ON p."Brand" = pp."Brand"
        WHERE p."PurchasePrice" > 0
        GROUP BY
            p."VendorNumber",
            p."VendorName",
            p."Brand",
            p."Description",
            p."PurchasePrice",
            pp."Price",
            pp."Volume"
    ),

    SalesSummary AS (
        SELECT
            "VendorNo",
            "Brand",
            SUM("SalesQuantity") AS "TotalSalesQuantity",
            SUM("SalesDollars") AS "TotalSalesDollars",
            SUM("SalesPrice") AS "TotalSalesPrice",
            SUM("ExciseTax") AS "TotalExciseTax"
        FROM sales
        GROUP BY "VendorNo", "Brand"
    )

    SELECT
        ps."VendorNumber",
        ps."VendorName",
        ps."Brand",
        ps."Description",
        ps."PurchasePrice",
        ps."ActualPrice",
        ps."Volume",
        ps."TotalPurchaseQuantity",
        ps."TotalPurchaseDollars",
        ss."TotalSalesQuantity",
        ss."TotalSalesDollars",
        ss."TotalSalesPrice",
        ss."TotalExciseTax",
        fs."FreightCost"
    FROM PurchaseSummary ps
    LEFT JOIN SalesSummary ss
        ON ps."VendorNumber" = ss."VendorNo"
        AND ps."Brand" = ss."Brand"
    LEFT JOIN FreightSummary fs
        ON ps."VendorNumber" = fs."VendorNumber"
    """

    # Execute query
    df = pd.read_sql(query, engine)

    return df,engine
