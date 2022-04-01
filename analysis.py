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
  
  ticker_name = TICKER_FILE_NAME.strip('.csv')

  vix = pandas.read_csv(FOLDER_PATH + VIX_FILE_NAME)
  ticker = pandas.read_csv(FOLDER_PATH + TICKER_FILE_NAME)

  # convert Date column values to datetime64
  vix['Date'] = pandas.to_datetime(vix['Date'], format = '%Y-%m-%d')
  vix.set_index(['Date'], inplace=True)

  ticker['Date'] = pandas.to_datetime(ticker['Date'], format = '%Y-%m-%d')
  ticker.set_index(['Date'], inplace=True)

  LAST_PRECOVID_DATE = ticker.index[-1].date()

  # filter rows so that both vix and ticker share the same start and end date
  common_start_date = ticker.index[0].date()
  filtered_vix = vix.query(f"Date >= '{common_start_date}'")
  filtered_ticker = ticker.query(f"Date >= '{common_start_date}'")

  # plot data with matplotlib                            
  filtered_vix['Close'].plot(label = 'VIX (Market Volatility)')
  filtered_ticker['Close'].plot(label = TICKER_FILE_NAME.strip('.csv'))
  plt.title(f'Historical Closing Values\nFrom {common_start_date} to {LAST_PRECOVID_DATE}')
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
  output_df.to_csv ('output_daily_gain_loss.csv', index = False, header=True)

  print(f'\n^Previous Day Gain/Loss % of VIX & {ticker_name}')
  print(f'\n{len(dates)} days analyzed...')
  print(f'Found {yes} days where VIX and {ticker_name} were opposite signs...')
  print(f'Found {no} days where VIX and {ticker_name} were the same signs...')
  print(f'Inverse correlation percentage: {round(yes / len(vix_trend) * 100, 2)}%')

# uncomment to save results to dictionary
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

def show_recent(use_inverse, show_analysis):
  symbols = ['^VIX', 'VFIAX']
  tickers = yf.Tickers(symbols)
  df = tickers.download(group_by='ticker', start='2022-01-01')

  vix = df['^VIX']
  vix_close = vix['Close'].to_list()

  ticker = df['VFIAX']
  ticker_close = ticker['Close'].to_list()

  if show_analysis == True:
    show_gain_loss(vix, ticker, 'VFIAX')

  vix_trend = calculate_gain_loss(vix_close)
  ticker_trend = calculate_gain_loss(ticker_close)

  if use_inverse is True:
    vix_trend = [value * -1 for value in vix_trend]

  dates = vix.index[1:]
  plt.plot(dates, vix_trend, label='VIX')
  plt.plot(dates, ticker_trend, label='VFIAX')
  plt.axhline(0, color='black')
  if use_inverse == True:
      plt.title('VIX (inverse) vs VFIAX performance')
  else:
    plt.title('VIX vs VFIAX performance')

  plt.xlabel('Date')
  plt.ylabel('% Gain / Loss From Previous Day')
  plt.legend(loc="upper right")
  plt.show()