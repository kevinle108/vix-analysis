from cProfile import label
from turtle import color
from matplotlib import dates
from numpy import diff
import pandas as pandas
import numpy as np
import matplotlib.pyplot as plt
import yfinance as yf
import colorama
from colorama import Fore

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
  FOLDER_PATH = 'data/historical/'
  VIX_FILE_NAME = '^VIX.csv'
  TICKER_FILE_NAME= 'VFIAX.csv'
  LAST_PRECOVID_DATE = '2019-12-31'
  ticker_name = TICKER_FILE_NAME.strip('.csv')

  vix = pandas.read_csv(FOLDER_PATH + VIX_FILE_NAME)
  ticker = pandas.read_csv(FOLDER_PATH + TICKER_FILE_NAME)

  # convert Date column values to datetime64
  vix['Date'] = pandas.to_datetime(vix['Date'], format = '%Y-%m-%d')
  vix.set_index(['Date'], inplace=True)

  ticker['Date'] = pandas.to_datetime(ticker['Date'], format = '%Y-%m-%d')
  ticker.set_index(['Date'], inplace=True)

  

  # filter rows so that both vix and ticker share the same start and end date
  common_start_date = ticker.index[0].date()
  filtered_vix = vix.query(f"Date >= '{common_start_date}' and Date <= '{LAST_PRECOVID_DATE}'")
  filtered_ticker = ticker.query(f"Date >= '{common_start_date}' and Date <= '{LAST_PRECOVID_DATE}'")
  print(filtered_vix)

  # plot data with matplotlib                            
  filtered_vix['Close'].plot(label = 'VIX (Market Volatility)')
  filtered_ticker['Close'].plot(label = TICKER_FILE_NAME.strip('.csv'))
  plt.title(f'Historical Trends, Pre-COVID\nFrom {common_start_date} to {LAST_PRECOVID_DATE}')
  plt.xlabel('Date')
  plt.ylabel('Index')
  plt.legend(loc="upper right")
  plt.show()
  show_gain_loss(filtered_vix, filtered_ticker, ticker_name)


def analyze_correlation(vix_trend, ticker_trend, ticker_name, dates):
  yes = 0
  no = 0

  message = ''
  output_dates = []
  output_vix = []
  output_ticker = []
  output_inverse_correlation = []

  for i, date in enumerate(dates):
    vix_val = f'{(round(vix_trend[i],3))}%'
    ticker_val = f'{(round(ticker_trend[i],3))}%'
    
    if vix_trend[i] > 0:
      vix_val = '+' + vix_val
    if ticker_trend[i] > 0:
      ticker_val = '+' + ticker_val

    # add to output data
    output_dates.append(f'{date.date()}')
    output_vix.append(f'{vix_val}')
    output_ticker.append(f'{ticker_val}')

    # print to console a message for each day  
    vix_val = (vix_val + ' ').ljust(10)
    ticker_val = (ticker_val + ' ').ljust(10)
    message = f'Date: {date.date()}   VIX: {vix_val} {ticker_name}: {ticker_val}'
    if (np.sign(vix_trend[i]) != np.sign(ticker_trend[i])):
      yes += 1
      output_inverse_correlation.append('yes')
      print(Fore.GREEN, message, Fore.RESET)
    else:
      no += 1
      output_inverse_correlation.append('no')
      print(Fore.RED, message,  Fore.RESET)
    
  output_data = {
    'Date': output_dates,
    'VIX': output_vix,
    f'{ticker_name}': output_ticker,
    'Inverse_Correlated?': output_inverse_correlation
  }
  output_df = pandas.DataFrame(output_data, columns=['Date', 'VIX', ticker_name, 'Inverse_Correlated?'])
  output_df.to_csv ('output/historical_gain_loss.csv', index = False, header=True)

  print(f'\n^Previous Day Gain/Loss % of VIX & {ticker_name}')
  print(f'\n{len(dates)} days analyzed...')
  print(f'Found {yes} days where VIX and {ticker_name} were opposite signs...')
  print(f'Inverse correlation percentage: {round(yes / len(vix_trend) * 100, 2)}%')

# used for saving results to dictionary
# def correlation_dict(vix_trend, ticker_trend, ticker_name, dates):
#   result = {}
#   for i, date in enumerate(dates):
#     result[date.strftime('%m/%d/%Y')] = {
#       '^VIX': vix_trend[i],
#       ticker_name: ticker_trend[i]
#     }
#   print(result)

def show_gain_loss(vix, ticker, ticker_name):
  dates = vix.index[1:]
  vix_close = convert_values_to_float(vix['Close'].to_list())
  vix_trend = calculate_gain_loss(vix_close)
  ticker_close = convert_values_to_float(ticker['Close'].to_list())
  ticker_trend = calculate_gain_loss(ticker_close)

  analyze_correlation(vix_trend, ticker_trend, ticker_name, dates)

  # plt.plot(dates, vix_trend, label='VIX')
  # plt.plot(dates, ticker_trend, label='Ticker')
  # plt.axhline(0, color='black')
  # plt.title(f'Daily Performance of VIX vs {ticker_name}')
  # plt.xlabel('Date')
  # plt.ylabel('% Gain / Loss From Previous Day')
  # plt.legend(loc="upper right")
  # plt.show()
  

def show_recent(use_inverse):
  # plots percentage gain and loss

  # ticker = yf.Ticker('VTSAX')
  # vix = yf.Ticker('^VIX')

  symbols = ['^VIX', 'VTSAX']
  tickers = yf.Tickers(symbols)
  df = tickers.download(group_by='ticker', start='2022-01-01')

  vix = df['^VIX']
  vix_close = vix['Close'].to_list()

  ticker = df['VTSAX']
  ticker_close = ticker['Close'].to_list()

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

  ticker_trend = calculate_gain_loss(ticker_close)

  yes = 0
  no = 0
  for vix,ticker in zip(vix_trend, ticker_trend):
    if (np.sign(vix) != np.sign(ticker)):
      yes += 1
      print(f'vix: {vix}', ticker, 'yes')
    else:
      no += 1
      print(vix, ticker, 'no')

  dates = df.index[1:]
  print(f'length of lists:')
  print(len(dates))
  print(len(vix_trend))
  print(len(ticker_trend))
  print(f'yes: {yes}')
  print(f'no: {no}')
  print(f'sum of yes & no: {yes + no}')
  print(f'yes percentage: {round(yes / len(vix_trend) * 100, 2)}%')

  plt.plot(dates, vix_trend, label='VIX')
  plt.plot(dates, ticker_trend, label='VTSAX')
  plt.axhline(0, color='black')

  # x_day = []
  # day = 0
  # for date in range(len(dates)):
  #   x_day.append(day)
  #   day = day + 1
  # # x_day.pop(0)
  # print(x_day)
  # vix_deriv = diff(vix_trend)/diff(x_day)
  # ticker_deriv = diff(ticker_trend)/diff(x_day)
  # new_dates = dates[1:]
  # plt.plot(new_dates, vix_deriv, label='vix_deriv')
  # plt.plot(new_dates, ticker_deriv, label='ticker_deriv')

  if use_inverse == True:
      plt.title('VIX (inverse) vs VTSAX performance')
  else:
    plt.title('VIX vs VTSAX performance')


  plt.xlabel('Date')
  plt.ylabel('% Gain / Loss From Previous Day')
  plt.legend(loc="upper right")
  plt.show()



  # ticker['Close'].plot(label = 'VTSAX')


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
