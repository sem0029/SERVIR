# -*- coding: utf-8 -*-
"""
Created on Wed Jul 22 08:40:39 2020

author: Sara Miller
seasonal cultivar analysis
using long term data
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import sys

r'''
########################################################################
#clean data from MOA and calcuate county level yields
df = pd.DataFrame()
xls = pd.ExcelFile(r'C:\Users\smille25\Downloads\MAIZE DATA FROM SUBCOUNTY LEVEL 2014 TO 2019 SEASONBY SEASON.xlsx')
for sheet in xls.sheet_names:
    data = pd.read_excel(xls,sheet)
    data = data.groupby(['County']).sum()
    columns = data.columns
    data[sheet] = data[columns[1]] / data[columns[0]]
    df = pd.concat([df,data[sheet]], axis=1)
df = df.transpose()
print(df)
df.to_csv(r'C:\Users\smille25\Downloads\Kenya_seasonal_yield.csv')
#########################################################################

df1 = pd.read_csv(r'C:\Users\smille25\Downloads\cultivartests\cultivarselectedyields_individual.csv')

#get season information from planting date
df1['planting'] = pd.to_datetime(df1['planting'])
df1 = df1.set_index('planting')
df1['Year'] = df1.index.year.values
df1['season1'] = np.where((df1.index.month<5),'LR','SR')
df1['Season'] = df1['Year'].astype(str)+' '+df1['season1']

#optionally: add in 0s where less than selected number of ensembles present
#for cul in df1.cultivar.unique():
        

    #df = df1.loc[df1['cultivar']==cul]
    
    #nens = 300
    #for c in df['cname'].unique():
    #    for p in df['Season'].unique():
    #        dfa = df.loc[(df['cname']==c)&(df['Season']==p)]
    #        while(len(df1.loc[(df1['cname']==c)&(df1['cultivar']==cul)&(df1['Season']==p)])<nens):
    #            df1 = df1.append({'cultivar':cul,'Season': p,'cname':c,'season1':p[-2:],'gwad':0}, ignore_index=True)
    #    print(cul,c)
    #sys.exit()

df1.to_csv(r'C:\Users\smille25\Downloads\cultivartests\cultivarselectedyields_individual1.csv')
'''

culeval = pd.DataFrame(columns=['county','season','cultivar','rmse','%rmse','unbiased rmse','bias','correlation'])


df1 = pd.read_csv(r'C:\Users\smille25\Downloads\cultivartests\cultivarselectedyields_individual2.csv')


dfharvest = pd.DataFrame()
#evaluate each cultivar
for cul in df1.cultivar.unique():
    
    df = df1.loc[df1['cultivar']==cul]
    df.harvest = (pd.to_datetime(df.harvest)).dt.dayofyear
    #df['plant2'] = (pd.to_datetime(df.planting)).dt.dayofyear

    df75 = pd.DataFrame()
    
    #get average # of ensembles that failed for each cultivar and avg harvest date
    for c in df.cname.unique():
        for s in df.season1.unique():
            zeros = df.loc[(df.cname==c)&(df.season1==s)&(df.gwad==0)]
            failed_ens = zeros.shape[0]
            try:
                ens_fail = (failed_ens/(df.loc[(df.cname==c)&(df.season1==s)].shape[0]))*100
                har = (df['harvest'].loc[(df.cname==c)&(df.season1==s)]).mean()
                har = pd.to_datetime(har, format='%j').strftime('%m-%d')
                dfharvest = dfharvest.append({'county':c,'cultivar':cul,'season':s,'avg_ens_fail':ens_fail,'avg_harvest':har}, ignore_index=True)

            except:
                pass

    # get seasonal yields for selected cultivar
    df = df.groupby(['Season','season1', 'cname']).mean()


    # remove unnecessary columns
    df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
    df = df.drop(columns=['Year','harvest'])


    df = df.unstack(level=2)

    df.columns = df.columns.droplevel()
    counties = list(df.columns)
    df = df.reset_index(level=1)
    
    # read csv with measured yields
    fao = pd.read_csv(r'C:\Users\smille25\Downloads\Kenya_seasonal_yield_MOA.csv')
    fao = fao.set_index(['Season','season1'])
    
    # convert to kg/ha 
    fao = (fao * 1000)
    fao = fao.reset_index(level=1)

    
    for c in counties:
        for season in ['LR','SR']:
            #get dssat yields for specified county and cultivar
            df2 = df[c].loc[df['season1']==season]
            df2 = df2.fillna(0)

            fao1 = fao[c].loc[fao['season1']==season]
            
            if season=='LR':
                fao2 = fao1.iloc[-5:]
                df3 = df2.iloc[-5:]

            if season=='SR':
                fao2 = fao1.iloc[-5:]
                df3 = df2.iloc[-5:]


            if (df3.shape[0] >= fao2.shape[0]):
                #   calculate correlation and RMSE for that cultivar with the measured data
                corr = df3.corr(fao2)
                rmse = np.sqrt(((df3-fao2)**2).mean())
                perrmse = np.sqrt(((df3-fao2)**2).mean())/(fao2.mean())*100
                ubrmse = np.sqrt((((df3-df3.mean())-(fao2-fao2.mean()))**2).mean())
                bias = (df3-fao2).mean()

                culeval = culeval.append({'county':c,'season':season, 'rmse':rmse, '%rmse':perrmse,'unbiased rmse':ubrmse, 'bias':bias, 'correlation':corr, 'cultivar':cul}, ignore_index=True)

culeval = culeval.set_index(['county','season','cultivar'])
dfharvest = dfharvest.set_index(['county','season','cultivar'])
culeval = pd.concat([culeval,dfharvest],axis=1)
print(culeval,dfharvest)
culeval.to_csv(r'C:\Users\smille25\Downloads\cultivartests\culeval_individual2.csv')


