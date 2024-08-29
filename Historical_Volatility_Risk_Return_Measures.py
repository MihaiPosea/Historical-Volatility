import pandas as pd 
import numpy as np
import yfinance as yf

import matplotlib.pyplot as plt
import plotly.offline as pyo
import plotly.graph_objects as go
from plotly.subplots import make_subplots

pyo.init_notebook_mode(connected = True)
pd.options.plotting.backend = 'plotly'

#input section for user

Ticker = input("Please Input ticker symbol in lowercase:")

#We first get our stock information
Stock = yf.Ticker(Ticker)
df = Stock.history(period="max")

## Fixes Date and makes it index
df.to_csv("{}.csv".format(Ticker))
df = pd.read_csv("{}.csv".format(Ticker))

##This will compute log returns using numpy, the shift just goes down one price and moves on, then drops any na
log_return = np.log(df["Close"]/df["Close"].shift(1)).dropna()

##Here I calculate the standard deviation in the return that we are getting on average for each day
##Annualized standard deviation, think of ACTSC when converting rates from days to year.
standard_deviation_of_return = np.std(log_return)
annualized_std = np.sqrt(252) * standard_deviation_of_return * 100

## Calculate the volatility of the stock over time times the sqrt of trading days to make it annualized
Trading_Days = int(input("Please input the amount of trading days you would like to use for ratios:"))
volatility = log_return.rolling(window = Trading_Days).std()*np.sqrt(Trading_Days)


## There exists Ratios to quantify the relationship between risk and return given the sample data. We then plot it.
## Sharpe Ratio: average return earned in excess of the risk-free rate per unit of volatility (above 3 is excellent, above 2 is very good, above 3 is excellent)

Risk_Free_Rate = 0.01/252
sharpe_ratio = (((log_return.rolling(window = Trading_Days).mean() - Risk_Free_Rate)*Trading_Days) / volatility).dropna()

## Sortino Ratio: This is similar to above, yet it puts more emphasis on the downside volalitity since we care more about that. 

downside_deviation = log_return[log_return<0].rolling(window = Trading_Days, center = True, min_periods = 10).std()*np.sqrt(Trading_Days)
sortino_ratio= (((log_return.rolling(window = Trading_Days).mean() - Risk_Free_Rate)*Trading_Days) / downside_deviation).dropna()

def Risk_Calculator(sharpe_ratio_input,sortino_ratio_input):
    print("Sortino Ratio = {}".format(sortino_ratio.mean()))
    print("Sharpe Ratio = {}".format(sharpe_ratio.mean()))
    if sharpe_ratio_input and sortino_ratio_input < 1:
        print("The Investment does not adequetely compensate for the risk, returns might not justify the potential for losses")
    elif  1 <= sharpe_ratio_input and sortino_ratio_input <= 2:
        print("The Investment adequetely compensates for the risk, returns might justify the potential for losses")
    elif  2 <= sharpe_ratio_input and sortino_ratio_input <= 3:
        print("The Investment provides a good compensatation for the risk, returns would justify the potential for losses")
    else:
        print("The Investment provides a great compensatation for the risk, returns justify the potential for losses")
    

Risk_Calculator(sharpe_ratio.mean(),sortino_ratio.mean())


fig1 = make_subplots(rows = 1, cols = 1)
fig2 = make_subplots(rows = 1, cols = 1)
fig1.add_trace(go.Scatter(x = sortino_ratio.index, y = sortino_ratio, mode = "lines", name = "Sortino Ratio"))
fig2.add_trace(go.Scatter(x = sharpe_ratio.index, y = sharpe_ratio, mode = "lines", name = "Sharp Ratio"))
fig1.update_layout(title = "Sortino Ratio Over Time", xaxis_title = "Date", yaxis_title = "Sortino Ratio")
fig2.update_layout(title = "Sharpe Ratio Over Time", xaxis_title = "Date", yaxis_title = "Sharpe Ratio")
fig1.show()
fig2.show()






