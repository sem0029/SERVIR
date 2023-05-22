# -*- coding: utf-8 -*-
"""
Created on Fri Jun 26 10:33:26 2020

author: Sara Miller
compare rendvi index to livestock deaths
"""

import pandas as pd
import numpy as np
import sys
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as ss
import matplotlib.lines as mlines
from scipy.optimize import curve_fit

r'''
#read in livestock loss data from panel surveys
#livestock losses
data = pd.read_csv(r'C:\Users\smille25\Downloads\paneldata20170823\panel_data\S6C Livestock Losses.csv')
data = data.set_index('hhid')
#identification
iddata = pd.read_csv(r'C:\Users\smille25\Downloads\paneldata20170823\panel_data\S0A_HouseholdIdentificationInformationUAIs.csv')
iddata = iddata.set_index('hhid')
#livestock accounting per year
accounting = pd.read_csv(r'C:\Users\smille25\Downloads\paneldata20170823\panel_data\S6B Livestock Accounting.csv')
accounting = accounting.set_index('hhid')
#livestock total animals
stock = pd.read_csv(r'C:\Users\smille25\Downloads\paneldata20170823\panel_data\S6A Livestock Stock.csv')
stock = stock.set_index('hhid')
#livestock intake year/month
intake = pd.read_csv(r'C:\Users\smille25\Downloads\paneldata20170823\panel_data\S6D Livestock Intake.csv')
intake = intake.set_index('hhid')
#livestock offtake year/month
offtake = pd.read_csv(r'C:\Users\smille25\Downloads\paneldata20170823\panel_data\S6E Livestock Offtake.csv')
offtake = offtake.set_index('hhid')
#livestock births year/month
births = pd.read_csv(r'C:\Users\smille25\Downloads\paneldata20170823\panel_data\S6F Livestock Births.csv')
births = births.set_index('hhid')
#livestock slaughter year/month
slaughter = pd.read_csv(r'C:\Users\smille25\Downloads\paneldata20170823\panel_data\S6G Livestock Slaughter.csv')
slaughter = slaughter.set_index('hhid')

#index data
elr = pd.read_csv(r'C:\Users\smille25\Downloads\emodispayouts.csv')

rlr = pd.read_csv(r'C:\Users\smille25\Downloads\rendvipayouts.csv')


#match id data to uais
for i in data.index:
    try:
        data.at[i,'UAI'] = int(iddata.at[i,'UAI'].mean())
    except:
        pass

#total animals per household at survey time
stock = stock.groupby(['hhid','year']).sum()
stocksr = pd.DataFrame(stock['s6q1'])
stocksr = stocksr.reset_index()
stocksr['season1'] = stocksr['year'].astype(str)+'sr'
stocksr = stocksr.set_index(['hhid','season1'])

#get total livestock births/deaths/intake/outtake before long rains
intake['season'] = np.nan
intake['season'] = np.where(((intake['month'] > 2) & (intake['month'] < 10)), 'lr', 'sr')
intake['season'].loc[intake['month']<1] = np.nan
intake['season1'] = np.where((intake['month'] > 2), (intake['s6q27a'].astype(str)+intake['season']), ((intake['s6q27a']-1).astype(str)+intake['season']))
intake = intake.loc[(((intake['month']>9) | (intake['month']<3)))]
intake = intake.groupby(['hhid','season1']).sum()
intakesr = pd.DataFrame(intake['s6q30'].reset_index()).set_index(['hhid','season1'])

offtake['season'] = np.nan
offtake['season'] = np.where(((offtake['month'] > 2) & (offtake['month'] < 10)), 'lr', 'sr')
offtake['season'].loc[offtake['month']<1] = np.nan
offtake['season1'] = np.where((offtake['month'] > 2), (offtake['s6q36a'].astype(str)+offtake['season']), ((offtake['s6q36a']-1).astype(str)+offtake['season']))
offtake = offtake.loc[(((offtake['month']>9) | (offtake['month']<3)))]
offtake = offtake.groupby(['hhid','season1']).sum()
offtakesr = pd.DataFrame(offtake['s6q39'].reset_index()).set_index(['hhid','season1'])

births['season'] = np.nan
births['season'] = np.where(((births['month'] > 2) & (births['month'] < 10)), 'lr', 'sr')
births['season'].loc[births['month']<1] = np.nan
births['year'] = births['year'].fillna(0)
births['year'] = births['year'].astype(int)
births['season1'] = np.where((births['month'] > 2), (births['year'].astype(str)+births['season']), ((births['year']-1).astype(str)+births['season']))
births = births.loc[(((births['month']>9) | (births['month']<3)))]
births = births.groupby(['hhid','season1']).sum()
birthssr = pd.DataFrame(births['s6q47'].reset_index()).set_index(['hhid','season1'])

slaughter['season'] = np.nan
slaughter['season'] = np.where(((slaughter['s6q49b'] > 2) & (slaughter['s6q49b'] < 10)), 'lr', 'sr')
slaughter['season'].loc[slaughter['s6q49b']<1] = np.nan
slaughter['s6q49a'] = slaughter['s6q49a'].fillna(0)
slaughter['s6q49a'] = slaughter['s6q49a'].astype(int)
slaughter['season1'] = np.where((slaughter['s6q49b'] > 2), (slaughter['s6q49a'].astype(str)+slaughter['season']), ((slaughter['s6q49a']-1).astype(str)+slaughter['season']))
slaughter = slaughter.loc[(((slaughter['s6q49b']>9) | (slaughter['s6q49b']<3)))]
slaughter = slaughter.groupby(['hhid','season1']).sum()
slaughtersr = pd.DataFrame(slaughter['s6q51'].reset_index()).set_index(['hhid','season1'])



#get total losses per season/UAI
data['season'] = np.nan
data['season'] = np.where(((data['s6q20b'] > 2) & (data['s6q20b'] < 10)), 'lr', 'sr')
data['season'].loc[data['s6q20b']<1] = np.nan
data['season1'] = np.where((data['s6q20b'] > 2), (data['s6q20a'].astype(str)+data['season']), ((data['s6q20a']-1).astype(str)+data['season']))
#print(data[['s6q20a','s6q20b','season1']])
#losses = data.loc[data['s6q22']=='Starvation/Drought']
lossdata = data.groupby(['hhid','season1']).sum()
lossdata = pd.DataFrame(lossdata['s6q24'])


#get total livestock at start of long rains
calc = pd.concat([stocksr,intakesr,offtakesr,birthssr,slaughtersr,lossdata],axis=1)
calc = calc.fillna(0)
calc['stocklr'] = calc['s6q1'] - calc['s6q24']+calc['s6q30']-calc['s6q39']+calc['s6q47']-calc['s6q51']
calc1 = calc['stocklr'].reset_index()
calc1['year'] = ((calc1['season1'].str[:4]).astype(int)) + 1
calc1 = calc1.loc[(calc1['season1'].str[4:]=='sr')]
calc1['season1'] = calc1['year'].astype(str)+'lr'
calc1 = calc1.rename(columns={'stocklr': 's6q1'})
calc1 = calc1.set_index(['hhid','season1'])
stocknum = pd.concat([stocksr,calc1])
stocknum = stocknum.reset_index()
stocknum = stocknum.set_index('hhid')
stocknum = stocknum.loc[(stocknum['year']>2009)]

#match id data to uais
for i in stocknum.index:
    try:
        stocknum.at[i,'UAI'] = int(iddata.at[i,'UAI'].mean())
    except:
        pass

stocknum = stocknum.groupby(['UAI','season1']).sum()
stocknum = stocknum.drop(columns='year')


losses1 = data.groupby(['UAI','season1']).sum()
losses = pd.concat([losses1,stocknum],axis=1)
losses = losses.reset_index()
losses['emodis'] = np.nan
losses['rendvi'] = np.nan
for index, row in losses.iterrows():
    a = losses['season1'].loc[index]
    b = losses['UAI'].loc[index]
    losses['emodis'].loc[index] = elr[a].loc[b]
    losses['rendvi'].loc[index] = rlr[a].loc[b]
    

losses['avgloss'] = losses['s6q24']/losses['s6q1']

    
#plot index for uais compared to livestock losses
losses.to_csv(r'C:\Users\smille25\Downloads\livestocklosscomparisonpay.csv')

'''

