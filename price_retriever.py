import os
import yfinance as yf

with open('symbols.csv') as f:
  lines = f.read().splitlines()
  for symbol in lines:
    data = yf.download(symbol, start="2021-01-01", end="2021-05-30")
    data.to_csv(f"datasets/{symbol}.csv")