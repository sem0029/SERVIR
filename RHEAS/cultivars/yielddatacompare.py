# -*- coding: utf-8 -*-
"""
Created on Tue Jan  4 13:23:20 2022

author: Sara Miller
plot different measured yield datasets for kenya
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import sys

fao = pd.read_csv(r'D:\Downloads\Kenya_Yield_2010-17.csv')
fews = pd.read_csv(r'D:\Downloads\maize_yield_ke_210303.csv')
mag = pd.read_csv(r'C:\Users\smille25\Downloads\Kenya_seasonal_yield_MOA.csv')

#format each data source
fao['season1'] = 'Annual'
fao = fao.set_index(['Year','season1'])
fao = fao.stack()
fao = fao.reset_index()
fao = fao.rename(columns={'level_2':'cname',0:'FAO yield'})
fao = fao.set_index(['Year','season1','cname'])

fews = fews.loc[fews['Year']>1999]
fews['season1'] = np.nan
fews['season1'].loc[fews['season'] == 'Annual'] = 'Annual'
fews['season1'].loc[fews['season'] == 'Long'] = 'LR'
fews['season1'].loc[fews['season'] == 'Short'] = 'SR'
fews = fews.set_index(['Year','season1','cname'])

mag = mag.drop(columns={'Season'})
mag = mag.set_index(['Year','season1'])
mag = mag.stack()
mag = mag.reset_index()
mag = mag.rename(columns={'level_2':'cname',0:'MAG yield'})
mag = mag.set_index(['Year','season1','cname'])

combo = pd.concat([fao,fews,mag],axis=1)
print(combo)
combo = combo.reset_index()
combo = combo.set_index('Year')

#plot yields for each county
for c in combo.cname.unique():
    fig, ax = plt.subplots(figsize=(12,6))
    plt.title(c)
    combo1 = combo.loc[combo['cname']==c]
    combo1['FAO yield'].loc[combo1['season1']=='Annual'].plot(color='blue',style='-', label='FAO Annual yield')
    combo1['FEWS NET yield'].loc[combo1['season1']=='LR'].plot(color='orange',style='--', label='FEWS NET LR yield')
    combo1['FEWS NET yield'].loc[combo1['season1']=='SR'].plot(color='orange',style=':',label='FEWS NET SR yield')  
    combo1['FEWS NET yield'].loc[combo1['season1']=='Annual'].plot(color='orange',style='-',label='FEWS NET Annual yield')
    combo1['MAG yield'].loc[combo1['season1']=='LR'].plot(color='green',style='--',label='Ministry LR yield')
    combo1['MAG yield'].loc[combo1['season1']=='SR'].plot(color='green',style=':',label='Ministry SR yield')
    plt.legend()