loss = pd.read_csv(r'C:\Users\smille25\Downloads\livestocklosscomparisonpay.csv')
#get rid of unrealistic loss data
loss = loss.loc[((loss['avgloss']<1) & (loss['avgloss']>0))]
loss['avgloss'] = loss['avgloss']*100
#plot losses vs index
slope, intercept, r_value, p_value, std_err = ss.linregress(loss['emodis'],loss['avgloss'])
slope1, intercept1, r_value1, p_value1, std_err1 = ss.linregress(loss['rendvi'],loss['avgloss'])
fig, ax = plt.subplots(figsize=(6,5))
#sns.regplot(loss['emodis'], loss['avgloss'])
#sns.regplot(loss['rendvi'], loss['avgloss'])

loss = loss.rename(columns={'rendvi':'reNDVI','emodis':'eMODIS','avgloss':'Livestock Mortality %'})


pal = dict(reNDVI="#a8423f", eMODIS="#416fa6")
#g = sns.FacetGrid(loss, palette=pal, size=5);
loss.plot.scatter("eMODIS", "Livestock Mortality %", s=50, alpha=.7, linewidth=.5, edgecolor="white",ax=ax,color="#416fa6")
loss.plot.scatter("reNDVI", "Livestock Mortality %", s=50, alpha=.7, linewidth=.5, edgecolor="white",color="#a8423f",ax=ax)
blue_star = mlines.Line2D([], [], color='#416fa6', marker='o', linestyle='None',
                          markersize=5, label='eMODIS')
