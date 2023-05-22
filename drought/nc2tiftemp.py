# -*- coding: utf-8 -*-
"""
Created on Thu Apr 13 10:22:02 2023

author: Sara Miller
convert era5 temperature netcdf data to tif files
"""

import rasterio as rio 
#import rioxarray
#import xarray
from netCDF4 import Dataset
from datetime import date, timedelta
import numpy as np
from scipy import interpolate
from shapely.geometry import Point
import geopandas as gpd
from geopy.distance import geodesic
import matplotlib.pyplot as plt
import sys 
from rasterio.plot import reshape_as_raster, reshape_as_image
import glob
import itertools

path1 = glob.glob(r'C:\Users\smille25\Downloads\era5temp\data.nc')

for path in path1:
    xds = Dataset(path)
    date1 = xds['time'][:]

    for d in range(len(date1)):

            #get precip for one ensemble and day
            temp1 = xds['t2m'][d][:][:]

            lat = xds['latitude'][:]
            lon = xds['longitude'][:]
            #lat = lat.filled(-1000)
            #lon = lon.filled(-1000)

            
            #get the day
            start = date(1900,1,1)
            day = start + timedelta(hours=int(xds['time'][d]))

            temp = temp1.flatten()
            temp = temp.data
            temp[temp==-32767]=np.nan
            temp = temp[:50851]
            lat = lat.flatten().data.tolist()
            lon = lon.flatten().data.tolist()
            xypoints = [lat,lon]
            combinations = [p for p in itertools.product(*xypoints)]
            #calculate the real distance between corners and get the width and height in pixels assuming you want a pixel resolution of at least 7 by 7 kilometers
            w = 211
            h = 241
            
            # create a geopandas with as its rows the latitude, longitude an the measurement values. transform it to the webmercator projection (or projection of your choosing)
            points = [Point(xy) for xy in combinations]
            
            crs = {'init': 'epsg:4326'}
            data = gpd.GeoDataFrame({'value':temp}, crs=crs, geometry=points)
            #data = data.to_crs({'init': 'epsg:3395'})
            data['lon'] = data.bounds['maxx'].values
            data['lat'] = data.bounds['maxy'].values
            #make grid of coordinates. You nee de calculate the coordinate of each pixel in the desired raster
            minlon = 31.95
            maxlon = 53.05
            minlat = -8.05
            maxlat = 16.05
            
            lon_list = np.arange(minlon, maxlon, (maxlon-minlon)/w )
            lat_list = np.arange(minlat, maxlat, (maxlat-minlat)/h)
            
            lon_2d, lat_2d = np.meshgrid(lon_list, lat_list)
            
            #print(minlat,maxlat,minlon,maxlon)
            
            #use the values in the geopandas dataframe to interpolate values int the coordinate raster
            r = interpolate.griddata(points = (data['lon'].values,data['lat'].values), values = data['value'].values, xi = (lon_2d, lat_2d))
            r = np.flip(r, axis = 0)
            
            #check result
            #plt.imshow(r)
            temp1 = np.flip(temp1, axis = 0)
            temp1 = temp1[1]
            temp1[temp1.data==-32767]=np.nan
            temp1 = np.float32(temp1)

            plt.imshow(temp1)
            b = temp1[:, :, np.newaxis]
            b = reshape_as_raster(b)
            #print(b.shape)
            #save raster
            transform = rio.transform.from_bounds(south = minlat, east = maxlon, north = maxlat, west = minlon, width = temp1.shape[1], height = temp1.shape[0]   )
            file_out = path[:-3]+'_{0}.tiff'.format(day)
            new_dataset = rio.open(file_out , 'w', driver='Gtiff',
                                                height = temp1.shape[0], width = temp1.shape[1],
                                                count= 1, dtype=str(temp1.dtype),
                                                crs= data.crs,
                                                transform= transform)
            new_dataset.write(b)
            new_dataset.close()
