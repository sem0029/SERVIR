# -*- coding: utf-8 -*-
"""
Created on Wed Oct 23 09:45:31 2019

author: Sara Miller
make a time series graph for NDVI, index values, and trigger/exit
for payouts for a selected UAI
"""
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

smodislrdf = pd.read_csv(r'C:\Users\smille25\Downloads\rendvistuff\smodislrdf.csv')
emodislrdf = pd.read_csv(r'C:\Users\smille25\Downloads\rendvistuff\emodislrdf.csv')
smodissrdf = pd.read_csv(r'C:\Users\smille25\Downloads\rendvistuff\smodissrdf.csv')
emodissrdf = pd.read_csv(r'C:\Users\smille25\Downloads\rendvistuff\emodissrdf.csv')

columnlist = ['cm2003', 'cm2004', 'cm2005', 'cm2006', 'cm2007', 'cm2008', 'cm2009', 'cm2010', 'cm2011', 'cm2012', 'cm2013', 'cm2014', 'cm2015', 'cm2016','cm2017','cm2018','cm2019']
columnlist1 = ['index2003', 'index2004', 'index2005', 'index2006', 'index2007', 'index2008', 'index2009', 'index2010', 'index2011', 'index2012', 'index2013', 'index2014', 'index2015', 'index2016','index2017','index2018','index2019']
yearlist=[2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018,2019]

#make time series graphs for cumulative NDVI, index values, and trigger and exit values for a UAI for long rains
smodislr2 = smodislrdf.transpose(copy=True)
emodislr2 = emodislrdf.transpose(copy=True)
uainumber = 166

plt.xticks(rotation=45)
plt.rcParams.update({'font.size': 8})
f, [ax1, ax2] = plt.subplots(2, 1)

ax1.plot(smodislr2[uainumber].loc[columnlist].reset_index(drop=True), color='#a8423f', label='reNDVI cumulative NDVI')
ax1.plot(smodislr2[uainumber].loc[columnlist1].reset_index(drop=True), color='#d99694', label='reNDVI index')
ax1.axhline(y=smodislr2[uainumber].loc['trigger'], linestyle='dashed', label='reNDVI trigger', color='#a8423f')
ax1.axhline(y=smodislr2[uainumber].loc['exit'], linestyle='dotted', label='reNDVI exit', color='#a8423f')
ax1.plot(emodislr2[uainumber].loc[columnlist].reset_index(drop=True), color='#416fa6', label='eMODIS cumulative NDVI')
ax1.plot(emodislr2[uainumber].loc[columnlist1].reset_index(drop=True), color='#95b3d7', label='eMODIS index')
ax1.axhline(y=emodislr2[uainumber].loc['trigger'], linestyle='dashed', label='eMODIS trigger', color='#416fa6')
ax1.axhline(y=emodislr2[uainumber].loc['exit'], linestyle='dotted', label='eMODIS exit', color='#416fa6')
legend = plt.legend(loc='lower right', ncol=2, bbox_to_anchor=(0.9, -0.57))
plt.setp(ax1, xticks=np.arange(17), xticklabels=yearlist)

ax1.set_ylabel('Cumulative NDVI and Index Values')
ax1.grid(axis='y', color='gray')


smodissr2 = pd.DataFrame(smodissrdf.transpose(copy=True))
emodissr2 = pd.DataFrame(emodissrdf.transpose(copy=True))


ax2.plot(smodissr2[uainumber].loc[columnlist].reset_index(drop=True), color='#a8423f', label='reNDVI cumulative NDVI')
ax2.plot(smodissr2[uainumber].loc[columnlist1].reset_index(drop=True), color='#d99694', label='reNDVI index')
ax2.axhline(y=smodissr2[uainumber].loc['trigger'], linestyle='dashed', label='reNDVI trigger', color='#a8423f')
ax2.axhline(y=smodissr2[uainumber].loc['exit'], linestyle='dotted', label='reNDVI exit', color='#a8423f')
ax2.plot(emodissr2[uainumber].loc[columnlist].reset_index(drop=True), color='#416fa6', label='eMODIS cumulative NDVI')
ax2.plot(emodissr2[uainumber].loc[columnlist1].reset_index(drop=True), color='#95b3d7', label='eMODIS index')
ax2.axhline(y=emodissr2[uainumber].loc['trigger'], linestyle='dashed', label='eMODIS trigger', color='#416fa6')
ax2.axhline(y=emodissr2[uainumber].loc['exit'], linestyle='dotted', label='eMODIS exit', color='#416fa6')
ax2.legend(loc='lower right', ncol=2, bbox_to_anchor=(.9,-.57))
plt.setp(ax2, xticks=np.arange(17), xticklabels=yearlist)
ax2.set_xticks(np.arange(17), yearlist)
#ax2.tick_params(labelrotation=45)
ax2.set_xlabel('Year')
ax2.set_ylabel('Cumulative NDVI and Index Values')
ax2.grid(axis='y', color='gray')


f.set_size_inches(6, 7)

f.tight_layout()
f.savefig(r'C:\Users\smille25\Downloads\rendvistuff\paperimages\FIG7_.png', format='png', dpi=300, frameon=True, bbox_inches='tight')
plt.show()