red_square = mlines.Line2D([], [], color='#a8423f', marker='o', linestyle='None',
                          markersize=5, label='reNDVI')


plt.legend(handles=[blue_star, red_square])

#add trendline
x = np.array(loss['eMODIS'])
y = np.array(loss['Livestock Mortality %'])
m, b = np.polyfit(x, y, 1)
#m = slope, b=intercept
plt.plot(x, m*x + b)
x1 = np.array(loss['reNDVI'])
m1, b1 = np.polyfit(x1, y, 1)
#m = slope, b=intercept
plt.plot(x1, m*x1 + b1,color='#a8423f')

plt.xlabel('Index')
plt.tight_layout()
plt.savefig(r'C:\Users\smille25\Downloads\rendvistuff\paperimages\FIG9_.png', format='png', dpi=300, frameon=True, bbox_inches='tight')

plt.show()

print('emodis r:{0} p:{1}; rendvi r:{2} p:{3}'.format(r_value,p_value,r_value1,p_value1))

r'''
#mask index values greater than 0
loss1 = loss.loc[loss['rendvi'] < 0]
loss2 = loss.loc[loss['emodis'] < 0]

slope, intercept, r_value, p_value, std_err = ss.linregress(loss2['emodis'],loss2['avgloss'])
slope1, intercept1, r_value1, p_value1, std_err1 = ss.linregress(loss1['rendvi'],loss1['avgloss'])
fig, ax = plt.subplots(figsize=(9,6))
sns.regplot(loss2['emodis'], loss2['avgloss'])
sns.regplot(loss1['rendvi'], loss1['avgloss'])
print('emodis r:{0} p:{1}; rendvi r:{2} p:{3}'.format(r_value,p_value,r_value1,p_value1))
'''
