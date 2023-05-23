# -*- coding: utf-8 -*-
"""
Created on Wed Mar 30 11:11:47 2022

@author: smille25

yield anomaly scatterplot by aez
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
from matplotlib.offsetbox import AnchoredText


#csv with measured yields
faodssat = pd.read_csv(r'C:\Users\smille25\Downloads\Kenya_seasonal_yield_MOA.csv')
# read csv with dssat yields
df = pd.read_csv(r'C:\Users\smille25\Downloads\cultivartests\cultivarselectedyields_individual1.csv')

df['planting'] = pd.to_datetime(df['planting'])
df = df.set_index('planting')
df['Year'] = df.index.year.values
df['season1'] = np.where((df.index.month<5),'LR','SR')

# get seasonal yields for selected cultivar
df = df.groupby(['Year', 'season1','cname']).mean()

# get list of county names
dfb = df.unstack(level=2)
dfb.columns = dfb.columns.droplevel()
counties = list(dfb.columns)

df = df.rename(columns={'gwad':'DSSAT'})

# read csv with measured yields
fao = pd.read_csv(r'C:\Users\smille25\Downloads\Kenya_seasonal_yield_MOA.csv')
fao['Year'] = (fao['Season'].str[:4]).astype(int)
fao = fao.set_index(['Year','season1'])
# convert to kg/ha for selected counties
fao = (fao[counties] * 1000).stack()
fao = fao.rename('MOA')
fao.index.names = ['Year','season1','cname']
fao = fao.loc[~fao.index.duplicated(keep='first')]

df2 = pd.concat([df,fao], axis=1)

df2 = df2.rename_axis(index=["Year", "season1","cname"])
df2 = df2.reset_index()
df2 = df2.loc[(df2['Year'].astype(int)>2014)]

df2 = df2.set_index(['Year','cname'])
df2 = df2.loc[df2['MOA']>0]
#add AEZ zone names
df2['aez'] = np.nan
def c():
    return df2.index.get_level_values('cname')
    
df2['aez'].loc[c() == 'Bomet'] = 'High Potential Maize'
df2['aez'].loc[c() == 'Bungoma'] = 'Western Transition'
df2['aez'].loc[c() == 'Busia'] = 'Wet'
df2['aez'].loc[c() == 'Embu'] = 'Wet'
df2['aez'].loc[c() == 'Homa Bay'] = 'Wet'
df2['aez'].loc[c() == 'Kakamega'] = 'Western Transition'
df2['aez'].loc[c() == 'Kericho'] = 'Wet'
df2['aez'].loc[c() == 'Kiambu'] = 'Wet'
df2['aez'].loc[c() == 'Kilifi'] = 'Coastal Lowlands'
df2['aez'].loc[c() == 'Kirinyaga'] = 'Wet'
df2['aez'].loc[c() == 'Kisii'] = 'Western Highlands'
df2['aez'].loc[c() == 'Kisumu'] = 'Western Lowlands'
df2['aez'].loc[c() == 'Kwale'] = 'Coastal Lowlands'
df2['aez'].loc[c() == 'Lamu'] = 'Wet'
df2['aez'].loc[c() == 'Makueni'] = 'Eastern Lowlands'
df2['aez'].loc[c() == 'Meru'] = 'Central Highlands'
df2['aez'].loc[c() == 'Migori'] = 'Wet'
df2['aez'].loc[c() == 'Mombasa'] = 'Wet'
df2['aez'].loc[c() == 'Murang\'a'] = 'Central Highlands'
df2['aez'].loc[c() == 'Nakuru'] = 'High Potential Maize'
df2['aez'].loc[c() == 'Nandi'] = 'Wet'
df2['aez'].loc[c() == 'Narok'] = 'High Potential Maize'
df2['aez'].loc[c() == 'Nyamira'] = 'Wet'
df2['aez'].loc[c() == 'Nyandarua'] = 'Wet'
df2['aez'].loc[c() == 'Nyeri'] = 'Central Highlands'
df2['aez'].loc[c() == 'Samburu'] = 'Semi Arid'
df2['aez'].loc[c() == 'Siaya'] = 'Western Lowlands'
df2['aez'].loc[c() == 'Taita Taveta'] = 'Eastern Lowlands'
df2['aez'].loc[c() == 'Trans Nzoia'] = 'High Potential Maize'
df2['aez'].loc[c() == 'Uasin Gishu'] = 'High Potential Maize'
df2['aez'].loc[c() == 'Vihiga'] = 'Western Highlands'
df2['aez'].loc[c() == 'Kitui'] = 'Eastern Lowlands'
df2['aez'].loc[c() == 'Machakos'] = 'Eastern Lowlands'
df2['aez'].loc[c() == 'West Pokot'] = 'Semi Arid'

#calculate z scores of the yield by county
df2 = df2.reset_index()
for c in df2.cname.unique():
    for s in df2.season1.unique():
        df2['DSSAT'].loc[(df2['cname']==c)&(df2['season1']==s)] = stats.zscore(df2['DSSAT'].loc[(df2['cname']==c)&(df2['season1']==s)])
        df2['MOA'].loc[(df2['cname']==c)&(df2['season1']==s)] = stats.zscore(df2['MOA'].loc[(df2['cname']==c)&(df2['season1']==s)])


#calculate correlation
corr = df2['MOA'].corr(df2['DSSAT'])
print(corr)
r2 = corr*corr
print(r2)

#scatter plots of anomalies by AEZ
g = sns.FacetGrid(df2,col='aez',col_wrap=3,sharex=False,sharey=False)
g.map(sns.regplot, 'MOA','DSSAT')

#add correlations and n values to each plot
for aez in df2['aez'].unique():
    print(aez)
    r, p = sp.stats.pearsonr(df2['MOA'].loc[df2['aez']==aez].dropna(), df2['DSSAT'].loc[df2['aez']==aez].dropna())
    print(r)
    n = len(df2['MOA'].loc[df2['aez']==aez])
    print(n)
    anc = AnchoredText('r={0:.2f}\nn={1}'.format(r,n), loc="upper left", frameon=False)
    if(aez=='High Potential Maize'):
        g.axes[0].add_artist(anc)
    elif(aez=='Western Transition'):
        g.axes[1].add_artist(anc)
    elif(aez=='Wet'):
        g.axes[2].add_artist(anc)
    elif(aez=='Coastal Lowlands'):
        g.axes[3].add_artist(anc)
    elif(aez=='Western Highlands'):
        g.axes[4].add_artist(anc)
    elif(aez=='Western Lowlands'):
        g.axes[5].add_artist(anc)
    elif(aez=='Eastern Lowlands'):
        g.axes[6].add_artist(anc)
    elif(aez=='Central Highlands'):
        g.axes[7].add_artist(anc)
    elif(aez=='Semi Arid'):
        g.axes[8].add_artist(anc)
        
g.set_titles(col_template="{col_name}", row_template="{row_name}")
g.fig.suptitle('Observed vs Simulated Yield Anomolies', y=1.00)

plt.savefig(r'C:\Users\smille25\Downloads\cultivartests\Leepaperfigs\scatter_anomoly_AEZ.png',dpi=300)

