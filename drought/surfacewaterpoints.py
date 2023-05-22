# -*- coding: utf-8 -*-
"""
Created on Fri Mar 10 10:54:24 2023

author: Sara Miller

analyze and plot surface water point data for Kenya, Ethiopia, and Somalia
"""

import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import glob
import sys
import re
import geopandas as gpd

kcsvs = glob.glob(r'D:\droughtpaper\surfacewater\KenyaWaterpointData\*.csv')
ecsvs = glob.glob(r'D:\droughtpaper\surfacewater\EthiopiaWaterpointData\*.csv')
scsvs = glob.glob(r'D:\droughtpaper\surfacewater\SomaliaWaterpointData\*.csv')
allcsvs = glob.glob(r'D:\droughtpaper\surfacewater\*WaterpointData\*.csv')
#read all csvs for one country and append to single df
df = pd.DataFrame()
coords = pd.DataFrame()
for csv in allcsvs:
    dfappend = pd.read_csv(csv)
    lat = dfappend['y_coord'][1]
    lon = dfappend['x_coord'][1]
    name = re.search('Data'+'(.+?)'+'.csv', csv).group(1)
    latlondf = pd.DataFrame({'name':[name],'latitude':[lat],'longitude':[lon]})
    try:
        dfappend['date'] = pd.to_datetime(dfappend['date'],format='%m/%d/%Y')
    except:
        dfappend['date'] = pd.to_datetime(dfappend['date'],format='%Y-%m-%d')
    dfappend = dfappend[['date','scaled_depth']]
    dfappend = dfappend.set_index('date')
    #dfappend = dfappend.rename(columns={'scaled_depth':name})
    #print(dfappend)
    #df = pd.concat([df,dfappend],axis=1)
    coords = pd.concat([coords,latlondf])
'''
print(df)
fig, ax = plt.subplots(figsize=(16,6))
df.plot(color='gray',linewidth=0.5,alpha=0.3,legend=False,ax=ax)
df['average'] = df.mean(axis=1)
df['average'].plot(linewidth=2,ax=ax)
plt.title('Somalia Surface Water')
plt.ylabel('Percent of Maximum Depth')
plt.tight_layout()
plt.show()
'''
fig, ax = plt.subplots(figsize=(6,6))
ken = gpd.read_file(r'C:\Users\smille25\Downloads\rheasexpansion\Kenya\gadm36_KEN_0.shp')
som = gpd.read_file(r'C:\Users\smille25\Downloads\rheasexpansion\Somalia\gadm36_SOM_shp\gadm36_SOM_0.shp')
eth = gpd.read_file(r'C:\Users\smille25\Downloads\rheasexpansion\Ethiopia\gadm36_ETH_0.shp')

geometry = gpd.points_from_xy(coords.longitude, coords.latitude)
geo_df = gpd.GeoDataFrame(geometry = geometry)
ken.boundary.plot(ax=ax)
eth.boundary.plot(ax=ax)
som.boundary.plot(ax=ax)
geo_df.plot(ax=ax)
plt.show()