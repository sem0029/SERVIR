# -*- coding: utf-8 -*-
"""
Created on Tue Apr 26 13:16:44 2022

author: Sara Miller
format DSSAT forecasts for excel sheet for intercomparison
"""

import pandas as pd
import numpy as np
import sys

df = pd.read_csv(r'C:\Users\smille25\Downloads\cultivartests\nowcasts_selected_300ens25km.csv')
counties = ['Baringo', 'Bomet', 'Bungoma', 'Busia',
       'Eg Tanariver', 'Elgeyo Marakwet', 'Embu', 'Garissa', 'Homa Bay',
       'Isiolo', 'Kajiado', 'Kakamega', 'Kericho', 'Kiambu', 'Kilifi',
       'Kirinyaga', 'Kisii', 'Kisumu', 'Kitui', 'Kwale', 'Laikipia', 'Lamu',
       'Machakos', 'Makueni', 'Mandera ', 'Marsabit', 'Meru', 'Migori',
       'Mombasa', 'Murang\'a', 'Nairobi', 'Nakuru', 'Nandi', 'Narok', 'Nyamira',
       'Nyandarua', 'Nyeri', 'Samburu', 'Siaya', 'Taita Taveta', 'Tana River',
       'Tharaka Nithi', 'Trans Nzoia', 'Turkana', 'Uasin Gishu', 'Vihiga',
       'Wajir', 'West Pokot']

#get season information from forecast dates
df['country'] = 'Kenya'
df['forecast_date'].loc[df['forecast_date'].str[:5]=='02_30'] = '02_28'+ df['forecast_date'].str[5:]
df['date'] = pd.to_datetime(df['forecast_date'],format='%m_%d_%y')
df['year'] = df['date'].dt.year
df['month'] = df['date'].dt.month
df['day'] = df['date'].dt.day
df['season'] = np.nan
df['season'].loc[((df['month']>2)&(df['month']<10))] = 'Long'
df['season'].loc[((df['month']<=2)|(df['month']>=10))] = 'Short'
df = df.rename(columns={'cname':'admin1'})
df = df.loc[(df['day']==30)|(df['day']==28)]



for m in df.month.unique():
    df1 = pd.DataFrame()
    for c in counties:
        dfa = df.loc[df['month']==m]
        for d in dfa['forecast_date'].unique():
            if (dfa.loc[((dfa['admin1']==c)&(dfa['forecast_date']==d))]).empty:
                yr=dfa.loc[((dfa['forecast_date']==d))]['year'].mean()
                month=dfa.loc[((dfa['forecast_date']==d))]['month'].mean()
                day=dfa.loc[((dfa['forecast_date']==d))]['day'].mean()
                sn=dfa.loc[((dfa['forecast_date']==d))]['season'].unique()
                
                #if forecast does not exist for the county/season, append NaNs
                df1 = df1.append({'country':'Kenya',
                                  'admin1':c,'year':yr,'season':sn,'month':m,
                                  'day':day,'variable':'yield_fcst_rheas',
                                  'Value':np.nan,'Unit':'kg/ha'},ignore_index=True)
                df1 = df1.append({'country':'Kenya',
                              'admin1':c,'year':yr,'season':sn,'month':m,
                              'day':day,'variable':'yield_fcst_low_rheas',
                              'Value':np.nan,'Unit':'kg/ha'},ignore_index=True)
                df1 = df1.append({'country':'Kenya',
                              'admin1':c,'year':yr,'season':sn,'month':m,
                              'day':day,'variable':'yield_fcst_high_rheas',
                              'Value':np.nan,'Unit':'kg/ha'},ignore_index=True)
                df1 = df1.append({'country':'Kenya',
                              'admin1':c,'year':yr,'season':sn,'month':m,
                              'day':day,'variable':'yield_fcst_std_rheas',
                              'Value':np.nan,'Unit':'kg/ha'},ignore_index=True)

            else:
                fsct = dfa.loc[((dfa['admin1']==c)&(dfa['forecast_date']==d))]['gwad'].mean()
                high = dfa.loc[((dfa['admin1']==c)&(dfa['forecast_date']==d))]['gwad'].max()
                low= dfa.loc[((dfa['admin1']==c)&(dfa['forecast_date']==d))]['gwad'].min()
                stddev = dfa.loc[((dfa['admin1']==c)&(dfa['forecast_date']==d))]['gwad'].std()
                yr=dfa.loc[((dfa['admin1']==c)&(dfa['forecast_date']==d))]['year'].mean()
                month=dfa.loc[((dfa['admin1']==c)&(dfa['forecast_date']==d))]['month'].mean()
                day=dfa.loc[((dfa['admin1']==c)&(dfa['forecast_date']==d))]['day'].mean()
                sn=dfa.loc[((dfa['admin1']==c)&(dfa['forecast_date']==d))]['season'].unique()
                
                #append mean, min, max, and standard deviation of yield for each forecast
                df1 = df1.append({'country':'Kenya',
                                  'admin1':c,'year':yr,'season':sn,'month':m,
                                  'day':day,'variable':'yield_fcst_rheas',
                                  'Value':fsct,'Unit':'kg/ha'},ignore_index=True)
                df1 = df1.append({'country':'Kenya',
                              'admin1':c,'year':yr,'season':sn,'month':m,
                              'day':day,'variable':'yield_fcst_low_rheas',
                              'Value':low,'Unit':'kg/ha'},ignore_index=True)
                df1 = df1.append({'country':'Kenya',
                              'admin1':c,'year':yr,'season':sn,'month':m,
                              'day':day,'variable':'yield_fcst_high_rheas',
                              'Value':high,'Unit':'kg/ha'},ignore_index=True)
        
                df1 = df1.append({'country':'Kenya',
                              'admin1':c,'year':yr,'season':sn,'month':m,
                              'day':day,'variable':'yield_fcst_std_rheas',
                              'Value':stddev,'Unit':'kg/ha'},ignore_index=True)

        
    print(df1)
    #df1 = df1.set_index(['admin1','variable'])
    df1 = df1.drop(columns=['Unit','country','month','day','season'])
    print(df1)
    df1 = df1.pivot(index=['admin1','variable'],columns='year')
    print(df1)
    #sys.exit()
    df1.to_csv(r'C:\Users\smille25\Downloads\astcomparison\forecasts_month{0}.csv'.format(m))
