# Project: Automated Stock Data Analysis 

![Preview](./preview_small.png)

This repository contains functions written in python to analyse stock data and retrieve them via e-mail. You can automate running the script by creating a docker image of it (Dockerfile in repository).

## Getting Started

These instructions will help you to run the script on your maschine. First of all you need `python3` installed, as well as following packages:

~~~
numpy==1.13.3
pandas==0.23.4
alpha_vantage==2.1.0
matplotlib==2.1.1
mpl_finance==0.10.0
python_dateutil==2.8.0
~~~

### Installing

Before running the script clone the repository to your desired directory:

~~~
cd /path/to/desired/directory
git clone git@github.com:Schlagoo/stock_analysis.git
~~~

First of all you need to generate an [API Key from Alpha Vantage](https://www.alphavantage.co/support/#api-key). Put this string inside the `API_KEY` variable at the beginning of `stock_analysis.py` file, as well as your desired stock by its symbol. Afterwards specify the timeframe at the beginning of the code too. **Reminder: If you set a timeframe of more or less than one day you need to configure the candlestick width inline! Please note, that you can't get stock data at weekend days.**

After calling the desired function with all arguments, you can run the script from the terminal (linux) via:

(Make shure you the file is executable: `sudo chmod +x whatsapp_data_analysis.py`!)  

~~~
./stock_analysis.py
~~~

### Docker

You can automate running this script by building a docker container. Therefore install [docker](https://www.docker.com/) and build an image with following command:

~~~
docker build ./ -t <img-tag>
~~~

After building the image, you can run an container instance by:

~~~
docker run <image-id/-name>
~~~


## Built with

* [Python 3.6.8](https://www.python.org/) - Programming language
* [Alpha Vantage](https://www.alphavantage.co/documentation/) - Stock timeseries API
* [Docker](https://www.docker.com/) - Container Engine


## Author

* **Pascal Schlaak** - *Student/intern at BMW* - [Schlagoo](https://github.com/Schlagoo)

