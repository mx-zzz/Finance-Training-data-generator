# Price Data Generator

Price Data Generator is a Python script developed to fetch, process, and store historical stock price data from Yahoo Finance. The extracted data includes daily opening, closing, highest, and lowest prices, dividends, and volume for the selected stocks. Additionally, it computes the estimated daily revenue based on the stock's closing price and its trading volume.

## Table of Contents
- [Features](#features)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
- [Errors and Exceptions](#errors-and-exceptions)
- [Output](#output)
- [Notes](#notes)
- [Disclaimer](#disclaimer)

## Features

- Fetches historical price data for any given list of stocks listed on NASDAQ or NYSE.
- Estimates daily revenue for each stock based on closing price and volume.
- Performs data validation by comparing the number of rows and columns in each CSV file against expected values, raising appropriate errors if any discrepancies are found.
- The output data is stored in CSV format, allowing easy import into any data analysis tool or software.

## Prerequisites

Ensure you have the following installed on your system:

- Python 3.x
- [yfinance](https://pypi.org/project/yfinance/) library
- [pandas](https://pypi.org/project/pandas/) library
- [pandas_market_calendars](https://pypi.org/project/pandas-market-calendars/)

## Installation

1. Install the required libraries using pip:

    ```bash
    pip install yfinance pandas pandas_market_calendars
    ```

2. Clone or download this repository to your local system.

## Usage

1. Modify the `stock_names` list in the script with the ticker symbols of the stocks you are interested in.

NOTE: Only Works for NYSE and NASDAQ Listed Tickers.

3. Modiy Start and Date times to desired period of time (OPTIONAL)

4. Run the script using the following command:

    ```bash
    python PriceDataGenerator.py
    ```
    
5. The script fetches historical stock price data, computes revenue, validates the data, and saves it to separate CSV files in a directory named `TrainingData`.

## Errors and Exceptions

- `SampleSizeError`: Raised when the number of rows or columns in the data does not match the expected values. It indicates issues with the data size.

- `InvalidDataError`: Raised when data cannot be fetched for a stock, such as when the symbol is delisted or no data is available for the API to retrieve.

## Output

The script generates price data for each stock and saves it in CSV format in the `TrainingData` directory. Each CSV file contains the following columns:

- `Open`: The opening price of the stock on a specific date.
- `High`: The highest price the stock reached on a specific date.
- `Low`: The lowest price the stock dropped to on a specific date.
- `Close`: The closing price of the stock on a specific date.
- `Volume`: The trading volume of the stock on a specific date.
- `Dividends`: The dividends paid by the stock on a specific date (if any).
- `Stock Splits`: The stock splits that occurred on a specific date (if any).
- `Revenue`: The estimated daily revenue, calculated by multiplying the `Close` price with the `Volume`.

## Notes

- An internet connection is required to fetch data from Yahoo Finance.
- This script is optimized for weekly and daily revenue calculations. However, you can modify it according to your specific requirements.
- Please ensure you adhere to the terms of service of the data provider while using this data.

## Disclaimer

This script is intended for educational and research purposes only. It should not be used for actual trading or financial analysis. Always verify the accuracy of the data before making any decisions based on it.

**USE AT YOUR OWN RISK!** The authors and contributors of this script are not responsible for any financial losses or damages that may occur due to its usage. Always consult with a certified financial advisor before making investment decisions.
