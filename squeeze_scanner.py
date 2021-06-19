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

  Instead of bands tracking the stddev's from the sma, we'll have them be a multiple of the average
  true range (ATR) above/below the middle line/channel, which we'll use the 20 day sma for (though
  the official definition uses the 20 day Exponential MA)

When Bollinger Bands are within Keltner Channels (squeezed), low volatility is indicated. We then are 
looking for a breakout

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
  # define upper & lower bollinger bands (multipliers can be variable)
  df['lower_band'] = df['20sma'] - (2 * df['stddev'])
  df['upper_band'] = df['20sma'] + (2 * df['stddev'])
  # define true range and average true range
  df['TR'] = abs(df['High'] - df['Low'])
  df['ATR'] = df['TR'].rolling(window=20).mean()
  # define upper & lower keltner channels (multipliers can be variable)
  df['lower_keltner'] = df['20sma'] - (1.5 * df['ATR'])
  df['upper_keltner'] = df['20sma'] + (1.5 * df['ATR'])

  # candlestick = go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])
  # upper_band = go.Scatter(x=df['Date'], y=df['upperband'], name='Upper Bollinger Band', line={'color': 'blue'})
  # lower_band = go.Scatter(x=df['Date'], y=df['lowerband'], name='Lower Bollinger Band', line={'color': 'blue'})
  # upper_kc = go.Scatter(x=df['Date'], y=df['upper_keltner'], name='Upper Keltner Channel', line={'color': 'orange'})
  # lower_kc = go.Scatter(x=df['Date'], y=df['lower_keltner'], name='Lower Keltner Channel', line={'color': 'orange'})

  # fig = go.Figure(data=[candlestick, upper_band, lower_band, upper_kc, lower_kc])
  # fig.layout.xaxis.type = 'category' # gets rid of weekend spaces with no data
  # fig.layout.xaxis.rangeslider.visible = False

  # fig.show()
  break
