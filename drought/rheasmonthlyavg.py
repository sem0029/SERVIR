# -*- coding: utf-8 -*-
"""
Created on Thu Mar 31 13:07:20 2022

author: Sara Miller
get monthly average soil moisture from RHEAS daily tif files
"""

import glob
import rasterio as rio
import numpy as np
import sys

for m in range(1,13):
    for yr in range(2000,2022):
        for lyr in ['1','2','3']:
            var = 'soil_moist'
            try:
                file_list = glob.glob(r'D:\drought\drought\{0}\ken_n_5_{0}_{1}-{2}*_{3}.tiff'.format(var,yr,str(m).zfill(2),lyr))
                def read_file(file):
                    with rio.open(file) as src:
                        return(src.read(1))
                print(file_list)
                # Read all data as a list of numpy arrays 
                array_list = [read_file(x) for x in file_list]
                # Perform averaging
                array_out = np.mean(array_list, axis=0)
                
                # Get metadata from one of the input files
                with rio.open(file_list[0]) as src:
                    meta = src.meta
                
                meta.update(dtype=rio.float32)
                
                # Write output file
                out_path = r'D:\drought\{0}_lyr{1}\{0}lyr{1}_{2}_{3}.tif'.format(var,lyr,m,yr)
                with rio.open(out_path, 'w', **meta) as dst:
                    dst.write(array_out.astype(rio.float32), 1)
            except:
                print(file_list,m,yr,var)
                sys.exit()
                #continue