#!/usr/bin/python3

"""
    Title:          stock_analysis.py
    Description:    Script to visualize stock data in candlestick plot using
                    the Alpha Vantage API
    Author:         Pascal Schlaak
    Date:           2019-07-28
    Python:         3.6.7
"""

import numpy as np
import pandas as pd
import datetime as dt
from dateutil import parser

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from mpl_finance import candlestick_ohlc
from alpha_vantage.timeseries import TimeSeries


# TODO: Specify aplha_vantage api key to access stock data
API_KEY = "<API-KEY>"
# TODO: Define the stock by symbol which sould be requested
stock_symbol = "MSFT"

# TODO: Specify t0 and t1 to plot data inbetween!
today = dt.date.today()
t0 = today - dt.timedelta(days=3)
t1 = today + dt.timedelta(days=2)


def fetch_data(t0, t1, stock_symbol):

    """
    Fetch data from a specified stock by day
    
    :param  date    t0:             Day before to be analysed time window
    :param  date    t1:             Day after to be analysed time window
    :param  date    stock_symbol:   Stock to be analysed by symbol
    :return pandas  current_data:   Data of to be analysed frame

    """
    
    # Alpha vantage timeseries object to fetch data (value every 5 min) in pandas-format
    ts = TimeSeries(API_KEY, output_format="pandas")
    data, _ = ts.get_intraday(symbol=stock_symbol, interval="5min", outputsize="full")

    # Cut current time window data
    current_data = data[str(t0):str(t1)]

    return current_data


def calculate_derivative(current_data):

    """
    Calculate derivative for every entries
    
    :param  pandas  current_data:   Data of to be analysed frame
    :return pandas  current_data:   Data with new derivative column 

    """

    # Declare array with first value equals zero to build gradient
    derivative_data = [0]
    derivative_data = np.gradient(current_data["4. close"])
    # Add gradient values as column to current dataframe
    current_data["gradient"] = derivative_data

    return current_data


def calculcate_candlestick(current_data, stock_symbol, save_plot):

    """
    Calculate candlestick graph of specified time window
    
    :param  pandas  current_data:   Data of to be analysed frame
    """

    data_indexes = []
    # Get date needed for saving plot to file
    plot_date = str((current_data.index)[0])
    # Parse timestamps
    for i in current_data.index:
        i = parser.parse(i)
        data_indexes.append(mdates.date2num(i))

    # Create plot
    _, ax = plt.subplots()

    # Create candlesticks from data
    candlestick_ohlc(ax, zip(data_indexes, current_data["1. open"], current_data["2. high"], 
    current_data["3. low"], current_data["4. close"]), width=1./(24*60)*4, colorup="g", colordown="r")

    # Plot hours as x-ticks and autoscale
    ax.xaxis_date()
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%H-%M"))
    plt.autoscale()
    # Add grid lines
    plt.grid(b=True, axis="y", color="0.15", linewidth="0.1")
    # Set axis labels and title
    plt.xlabel("Time [hours]")
    plt.ylabel("Stock price [USD]")
    plt.title("Stock: " + stock_symbol)
    
    # Check if plot should be showed or saved
    if save_plot == 0:
        plt.show()
    elif save_plot == 1:
        plot_name = plot_date[0:10] + "_" + stock_symbol.lower() + ".png"
        plt.savefig(plot_name, dpi=400)
        plt.close()
    else:
        print("\nError: Wrong save_plot value! Should be 0 or 1 see help() of function!")


td = fetch_data(t0, t1, stock_symbol)
calculcate_candlestick(td, stock_symbol, 0)
