# -*- coding: utf-8 -*-
"""
Created on Wed Apr 19 13:52:42 2023

author: Sara Miller
compare Zambia datasets: clean preharvest surveys
compare preharvest, postharvest, and FAO data
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import zscore


#clean preharvest survey data
pre = pd.read_csv(r'C:\Users\smille25\Downloads\rheasexpansion\Zambia\zambia_preharvest_data.csv')
print(len(pre))
#drop duplicate inputs
pre = pre.drop_duplicates()
print(len(pre))
#calculate yield
pre = pre.groupby(['district','year']).sum()
pre['yield'] = pre['production(mt)'] / pre['area_planted'] * 1000

#calculate z scores of yield and flag any anomalies
df1 = pd.DataFrame()
pre = pre.reset_index()
for d in pre.district.unique():
    df = pre.loc[pre['district']==d]
    df['zyield'] = zscore(df['yield'])
    df1 = pd.concat([df1,df])
print(df1)
df1['flag'] = 0
df1['flag'].loc[((df1['zyield']>1.96)|(df1['zyield']<-1.96))] = 1
df1['flag'].loc[((df1['zyield']>2.58)|(df1['zyield']<-2.58))] = 2
df1.to_csv(r'C:\Users\smille25\Downloads\rheasexpansion\Zambia\zambia_preharvest_data_clean.csv')

'''
#aggregate preharvest surveys to province level and compare to postharvest
pre = pd.read_csv(r'C:\Users\smille25\Downloads\rheasexpansion\Zambia\zambia_preharvest_data_clean.csv')
post = pd.read_csv(r'C:\Users\smille25\Downloads\rheasexpansion\Zambia\moa_data.csv')
code = pd.read_csv(r'C:\Users\smille25\Downloads\rheasexpansion\Zambia\district_province_code.csv')

pre = pre.set_index('district')
code = code.set_index('district')
pre = pre.join(code)
pre = pre.reset_index()
#try filtering out flagged values
#aggregate to province level
pre = pre.loc[pre['flag']==0]
pre = pre.groupby(['province','year']).sum()
pre['preharvestyield'] = pre['production(mt)'] / pre['area_planted'] * 1000
pre = pre['preharvestyield']
post = post.set_index(['province','year'])
post = post['yield']
df = pd.concat([pre,post],axis=1)
df= df.reset_index(level=0)

fig,ax = plt.subplots(2,5,figsize=(12,4))
ax = ax.ravel()
i=0
for p in df.province.unique():
    df1 = df.loc[df['province']==p]
    df1['preharvestyield'].dropna().plot(linewidth=2,ax=ax[i])
    df1['yield'].plot(ax=ax[i])
    ax[i].title.set_text(p)
    #ax[i].legend()
    #plt.show()
    i+=1
    #sys.exit()
plt.tight_layout()
plt.show()
plt.savefig(r'C:\Users\smille25\Downloads\rheasexpansion\Zambia\yieldcomparison_quality2.png')
'''
#aggregate to national level to compare all sources
#or aggregate to province level to compare pre and post harvest data
#plot preharvest, postharvest, and FAO data
pre = pd.read_csv(r'C:\Users\smille25\Downloads\rheasexpansion\Zambia\zambia_preharvest_data_clean.csv')
post = pd.read_csv(r'C:\Users\smille25\Downloads\rheasexpansion\Zambia\moa_data.csv')
code = pd.read_csv(r'C:\Users\smille25\Downloads\rheasexpansion\Zambia\district_province_code.csv')
fao = pd.read_csv(r'C:\Users\smille25\Downloads\rheasexpansion\Zambia\FAOSTAT_data.csv')

pre = pre.set_index('district')
code = code.set_index('district')
pre = pre.join(code)
pre = pre.reset_index()
#try filtering out flagged values
#pre = pre.loc[pre['flag']==0]
pre = pre.groupby(['year']).sum()
pre['Preharvest Yield'] = pre['production(mt)'] / pre['area_planted'] * 1000
pre = pre.rename(columns={'production(mt)':'Preharvest Production','area_planted':'Preharvest Area'})
post = post.groupby(['year']).sum()
post['Postharvest Yield'] = post['production'] / post['hectares'] * 1000
post = post.rename(columns={'production':'Postharvest Production','hectares':'Postharvest Area'})
fao = fao.set_index('year')
fao = fao.rename(columns={'Production':'FAO Production','Area':'FAO Area'})

pre = pre['Preharvest Production']
post = post['Postharvest Production']
fao = fao['FAO Production']

#plot yield or production
df = pd.concat([pre,post,fao],axis=1)
df['FAO Production'].plot()
df['Preharvest Production'].dropna().plot()
df['Postharvest Production'].plot()
plt.legend()
plt.title('Zambia Maize Production (metric tons)')
plt.tight_layout()
plt.show()
#plt.savefig(r'C:\Users\smille25\Downloads\rheasexpansion\Zambia\productioncomparison_national.png')

