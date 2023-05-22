# -*- coding: utf-8 -*-
"""
Created on Mon Mar 23 13:13:06 2020

author: Sara Miller
convert netcdf containing time series of images to one tif file per time step
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

path1 = glob.glob(r'D:\*.nc')

for path in path1:
    xds = Dataset(path)
    date1 = xds['time'][:]
    for d in range(len(date1)):
        ensemble = xds['ensemble'][-24:]
        for e in range(len(ensemble)):
            e1 = e+81

            #get precip for one ensemble and day
            precip1 = xds['precip'][d][e][:][:]

            lat = xds['lat'][:]
            lon = xds['lon'][:]
            #lat = lat.filled(-1000)
            #lon = lon.filled(-1000)
            
            #get the ensemble and day
            ens = int(xds['ensemble'][e])
            start = date(1800,1,1)
            day = start + timedelta(int(xds['time'][d]))
            print(ens,day)
            
            precip = precip1.flatten()
            lat = lat.flatten()
            lon = lon.flatten()
            
            #calculate the real distance between corners and get the width and height in pixels assuming you want a pixel resolution of at least 7 by 7 kilometers
            w = 23
            h = 27
            
            # create a geopandas with as its rows the latitude, longitude an the measrument values. transfrom it to the webmercator projection (or projection of your choosing)
            points = [Point(xy) for xy in zip(lon, lat)]
            
            crs = {'init': 'epsg:4326'}
            data = gpd.GeoDataFrame({'value':precip}, crs=crs, geometry=points)
            #data = data.to_crs({'init': 'epsg:3395'})
            data['lon'] = data.bounds['maxx'].values
            data['lat'] = data.bounds['maxy'].values
            sys.exit()
            #make grid of coordinates. You nee de calculate the coordinate of each pixel in the desired raster
            minlon = 32
            maxlon = 43.5
            minlat = -6
            maxlat = 7.5
            
            lon_list = np.arange(minlon, maxlon, (maxlon-minlon)/w )
            lat_list = np.arange(minlat, maxlat, (maxlat-minlat)/h)
            
            lon_2d, lat_2d = np.meshgrid(lon_list, lat_list)
            
            #print(minlat,maxlat,minlon,maxlon)
            
            #use the values in the geopandas dataframe to interpolate values int the coordinate raster
            r = interpolate.griddata(points = (data['lon'].values,data['lat'].values), values = data['value'].values, xi = (lon_2d, lat_2d))
            r = np.flip(r, axis = 0)
            
            #check result
            #plt.imshow(r)
            precip1 = np.flip(precip1, axis = 0)
            
            #plt.imshow(precip1)
            b = precip1[:, :, np.newaxis]
            b = reshape_as_raster(b)
            #print(b.shape)
            #save raster
            transform = rio.transform.from_bounds(south = minlat, east = maxlon, north = maxlat, west = minlon, width = precip1.shape[1], height = precip1.shape[0]   )
            file_out = path[:-3]+'_{0}_{1}.tiff'.format(day,ens)
            new_dataset = rio.open(file_out , 'w', driver='Gtiff',
                                                height = precip1.shape[0], width = precip1.shape[1],
                                                count= 1, dtype=str(precip1.dtype),
                                                crs= data.crs,
                                                transform= transform)
            new_dataset.write(b)
            new_dataset.close()
