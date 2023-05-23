# -*- coding: utf-8 -*-
"""
Created on Fri Apr  8 10:25:59 2022

author: Sara Miller
create time series box plots of yield anomalies from dssat 
compared to time series of measured yields
"""
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.lines import Line2D
import sys
import seaborn as sns
import scipy.stats as stats
import scipy as sp

# read csv with dssat yields
df = pd.read_csv(r'C:\Users\smille25\Downloads\cultivartests\cultivarselectedyields_individual1.csv')

# get season from planting date
df['planting'] = pd.to_datetime(df['planting'])
df = df.set_index('planting')
df['Year'] = df.index.year.values
df['season1'] = np.where((df.index.month<5),'LR','SR')
df['Season'] = df['Year'].astype(str)+' '+df['season1'].astype(str)
df = df.reset_index()
counties = df.cname.unique()

df = df.set_index(['Year','season1','Season','cname'])
df = df.rename(columns={'gwad':'DSSAT'})

# read csv with measured yields
fao = pd.read_csv(r'C:\Users\smille25\Downloads\Kenya_seasonal_yield_MOA.csv')
fao['Year'] = (fao['Season'].str[:4]).astype(int)
fao = fao.set_index(['Year','season1','Season'])

# convert to kg/ha for selected counties
fao = (fao[counties] * 1000).stack()
fao = fao.rename('MOA')
fao.index.names = ['Year','season1','Season','cname']
fao = fao.loc[~fao.index.duplicated(keep='first')]


df = df.reset_index()
fao = fao.reset_index()
df = df.loc[(df['Year'].astype(int)>2014)]


df = df.set_index(['Year','cname'])
fao = fao.set_index(['Year','cname'])
fao = fao.loc[fao['MOA']>0]

#add AEZ zone names
df['aez'] = np.nan
fao['aez'] = np.nan
def c():
    return df.index.get_level_values('cname')
    
df['aez'].loc[c() == 'Bomet'] = 'High Potential Maize'
df['aez'].loc[c() == 'Bungoma'] = 'Western Transition'
df['aez'].loc[c() == 'Busia'] = 'Wet'
df['aez'].loc[c() == 'Embu'] = 'Wet'
df['aez'].loc[c() == 'Homa Bay'] = 'Wet'
df['aez'].loc[c() == 'Kakamega'] = 'Western Transition'
df['aez'].loc[c() == 'Kericho'] = 'Wet'
df['aez'].loc[c() == 'Kiambu'] = 'Wet'
df['aez'].loc[c() == 'Kilifi'] = 'Coastal Lowlands'
df['aez'].loc[c() == 'Kirinyaga'] = 'Wet'
df['aez'].loc[c() == 'Kisii'] = 'Western Highlands'
df['aez'].loc[c() == 'Kisumu'] = 'Western Lowlands'
df['aez'].loc[c() == 'Kwale'] = 'Coastal Lowlands'
df['aez'].loc[c() == 'Lamu'] = 'Wet'
df['aez'].loc[c() == 'Makueni'] = 'Eastern Lowlands'
df['aez'].loc[c() == 'Meru'] = 'Central Highlands'
df['aez'].loc[c() == 'Migori'] = 'Wet'
df['aez'].loc[c() == 'Mombasa'] = 'Wet'
df['aez'].loc[c() == 'Murang\'a'] = 'Central Highlands'
df['aez'].loc[c() == 'Nakuru'] = 'High Potential Maize'
df['aez'].loc[c() == 'Nandi'] = 'Wet'
df['aez'].loc[c() == 'Narok'] = 'High Potential Maize'
df['aez'].loc[c() == 'Nyamira'] = 'Wet'
df['aez'].loc[c() == 'Nyandarua'] = 'Wet'
df['aez'].loc[c() == 'Nyeri'] = 'Central Highlands'
df['aez'].loc[c() == 'Samburu'] = 'Semi Arid'
df['aez'].loc[c() == 'Siaya'] = 'Western Lowlands'
df['aez'].loc[c() == 'Taita Taveta'] = 'Eastern Lowlands'
df['aez'].loc[c() == 'Trans Nzoia'] = 'High Potential Maize'
df['aez'].loc[c() == 'Uasin Gishu'] = 'High Potential Maize'
df['aez'].loc[c() == 'Vihiga'] = 'Western Highlands'
df['aez'].loc[c() == 'Kitui'] = 'Eastern Lowlands'
df['aez'].loc[c() == 'Machakos'] = 'Eastern Lowlands'
df['aez'].loc[c() == 'West Pokot'] = 'Semi Arid'
def c():
    return fao.index.get_level_values('cname')
