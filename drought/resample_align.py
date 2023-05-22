'''
author: Sara Miller
resample and align pixels of image stack to match template image
'''

import glob
import numpy as np
from osgeo import gdal, gdalconst, osr
import sys, os
import matplotlib.pyplot as plt
import scipy.stats as ss
from PIL import Image
import pandas as pd

# Access files that you want to resample
flist = glob.glob(r'path/to/image/files/*.tif') 
flist = np.sort(flist)

# access template image (image with the resolution you want above files to have)
template = glob.glob(r'path/to/template/image.tif') 


# resample and align pixels to template image
for x in flist:
    # Source
    src_filename = x
    src = gdal.Open(src_filename, gdalconst.GA_ReadOnly)
    src_proj = src.GetProjection()
    src_geotrans = src.GetGeoTransform()

    # We want a section of source that matches this:
    match_ds = gdal.Open(template, gdalconst.GA_ReadOnly)
    match_proj = match_ds.GetProjection()
    match_geotrans = match_ds.GetGeoTransform()
    wide = match_ds.RasterXSize
    high = match_ds.RasterYSize
 
    # Output / destination
    dst_filename = 'output/file/path/{0}'.format(x[-13:]) #change format to get your image name
    dst = gdal.GetDriverByName('GTiff').Create(dst_filename, wide, high, 1, gdalconst.GDT_Float32)
    dst.SetGeoTransform(match_geotrans)
    dst.SetProjection(match_proj)

    # Do the work
    gdal.ReprojectImage(src, dst, src_proj, match_proj, gdalconst.GRA_Bilinear)

    del dst # Flush