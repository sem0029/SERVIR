# -*- coding: utf-8 -*-
"""
Created on Mon Apr 24 08:46:30 2023

author: Sara Miller
cultivar selection
import csv containing cultivar statistics
select one cultivar per county/season: 
    throw out cultivars with unrealistic harvest dates,
    select correlation above 0.8 with lowest unbiased rmse
    if no correlation above 0.8 just select highest correlation
get yields for all the cultivars in one csv
"""

import pandas as pd
import sys
import numpy as np


culs = pd.read_csv(r'C:\Users\smille25\Downloads\cultivartests\culeval_individual.csv')
selected = pd.DataFrame()

for c in culs.county.unique():
    for season in ['LR','SR']:

        df = culs.loc[((culs['county']==c)&(culs['season']==season))]
        df['harvestmonth'] = pd.to_datetime(df['avg_harvest'],format='%m-%d').dt.month
        if season=='LR':
            earliestharvest = 7
        else:
            earliestharvest = 1
        df = df.loc[df['harvestmonth']>=earliestharvest]
        df1 = df.loc[df['correlation']>=0.8]
        
        if df1.empty:
            df1 = df.loc[df['correlation'] == df['correlation'].max()]
        else: 
            df1 = df1.loc[df1['unbiased rmse'] == df1['unbiased rmse'].min()]
        selected = pd.concat([selected,df1])

r'''
selected.to_csv(r'C:\Users\smille25\Downloads\cultivartests\cultivartests_individual1_selected.csv')

yields = pd.read_csv(r'C:\Users\smille25\Downloads\cultivartests\cultivarselectedyields_individual1.csv')
selected = pd.read_csv(r'C:\Users\smille25\Downloads\cultivartests\cultivartests_individual1_selected.csv')
yields2 = pd.DataFrame()

for c in selected.county.unique():
    sn = selected.loc[(selected['county']==c)]
    for season in sn.season.unique():
        df = selected.loc[((selected['county']==c)&(selected['season']==season))]
        y1 = yields.loc[((yields['cname']==c)&(yields['season1']==season))]
        cul = df['cultivar'].item()
        y2 = y1.loc[y1['cultivar']==cul]
        yields2 = pd.concat([yields2,y2])

yields2.to_csv(r'C:\Users\smille25\Downloads\cultivartests\cultivarselectedyields_individual2.csv')

df1 = pd.read_csv(r'C:\Users\smille25\Downloads\cultivartests\cultivarselectedyields_individual2.csv')
# get seasonal yields for selected cultivar
df = df1.groupby(['Season','season1', 'cname']).mean()
#culnum = df['cul#'].iloc[0]


# remove unnamed column, ensemble column, and gid column
df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
df = df.drop(columns=['Year'])


df = df.unstack(level=2)

df.columns = df.columns.droplevel()
counties = list(df.columns)
df = df.reset_index(level=1)

# read csv with FAO yields
fao = pd.read_csv(r'C:\Users\smille25\Downloads\Kenya_seasonal_yield_MOA.csv')
fao = fao.set_index(['Season','season1'])

# convert to kg/ha 
fao = (fao * 1000)
fao = fao.reset_index(level=1)
#fao['COUNTY'] = fao['COUNTY'].str.lower()


#fig, ax = plt.subplots(figsize=(12,6))
#fao = fao.rename('FAO')
#fao.plot(ax=ax, color=('r'))
culeval = pd.DataFrame(columns=['county','season','rmse','%rmse','unbiased rmse','bias','correlation'])


for c in counties:
    for season in ['LR','SR']:
        #get dssat yields for specified county and cultivar
        df2 = df[c].loc[df['season1']==season]
        df2 = df2.fillna(0)
        print(df2)

        #fao1 = fao.loc[fao['COUNTY']==c]
        #fao1 = fao1.groupby(['YEAR']).mean()
        #fao1 = fao1['MEAN']

        fao1 = fao[c].loc[fao['season1']==season]
        
        #use 2002-09 for calibration
        #use 2015 onward for validation
        stddev = fao1.std()
        #print(fao1,df2)
        #sys.exit()

        if season=='LR':
            fao2 = fao1.iloc[-5:]
            df3 = df2.iloc[-5:]

        if season=='SR':
            fao2 = fao1.iloc[-5:]
            df3 = df2.iloc[-5:]
            #print(fao2,df3)
            #sys.exit()
        #print(fao1,fao2)
        #print(df2,df3)
        #sys.exit()
        stddev = fao1.std()


        if (df3.shape[0] >= fao2.shape[0]):
            #print(df3,fao2)
            #   calculate correlation and RMSE for that cultivar with the FAO data
            corr = df3.corr(fao2)
            rmse = np.sqrt(((df3-fao2)**2).mean())
            perrmse = np.sqrt(((df3-fao2)**2).mean())/(fao2.mean())*100
            ubrmse = np.sqrt((((df3-df3.mean())-(fao2-fao2.mean()))**2).mean())
            #perubrmse = 
            bias = (df3-fao2).mean()
            
            culeval = culeval.append({'county':c,'season':season, 'rmse':rmse, '%rmse':perrmse,'unbiased rmse':ubrmse, 'bias':bias, 'correlation':corr}, ignore_index=True)
#print(culeval)
#culeval.to_csv(r'C:\Users\smille25\Downloads\cultivartests\seasonalcultivareval.csv')
culeval = culeval.set_index(['county','season'])
#dfharvest = dfharvest.set_index(['county','season','cultivar'])
#culeval = pd.concat([culeval,dfharvest],axis=1)
print(culeval)
culeval.to_csv(r'C:\Users\smille25\Downloads\cultivartests\culeval_individual2.csv')
'''