# -*- coding: utf-8 -*-
"""
Created on Thu Nov 12 12:52:24 2020

author: Sara Miller
evaluate forecasts at a county level for each forecast date through the years
evaluates all forecasts compared to nowcasts 
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
    #forecast csvs have the following columns: unnamed index,cname,forecast_date,gwad,harvest,planting
    forecast = pd.read_csv(r'C:\Users\smille25\Downloads\forecasts\updatedforecasts\allforecasts{0}.csv'.format(r))
    print(forecast)
    sys.exit()
    
    #nowcast file has the following columns: cname, gwad, harvest, Year, season1, Season
    nowcast = pd.read_csv(r'C:\Users\smille25\Downloads\forecasts\updatedforecasts\nowcasts1.csv')
    nowcast = nowcast.rename(columns={"gwad": "nowcast"})

    #assess forecasts at each forecast date (ex. may 30th forecasting date for all years)
    if not(forecast.empty):
        forecast['Year'] = pd.DatetimeIndex(forecast['planting']).year
        forecast['season1'] = np.nan
        forecast['season1'].loc[pd.DatetimeIndex(forecast['planting']).month>8] = 'SR'
        forecast['season1'].loc[pd.DatetimeIndex(forecast['planting']).month<6] = 'LR'
        forecast['Date1'] = forecast['forecast_date'].str[:5]
        for d in forecast.Date1.unique():
            f1 = forecast.loc[forecast['Date1']==d]
            if not (f1.empty): 
                #add season information
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
                    #average yields for both nowcasts and forecasts by season/county
                    forecast1 = forecast.loc[(forecast['Date1']==d)&(forecast['Year']==d1)].groupby(['cname','Year','season1']).mean()
                    nowcast1 = nowcast.loc[(nowcast['Year']==d1)&(nowcast['season1']==s1)].groupby(['cname','Year','season1']).mean()
    
                    df = pd.concat([forecast1,nowcast1],axis=1)
                    df1 = pd.concat([df1,df])


                #calculate county level metrics
                #calculate RMSE
                df1 = df1.reset_index()
                for c in df1.cname.unique():
                    df2 = df1.loc[df1['cname']==c]
                    rmse = np.sqrt(((df2['gwad']-df2['nowcast'])**2).mean())
        
                    #calculate bias
                    bias = (df2['gwad']-df2['nowcast']).mean()
                    #calculate correlation
                    corr = df2['nowcast'].corr(df2['gwad'])
                    #calculate percent error
                    perror = ((df2['gwad']-df2['nowcast'])/df2['nowcast']*100).mean()

                    table = table.append({'cname':c,'Date':d,'rmse':rmse,'bias':bias,'correlation':corr,'percent error':perror},ignore_index=True)


    table = table.groupby(['cname','Date']).mean()
    print(table)
    r'''
    #optionally: plot progression of forecast statistics be county
    for c in table.cname.unique():
        fig, ax = plt.subplots(figsize=(6,4))
        plt.rcParams.update({'font.size': 12})
        # hide axes
        #fig.patch.set_visible(False)
        #ax.axis('off')
        #ax.axis('tight')
        #table['perror'].plot.line(lw=.5,legend=False,ax=ax,label='Percent Error')
        table['rmse'].loc[table['cname']==c].plot.line(legend=False,ax=ax,label='RMSE')
        table['bias'].loc[table['cname']==c].plot.line(legend=False,ax=ax,label='Bias')
        plt.legend(loc='upper right')
        plt.ylabel('RMSE/Bias')
        ax1 = ax.twinx()
        table['corr'].loc[table['cname']==c].plot.line(color='green',legend=False,ax=ax1,label='Correlation')
        plt.title('{0}, {1}'.format(c,r))
        plt.ylabel('Correlation')
        plt.legend(loc='lower right')
        #ax.legend(loc='lower right')
        #ax2=ax.twinx()
        #table.plot.line(x='Month/Day', y='Correlation', ax=ax2, color='green')
        #ax2.legend(loc='upper right')
        #plt.xticks(rotation=40, ax=ax)
        fig.tight_layout()
        plt.show()
    
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

    table.to_csv(r'C:\Users\smille25\Downloads\forecasts\eval\{0}forecastevalcountry.csv'.format(r))
