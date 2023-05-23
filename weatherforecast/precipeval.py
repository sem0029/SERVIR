# -*- coding: utf-8 -*-
"""
Created on Thu May 13 13:19:23 2021

author: Sara Miller
evaluate stats (rmse,bias,corr) of forecasts at different lead times
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys
import glob


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

mo1 = 1
mo2 = 3
chirps['Date'] = pd.to_datetime(chirps['Date'], format='%Y/%m/%d')
chirps=chirps.set_index('Date')
chirps=chirps.loc[(chirps.index.month>=mo1)&(chirps.index.month<mo2)]
#chirps = chirps.groupby(pd.Grouper(key="Date", freq="10D")).sum()
chirp['Date'] = pd.to_datetime(chirp['Date'], format='%Y/%m/%d')
chirp=chirp.set_index('Date')
chirp=chirp.loc[(chirp.index.month>=mo1)&(chirp.index.month<mo2)]
#chirp = chirp.groupby(pd.Grouper(key="Date", freq="10D")).sum()
gefs['Date'] = pd.to_datetime(gefs['Date'], format='%Y/%m/%d')
gefs=gefs.set_index('Date')
gefs=gefs.loc[(gefs.index.month>=mo1)&(gefs.index.month<mo2)]
#gefs = gefs.groupby(pd.Grouper(key="Date", freq="10D")).sum()
nmme0['Date'] = pd.to_datetime(nmme0['Date'], format='%m/%d/%Y')
nmme0=nmme0.set_index('Date')
nmme0=nmme0.loc[(nmme0.index.month>=mo1)&(nmme0.index.month<mo2)]
#nmme0 = nmme0.groupby(pd.Grouper(key="Date", freq="10D")).sum()
nmme1['Date'] = pd.to_datetime(nmme1['Date'], format='%m/%d/%Y')
nmme1=nmme1.set_index('Date')
nmme1=nmme1.loc[(nmme1.index.month>=mo1)&(nmme1.index.month<mo2)]
#nmme1 = nmme1.groupby(pd.Grouper(key="Date", freq="10D")).sum()
nmme2['Date'] = pd.to_datetime(nmme2['Date'], format='%m/%d/%Y')
#nmme2=nmme2.iloc[9:]
nmme2=nmme2.set_index('Date')
nmme2=nmme2.loc[(nmme2.index.month>=mo1)&(nmme2.index.month<mo2)]
#nmme2 = nmme2.groupby(pd.Grouper(key="Date", freq="10D")).sum()
nmme3['Date'] = pd.to_datetime(nmme3['Date'], format='%m/%d/%Y')
#nmme3=nmme3.iloc[9:]
nmme3=nmme3.set_index('Date')
nmme3=nmme3.loc[(nmme3.index.month>=mo1)&(nmme3.index.month<mo2)]
#nmme3 = nmme3.groupby(pd.Grouper(key="Date", freq="10D")).sum()
nmme4['Date'] = pd.to_datetime(nmme4['Date'], format='%m/%d/%Y')
#nmme4=nmme4.iloc[8:]
nmme4=nmme4.set_index('Date')
nmme4=nmme4.loc[(nmme4.index.month>=mo1)&(nmme4.index.month<mo2)]
#nmme4 = nmme4.groupby(pd.Grouper(key="Date", freq="10D")).sum()
nmme5['Date'] = pd.to_datetime(nmme5['Date'], format='%m/%d/%Y')
#nmme5=nmme5.iloc[8:]
nmme5=nmme5.set_index('Date')
nmme5=nmme5.loc[(nmme5.index.month>=mo1)&(nmme5.index.month<mo2)]
#nmme5 = nmme5.groupby(pd.Grouper(key="Date", freq="10D")).sum()
nmme6['Date'] = pd.to_datetime(nmme6['Date'], format='%m/%d/%Y')
#nmme6=nmme6.iloc[7:]
nmme6=nmme6.set_index('Date')
nmme6=nmme6.loc[(nmme6.index.month>=mo1)&(nmme6.index.month<mo2)]
#nmme6 = nmme6.groupby(pd.Grouper(key="Date", freq="10D")).sum()
#print(chirps,chirp,gefs,nmme0)


#calculate RMSE
chirprmse = np.sqrt(((chirp-chirps)**2).mean()).rename('CHIRP RMSE')
#calculate bias
chirpbias = (chirp-chirps).mean().rename('CHIRP Bias')
#calculate correlation
chirpcorr = chirps.corrwith(chirp, axis=0).rename('CHIRP Correlation')
#print('CHIRP')
#print(chirprmse)

#calculate RMSE
gefsrmse = np.sqrt(((gefs-chirps)**2).mean()).rename('CHIRPS-GEFS RMSE')
#calculate bias
gefsbias = (gefs-chirps).mean().rename('CHIRPS-GEFS Bias')
#calculate correlation
gefscorr = chirps.corrwith(gefs, axis=0).rename('CHIRPS-GEFS Correlation')
#print('CHIRPS-GEFS')
#print(gefsrmse)

#calculate RMSE
nmme0rmse = np.sqrt(((nmme0-chirps)**2).mean()).rename('NMME 0 Month Lead RMSE')
#calculate bias
nmme0bias = (nmme0-chirps).mean().rename('NMME 0 Month Lead Bias')
#calculate correlation
nmme0corr = chirps.corrwith(nmme0, axis=0).rename('NMME 0 Month Lead Correlation')
#print('NMME Current Month Forecast')
#print(nmme0rmse)

#calculate RMSE
nmme1rmse = np.sqrt(((nmme1-chirps)**2).mean()).rename('NMME 1 Month Lead RMSE')
#calculate bias
nmme1bias = (nmme1-chirps).mean().rename('NMME 1 Month Lead Bias')
#calculate correlation
nmme1corr = chirps.corrwith(nmme1, axis=0).rename('NMME 1 Month Lead Correlation')
#print('NMME 1 Month Forecast')
#print(nmme1rmse)

#calculate RMSE
nmme2rmse = np.sqrt(((nmme2-chirps)**2).mean()).rename('NMME 2 Month Lead RMSE')
#calculate bias
nmme2bias = (nmme2-chirps).mean().rename('NMME 2 Month Lead Bias')
#calculate correlation
nmme2corr = chirps.corrwith(nmme2, axis=0).rename('NMME 2 Month Lead Correlation')
#print('NMME 2 Month Forecast')
#print(nmme2rmse)

#calculate RMSE
nmme3rmse = np.sqrt(((nmme3-chirps)**2).mean()).rename('NMME 3 Month Lead RMSE')
#calculate bias
nmme3bias = (nmme3-chirps).mean().rename('NMME 3 Month Lead Bias')
#calculate correlation
nmme3corr = chirps.corrwith(nmme3, axis=0).rename('NMME 3 Month Lead Correlation')
#print('NMME 3 Month Forecast')
#print(nmme3rmse,nmme3bias,nmme3corr)

#calculate RMSE
nmme4rmse = np.sqrt(((nmme4-chirps)**2).mean()).rename('NMME 4 Month Lead RMSE')
#calculate bias
nmme4bias = (nmme4-chirps).mean().rename('NMME 4 Month Lead Bias')
#calculate correlation
nmme4corr = chirps.corrwith(nmme4, axis=0).rename('NMME 4 Month Lead Correlation')
#print('NMME 4 Month Forecast')
#print(nmme4rmse,nmme4bias,nmme4corr)

#calculate RMSE
nmme5rmse = np.sqrt(((nmme5-chirps)**2).mean()).rename('NMME 5 Month Lead RMSE')
#calculate bias
nmme5bias = (nmme5-chirps).mean().rename('NMME 5 Month Lead Bias')
#calculate correlation
nmme5corr = chirps.corrwith(nmme5, axis=0).rename('NMME 5 Month Lead Correlation')
#print('NMME 5 Month Forecast')
#print(nmme5rmse,nmme5bias,nmme5corr)

#calculate RMSE
nmme6rmse = np.sqrt(((nmme6-chirps)**2).mean()).rename('NMME 6 Month Lead RMSE')
#calculate bias
nmme6bias = (nmme6-chirps).mean().rename('NMME 6 Month Lead Bias')
#calculate correlation
nmme6corr = chirps.corrwith(nmme6, axis=0).rename('NMME 6 Month Lead Correlation')
#print('NMME 6 Month Forecast')
#print(nmme6rmse,nmme6bias,nmme6corr)

allstats = pd.concat([chirprmse,chirpbias,chirpcorr,gefsrmse,gefsbias,gefscorr,
                      nmme0rmse,nmme0bias,nmme0corr,nmme1rmse,nmme1bias,nmme1corr,
                      nmme2rmse,nmme2bias,nmme2corr,nmme3rmse,nmme3bias,nmme3corr,
                      nmme4rmse,nmme4bias,nmme4corr,nmme5rmse,nmme5bias,nmme5corr,
                      nmme6rmse,nmme6bias,nmme6corr], axis=1)
allstats.to_csv(r'C:\Users\smille25\Downloads\forecasts\precip\precipevalsd.csv')