from cProfile import label
import yfinance as yf
import pandas as pandas
import matplotlib.pyplot as plt

# plots percentage gain and loss

# fskax = yf.Ticker('FSKAX')
# vix = yf.Ticker('^VIX')

# print('\nVIX')
# print(vix.history())

symbols = ['^VIX', 'FSKAX']
tickers = yf.Tickers(symbols)
df = tickers.download(group_by='ticker', start='2022-01-01', end='2022-03-11')

# vix['Close'].plot(label = 'VIX (fear)')
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

plt.plot(
  dates, vix_trend,
  dates, fskax_trend,
)

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

