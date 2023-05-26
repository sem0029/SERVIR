# -*- coding: utf-8 -*-
"""
Created on Wed Sep 21 14:49:58 2022

author: Sara Miller
get regression plots for cumulative vic variables compared to MOA yields
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import sys
import datetime
import seaborn as sns
import scipy.stats as stats
import scipy as sp
from pylab import figure, text

variables = ['evap','net_long', 'net_short', 'rootmoist', 'rainf', 'tmax', 'tmin', 'soil_moist_1','soil_moist_2','soil_moist_3']


#csv containing cumulative vic variables per forecast date
forecast = pd.read_csv(r'C:\Users\smille25\Downloads\forecasts\updatedforecasts\vicforecast.csv')
#add season information
forecast['Year'] = 2000+(forecast['forecast_date'].str[-2:]).astype(int)
forecast['Month'] = forecast['forecast_date'].str[:2]
forecast['Day'] = forecast['forecast_date'].str[3:5]
forecast['season1'] = np.nan
forecast['season1'].loc[(forecast['Month'].astype(int)>9)|(forecast['Month'].astype(int)<3)] = 'SR'
forecast['season1'].loc[(forecast['Month'].astype(int)>2)&(forecast['Month'].astype(int)<10)] = 'LR'
forecast['Season'] = np.nan
forecast['Season'] = forecast['Year'].astype(str)+' '+forecast['season1']
forecast['Season'].loc[(forecast['Month'].astype(int)<3)] = (forecast['Year'] - 1).astype(str)+' '+forecast['season1']

counties = ['Baringo', 'Bomet', 'Bungoma', 'Busia',
       'Eg Tanariver', 'Elgeyo Marakwet', 'Embu', 'Garissa', 'Homa Bay',
       'Isiolo', 'Kajiado', 'Kakamega', 'Kericho', 'Kiambu', 'Kilifi',
       'Kirinyaga', 'Kisii', 'Kisumu', 'Kitui', 'Kwale', 'Laikipia', 'Lamu',
       'Machakos', 'Makueni', 'Mandera ', 'Marsabit', 'Meru', 'Migori',
       'Mombasa', 'Murang\'a', 'Nairobi', 'Nakuru', 'Nandi', 'Narok', 'Nyamira',
       'Nyandarua', 'Nyeri', 'Samburu', 'Siaya', 'Taita Taveta', 'Tana River',
       'Tharaka Nithi', 'Trans Nzoia', 'Turkana', 'Uasin Gishu', 'Vihiga',
       'Wajir', 'West Pokot']

#add in MOA measured yield to each matching season/year
moalong = pd.DataFrame()
for dates in forecast.forecast_date.unique():
    moa = pd.read_csv(r'C:\Users\smille25\Downloads\Kenya_seasonal_yield_MOA.csv')
    moa['Year'] = (moa['Season'].str[:4]).astype(int)
    moa = moa.set_index(['Year','season1','Season'])
    #counties = list(forecast.cname.unique())#change this to only dssat counties
    # convert to kg/ha for selected counties
    moa = (moa[counties] * 1000).stack()
    moa = moa.rename('MOA')
    moa.index.names = ['Year','season1','Season','cname']
    moa = moa.loc[~moa.index.duplicated(keep='first')]
    moa = moa.reset_index()
    moa['forecast_date'] = dates
    moalong = moalong.append(moa)

forecast = forecast.set_index(['Season','cname','forecast_date'])
moalong = moalong.set_index(['Season','cname','forecast_date'])
moalong = moalong.loc[moalong['MOA']>0]
moalong = moalong.drop(columns=['Year','season1'])
df = pd.concat([forecast,moalong],axis=1,join='inner')
df = df.reset_index()
df['month/day'] = df['Month'].astype(str)+'/'+df['Day'].astype(str)


rdf = pd.DataFrame()
column = 0
for var in variables:
    row = 0
    for date in df['month/day'].unique():
        df1 = df.loc[df['month/day']==date]

        r, p = sp.stats.pearsonr(df1['MOA'], df1[var])
        r_squared = r*r
        df2 = pd.DataFrame(data={'correlation':[r],'variable':[var],'date':[date]})
        rdf = pd.concat([rdf,df2])
        row = row+1
    column = column+1


labels = ['Evapotranspiration','Net Longwave Radiation', 'Net Shortwave Radiation', 'Precipitation', 'Maximum Temperature', 'Mimimum Temperature', 'Surface Soil Moisture','Layer 2 Soil Moisture','Layer 3 Soil Moisture']
variables = ['evap','net_long', 'net_short', 'rainf', 'tmax', 'tmin', 'soil_moist_1','soil_moist_2','soil_moist_3']

#plot correlations of each variable with final yield by forecast date
fig, ax = plt.subplots(figsize=(8,4))
for i,var in enumerate(variables):
    df3 = rdf.loc[rdf['variable']==var]
    #insert break in graph between lr and sr seasons
    df2 = pd.DataFrame(data={'correlation':[np.nan],'variable':[var],'date':['10/01']})
    df3 = pd.concat([df3,df2])
    df3 = df3.set_index('date')
    #reorder so long rains and short rains are grouped together
    df3 = df3.reindex(['03/15','03/30','04/15','04/30','05/15','05/30','06/15',
                       '06/30','07/15','07/30','08/15','08/30','09/15','09/30','10/01','10/15','10/30',
                       '11/15','11/30','12/15','12/30','01/15','01/30','02/15','02/30'])
    print(df3)
    df3['correlation'].plot(ax=ax,label=labels[i])
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5))
plt.xlabel('Month/Day')
plt.ylabel('Correlation')
plt.tight_layout()
plt.show()
plt.savefig(r'C:\Users\smille25\Downloads\forecasts\updatedforecasts\viccorrelations.png')
