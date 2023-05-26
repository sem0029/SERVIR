# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 12:52:24 2020

author: Sara Miller
calculates percent difference of forecasts from measured yield data
plots seasonal forecast percent differences compared to measured percent difference from normal
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import sys
import datetime


#get list of forecast files
cfsv2 = pd.read_csv(r'C:\Users\smille25\Downloads\forecasts\updatedforecasts\allforecastsCFSv2.csv')
cfsv2['Method'] = 'CFSv2'
chirp = pd.read_csv(r'C:\Users\smille25\Downloads\forecasts\updatedforecasts\allforecastsCHIRP.csv')
chirp['Method'] = 'CHIRP'
gefs = pd.read_csv(r'C:\Users\smille25\Downloads\forecasts\updatedforecasts\allforecastsGEFS.csv')
gefs['Method'] = 'GEFS'
esp = pd.read_csv(r'C:\Users\smille25\Downloads\forecasts\updatedforecasts\allforecastsESP.csv')
esp['Method'] = 'ESP'
forecasts = pd.concat([cfsv2,chirp,gefs,esp])
forecasts['Year'] = pd.DatetimeIndex(forecasts['planting']).year
forecasts['season1'] = np.nan
forecasts['season1'].loc[pd.DatetimeIndex(forecasts['planting']).month>8] = 'SR'
forecasts['season1'].loc[pd.DatetimeIndex(forecasts['planting']).month<6] = 'LR'
forecasts['Month/Day'] = (forecasts['forecast_date'].str[:2])+'/'+(forecasts['forecast_date'].str[3:5])
counties = list(forecasts.cname.unique())

forecasts = forecasts.groupby(['forecast_date','Year','season1','Month/Day','Method']).mean()
forecasts = forecasts.reset_index()

#read in measured yield data
fao = pd.read_csv(r'C:\Users\smille25\Downloads\Kenya_seasonal_yield_MOA.csv')
fao['Year'] = (fao['Season'].str[:4]).astype(int)
fao = fao.set_index(['Year','season1'])
# convert to kg/ha for selected counties
fao = (fao[counties] * 1000).stack()
fao = fao.reset_index()
faomeanlr = (fao.loc[fao['season1']=='LR'].groupby(['Year','season1']).mean())[0].mean()
faomeansr = (fao.loc[fao['season1']=='SR'].groupby(['Year','season1']).mean())[0].mean()

fig, ax = plt.subplots(5,2,figsize=(6,10))
column = 0
for yr in range(2015,2020):
    row = 0
    for sn in ['LR','SR']:
        table = pd.DataFrame()
        #get yields for a year/season as a percent of the average yield over the country
        forecast = forecasts.loc[(forecasts['Year']==yr)&(forecasts['season1']==sn)]
        fao1 = fao.loc[(fao['Year']==yr)&(fao['season1']==sn)]
        
        #customize date axis as short rains last into the following year
        if sn=='LR':
            mdlist = ['03/15','03/30','04/15','04/30','05/15','05/30','06/15','06/30','07/15','07/30','08/15','08/30','09/15','09/30']
            observed = (fao1[0].mean()-faomeanlr)/faomeanlr*100
        if sn=='SR':
            mdlist = ['10/15','10/30','11/15','11/30','12/15','12/30','01/15','01/30','02/15','02/30']
            observed = (fao1[0].mean()-faomeansr)/faomeansr*100
        print(observed)
        for days in mdlist:
            table2 = pd.DataFrame()
            table2 = forecast.loc[forecast['Month/Day']==days]
        
            CFSv2mean = forecasts['gwad'].loc[(forecasts['Month/Day']==days)&(forecasts['Method']=='CFSv2')].mean()
            CHIRPmean = forecasts['gwad'].loc[(forecasts['Month/Day']==days)&(forecasts['Method']=='CHIRP')].mean()
            GEFSmean = forecasts['gwad'].loc[(forecasts['Month/Day']==days)&(forecasts['Method']=='GEFS')].mean()
            ESPmean = forecasts['gwad'].loc[(forecasts['Month/Day']==days)&(forecasts['Method']=='ESP')].mean()
            #measuredmean = table2['Measured'].mean()
            table4 = pd.DataFrame()

            table2 = table2.set_index('Month/Day')
            table4['CFSv2'] = (table2['gwad'].loc[table2['Method']=='CFSv2']-CFSv2mean)/CFSv2mean *100    
            table4['CHIRP'] = (table2['gwad'].loc[table2['Method']=='CHIRP']-CHIRPmean)/CHIRPmean *100
            table4['GEFS'] = (table2['gwad'].loc[table2['Method']=='GEFS']-GEFSmean)/GEFSmean *100
            table4['ESP'] = (table2['gwad'].loc[table2['Method']=='ESP']-ESPmean)/ESPmean *100
            table4['Month/Day']= days
            table4 = table4.set_index('Month/Day')
            table = pd.concat([table,table4])
            
        table['Measured'] = observed
        
        #plot forecasts compared to measured yields
        table.plot.line(ax=ax[column,row])
        ax[column,row].title.set_text(str(yr)+' '+str(sn))
        ax[column,row].set(ylabel='Percent Difference from Mean')
        row = row +1
    column = column +1
fig.tight_layout()
plt.show()
        
       