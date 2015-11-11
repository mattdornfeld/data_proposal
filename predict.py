import Quandl
import finsymbols as fin
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from statsmodels.stats.stattools import jarque_bera
import statsmodels.api as sm
from statsmodels import regression

start_date = '2014-07-25'
end_date = '2015-07-25'
offset_start_date = '2014-08-25'
offset_end_date = '2015-08-25'

asset1 = Quandl.get('WIKI/MMM', trim_start= offset_start_date, trim_end=offset_end_date, 
	authtoken=AUTHTOKEN)['Adj. Close'].pct_change()[1:]
treasury_ret = Quandl.get('FRED/DTB3', trim_start= start_date, trim_end=end_date, authtoken=AUTHTOKEN)['VALUE'].pct_change()[1:]
bench = Quandl.get('YAHOO/INDEX_GSPC', trim_start= start_date, trim_end=end_date, authtoken=AUTHTOKEN)['Adjusted Close'].pct_change()[1:]

constant = pd.TimeSeries(np.ones(len(asset1.index)), index=asset1.index)
df = pd.DataFrame({'R1': asset1, 'SPY': bench, 'RF': treasury_ret, 'Constant': constant})
df = df.dropna()

OLS_model = regression.linear_model.OLS(df['R1'], df[['SPY', 'RF', 'Constant']])
fitted_model = OLS_model.fit()
b_SPY = fitted_model.params['SPY']
b_RF = fitted_model.params['RF']
a = fitted_model.params['Constant']

start_date = '2015-07-25'
end_date = '2015-08-25'
last_month_treasury_ret = Quandl.get('FRED/DTB3', trim_start= start_date, trim_end=end_date, authtoken=AUTHTOKEN)['VALUE'].pct_change()[1:]
last_month_bench = Quandl.get('YAHOO/INDEX_GSPC', trim_start= start_date, trim_end=end_date, authtoken=AUTHTOKEN)['Adjusted Close'].pct_change()[1:]

predictions = b_SPY * last_month_bench + b_RF * last_month_treasury_ret + a
predictions.index = predictions.index + pd.DateOffset(months=1)

start_date = '2015-07-25'
end_date = '2015-09-25'
asset1 = Quandl.get('WIKI/MMM', trim_start= start_date, trim_end=end_date, 
	authtoken=AUTHTOKEN)['Adj. Close'].pct_change()[1:]

plt.plot(asset1.index, asset1.values, 'b-')
plt.plot(predictions.index, predictions, 'b--')
plt.title("Return Percentage of MMM")
plt.ylabel('Return Percentage')
plt.legend(['Actual', 'Predicted'])