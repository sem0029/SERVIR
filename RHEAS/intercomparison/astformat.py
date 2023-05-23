# -*- coding: utf-8 -*-
"""
Created on Wed Jun 23 08:15:36 2021

author: Sara Miller

format DSSAT forecasts to template for comparison with AST forecasts
"""

import pandas as pd
import sys

df = pd.read_excel(r'C:\Users\smille25\Downloads\astcomparison\astnowcasts.xlsx',sheet_name='astnowcasts')
mean10 = pd.read_excel(r'C:\Users\smille25\Downloads\astcomparison\astnowcasts.xlsx',sheet_name='Sheet1')

df1 = pd.DataFrame()

for c in df['admin1'].unique():
    for yr in df['year'].unique():
        #high = df.loc[df['admin1']==c]['Value'].max()
        #low = df.loc[df['admin1']==c]['Value'].min()
        fsct = df.loc[(df['admin1']==c)&(df['year']==yr)]['Value'].mean()
        mean10c = mean10.loc[mean10['admin1']==c]['Value'].mean()*1000
        #p10 = (fsct/mean10c)*100
        #highp10 = (high/mean10c)*100
        #lowp10 = (low/mean10c)*100
        
        df1 = df1.append({'fnid':mean10.loc[mean10['admin1']==c]['fnid'].item(),'country':'Kenya',
                          'admin1':c,'year':yr,'season':'Long','month':'6',
                          'day':'15','variable':'yield_nowcast_rheas',
                          'Value':fsct,'Unit':'kg/ha'},ignore_index=True)
        '''
        df1 = df1.append({'fnid':mean10.loc[mean10['admin1']==c]['fnid'].item(),'country':'Kenya',
                      'admin1':c,'year':'2021','season':'Long','month':'6',
                      'day':'15','variable':'yield_fcst_high_rheas',
                      'Value':high,'Unit':'kg/ha'},ignore_index=True)
        df1 = df1.append({'fnid':mean10.loc[mean10['admin1']==c]['fnid'].item(),'country':'Kenya',
                      'admin1':c,'year':'2021','season':'Long','month':'6',
                      'day':'15','variable':'yield_fcst_low_rheas',
                      'Value':low,'Unit':'kg/ha'},ignore_index=True)
        df1 = df1.append({'fnid':mean10.loc[mean10['admin1']==c]['fnid'].item(),'country':'Kenya',
                      'admin1':c,'year':'2021','season':'Long','month':'6',
                      'day':'15','variable':'yield_fcst_p10_rheas',
                      'Value':p10,'Unit':'kg/ha'},ignore_index=True)
        df1 = df1.append({'fnid':mean10.loc[mean10['admin1']==c]['fnid'].item(),'country':'Kenya',
                      'admin1':c,'year':'2021','season':'Long','month':'6',
                      'day':'15','variable':'yield_fcst_high_p10_rheas',
                      'Value':highp10,'Unit':'kg/ha'},ignore_index=True)
        df1 = df1.append({'fnid':mean10.loc[mean10['admin1']==c]['fnid'].item(),'country':'Kenya',
                      'admin1':c,'year':'2021','season':'Long','month':'6',
                      'day':'15','variable':'yield_fcst_low_p10_rheas',
                      'Value':lowp10,'Unit':'kg/ha'},ignore_index=True)
        '''
        
    
#df = df.groupby(['admin1'])
print(df1)
df1.to_csv(r'C:\Users\smille25\Downloads\astcomparison\astnowcast.csv')
