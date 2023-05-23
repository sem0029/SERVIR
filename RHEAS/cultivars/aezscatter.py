# -*- coding: utf-8 -*-
"""
Created on Fri Oct  4 12:14:42 2019

@author: smille25
plot dssat outputs as a scatterplot compared to measured yield
group agroecological zones by color
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
from matplotlib.lines import Line2D
import sys


# read csv with dssat yields
df = pd.read_csv(r'C:\Users\smille25\Downloads\cultivartests\cultivarselectedyields_individual2.csv')

# assign season based on planting date
df['planting'] = pd.to_datetime(df['planting'])
df = df.set_index('planting')
df['Year'] = df.index.year.values
df['season1'] = np.where((df.index.month<5),'LR','SR')

# get yearly yields for selected cultivar
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
fao = fao.rename('FAO')
fao.index.names = ['Year','season1','cname']
fao = fao.loc[~fao.index.duplicated(keep='first')]

df2 = pd.concat([df,fao], axis=1)

df2 = df2.rename_axis(index=["Year", "season1","cname"])
df2 = df2.reset_index()
df2 = df2.loc[(df2['Year'].astype(int)>2014)]


df2 = df2.set_index(['Year','cname'])
df2 = df2.loc[df2['FAO']>0]

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


# optionally: plot for only long or short rains
#df2 = df2.loc[df2['season1']=='LR']

# remove bias at county level
df2 = df2.reset_index()

for c in df2.cname.unique():
    for s in df2.season1.unique():
        bias = (df2['DSSAT'].loc[(df2['cname']==c)&(df2['season1']==s)] - df2['FAO'].loc[(df2['cname']==c)&(df2['season1']==s)]).mean()
        df2['DSSAT'].loc[(df2['cname']==c)&(df2['season1']==s)] = df2['DSSAT'].loc[(df2['cname']==c)&(df2['season1']==s)] - bias
        print(c,bias)
df2['DSSAT'].loc[(df2['DSSAT']<0)] = 0

df2 = df2.set_index(['Year','cname'])

#group yield by AEZ
df3 = df2.groupby(['Year','aez','season1']).mean()
df3 = df3.reset_index(level=1)
df2 = df2.iloc[df2.index.get_level_values(1) != 'Lamu']
print(df2)
#sys.exit()
fig, ax = plt.subplots(figsize=(10,6))
colors = {'Western Lowlands':'red', 'Western Transition':'purple', 'Western Highlands':'pink',
              'Central Highlands':'gray', 'Wet':'blue', 'High Potential Maize':'green', 
              'Coastal Lowlands':'brown', 'Eastern Lowlands':'orange','Semi Arid':'black'}

#convert to MT/ha instead of kg/ha and plot
df2['FAO'] = df2['FAO'] / 1000
df2['DSSAT'] = df2['DSSAT'] / 1000
ax.scatter(x=df2['FAO'], y=df2['DSSAT'], c=df2['aez'].apply(lambda x: colors[x]))
x = np.linspace(0,5,100)
y = x
plt.plot(x, y, 'black')
plt.rcParams.update({'font.size': 16})
matplotlib.rc('xtick', labelsize=14) 
matplotlib.rc('ytick', labelsize=14)
plt.title('Maize Yield (MT/ha)')
plt.xlabel('Measured Yield')
plt.ylabel('County Level Bias-Corrected DSSAT Yield')
legend_elements = [Line2D([0], [0], marker='o', color='w', markerfacecolor='gray', label='Central Highlands'),
                       Line2D([0], [0], marker='o', color='w', markerfacecolor='brown', label='Coastal Lowlands'),
                       Line2D([0], [0], marker='o', color='w', markerfacecolor='orange', label='Eastern Lowlands'),
                       Line2D([0], [0], marker='o', color='w', markerfacecolor='green', label='High Potential Maize'),
                       Line2D([0], [0], marker='o', color='w', markerfacecolor='black', label='Semi Arid'),
                       Line2D([0], [0], marker='o', color='w', markerfacecolor='pink', label='Western Highlands'),
                       Line2D([0], [0], marker='o', color='w', markerfacecolor='red', label='Western Lowlands'),
                       Line2D([0], [0], marker='o', color='w', markerfacecolor='purple', label='Western Transition'),
                       Line2D([0], [0], marker='o', color='w', markerfacecolor='blue', label='Wet')]
#calculate correlation
corr = df2['FAO'].corr(df2['DSSAT'])
print(corr)
r2 = corr*corr
print(r2)


plt.legend(title='$r$ = {0:.2f}'.format(corr), handles=legend_elements,bbox_to_anchor=(1.04, 1))
plt.tight_layout()
plt.show()


