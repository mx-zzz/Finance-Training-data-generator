# Price Data Generator

The Price Data Generator is a Python script designed to fetch, process, and store historical stock price data from the S&P 500 index. This data is primarily used for training Neural Networks. The script extracts daily opening, closing, highest, and lowest prices, along with dividends, stock splits, and trading volume for stocks listed on the S&P 500 within a specified time period.

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

- Fetches historical price data for all tickers on the S&P 500.
- Validates data integrity by ensuring the correct number of rows and columns in each CSV file, raising appropriate errors for any discrepancies.
- Automatically removes unobtainable data (e.g., data for delisted tickers).
- Normalizes data using MinMaxScaler to transform features by scaling each feature to a given range, typically between 0 and 1, which is essential for Neural Network training.
- Stores output data in CSV format for easy integration with various data analysis tools and software.

## Prerequisites

Before using this script, ensure the following are installed on your system:

- Python 3.x
- [yfinance](https://pypi.org/project/yfinance/) library
- [pandas](https://pypi.org/project/pandas/) library
- [pandas_market_calendars](https://pypi.org/project/pandas-market-calendars/) library
- [scikit-learn](https://pypi.org/project/scikit-learn/) library for data normalization

## Installation

1. Install the required libraries using pip:

    ```bash
    pip install yfinance pandas pandas_market_calendars scikit-learn
    ```

2. Clone or download this repository to your local machine.

## Usage

1. Modify the `start_date` and `end_date` variables to your desired time period (optional).

2. Execute the script with the following command:

    ```bash
    python PriceDataGenerator.py
    ```
    
3. The script fetches historical stock price data, performs data validation, normalization, and saves it to CSV files in a directory named `TrainingData`.

4. When prompted, enter 'Y' (yes) or 'N' (no) to remove invalid tickers.

## Errors and Exceptions

- `SampleSizeError`: Raised if the number of rows or columns in the dataset does not match expected values, indicating data size inconsistencies.

- `InvalidDataError`: Raised when data cannot be retrieved for a stock, such as when the symbol is delisted or there is no data available from the API.

## Output

The script saves the generated price data for each stock in CSV format in the `TrainingData` directory. Each CSV file contains the following columns:

- `Open`: Opening price of the stock on a given date.
- `High`: Highest price reached by the stock on that date.
- `Low`: Lowest price of the stock on that date.
- `Close`: Closing price of the stock on that date.
- `Volume`: Trading volume of the stock on that date.
- `Dividends`: Dividends paid by the stock on that date (if any).
- `Stock Splits`: Stock splits occurring on that date (if any).
- `Normalized Data`: Data columns normalized using MinMaxScaler.

## Notes

- An active internet connection is required to fetch data from Yahoo Finance.
- This script is optimized for weekly and daily revenue calculations. It can be modified to suit specific requirements.
- Adhere to the terms of service of the data provider when using this data.

## Disclaimer

This script is intended for educational and research purposes only and should not be used for actual trading or financial analysis. Verify the accuracy of the data before making any decisions based on it.

**USE AT YOUR OWN RISK!** The authors and contributors of this script are not responsible for any financial losses or damages resulting from its

