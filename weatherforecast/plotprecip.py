# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 14:16:43 2020

author: Sara Miller
plot 10 day precipitation for chirps and nmme at different lead times
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

chirps = pd.read_csv(r'C:\Users\smille25\Downloads\forecasts\precip\chirpsprecip.csv')
chirp = pd.read_csv(r'C:\Users\smille25\Downloads\forecasts\precip\chirpprecip.csv')
gefs = pd.read_csv(r'C:\Users\smille25\Downloads\forecasts\precip\chirpsgefsprecip.csv')
nmme = pd.read_csv(r'C:\Users\smille25\Downloads\forecasts\precip\nmmeall.csv')
nmme0 = nmme.loc[nmme['Months']==0].drop(columns=['Months','forecast_date'])
nmme1 = nmme.loc[nmme['Months']==1].drop(columns=['Months','forecast_date'])
nmme2 = nmme.loc[nmme['Months']==2].drop(columns=['Months','forecast_date'])
nmme3 = nmme.loc[nmme['Months']==3].drop(columns=['Months','forecast_date'])
nmme4 = nmme.loc[nmme['Months']==4].drop(columns=['Months','forecast_date'])
nmme5 = nmme.loc[nmme['Months']==5].drop(columns=['Months','forecast_date'])
nmme6 = nmme.loc[nmme['Months']==6].drop(columns=['Months','forecast_date'])

# set dataframe index as date
#chirps = chirps.set_index('Date')['Embu'].rename('chirps')
chirps['Date'] = pd.to_datetime(chirps['Date'], format='%Y/%m/%d')
chirps = chirps.groupby(pd.Grouper(key="Date", freq="10D")).sum()['Embu'].rename('CHIRPS')
chirp['Date'] = pd.to_datetime(chirp['Date'], format='%Y/%m/%d')
chirp = chirp.groupby(pd.Grouper(key="Date", freq="10D")).sum()['Embu'].rename('CHIRP')
gefs['Date'] = pd.to_datetime(gefs['Date'], format='%Y/%m/%d')
gefs = gefs.groupby(pd.Grouper(key="Date", freq="10D")).sum()['Embu'].rename('CHIRPS-GEFS')
nmme0['Date'] = pd.to_datetime(nmme0['Date'], format='%m/%d/%Y')
nmme0 = (nmme0.groupby(pd.Grouper(key="Date", freq="10D")).sum())['Embu'].rename('NMME Current Month')
nmme1['Date'] = pd.to_datetime(nmme1['Date'], format='%m/%d/%Y')
nmme1 = (nmme1.groupby(pd.Grouper(key="Date", freq="10D")).sum())['Embu'].rename('NMME 1 Month Forecast')
nmme2['Date'] = pd.to_datetime(nmme2['Date'], format='%m/%d/%Y')
nmme2 = (nmme2.groupby(pd.Grouper(key="Date", freq="10D")).sum())['Embu'].rename('NMME 2 Month Forecast')
nmme3['Date'] = pd.to_datetime(nmme3['Date'], format='%m/%d/%Y')
nmme3 = (nmme3.groupby(pd.Grouper(key="Date", freq="10D")).sum())['Embu'].rename('NMME 3 Month Forecast')
nmme4['Date'] = pd.to_datetime(nmme4['Date'], format='%m/%d/%Y')
nmme4 = (nmme4.groupby(pd.Grouper(key="Date", freq="10D")).sum())['Embu'].rename('NMME 4 Month Forecast')
nmme5['Date'] = pd.to_datetime(nmme5['Date'], format='%m/%d/%Y')
nmme5 = (nmme5.groupby(pd.Grouper(key="Date", freq="10D")).sum())['Embu'].rename('NMME 5 Month Forecast')
nmme6['Date'] = pd.to_datetime(nmme6['Date'], format='%m/%d/%Y')
nmme6 = (nmme6.groupby(pd.Grouper(key="Date", freq="10D")).sum())['Embu'].rename('NMME 6 Month Forecast')

#print(chirps,nmme2)
r'''chirp = chirp.set_index('Date')['Embu'].rename('chirp')
gefs = gefs.set_index('Date')['Embu'].rename('chirps gefs')
nmme2 = nmme2.set_index('Date')['Embu'].rename('nmme 2')
nmme2 = nmme2.reset_index()
nmme2 = nmme2.groupby(['Date']).mean()
nmme3 = nmme3.set_index('Date')['Embu'].rename('nmme 3')
nmme3 = nmme3.reset_index()
nmme3 = nmme3.groupby(['Date']).mean()
nmme4 = nmme4.set_index('Date')['Embu'].rename('nmme 4')
nmme4 = nmme4.reset_index()
nmme4 = nmme4.groupby(['Date']).mean()
nmme5 = nmme5.set_index('Date')['Embu'].rename('nmme 5')
nmme5 = nmme5.reset_index()
nmme5 = nmme5.groupby(['Date']).mean()
nmme6 = nmme6.set_index('Date')['Embu'].rename('nmme 6')
nmme6 = nmme6.reset_index()
nmme6 = nmme6.groupby(['Date']).mean()
nmme7 = nmme7.set_index('Date')['Embu'].rename('nmme 7')
nmme7 = nmme7.reset_index()
nmme7 = nmme7.groupby(['Date']).mean()
nmme8 = nmme8.set_index('Date')['Embu'].rename('nmme 8')
nmme8 = nmme8.reset_index()
nmme8 = nmme8.groupby(['Date']).mean()
'''
combo = pd.concat([chirps,nmme0,nmme2,nmme3,nmme4,nmme5,nmme6],axis=1)
print(combo)
combo1 = combo#.iloc[7:20]
# save dataframe as csv
#df.to_csv('/home/Socrates/rheas/RHEAS/Kenya_VIC/forecastprecip.csv') # change path to wherever you want it saved
# plot time series for a selected county
#combo1.plot(lw=1)
fig, ax = plt.subplots(figsize=(6,4))
for col in combo1.columns:
        plot_data = combo1[col].dropna()
        ax.plot(plot_data.index.values, plot_data.values, label=col)

plt.xlabel('Date')
plt.ylabel('Precipitation (mm)')
plt.title('10 Day Total Precipitation')
plt.legend()
plt.show()
