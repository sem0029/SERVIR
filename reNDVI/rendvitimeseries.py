'''
create example time series graphs from CSV for reNDVI paper
one showing good agreement between reNDVI and eMODIS
and one showing poor agreement
author: Sara Miller
'''

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


gooddf = pd.read_csv(r'C:\Users\smille25\Downloads\goodtimeseries.csv')
baddf = pd.read_csv(r'C:\Users\smille25\Downloads\badtimeseries.csv')

gooddf['datetime'] = pd.to_datetime(gooddf['system:time_start'])
gooddf = gooddf.set_index('datetime')
baddf['datetime'] = pd.to_datetime(baddf['system:time_start'])
baddf = baddf.set_index('datetime')


plt.rcParams.update({'font.size': 8})
f, axes = plt.subplots(2, 2, figsize=(8,5), gridspec_kw={'width_ratios': [4, 1.5]})


axes[0,0].plot(gooddf['emodis'], color='#416fa6', label='eMODIS NDVI')
axes[0,0].plot(gooddf['smodis'], color='#a8423f', label='reNDVI')
axes[1,0].plot(baddf['emodis'], color='#416fa6', label='eMODIS NDVI')
axes[1,0].plot(baddf['smodis'], color='#a8423f', label='reNDVI')


axes[1,0].set_ylabel('NDVI')
axes[1,0].set_xlabel('Year')
axes[0,0].set_ylabel('NDVI')
axes[1,0].legend(loc='lower left', ncol=2)
#axes[0,0].text(0.5, 0.5, 'a.', fontsize=8)
#axes[1,0].text(0.65, 0.0, 'b.', fontsize=8)
axes[0,0].set_title('a.', x=-.15)
axes[1,0].set_title('b.', x=-.15)

axes[0,1].scatter(x=gooddf['emodis'],y=gooddf['smodis'], s=8)
axes[1,1].scatter(x=baddf['emodis'],y=baddf['smodis'], s=8)
axes[0,1].set_ylabel('reNDVI')
axes[1,1].set_ylabel('reNDVI')
axes[1,1].set_xlabel('eMODIS NDVI')
x = np.linspace(0,0.4,100)
y = x
axes[0,1].plot(x, y, 'black', linestyle = '--', label='1:1')
x = np.linspace(0,0.9,100)
y = x
axes[1,1].plot(x, y, 'black', linestyle = '--', label='1:1')
axes[1,1].legend(loc='lower left')
#add text box with correlation and mapd values
props = dict(facecolor='white', alpha=0.5, edgecolor='none')
axes[1,1].text(0.65, 0.0, 'Correlation=0.45\nMAPD=25.55%', fontsize=8,
        verticalalignment='bottom', horizontalalignment='center', bbox=props)
axes[0,1].text(0.287, 0.0, 'Correlation=0.94\nMAPD=5.87%', fontsize=8,
        verticalalignment='bottom', horizontalalignment='center', bbox=props)

f.tight_layout()
f.savefig(r'C:\Users\smille25\Downloads\rendvistuff\paperimages\FIG5_new.png', format='png', dpi=300, frameon=True, bbox_inches='tight')
plt.show()
