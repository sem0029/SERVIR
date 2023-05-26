# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 08:57:03 2020

author: Sara Miller
evaluate forecasts at a county level for each forecast date through the years
evaluates all forecasts compared to available measured data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import glob
import sys
import datetime

table = pd.DataFrame()
for r in ['CFSv2','CHIRP','GEFS','ESP']:
    #plot all forecast periods

    forecast = pd.read_csv(r'C:\Users\smille25\Downloads\forecasts\updatedforecasts\allforecasts{0}.csv'.format(r))
    nowcast = pd.read_csv(r'C:\Users\smille25\Downloads\Kenya_seasonal_yield_MOA.csv')

    #get average county level yields
    if not(forecast.empty):
        forecast['Year'] = pd.DatetimeIndex(forecast['planting']).year
        forecast['season1'] = np.nan
        forecast['season1'].loc[pd.DatetimeIndex(forecast['planting']).month>8] = 'SR'
        forecast['season1'].loc[pd.DatetimeIndex(forecast['planting']).month<6] = 'LR'
        forecast['Date1'] = forecast['forecast_date'].str[:5]
        perror = pd.DataFrame()
        for d in forecast.Date1.unique():
            f1 = forecast.loc[forecast['Date1']==d]
            if not (f1.empty): 

                #yr = f1['Year'].mean()
                if(d=='02_30'):
                    s1 = 'SR'
                else:
                    sn = pd.to_datetime(pd.to_datetime(f1['Date1'],format='%m_%d').values.astype(np.int64).mean())

                    if((sn.month>2)&(sn.month<10)):
                        s1 = 'LR'
                    else:
                        s1 = 'SR'
                df1 = pd.DataFrame()
                for d1 in f1.Year.unique():
                    forecast1 = forecast.loc[(forecast['Date1']==d)&(forecast['Year']==d1)].groupby(['cname','Year','season1']).mean()
                    nowcast1 = nowcast.loc[(nowcast['Year']==d1)&(nowcast['season1']==s1)].groupby(['cname','Year','season1']).mean()
    
                    df = pd.concat([forecast1,nowcast1],axis=1)
                    df1 = pd.concat([df1,df])

                #calculate county level metrics
                #calculate RMSE
                df1 = df1.reset_index()
                for c in df1.cname.unique():
                    df2 = df1.loc[df1['cname']==c]
                    perror['rmse'] = np.sqrt(((df2['gwad']-df2['nowcast'])**2).mean())
        
                    #calculate bias
                    perror['bias'] = (df2['gwad']-df2['nowcast']).mean()
                    #calculate correlation
                    perror['corr'] = df2['nowcast'].corr(df2['gwad'])
                    #calculate percent error
                    perror['perror'] = (df2['gwad']-df2['nowcast'])/df2['nowcast']*100
                    perror['Date']=d
                    perror['cname']=c

                    table = pd.concat([table,perror], ignore_index=True)


    print(table)
    table = table.groupby(['Date']).mean()
    print(table)
    fig, ax = plt.subplots(figsize=(6,4))
    plt.rcParams.update({'font.size': 12})
    table['rmse'].plot.line(legend=False,ax=ax,label='RMSE')
    table['bias'].plot.line(legend=False,ax=ax,label='Bias')
    plt.legend(loc='upper right')
    plt.ylabel('RMSE/Bias')
    ax1 = ax.twinx()
    table['corr'].plot.line(color='green',legend=False,ax=ax1,label='Correlation')
    plt.title('{0}'.format(r))
    plt.ylabel('Correlation')
    plt.legend(loc='lower right')

    fig.tight_layout()
    plt.show()
    r'''
    fig, ax = plt.subplots(figsize=(10,6))
    plt.rcParams.update({'font.size': 12})
    ax.table(cellText=table2.values, colLabels=table2.columns, loc='center')
    # hide axes
    fig.patch.set_visible(False)
    ax.axis('off')
    ax.axis('tight')
    fig.tight_layout()
    plt.show()
    '''

    table.to_csv(r'C:\Users\smille25\Downloads\forecasts\eval\{0}forecasteval.csv'.format(r))

