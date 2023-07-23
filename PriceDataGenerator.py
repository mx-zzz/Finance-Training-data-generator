
import csv
import yfinance as yf
import pandas as pd
from InvalidDataError import InvalidDataError
from SampleSizeError import SampleSizeError
import pandas_market_calendars as mcal
from datetime import datetime


# Enter Stock Tickers here.
# Note: Only works for NYSE and NASDAQ Listed Stock Tickers.

stock_names = [
    "AAPL", "MSFT", "GOOGL", "TSLA", "NVDA", "INTC", "ADBE", "CSCO",
    "CMCSA", "ASML", "AVGO", "TXN", "ORCL", "QCOM", "SAP", "CRM", "SHOP", "IBM",
    "AMD", "ADSK", "FIS", "ACN", "AMAT", "TMUS", "TEL", "NVZMY", "INTU", "WDAY",
    "VMW", "ATVI", "ADI", "INFY", "EA", "MTCH", "LRCX", "CTSH", "MU", "APH",
    "KLAC", "NXPI", "ADP", "ERIC", "BIDU", "TELNY", "SNPS", "MCHP", "SWKS", "WD",
    "GLW", "STX", "ANSS", "CDNS", "FLT", "DXC", "WDC", "KEYS", "NTES", "VRSN"
]


# Adjust start and end dates of the collected Data.

start_date = "2017-06-01"
end_date = "2023-06-01"


invalid_tickers = []

def get_trading_days(start_date, end_date):
    # Convert input dates to datetime
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    nasdaq = mcal.get_calendar('NASDAQ')

    trading_days = nasdaq.valid_days(start_date=start_date, end_date=end_date)

    return len(trading_days)


def check_training_data(index, name,start_date, end_date):
    rows = get_trading_days(start_date,end_date)
    columns = 8
    file_path = "TrainingData\\" + str(index) + ".csv"

    with open(file_path, 'r') as file:
        lines = 0
        trainingdata = csv.reader(file)
        lines = sum(1 for line in trainingdata)  # Count the number of lines
        if lines != rows:
            invalid_tickers.append(name)
            raise SampleSizeError(f"Wrong Amount of lines in TrainingData\nShould be {rows}\nWas Instead: {lines}\n Ticker Name: {name}")

    with open(file_path, 'r') as trainingdata_file:
        trainingdata = csv.reader(trainingdata_file)
        for i in range(rows):
            row = next(trainingdata)
            column_count = len(row)
            if columns != column_count:
                invalid_tickers.append(name)
                raise SampleSizeError(f"Wrong Amount of Columns in TrainingData\nShould be {columns}\nWas Instead: {column_count}\nFile Name: {str(index)}\n Ticker Name: {name}")


def init_training_data(name, start_date, end_date):

    try:
        stock = yf.Ticker(name)
        data = stock.history(start=start_date, end=end_date)

        print(data)

        # Estimate revenue by multiplying Close price with Volume
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


        # Remove unnecessary columns
        del data['Week_Start']
        del data['Revenue_Weekly']
        #data.drop(['Stock Splits'], axis=1, inplace=True)
        del data['Date']

        # Save the price history to a CSV file
        index_str = str(stock_names.index(name))
        file_path = "TrainingData\\" + index_str + ".csv"

        data.to_csv(file_path, index=False, quoting=csv.QUOTE_NONE)

        print(f"Data for {name} saved to {str(stock_names.index(name))}")

    except TypeError as e:
        raise InvalidDataError(f"Cannot Get Data for {name}, Symbol is likely delisted or there is no data for API to retrieve")

def generate_training_data():
    for name in stock_names:
        index = stock_names.index(name)
        try:
            init_training_data(name, start_date, end_date)
            check_training_data(int(index), name,start_date, end_date)
        except SampleSizeError as e:
            print("")
            print("Sample Size Error", e)
            print("")
        except InvalidDataError as e:
            invalid_tickers.append(name)
            print("")
            print("Invalid Data Error", e)
            print("")
        else:
            print("")

    if len(invalid_tickers) > 0:
        print("The Following Tickers are invalid: ", invalid_tickers)
    else:
        print("All data correctly saved and Valid")

def main():
    generate_training_data()

if __name__ == "__main__":
    main()




