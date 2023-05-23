'''
author: Sara Miller
calculate cfsv2 forecast skill at 0-6 month lead times
'''

import glob
import numpy as np
from osgeo import gdal, gdalconst, osr
import sys, os
import matplotlib.pyplot as plt
import scipy.stats as ss
from PIL import Image
import pandas as pd

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

for m1 in range(0,7):
    # Access resampled vic soil moisture
    viclist = glob.glob('/home/Socrates/rheas/RHEAS/Kenya_VIC/chirpsresample/*.tiff') #change to schema name, table1 name /* .tif (or .tiff)
    viclist = np.sort(viclist)
    # access SMAP soil moisture
    smaplist = glob.glob('/home/Socrates/rheas/RHEAS/monthlynmme/nmme{0}month/nmme_bcsd_spatial_forcing_*.tiff'.format(m1)) #change to schema name, table1 name /* .tif (or .tiff)
    smaplist = np.sort(smaplist)
    
    
    # filter dates so vic and smap are temporally aligned
    viclist = [x for x in viclist if(int(x[-13:-5]) >= 19900101)]
    viclist = [x for x in viclist if(int(x[-13:-5]) <= 20201231)]
    
    smaplist = [x for x in smaplist if((int(x[83:87])*10000+int(x[88:90])*100+int(x[91:93])) >= 19900101)]
    smaplist = [x for x in smaplist if((int(x[83:87])*10000+int(x[88:90])*100+int(x[91:93])) <= 20201231)]
    #smaplist = [x for x in smaplist if(int(x[-13:-5]) <= 20200220)]
    #print((x[-13:-5] for x in viclist),(x[-13:-5] for x in smaplist))
    #get dates to make sure smap and vic are aligned
    vdates = np.empty(len(viclist))
    vdates = [x[-13:-5] for x in viclist]
    sdates = np.empty(len(smaplist))
    sdates = [str((int(x[83:87])*10000+int(x[88:90])*100+int(x[91:93]))) for x in smaplist]
    #sdates = [x[-13:-5] for x in smaplist]
    
    difdates = [item for item in vdates if item not in sdates]
    #alldates = np.column_stack((vdates, sdates))
    #np.set_printoptions(threshold=np.nan)
    #print(difdates)
    #viclist = [x for x in viclist if((x[-13:-5]) not in difdates)]
    #vdates = [x[-13:-5] for x in viclist]
    
    #print(len(viclist),len(smaplist))
    #sys.exit()
    for m2 in range(1,13):
        # get skill scores per pixel
        image_height = 27
        image_width = 23
        
        vic_stack = np.empty((image_height, image_width, len(viclist))) # Create empty HxWxN array/matrix
        
        smap_stack = np.empty((image_height, image_width, len(smaplist))) # Create empty HxWxN array/matrix
        
        #p = np.empty((image_height, image_width))
        
        for i, fname in enumerate(viclist):
            im = Image.open(fname)
            img = np.array(im)
            vic_stack[:,:,i] = img # Set the i:th slice to this image
        
        for i, fname in enumerate(smaplist):
            im = Image.open(fname)
            img = np.array(im)
            smap_stack[:,:,i] = img # Set the i:th slice to this image
        
        pod = np.empty((image_height, image_width))
        far = np.empty((image_height, image_width))
        csi = np.empty((image_height, image_width))
        hss = np.empty((image_height, image_width))
        
        #loop through each pixel and calculate onset dates for each season
        for i in range(0,27):
            for j in range(0,23):
                if(vic_stack[i,j,:].all() != -9999):
                    df = pd.DataFrame()
                    df1 = pd.DataFrame()
                    df1['CFSv2'] = smap_stack[i,j,:]
                    df['CHIRPS'] = vic_stack[i,j,:]
                    df['date'] = vdates
                    #pd.set_option("display.max_rows", None, "display.max_columns", None)
                    df = df.set_index(['date'])
                    df1['date'] = sdates
                    df1 = df1.groupby(['date']).mean()
                    #df1.index = pd.to_datetime(df1.index,format='%Y%m%d')
                    df = pd.concat([df,df1],axis=1)
                    df.index = pd.to_datetime(df.index,format='%Y%m%d')
                    df = df.groupby(pd.Grouper(freq='M')).sum()
        
                    #get only rainy seasons
                    df = df[(df.index.month == m2)]
                    #print(df)
                    
                    #classify as normal, wet or dry based on 20th and 80th percentiles
                    df['Cperc'] = df['CHIRPS'].rank(pct=True)
                    df['fperc'] = df['CFSv2'].rank(pct=True)    
                    df['observed'] = 0
                    df['observed'].loc[df['Cperc']<=0.20] = 1
                    df['forecast'] = 0
                    df['forecast'].loc[df['fperc']<=0.20] = 1
                    
                    a = len(df[(df['observed']==1) & (df['forecast']==1)])
                    b = len(df[(df['observed']==0) & (df['forecast']==1)])
                    c = len(df[(df['observed']==1) & (df['forecast']==0)])
                    d = len(df[(df['observed']==0) & (df['forecast']==0)])
                    try:
                        POD = a/(a+c)
                    except:
                        POD = np.nan
                    try:
                        FAR = b/(a+b)
                    except:
                        FAR = np.nan
                    try:
                        CSI = a/(a+b+c)
                    except:
                        CSI = np.nan
                    try:
                        HSS = (2*(a*d-b*c))/(((a+c)*(c+d))+((a+b)*(b+d)))
                    except:
                        HSS = np.nan
                    pod[i,j]=POD
                    far[i,j]=FAR
                    csi[i,j]=CSI
                    hss[i,j]=HSS
                    print(a,b,c,d,POD,FAR,CSI,HSS)
                    
        
        
        reference = gdal.Open(viclist[1])
        write_gtiff(pod, reference, '/home/Socrates/rheas/RHEAS/Kenya_VIC/skill/pod{0}_{1}d.tiff'.format(m1,m2))
        write_gtiff(far, reference, '/home/Socrates/rheas/RHEAS/Kenya_VIC/skill/far{0}_{1}d.tiff'.format(m1,m2))
        write_gtiff(csi, reference, '/home/Socrates/rheas/RHEAS/Kenya_VIC/skill/csi{0}_{1}d.tiff'.format(m1,m2))
        write_gtiff(hss, reference, '/home/Socrates/rheas/RHEAS/Kenya_VIC/skill/hss{0}_{1}d.tiff'.format(m1,m2))
