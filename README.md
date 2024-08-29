Overview
This script analyzes the risk and volatility of a stock using historical data from Yahoo Finance (yfinance). It calculates key metrics such as the Sharpe Ratio and Sortino Ratio, and visualizes these ratios over time to help assess the stock's performance.

Requirements
You'll need the following Python libraries:

pandas
numpy
yfinance
matplotlib
plotly


Usage
Input the stock symbol: Provide the ticker symbol of the stock in lowercase.
Data Fetching: The script retrieves the stock's historical data and calculates log returns.
Volatility Calculation: Input the number of trading days for rolling volatility and ratio calculations.

Ratio Calculations:
Sharpe Ratio: Measures return per unit of risk, adjusted for the risk-free rate.
Sortino Ratio: Similar to the Sharpe Ratio, but focuses on downside volatility.

Risk Evaluation: The script evaluates the investment risk based on the calculated ratios.
Visualization: Plots the Sharpe and Sortino Ratios over time.

Outputs:
Risk Assessment: Based on Sharpe and Sortino Ratios.
Plots: Time-series plots for both ratios.
