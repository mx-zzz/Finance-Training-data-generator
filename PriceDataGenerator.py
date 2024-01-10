
import csv
import yfinance as yf
import pandas as pd
from InvalidDataError import InvalidDataError
from SampleSizeError import SampleSizeError
import pandas_market_calendars as mcal
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler


# Enter Stock Tickers here.
# Note: Only works for NYSE and NASDAQ Listed Stock Tickers.



stock_names = ["ADSK", "ALGN", "ALNY", "ALTR", "AMTD", "AMZN", "ANSS", "AON", "APA", "APD", "APH", "ARG",
"ASML", "ATVI", "AVGO", "BIDU", "BIIB", "BKNG", "BMRN", "CDNS", "CDW", "CERN", "CHKP", "CHTR", "CMCSA", "COST",
"CPRT", "CSCO", "CSGP", "CSX", "CTAS", "CTRP", "CTXS", "DLTR", "DOCU", "DXCM", "EA", "EBAY", "ESRX", "EXC", "EXPE",
"FAST", "FB", "FISV", "FOX", "FOXA", "GILD", "GOOG", "GOOGL", "IDXX", "ILMN", "INCY", "INTC", "INTU", "ISRG", "JD",
"KDP", "KHC", "KLAC", "LBTYA", "LBTYB", "LBTYK", "LULU", "MAR", "MCHP", "MDLZ", "MELI", "MNST", "MSFT", "MTCH", "MU",
"MXIM", "NLOK", "NTAP", "NTES", "NVDA", "NXPI", "ORLY", "PAYX", "PCAR", "PDD", "PEP", "PYPL", "QCOM", "REGN", "ROST",
"SBUX", "SGEN", "SIRI", "SNPS", "SPLK", "SWKS", "TCOM", "TMUS", "TSLA", "TTWO", "TXN", "UAL", "VRSK", "VRSN", "VRTX",
"WBA", "WDAY", "WDC", "XEL", "XLNX", "ZM","AAPL", "MSFT", "AMZN", "GOOGL", "FB", "INTC", "CSCO", "CMCSA", "PEP", "AMGN", "COST", "NFLX", "ADBE",
"MDLZ", "PYPL", "SBUX", "GILD", "TMUS", "TXN", "QCOM", "BIDU", "AVGO", "NVDA", "ADP", "VRTX", "ATVI", "MU", "INTU",
"MELI", "CERN", "CTSH", "CSX", "DLTR", "EXPD", "FAST", "FISV", "HSIC", "IDXX", "JBHT", "CHKP", "CTAS", "ADI", "EXPE",
"ROST", "WDC", "ALXN", "AMAT", "BBBY", "BIIB", "CA", "CELG", "CTXS", "DISCA", "DISH", "EBAY", "ESRX", "FOXA", "GOOG",
"HAS", "HOLX", "ILMN", "INCY", "ISRG", "LBTYA", "LRCX", "MAR", "MCHP", "MYL", "NLOK", "NTAP", "ORLY", "PCAR", "PCLN",
"REGN", "SHPG", "SIRI", "STX", "SYMC", "TSLA", "VIAB", "VOD", "WBA", "XRAY", "YHOO", "ZION", "KLAC", "SGEN", "SPLK",
"TTWO", "ULTA", "VRSK", "VRSN", "WFM", "XLNX"]

index_offset = 251


start_date = "2011-06-01"
end_date = "2017-06-01"



invalid_tickers = []

def get_trading_days(start_date, end_date):
    # Convert input dates to datetime
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    nasdaq = mcal.get_calendar('NASDAQ')

    trading_days = nasdaq.valid_days(start_date=start_date, end_date=end_date)

    return len(trading_days)-4


def check_training_data(index, name,start_date, end_date):
    rows = get_trading_days(start_date,end_date)
    columns = 7
    file_path = "TrainingData\\" + str(index) + ".csv"

    with open(file_path, 'r') as file:
        lines = 0
        trainingdata = csv.reader(file)
        lines = sum(1 for line in trainingdata)  # Count the number of lines
        if lines < 700:
            invalid_tickers.append(name)
            raise SampleSizeError(f"Wrong Amount of lines in TrainingData\nShould be {rows}\nWas Instead: {lines}\n Ticker Name: {name}")

    with open(file_path, 'r') as trainingdata_file:
        trainingdata = csv.reader(trainingdata_file)
        for i in range(rows):
            try:
                row = next(trainingdata)
                column_count = len(row)
                if columns != column_count:
                    invalid_tickers.append(name)
                    raise SampleSizeError(f"Wrong Amount of Columns in TrainingData\nShould be {columns}\nWas Instead: {column_count}\nFile Name: {str(index)}\n Ticker Name: {name}")
            except StopIteration:
                break  # or do something else if you want

def normalize_training_data(filenum) :
    data = pd.read_csv("TrainingData\\" + filenum + ".csv", skiprows=1)
    scaler = MinMaxScaler()

    data_normalized = data.apply(lambda x: scaler.fit_transform(x.values.reshape(-1, 1)).flatten() if x.name in data else x)
    data_normalized.to_csv("TrainingData\\" + filenum + ".csv", index=False, quoting=csv.QUOTE_NONE)
    data_normalized = pd.read_csv("TrainingData\\" + filenum + ".csv", skiprows=2)
    data_normalized.to_csv("TrainingData\\" + filenum + ".csv", index=False, quoting=csv.QUOTE_NONE)



def init_training_data(index,stock_names,name, start_date, end_date):

    try:
        stock = yf.Ticker(name)
        data = stock.history(start=start_date, end=end_date)

        #print(data)

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
        del data['Stock Splits']

        del data['Date']

        # Save the price history to a CSV file
        index_str = str(index)
        file_path = "TrainingData\\" + index_str + ".csv"

        data.to_csv(file_path, index=False, quoting=csv.QUOTE_NONE)

        # Remove trailing comma at the end of each row in the CSV file
        with open("TrainingData\\" + index_str + ".csv", 'r') as file:
            lines = file.readlines()
        with open("TrainingData\\" + index_str + ".csv", 'w', newline='') as file:
            writer = csv.writer(file)
            for line in lines[1:]:
                if line.strip():  # Remove empty lines
                    writer.writerow(line.strip().split(','))

        normalize_training_data(index_str)




    except TypeError as e:

        raise InvalidDataError(f"Cannot Get Data for {name}, Symbol is likely delisted or there is no data for API to retrieve")


def generate_training_data(stock_names,start_date,end_date,index_offset):
    for name in stock_names:
        index = index_offset + stock_names.index(name)
        try:
            init_training_data(index,stock_names,name, start_date, end_date)
            check_training_data(int(index), name,start_date, end_date)
        except SampleSizeError as e:
            print("")
            print("Sample Size Error", e)
            print("")
            invalid_tickers.append(name)
            stock_names.remove(name)
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
    generate_training_data(stock_names, start_date, end_date,index_offset)






if __name__ == "__main__":
    main()



