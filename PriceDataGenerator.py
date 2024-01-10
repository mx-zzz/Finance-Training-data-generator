
import csv
import yfinance as yf
import pandas as pd
from InvalidDataError import InvalidDataError
from SampleSizeError import SampleSizeError
import pandas_market_calendars as mcal
from datetime import datetime
from sklearn.preprocessing import MinMaxScaler
import os



index_offset = 0

start_date = "2011-06-01"
end_date = "2017-06-01"

invalid_tickers = []

def get_trading_days(start_date, end_date):
    # Convert input dates to datetime
    start_date = datetime.strptime(start_date, '%Y-%m-%d')
    end_date = datetime.strptime(end_date, '%Y-%m-%d')

    nasdaq = mcal.get_calendar('NASDAQ')

    trading_days = nasdaq.valid_days(start_date=start_date, end_date=end_date)

    return len(trading_days)


def check_training_data(file_path, name, rows):

    columns = 7
    error = False
    with open(file_path, 'r') as file:
        lines = 0
        trainingdata = csv.reader(file)
        lines = sum(1 for line in trainingdata)  # Count the number of lines
        try:
            if lines != rows:
                raise SampleSizeError(f"Wrong Amount of lines in TrainingData\nShould be {rows}\nWas Instead: {lines}\n Ticker Name: {name}")
        except SampleSizeError:
            error = True



    with open(file_path, 'r') as trainingdata_file:
        trainingdata = csv.reader(trainingdata_file)
        for i in range(rows):
            try:
                row = next(trainingdata)
                column_count = len(row)
                if columns != column_count:
                    error = True
                    raise SampleSizeError(f"Wrong Amount of Columns in TrainingData\nShould be {columns}\nWas Instead: {column_count}\nFile Name: {file_path}\n Ticker Name: {name}")
            except StopIteration:
                break
    if(error == True) :
        invalid_tickers.append(file_path)
    else :
        print(f"Ticker {name} Successfully Generated ")


def normalize_training_data(file_path):

    print(f"Normalizing data from {file_path}")

    try:
        data = pd.read_csv(file_path)
        print("Data after reading CSV:")
        print(data.head())  # Print first few lines of the data

        scaler = MinMaxScaler()
        data_normalized = data.apply(
            lambda x: scaler.fit_transform(x.values.reshape(-1, 1)).flatten() if x.name in data else x)
        data_normalized.to_csv(file_path, index=False, quoting=csv.QUOTE_NONE)

        # Additional debug: Check the data after normalization
        print("Data after normalization:")
        print(data_normalized.head())

    except(ValueError) as e:
        print(f"Error while normalizing data in file {file_path}: {e}")
        print(data.to_string())


def init_training_data(index,file_path, name, start_date, end_date,num_of_rows) :
    try:
        stock = yf.Ticker(name)
        data = stock.history(start=start_date, end=end_date)
        data_frame = pd.DataFrame(data)
    except Exception as e:
        raise InvalidDataError(f"No Data found for ticker : {name} in {file_path}")
        invalid_tickers.append(file_path)
        return

    try:
        if data.empty:
            raise InvalidDataError(f"No data fetched for {name}")
            invalid_tickers.append(file_path)
            return

        if data_frame.to_string().__contains__(".0.") :
            data_frame.replace("0.0.1","0.0",inplace=True)
            print(f"Data recieved from API contians invalid symbols but has been restored.")
            if data_frame.to_string().__contains__(".0.") :
                raise InvalidDataError(f"Data recieved from API contians invalid symbols.")
                return

        print(f"Writing data to {file_path}")
        data_frame.to_csv(file_path, index=False, quoting=csv.QUOTE_NONE)

        # Debug: Print the first few lines of the data
        print("Data preview:", data.head())

        normalize_training_data(file_path)

        check_training_data(file_path, name, num_of_rows)

    except TypeError as e:
        raise InvalidDataError(f"Cannot Get Data for {name}, Symbol is likely delisted or there is no data for API to retrieve")
        return
    except InvalidDataError as e:
        invalid_tickers.append(file_path)
        print(e)
        return



def generate_training_data(stock_names,start_date,end_date,index_offset):

    num_of_rows = get_trading_days(start_date,end_date)

    for name in stock_names:
        index = index_offset + stock_names.index(name)
        file_path = "TrainingData\\" + str(index) + ".csv"
        init_training_data(index,file_path,name, start_date, end_date,num_of_rows)



    if len(invalid_tickers) > 0:
        print("The Following Tickers are invalid: ", invalid_tickers)
        remove_tickers_prompt = input("Would you like to remove invalid tickers and Try again (Y/N) ")

        if remove_tickers_prompt.strip() == "Y" :
            print("Removing Invalid Tickers")
            remove_invalid_tickers()
            print("These are the Valid Tickers : ", stock_names)
            print("Regenerating Data set with valid tickers")
            rename_training_data()


    else:
        print("All data correctly saved and Valid")

def remove_invalid_tickers():
    for ticker in stock_names :
        if ticker in invalid_tickers :
            stock_names.remove(ticker)


def rename_training_data():
    base_path = "C:\\Users\\byzan\\PycharmProjects\\pythonProject\\"
    training_data_path = os.path.join(base_path, "TrainingData")

    # Remove invalid tickers
    for filename in invalid_tickers:
        file_path = os.path.join(base_path, filename)
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"File {file_path} has been deleted.")
        else:
            print(f"The file {file_path} does not exist.")

    # Rename files in TrainingData
    files = sorted(os.listdir(training_data_path), key=lambda x: int(x.split('.')[0]))
    for index, data_file in enumerate(files):
        current_file_path = os.path.join(training_data_path, data_file)
        new_file_name = f"{index}.csv"
        new_file_path = os.path.join(training_data_path, new_file_name)

        if data_file != new_file_name:
            os.rename(current_file_path, new_file_path)
            print(f"Renamed {data_file} to {new_file_name}")

def get_spx_tickers():
    url = 'https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    tables = pd.read_html(url)
    spx_table = tables[0]
    tickers = spx_table['Symbol'].tolist()
    return tickers

def main():
    spx_tickers = get_spx_tickers()
    generate_training_data(spx_tickers, start_date, end_date,index_offset)


if __name__ == "__main__":
    main()





