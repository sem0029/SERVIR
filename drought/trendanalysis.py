'''
author: Sara Miller
get time series of weather/vic output data
smooths yearly to remove seasonal variance and gets trend information
optionally gets trends for each season (long or short rains)
'''

import glob
import numpy as np
from osgeo import gdal, gdalconst, osr
import sys, os
#import matplotlib.pyplot as plt
import scipy.stats as ss
from PIL import Image
import pandas as pd


# Access resampled vic soil moisture
viclist = glob.glob('/data/RHEAS/kenya/nc/era5temp/data/*.tiff') #change to schema name, table1 name /* .tif (or .tiff)
viclist = np.sort(viclist)
vdates = [x[-15:-5] for x in viclist]

# get correlation per pixel
image_height = 241
image_width = 211

vic_stack = np.empty((image_height, image_width, len(viclist))) # Create empty HxWxN array/matrix
trends = np.empty((image_height, image_width))
rvals = np.empty((image_height, image_width))
pvals = np.empty((image_height, image_width))

for i, fname in enumerate(viclist):
    with Image.open(fname) as im:
        img = np.array(im)
    vic_stack[:,:,i] = img # Set the i:th slice to this image

#loop through each pixel and calculate correlation and p values
for i in range(0,image_height):
    for j in range(0,image_width):
        df = pd.DataFrame()
        df['vic'] = vic_stack[i,j,:]
        df['date'] = vdates 
        df = df.set_index('date')
        df.mask((df['vic'] < 0.0), inplace=True)
        if(pd.notnull(df["vic"]).any()==True):
            '''
            # yealy rolling mean
            df = df.rolling(window=365).sum()
            df = df.reset_index()
            df = df.loc[df['date']>'2011-1-1']
            df['year'] = pd.DatetimeIndex(df['date']).year
            df['jday'] = pd.DatetimeIndex(df['date']).dayofyear
            df['date2'] = (df['year']-2010)+(df['jday']/365)
            '''
            #seasonal rainfall total/temp mean trends
            df = df.reset_index()

            #select only long rains trends
            df = df.loc[((pd.DatetimeIndex(df['date']).month)>2)&((pd.DatetimeIndex(df['date']).month)<7)]
            #select only short rains trends
            #df = df.loc[((pd.DatetimeIndex(df['date']).month)>9)]

            df['year'] = pd.DatetimeIndex(df['date']).year
            df = df.groupby(['year']).mean()
            df = df.reset_index()
            df['date2'] = (df['year']-1982)


            #print(df)
            #calculate trends (slope) and significance (p values)
            x = df['date2']
            y = df['vic']
            slope, intercept, r, p, se = ss.linregress(x,y)
            r2 = r*r
            print(slope,r,r2,p)
            #sys.exit()
            trends[i,j] = slope
            rvals[i,j] = r
            pvals[i,j] = p


#write trend information to geotiffs

def write_gtiff(array, gdal_obj, outputpath, dtype=gdal.GDT_Float32, options=0, color_table=0, nbands=1, nodata=False):
    """
    Writes a geotiff.

    array: numpy array to write as geotiff
    gdal_obj: object created by gdal.Open() using a tiff that has the SAME CRS, geotransform, and size as the array you're writing
    outputpath: path including filename.tiff
    dtype (OPTIONAL): datatype to save as
    nodata (default: FALSE): set to any value you want to use for nodata; if FALSE, nodata is not set
    """

    gt = gdal_obj.GetGeoTransform()

    width = np.shape(array)[1]
    height = np.shape(array)[0]

    # Prepare destination file
    driver = gdal.GetDriverByName("GTiff")
    if options != 0:
        dest = driver.Create(outputpath, width, height, nbands, dtype, options)
    else:
        dest = driver.Create(outputpath, width, height, nbands, dtype)
    # Write output raster
    if color_table != 0:
        dest.GetRasterBand(1).SetColorTable(color_table)

    dest.GetRasterBand(1).WriteArray(array)

    if nodata is not False:
        dest.GetRasterBand(1).SetNoDataValue(nodata)

    # Set transform and projection
    dest.SetGeoTransform(gt)
    wkt = gdal_obj.GetProjection()
    srs = osr.SpatialReference()
    srs.ImportFromWkt(wkt)
    dest.SetProjection(srs.ExportToWkt())

    # Close output raster dataset 
    dest = None

# turn arrays back into images, set crs and save
reference = gdal.Open(viclist[1])
write_gtiff(trends, reference, '/data/RHEAS/kenya/drought/temptrendLR.tif')
write_gtiff(pvals, reference, '/data/RHEAS/kenya/drought/temppLR.tif')
