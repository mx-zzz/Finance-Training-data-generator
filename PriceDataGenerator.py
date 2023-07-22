import csv

import yfinance as yf
import pandas as pd


from SampleSizeError import SampleSizeError

stock_names = [
    "AAPL", "MSFT", "AMZN", "GOOGL", "TSLA", "NVDA", "INTC", "ADBE", "CSCO",
    "CMCSA", "ASML", "AVGO", "TXN", "ORCL", "QCOM", "SAP", "CRM", "SHOP", "IBM",
    "AMD", "ADSK", "FIS", "ACN", "AMAT", "TMUS", "TEL", "NVZMY", "INTU", "WDAY",
    "VMW", "ATVI", "ADI", "INFY", "EA", "MTCH", "LRCX", "CTSH", "MU", "APH",
    "KLAC", "NXPI", "ADP", "ERIC", "BIDU", "TELNY", "SNPS", "MCHP", "SWKS", "WD",
    "GLW", "STX", "ANSS", "CDNS", "FLT", "DXC", "WDC", "KEYS", "NTES", "VRSN"
]


# Create a Tickers object with the stock names
stocks = yf.Tickers(" ".join(stock_names))

invalid_tickers = []

def check_sample_size(index,name):

    features_rows = 2015
    features_columns = 8
    labels_columns = 31
    feature_file_path = "Features\\" + str(index) + ".csv"
    label_file_path = "Labels\\" + str(index) + ".csv"

    with open(feature_file_path, 'r') as feature_file:
        lines = 0
        feature_data = csv.reader(feature_file)
        lines = sum(1 for line in feature_data)  # Count the number of lines
        if lines != features_rows:
            invalid_tickers.append(name)
            raise SampleSizeError(f"Wrong Amount of lines in Features\nShould be {features_rows}\nWas Instead: {lines}\n Ticker Name: {name}")

    with open(feature_file_path, 'r') as feature_file:
        feature_data = csv.reader(feature_file)
        for i in range(features_rows):
            row = next(feature_data)
            column_count = len(row)
            if features_columns != column_count:
                invalid_tickers.append(name)
                raise SampleSizeError(
                    f"Wrong Amount of Columns in Features\nShould be {features_columns}\nWas Instead: {column_count}\nFile Name: {index}\n Ticker Name: {name}")

    with open(label_file_path, 'r') as label_file:
        label_data = csv.reader(label_file)
        row = next(label_data)
        column_count = len(row)
        if labels_columns != column_count:
            invalid_tickers.append(name)

            raise SampleSizeError(f"Wrong Amount of Columns in Labels\nShould be {labels_columns}\n Was Instead: {column_count}\n File Name: {index}\n Ticker Name: {name}")


for name in stock_names:

    # Fetch historical data for each stock
    data = stocks.tickers[name].history(start="2015-06-01", end="2023-06-01")

    # Calculate revenue by multiplying Close price with Volume
    data['Revenue'] = data['Close'] * data['Volume']

    # Group the data by week and sum the revenue
    revenue_by_week = data.groupby(pd.Grouper(freq='W'))['Revenue'].sum()

    # Reset the index to remove the default index
    revenue_by_week = revenue_by_week.reset_index()

    # Merge weekly revenue data with daily price data based on the nearest week start date
    data['Week_Start'] = data.index - pd.offsets.Week(weekday=0)
    data = data.merge(revenue_by_week, how='left', left_on='Week_Start', right_on='Date', suffixes=('', '_Weekly'))

    # Fill missing weekly revenue values forward
    data['Revenue_Weekly'].fillna(method='ffill', inplace=True)

    # Calculate daily revenue by dividing weekly revenue by 5 (assuming 5 trading days in a week)
    data['Revenue_Daily'] = data['Revenue_Weekly'] / 5

    # Remove unnecessary columns
    del data['Week_Start']
    del data['Revenue_Weekly']
    data.drop(['Stock Splits'], axis=1, inplace=True)
    del data['Date']

    # Save the price history to a CSV file
    index: str = str(stock_names.index(name))
    data.to_csv("Features\\" + index + ".csv", index=False, quoting=csv.QUOTE_NONE)

    # Remove trailing comma at the end of each row in the CSV file
    with open("Features\\" + index + ".csv", 'r') as file:
        lines = file.readlines()
    with open("Features\\" + index + ".csv", 'w', newline='') as file:
        writer = csv.writer(file)
        for line in lines[1:]:
            if line.strip():  # Remove empty lines
                writer.writerow(line.strip().split(','))

    print(f"Data for {name} saved to {str(stock_names.index(name))}")

    try:
        check_sample_size(int(index),name)
    except SampleSizeError as e:
        print("")
        print("Sample Size Error", e)
        print("")
    else:
        print("")


print(invalid_tickers)










