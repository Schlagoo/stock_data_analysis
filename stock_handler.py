import numpy as np
import pandas as pd
import datetime as dt
import matplotlib.pyplot as plt
from alpha_vantage.timeseries import TimeSeries


# aplha_vantage api key to access stock data
API_KEY = "V4M6OKQAKTF3IU2P"
# Get current day
today = dt.date.today()
tomorrow = today + dt.timedelta(days=1)
stock_symbol = "MSFT"


def fetch_data(today, tomorrow, stock_symbol):
    """ Fetch data from specified stock """
    
    ts = TimeSeries(API_KEY, output_format="pandas")
    data, _ = ts.get_intraday(symbol=stock_symbol, interval="1min", outputsize="full")

    todays_data = data[str(today):str(tomorrow)]
    calculate_derivative(todays_data)


def calculate_derivative(todays_data):
    """ Calculate derivative for every entries """

    closed_todays_data = todays_data["4. close"]
    difference_data = [0]
    # print(closed_todays_data)
    difference_data = np.gradient(closed_todays_data)
    # for index, value in enumerate(closed_todays_data):
    #     if closed_todays_data[index] != None and index >= 1:
    #         difference_data.append(round(float(closed_todays_data[index] - closed_todays_data[index-1]), 4))
    todays_data["gradient"] = difference_data
    
    plt.subplot(2, 1, 1)
    plt.plot(todays_data["gradient"], "r")
    plt.title("Stock value (gradient): Microsoft")
    plt.xticks([])
    plt.subplot(2, 1, 2)
    plt.plot(todays_data["4. close"], "b")
    plt.title("Stock value (closed): Microsoft")
    plt.xticks([])
    plt.show()

    #TODO: Save image


def send_mail():
    #TODO: Send image to at 20:01 (stock market closing) to mail-adress
    pass


fetch_data(today, tomorrow, stock_symbol)