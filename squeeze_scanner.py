import os
import pandas as pd
import plotly.graph_objects as go

'''
Bollinger Bands:

  upper band is 2 std dev above the sma, middle band is the sma, lower band is 2 std dev below sma
  default sma calculation is the 20 day moving average

  Method 1
    When we exceed upper band, expect a reversal to sma/middle band, sellpoint / short
    When we go under lower band, expect reversal back upward, buypoint / long
  
  Method 2
    When we exceed upper band, we ride the strong momentum and we ride along the top of upper BB

Keltner's Channels:


'''

for filename in os.listdir('datasets'):
  symbol = filename.split(".")[0] # remove .csv
  df = pd.read_csv(f'datasets/{filename}')
  if df.empty:
    continue
  
  # create new column '20sma', calculate using Close price and rolling window calc
  # of past 20 days, .mean() means the 21st day will be the mean of the 1st - 20th,
  # 22nd day will be mean of 2nd - 21st, etc. First 20 values will be NaN
  df['20sma'] = df['Close'].rolling(window=20).mean()
  # stddev found through rolling calc + std() from pd
  df['stddev'] = df['Close'].rolling(window=20).std()
  # define upper & lower bands
  df['lowerband'] = df['20sma'] - (2 * df['stddev'])
  df['upperband'] = df['20sma'] + (2 * df['stddev'])
  print(symbol)
  fig = go.Figure(data=[
      go.Candlestick(
        x=df['Date'],
        open=df['Open'],
        high=df['High'],
        low=df['Low'],
        close=df['Close'])
  ])

  fig.show()
  break
