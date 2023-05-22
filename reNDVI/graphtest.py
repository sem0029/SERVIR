# -*- coding: utf-8 -*-
"""
Created on Tue Sep 24 14:22:58 2019

author: Sara Miller
plot NDMA vegetation condition index
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import seaborn as sns
from matplotlib.patches import Patch
snewdf = pd.read_csv(r'C:\Users\smille25\Downloads\svcicounty.csv')

#snewdf = snewdf.set_index('COUNTY')
snewdf['year']= snewdf['index'].str[-4:]

snewdf['month']= snewdf['index'].apply(lambda st: st[st.find("i")+1:st.find("20")])

#create matrix plot of monthly VCI
county = 'Baringo'

table= snewdf.pivot_table(index='year', columns='month',values=county+'3monthVCI')  
table = table.reindex(columns=['1','2','3','4','5','6','7','8','9','10','11','12'])

#define color scale as NDMA's VCI categories
cmap1 = matplotlib.colors.ListedColormap(['darkred', 'red', 'yellow', 'lightgreen', 'green'])
bounds=[0,10,20,35,50,100]
norm1 = matplotlib.colors.BoundaryNorm(bounds, cmap1.N)

fig, ax = plt.subplots(figsize=(10,6))
img = sns.heatmap(table, cmap=cmap1,  norm=norm1, linewidths= 0.3, linecolor='black', cbar=False)
plt.yticks(rotation=0) 
plt.xlabel('Month')
plt.ylabel('Year')
matplotlib.axes.Axes.invert_yaxis(img)
plt.title('3 Month VCI for {0}'.format(county))

legend_elements = [Patch(facecolor='darkred', edgecolor='black', label='<10 Extreme Vegetation Deficit'),
                       Patch(facecolor='red', edgecolor='black', label='10 - 20 Severe Vegetation Deficit'),
                       Patch(facecolor='yellow', edgecolor='black', label='20 - 35 Moderate Vegetation Deficit'),
                       Patch(facecolor='lightgreen', edgecolor='black', label='35 - 50 Normal Vegetation Greenness'),
                       Patch(facecolor='green', edgecolor='black', label='>50 Vegetation Greenness Above Normal')]

plt.legend(handles=legend_elements, bbox_to_anchor=(0.7, -0.15))
plt.tight_layout()
plt.show()