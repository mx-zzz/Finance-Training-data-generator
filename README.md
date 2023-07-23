# Price Data Generator

This Python script is a price data generator that fetches historical stock price data from Yahoo Finance using the `yfinance` library and saves it to CSV files. It processes the data to calculate weekly and daily revenue based on stock price and volume.


## Prerequisites
- Python 3.x
- `yfinance` library
- `pandas` library

## Installation
1. Install the required libraries using pip:
pip install yfinance pandas


2. Clone or download the repository containing the script.

## Usage
1. Modify the `stock_names` list with the ticker symbols of the stocks you want to fetch data for.

2. Run the script `PriceDataGenerator.py`.

3. The script will fetch historical stock price data for each stock in the list, calculate revenue, and save the data to separate CSV files in the `TrainingData` directory.

4. The script also performs data validation by checking the number of rows and columns in each CSV file to ensure data consistency. If any inconsistencies are found, it raises appropriate errors.

## Handling Errors
- `SampleSizeError`: If the number of rows or columns in the data does not match the expected values, a `SampleSizeError` is raised, indicating the issue.

- `InvalidDataError`: If data cannot be fetched for a stock (e.g., symbol is delisted or no data available), an `InvalidDataError` is raised.

## Output
The generated price data for each stock is saved in CSV format in the `TrainingData` directory.

The CSV files contain the following columns:

- `Open`: The opening price of the stock on that date.
- `High`: The highest price of the stock on that date.
- `Low`: The lowest price of the stock on that date.
- `Close`: The closing price of the stock on that date.
- `Volume`: The trading volume of the stock on that date.
- `Dividends`: The dividends paid by the stock on that date (if available).
- `Stock Splits`: The stock splits that occurred on that date (if available).
- `Estimated Revenue`: The estimated revenue calculated by multiplying the `Close` price with the `Volume`. This represents the daily revenue based on stock price and trading volume.

## Notes
- Ensure you have an internet connection to fetch data from Yahoo Finance.

- The script is optimized for weekly and daily revenue calculations. Additional features or data can be calculated and saved based on specific requirements.

- Make sure you have permission to use the financial data according to the respective data provider's terms of service.

## Disclaimer
This script is intended for educational and research purposes only. It is not intended for actual trading or financial analysis. Use the data responsibly and verify its accuracy before making any decisions based on it.

**USE AT YOUR OWN RISK!** The authors and contributors of this script are not responsible for any financial losses or damages that may occur from its usage.
