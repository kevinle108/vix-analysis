from cProfile import label
from turtle import color
from numpy import diff
import pandas as pandas
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf

def convert_values_to_float(ticker_close_list):
  return [float(value) for value in ticker_close_list]

def calculate_gain_loss(ticker_close_list):
  gain_loss = []
  prev = -1.0
  for cur in ticker_close_list:
    # set up first values
    if prev == -1.0:
      prev = cur
      continue
    difference = cur - prev
    gl_percent = difference / cur * 100
    prev = cur
    gain_loss.append(gl_percent)
  return gain_loss

def show_historical():
  vix_file_path = 'data/raw/vix_daily_2012_2022.csv'
  vix = pandas.read_csv(vix_file_path)
  # print('VIX (fear index):\n\tmax single-day value:', vix.Close.max())
  # print('\tmin single-day value:', vix.Close.min())

  # vti = pandas.read_csv('data/raw/vti_daily_2012_2022.csv')
  # print('\nVTI:\n\tmax single-day value:', vti.Close.max())
  # print('\tmin single-day value:', vti.Close.min())

  # vtsax = pandas.read_csv('data/raw/vtsax_daily_2012_2022.csv')
  # print('\nvtsax:\n\tmax single-day value:', vtsax.Close.max())
  # print('\tmin single-day value:', vtsax.Close.min())

  vtsax = pandas.read_csv('data/raw/vtsax_daily_2012_2022.csv')
  # print('\nVTSAX:\n\tmax single-day value:', vtsax.Close.max())
  # print('\tmin single-day value:', vtsax.Close.min())

  vix['Date'] = pandas.to_datetime(vix['Date'], format = '%Y-%m-%d')
  vix.set_index(['Date'], inplace=True)
  vix['Close'].plot(label = 'VIX (fear)')

  # vti['Date'] = pandas.to_datetime(vti['Date'], format = '%Y-%m-%d')
  # vti.set_index(['Date'], inplace=True)
  # vti['Close'].plot(label = 'VTI')

  # vtsax['Date'] = pandas.to_datetime(vtsax['Date'], format = '%Y-%m-%d')
  # vtsax.set_index(['Date'], inplace=True)
  # vtsax['Close'].plot(label = 'VTSAX')

  vtsax['Date'] = pandas.to_datetime(vtsax['Date'], format = '%Y-%m-%d')
  vtsax.set_index(['Date'], inplace=True)
  vtsax['Close'].plot(label = 'VTSAX')

  plt.title('Historical Market Trends \n(Start of 2012 to End of 2021)')
  plt.xlabel('Date')
  plt.ylabel('Index')
  plt.legend(loc="upper left")
  # plt.plot(vix['Close'], label = 'VIX')
  # plt.plot(vtsax['Close'], label = 'VTSAX')

  # plt.show()

  vix_close = vix['Close'].to_list()
  vix_close = convert_values_to_float(vix_close)
  vix_trend = calculate_gain_loss(vix_close)
  print('historical vix length', len(vix_trend))
  
  vtsax_close = convert_values_to_float(vtsax['Close'].to_list())
  vtsax_trend = calculate_gain_loss(vtsax_close)
  print('historical fskax length', len(vtsax_close))

  yes = 0
  no = 0
  for vix,vtsax in zip(vix_trend, vtsax_trend):
    if (np.sign(vix) != np.sign(vtsax)):
      yes += 1
      print(vix, vtsax, 'yes')
    else:
      no += 1
      print(vix, vtsax, 'no')
  
  print(f'length of lists: {len(vix_trend)}')
  print(f'yes: {yes}')
  print(f'no: {no}')
  print(f'sum of yes & no: {yes + no}')
  print(f'yes percentage: {round(yes / len(vix_trend) * 100, 2)}%')
  


  # data visualizations: https://www.analyticsvidhya.com/blog/2021/07/stock-prices-analysis-with-python/
  # Check out dataframe.corr() method for correlations

def show_recent(use_inverse):
  # plots percentage gain and loss

  # vtsax = yf.Ticker('VTSAX')
  # vix = yf.Ticker('^VIX')

  symbols = ['^VIX', 'VTSAX']
  tickers = yf.Tickers(symbols)
  df = tickers.download(group_by='ticker', start='2022-01-01')

  vix = df['^VIX']
  vix_close = vix['Close'].to_list()
  vix_trend = []
  print('vix_close raw:', vix_close)

  vtsax = df['VTSAX']
  vtsax_close = vtsax['Close'].to_list()

  vix_close = convert_values_to_float(vix_close)
  vix_trend = calculate_gain_loss(vix_close)
  if use_inverse is True:
    vix_trend = [value * -1 for value in vix_trend]
  # prev = -1.0
  # for cur in vix_close:
  #   # set up first values
  #   if prev == -1.0:
  #     prev = float(cur)
  #     continue
  #   gain_loss = float(cur) - prev
  #   gl_percent = gain_loss / float(cur) * 100
  #   prev = float(cur)
  #   if use_inverse == True:
  #     vix_trend.append(gl_percent * -1)
  #   else:
  #     vix_trend.append(gl_percent)

  vtsax_trend = calculate_gain_loss(vtsax_close)

  dates = df.index[1:]

  plt.plot(dates, vix_trend, label='VIX')
  plt.plot(dates, vtsax_trend, label='VTSAX')
  plt.axhline(0, color='black')
  print('vix', vix_trend)
  print('VTSAX', vtsax_trend)

  # x_day = []
  # day = 0
  # for date in range(len(dates)):
  #   x_day.append(day)
  #   day = day + 1
  # # x_day.pop(0)
  # print(x_day)
  # vix_deriv = diff(vix_trend)/diff(x_day)
  # vtsax_deriv = diff(vtsax_trend)/diff(x_day)
  # new_dates = dates[1:]
  # plt.plot(new_dates, vix_deriv, label='vix_deriv')
  # plt.plot(new_dates, vtsax_deriv, label='vtsax_deriv')

  if use_inverse == True:
      plt.title('VIX (inverse) vs VTSAX performance')
  else:
    plt.title('VIX vs VTSAX performance')


  plt.xlabel('Date')
  plt.ylabel('% Gain / Loss From Previous Day')
  plt.legend(loc="upper right")
  plt.show()



  # vtsax['Close'].plot(label = 'VTSAX')


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
