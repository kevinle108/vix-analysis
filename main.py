from cProfile import label
import pandas as pandas
import numpy as np
import matplotlib.pyplot as plt

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

plt.title('VIX (CBOE volatility index)')
plt.xlabel('Date')
plt.ylabel('Index')
plt.legend(loc="upper left")
# plt.plot(vix['Close'], label = 'VIX')
# plt.plot(vtsax['Close'], label = 'VTSAX')

plt.show()

# data visualizations: https://www.analyticsvidhya.com/blog/2021/07/stock-prices-analysis-with-python/
# Check out dataframe.corr() method for correlations