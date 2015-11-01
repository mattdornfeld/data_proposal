import Quandl
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
import finsymbols as fin

def smooth(x, N):
    cumsum = np.cumsum(x) 
    return (cumsum[N:] - cumsum[:-N]) / N 

sp500 = fin.get_sp500_symbols()
symbols = [info['symbol'] for info in sp500]

authtoken = 'axGKor2CVwTbMk45mzzA'
stock_data = Quandl.get('WIKI/'+symbols[0], authtoken=authtoken)
days = np.array([(date - stock_data.index[0]).days for date in stock_data.index ])
adj_close = stock_data['Adj. Close'].values

N = 365
adj_close_avg = smooth(adj_close, N)
#plot(days[N:], adj_close_avg, days[N:], adj_close[N:])
sigma = std(adj_close[N:] - adj_close_avg)
greater = (adj_close[N:] - adj_close_avg) > 2*sigma
less = (adj_close[N:] - adj_close_avg) < -2*sigma
other = np.logical_not(greater + less)

plt.style.use('ggplot')
fig, ax = plt.subplots()
ax.set_title('Adjusted closing prices of ' + symbols[0])
ax.set_xlabel('Days since first recorded price')
ax.set_ylabel('Dollars')
ax.plot(days[N:], adj_close_avg, color='blue', label='Rolling Average (365 day window) of adjusted closing price')
ax.plot(days[N:][greater], adj_close[N:][greater], 'ro', markersize=5, label='High adjusted closing price (> 2 stds)')
ax.plot(days[N:][less], adj_close[N:][less], 'go', markersize=5, label='Low adjusted closing price (> 2 stds)')
ax.legend(loc = 'upper left')

stock_data = Quandl.get('WIKI/'+symbols[1], authtoken=authtoken)
days = np.array([(date - stock_data.index[0]).days for date in stock_data.index ])
adj_close = stock_data['Adj. Close'].values

N = 365
adj_close_avg = smooth(adj_close, N)
sigma = std(adj_close[N:] - adj_close_avg)
greater = (adj_close[N:] - adj_close_avg) > 2*sigma
less = (adj_close[N:] - adj_close_avg) < -2*sigma
other = np.logical_not(greater + less)

plt.style.use('ggplot')
fig, ax = plt.subplots()
ax.set_title('Adjusted closing prices of ' + symbols[1])
ax.set_xlabel('Days since first recorded price')
ax.set_ylabel('Dollars')
ax.plot(days[N:], adj_close_avg, color='blue', label='Rolling Average (365 day window) of adjusted closing price')
ax.plot(days[N:][greater], adj_close[N:][greater], 'ro', markersize=5, label='High adjusted closing price (> 2 stds)')
ax.plot(days[N:][less], adj_close[N:][less], 'go', markersize=5, label='Low adjusted closing price (> 2 stds)')
ax.legend(loc = 'upper left')

