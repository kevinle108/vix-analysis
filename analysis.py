from cProfile import label
import pandas as pandas
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

def show_historical():
  vix = pandas.read_csv('data/raw/vix_daily_2012_2022.csv')
  # print('VIX (fear index):\n\tmax single-day value:', vix.Close.max())
  # print('\tmin single-day value:', vix.Close.min())

  vti = pandas.read_csv('data/raw/vti_daily_2012_2022.csv')
  # print('\nVTI:\n\tmax single-day value:', vti.Close.max())
  # print('\tmin single-day value:', vti.Close.min())

  fskax = pandas.read_csv('data/raw/fskax_daily_2012_2022.csv')
  # print('\nFSKAX:\n\tmax single-day value:', fskax.Close.max())
  # print('\tmin single-day value:', fskax.Close.min())

  vtsax = pandas.read_csv('data/raw/vtsax_daily_2012_2022.csv')
  # print('\nVTSAX:\n\tmax single-day value:', vtsax.Close.max())
  # print('\tmin single-day value:', vtsax.Close.min())

  vix['Date'] = pandas.to_datetime(vix['Date'], format = '%Y-%m-%d')
  vix.set_index(['Date'], inplace=True)
  vix['Close'].plot(label = 'VIX (fear)')

  vti['Date'] = pandas.to_datetime(vti['Date'], format = '%Y-%m-%d')
  vti.set_index(['Date'], inplace=True)
  vti['Close'].plot(label = 'VTI')

  fskax['Date'] = pandas.to_datetime(fskax['Date'], format = '%Y-%m-%d')
  fskax.set_index(['Date'], inplace=True)
  fskax['Close'].plot(label = 'FSKAX')

  vtsax['Date'] = pandas.to_datetime(vtsax['Date'], format = '%Y-%m-%d')
  vtsax.set_index(['Date'], inplace=True)
  vtsax['Close'].plot(label = 'VTSAX')

  plt.title('Historical Market Trends \n(Start of 2012 to End of 2021)')
  plt.xlabel('Date')
  plt.ylabel('Index')
  plt.legend(loc="upper left")
  # plt.plot(vix['Close'], label = 'VIX')
  # plt.plot(vtsax['Close'], label = 'VTSAX')

  plt.show()

  # data visualizations: https://www.analyticsvidhya.com/blog/2021/07/stock-prices-analysis-with-python/
  # Check out dataframe.corr() method for correlations

def show_recent(use_inverse):
  # plots percentage gain and loss

  # fskax = yf.Ticker('FSKAX')
  # vix = yf.Ticker('^VIX')

  symbols = ['^VIX', 'FSKAX']
  tickers = yf.Tickers(symbols)
  df = tickers.download(group_by='ticker', start='2022-01-01')

  vix = df['^VIX']
  vix_close = vix['Close'].to_list()
  vix_trend = []

  fskax = df['FSKAX']
  fskax_close = fskax['Close'].to_list()
  fskax_trend = []

  prev = -1.0
  for cur in vix_close:
    # set up first values
    if prev == -1.0:
      prev = float(cur)
      continue
    gain_loss = float(cur) - prev
    gl_percent = gain_loss / float(cur) * 100
    prev = float(cur)
    if use_inverse == True:
      vix_trend.append(gl_percent * -1)
    else:
      vix_trend.append(gl_percent)

  prev = -1.0
  for cur in fskax_close:
    # set up first values
    if prev == -1.0:
      prev = float(cur)
      continue
    gain_loss = float(cur) - prev
    gl_percent = gain_loss / float(cur) * 100
    prev = float(cur)
    fskax_trend.append(gl_percent)

  dates = df.index[1:]

  plt.plot(dates, vix_trend, label='VIX')
  plt.plot(dates, fskax_trend, label='FSKAX')
  if use_inverse == True:
      plt.title('VIX (inverse) vs FSKAX performance')
  else:
    plt.title('VIX vs FSKAX performance')
  plt.xlabel('Date')
  plt.ylabel('% Gain / Loss From Previous Day')
  plt.legend(loc="upper right")
  plt.show()



  # fskax['Close'].plot(label = 'FSKAX')


  # vix['Date'] = pandas.to_datetime(vix['Date'], format = '%Y-%m-%d')
  # vix.set_index(['Date'], inplace=True)
  # df['^VIX']['Close'].plot(label='VIX')

  # prev = -1
  # diff = -1
  # for close in vix:
  #   # set up first values
  #   if prev == -1:
  #     prev = close
  #     continue
  #   gain_loss = close - prev
  #   prev = close
  #   print(gain_loss / close * 100)