fao['aez'].loc[c() == 'Bomet'] = 'High Potential Maize'
fao['aez'].loc[c() == 'Bungoma'] = 'Western Transition'
fao['aez'].loc[c() == 'Busia'] = 'Wet'
fao['aez'].loc[c() == 'Embu'] = 'Wet'
fao['aez'].loc[c() == 'Homa Bay'] = 'Wet'
fao['aez'].loc[c() == 'Kakamega'] = 'Western Transition'
fao['aez'].loc[c() == 'Kericho'] = 'Wet'
fao['aez'].loc[c() == 'Kiambu'] = 'Wet'
fao['aez'].loc[c() == 'Kilifi'] = 'Coastal Lowlands'
fao['aez'].loc[c() == 'Kirinyaga'] = 'Wet'
fao['aez'].loc[c() == 'Kisii'] = 'Western Highlands'
fao['aez'].loc[c() == 'Kisumu'] = 'Western Lowlands'
fao['aez'].loc[c() == 'Kwale'] = 'Coastal Lowlands'
fao['aez'].loc[c() == 'Lamu'] = 'Wet'
fao['aez'].loc[c() == 'Makueni'] = 'Eastern Lowlands'
fao['aez'].loc[c() == 'Meru'] = 'Central Highlands'
fao['aez'].loc[c() == 'Migori'] = 'Wet'
fao['aez'].loc[c() == 'Mombasa'] = 'Wet'
fao['aez'].loc[c() == 'Murang\'a'] = 'Central Highlands'
fao['aez'].loc[c() == 'Nakuru'] = 'High Potential Maize'
fao['aez'].loc[c() == 'Nandi'] = 'Wet'
fao['aez'].loc[c() == 'Narok'] = 'High Potential Maize'
fao['aez'].loc[c() == 'Nyamira'] = 'Wet'
fao['aez'].loc[c() == 'Nyandarua'] = 'Wet'
fao['aez'].loc[c() == 'Nyeri'] = 'Central Highlands'
fao['aez'].loc[c() == 'Samburu'] = 'Semi Arid'
fao['aez'].loc[c() == 'Siaya'] = 'Western Lowlands'
fao['aez'].loc[c() == 'Taita Taveta'] = 'Eastern Lowlands'
fao['aez'].loc[c() == 'Trans Nzoia'] = 'High Potential Maize'
fao['aez'].loc[c() == 'Uasin Gishu'] = 'High Potential Maize'
fao['aez'].loc[c() == 'Vihiga'] = 'Western Highlands'
fao['aez'].loc[c() == 'Kitui'] = 'Eastern Lowlands'
fao['aez'].loc[c() == 'Machakos'] = 'Eastern Lowlands'
fao['aez'].loc[c() == 'West Pokot'] = 'Semi Arid'

df = df.reset_index()
fao  = fao.reset_index()
fao = fao.reset_index()

df = df.loc[df['Year'].astype(int)>2014]
fao = fao.loc[fao['Year'].astype(int)>2014]
df = df.loc[df['season1']=='SR']
fao = fao.loc[fao['season1']=='SR']


#get z scores of yield by county for both dssat and measured
for c in fao.cname.unique():
    fao['MOA'].loc[fao['cname']==c] = stats.zscore(fao['MOA'].loc[fao['cname']==c])


for c in df.cname.unique():
    df['DSSAT'].loc[df['cname']==c] = stats.zscore(df['DSSAT'].loc[df['cname']==c])

#group by agro-ecological zone
fao = fao.groupby(['Year','season1','aez']).mean()
fao  = fao.reset_index()

df1 = pd.concat([df,fao])

#plot yield anomalies by aez
g = sns.FacetGrid(df1,col='aez',col_wrap=3,sharex=False,sharey=False)
g.map(sns.boxplot, 'Year','DSSAT')
g.map(sns.pointplot,'Year','MOA',color='red')

g.set_xticklabels(rotation=30)

g.fig.suptitle('Short Rains Yield Anomolies', y=1.00)
g.set_ylabels('Z Score')
plt.tight_layout()
plt.show()
plt.savefig(r'C:\Users\smille25\Downloads\cultivartests\Leepaperfigs\boxplot_anomoly_SR.png',dpi=300)