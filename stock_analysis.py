#!/usr/bin/python3

"""
    Title:          stock_analysis.py
    Description:    Script to visualize stock data in candlestick plot using
                    the Alpha Vantage API
    Author:         Pascal Schlaak
    Date:           2019-07-28
    Python:         3.6.7
"""

import os
import time
import smtplib
import numpy as np
import pandas as pd
import datetime as dt
from dateutil import parser

import matplotlib.pyplot as plt
import matplotlib.dates as mdates

from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

from mpl_finance import candlestick_ohlc
from alpha_vantage.timeseries import TimeSeries


# TODO: Specify aplha_vantage api key to access stock data
API_KEY = "<PUT API KEY HERE>"

# TODO: Specify t0 and t1 to plot data inbetween!
today = dt.date.today()
t0 = today - dt.timedelta(days=1)


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
    current_data["3. low"], current_data["4. close"]), width=1./(24*60)*3, colorup="g", colordown="r")

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

    return plot_name


def send_mail(plot_names):

    """
    Function to send plot images attached in e-mail.
    
    :param  list    plot_names: List with paths to plots
    """

    # Define message content
    msg = MIMEMultipart()
    msg["Subject"] = "Daily summary stocks"
    msg["From"] = "<sender>"
    msg["To"] = "<receiver>"

    # Append every plot to e-mail
    for plot in plot_names:
        # Read image of current plot
        img_data = open(plot, "rb").read()
        image = MIMEImage(img_data, name=os.path.basename(plot))
        msg.attach(image)

    # Open connection
    s = smtplib.SMTP("smtp.gmail.com", 587)
    s.ehlo()
    # Secure connection
    s.starttls()
    s.ehlo()
    s.login("<e-mail>", "<pw>")
    s.sendmail(msg["From"], msg["To"], msg.as_string())
    s.quit()

    print("E-Mail sent!")


def main(t0, t1, save_plot):

    """
    Main function to create plots for defined stocks at specific time.
    
    :param  date    t0:             Day before to be analysed time window
    :param  date    t1:             Day after to be analysed time window
    :param  date    stock_symbol:   Stock to be analysed by symbol
    :param  pandas  current_data:   Data of to be analysed frame
    """

    last_day = ""
    stocks, plot_names = [], []

    # Read all stocks by symbol into list
    stocks = open("stocks.txt","r").read().splitlines()

    # Wait until specific time is reached
    while True:
        # Get current time in "hour:min"-format
        t = dt.datetime.now().strftime("%H:%M")
        # Check if it"s later than 20:00 o"clock (24h time format)
        if t >= "19:00" and last_day != dt.date.today():
            print("Starting with creating candlestick graphs!")
            # Create candlestick plot for every specified stock
            for stock in stocks:
                td = fetch_data(t0, t1, stock)
                pn = calculcate_candlestick(td, stock, save_plot)
                # Add stock-image path to list
                plot_names.append(pn)
            # Send plots via e-mail
            send_mail(plot_names)
            last_day = dt.date.today()

        # Sleep 59 seconds before checking again
        time.sleep(59)


if __name__ == "__main__":
    main(t0, today, 1)
