# -*- coding: utf-8 -*-
"""
Created on Wed Oct 16 12:59:03 2019

author: Sara Miller

compare rainfall forecast to historical rainfall
plot onset date of rainy season
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

chirps = pd.read_csv(r'C:\Users\smille25\Downloads\chirpsprecip.csv')
#nmme = pd.read_csv(r'C:\Users\smille25\Downloads\nmmeprecip.csv')
#model = pd.read_csv(r'C:\Users\smille25\Downloads\modelprecip.csv')

#set date as index and extract month and day values
chirps['Date'] = pd.to_datetime(chirps['Date'])
chirps = chirps.set_index('Date')

#nmme['Date'] = pd.to_datetime(nmme['Date'])
#nmme = nmme.set_index('Date')
#model['Date'] = pd.to_datetime(model['Date'])
#model = model.set_index('Date')
'''
chirps['month'] = chirps.index.month.values
chirps['day'] = chirps.index.day.values
#get average precipitation for each day of the year
chirps = chirps.groupby(['month','day']).mean()
#do the same for forecasted precipitation
nmme['Date'] = pd.to_datetime(nmme['Date'])
nmme = nmme.set_index('Date')
nmme['month'] = nmme.index.month.values
nmme['day'] = nmme.index.day.values
nmme = nmme.groupby(['month','day']).mean()
d = chirps.index.get_level_values('day')
m = chirps.index.get_level_values('month')
'''

#combine dataframes and plot
#combo = pd.concat([nmme.mean(axis=1).rename('NMME'),chirps.mean(axis=1).rename('CHIRPS'), model.mean(axis=1).rename('model')], axis=1)
#fig, ax = plt.subplots(figsize=(10,6))
#combo.last('6M').plot(ax=ax)
chirps = chirps.mean(axis=1)
#chirps.last('8M').plot(ax=ax)

df = chirps.last('12M').rename('chirps')
#df = df.set_index(['date'])
d = df.index.day - np.clip((df.index.day-1) // 10, 0, 2)*10 - 1
date = df.index.values - np.array(d, dtype="timedelta64[D]")
df=df.groupby(date).sum()
df = df.reset_index()
df['c25mm'] = df['chirps']>25.
df['c20mm'] = np.nan
possible = df.index[df['c25mm']==True].tolist()
for p in possible:
    yes = df['chirps'][(p+1):(p+3)].sum()>20
    df['c20mm'][p] = yes

df['cstart'] = np.where((df['c25mm']==True)&(df['c20mm']==True), True, False)
df = df.set_index('index')
print(df)
x1=pd.to_datetime('2018-10-11')
y1=43.356611
x2=pd.to_datetime('2019-04-21')
y2=113.118500
fig, ax = plt.subplots(figsize=(10,6))
df['chirps'].plot(ax=ax)
ax.annotate('SR Start Date', xy=(x1, y1), xytext=(x1, 44),
            arrowprops=dict(facecolor='red', shrink=0.01),)
ax.annotate('LR Start Date', xy=(x2, y2), xytext=(x2, 112),
            arrowprops=dict(facecolor='red', shrink=0.01),)
plt.xlabel('Date')
plt.ylabel('10-day Total Precipitation (mm)')
plt.title('Onset Dates')


