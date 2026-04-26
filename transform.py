import numpy as np

def transform_data(df):

    # 1. Fix data types
    df['Volume'] = df['Volume'].astype('float64')

    # 2. Handle missing values
    null_cols = [
        'TotalSalesQuantity',
        'TotalSalesDollars',
        'TotalSalesPrice',
        'TotalExciseTax'
    ]

    df[null_cols] = df[null_cols].fillna(df[null_cols].mean())

    # 3. Clean text
    df['VendorName'] = df['VendorName'].str.strip()

    # 4. Feature Engineering
    df['GrossProfit'] = df['TotalSalesDollars'] - df['TotalPurchaseDollars']

    df['ProfitMargin'] = (
        df['GrossProfit'] / df['TotalSalesDollars']
    ) * 100

    df['StockTurnover'] = (
        df['TotalSalesQuantity'] / df['TotalPurchaseQuantity']
    )

    df['SalesPurchaseRatio'] = (
        df['TotalSalesDollars'] / df['TotalPurchaseDollars']
    )

    # 5. Fix logical error (IMPORTANT)
    df['UnsoldInventoryValue'] = np.maximum(
        (df['TotalPurchaseQuantity'] - df['TotalSalesQuantity']) * df['PurchasePrice'],
        0
    )

    return df