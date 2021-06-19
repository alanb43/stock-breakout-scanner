import os
import pandas as pd
import plotly.graph_objects as go

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
  df['lower_bollinger'] = df['20sma'] - (2 * df['stddev'])
  df['upper_bollinger'] = df['20sma'] + (2 * df['stddev'])
  # define true range and average true range
  df['TR'] = abs(df['High'] - df['Low'])
  df['ATR'] = df['TR'].rolling(window=20).mean()
  # define upper & lower keltner channels (multipliers can be variable)
  df['lower_keltner'] = df['20sma'] - (1.5 * df['ATR'])
  df['upper_keltner'] = df['20sma'] + (1.5 * df['ATR'])

  # determine if a stock is in a squeeze (based on data timeframe)
  def in_squeeze(df):
    return df['lower_bollinger'] > df['lower_keltner'] and df['upper_bollinger'] < df['upper_keltner']

  # function to graph candlesticks, bollinger bands, keltneer channels
  def graph(df):
    candlestick = go.Candlestick(x=df['Date'], open=df['Open'], high=df['High'], low=df['Low'], close=df['Close'])
    upper_band = go.Scatter(x=df['Date'], y=df['upper_bollinger'], name='Upper Bollinger Band', line={'color': 'blue'})
    lower_band = go.Scatter(x=df['Date'], y=df['lower_bollinger'], name='Lower Bollinger Band', line={'color': 'blue'})
    upper_kc = go.Scatter(x=df['Date'], y=df['upper_keltner'], name='Upper Keltner Channel', line={'color': 'orange'})
    lower_kc = go.Scatter(x=df['Date'], y=df['lower_keltner'], name='Lower Keltner Channel', line={'color': 'orange'})

    fig = go.Figure(data=[candlestick, upper_band, lower_band, upper_kc, lower_kc])
    fig.layout.xaxis.type = 'category' # gets rid of weekend spaces with no data
    fig.layout.xaxis.rangeslider.visible = False
    fig.show()

  # applies function to dataframe 
  df['squeeze_on'] = df.apply(in_squeeze, axis=1)

  # check if we're in a squeeze in the last row of the df
  if df.iloc[-1]['squeeze_on']:
    print(f'{symbol} is in the squeeze')
    graph(df)
  elif df.iloc[-3]['squeeze_on'] and not df.iloc[-1]['squeeze_on']:
    print(f'{symbol} is coming out of the squeeze')
    graph(df)
  