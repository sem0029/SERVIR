import numpy as np
import sys
from netCDF4 import Dataset
from datetime import date, timedelta
import gdal 
from osgeo import osr

path = r'C:\Users\smille25\Documents\nmmedata\CFSv2.BCSD.201208.nc'
file = Dataset(path, 'r')
precip = file.variables['precip']
temp = file.variables['tas']




for day in range(212):
    for ensemble in range(0,24):
        try:
            #select precip and temp data for each day/ensemble
            p = precip[day,ensemble,:,:]
            t = temp[day,ensemble,:,:]
            #convert temp from K to C
            t = t-273.15
    
            lat = file.variables['lat'][:,:]
            lon = file.variables['lon'][:,:]
            #get date from number of days after 1-1-1800
            start = date(1800,1,1)
            fdate = timedelta((file.variables['time'][day]).mean())+start
            ###################################################################################
            #write precip data to tif
            #from https://gis.stackexchange.com/questions/37238/writing-numpy-array-to-raster-file
            array=p
            
            #adding/subtracting 0.25 here since the lat/lon we have is from the pixel center
            xmin,ymin,xmax,ymax = [(lon.min()-0.25),(lat.min()-0.25),(lon.max()+0.25),(lat.max()+0.25)]
            nrows,ncols = np.shape(array)
            xres = ((xmax-xmin))/float(ncols)
            yres = ((ymax-ymin))/float(nrows)
            geotransform=(xmin,xres,180,ymax,0, -yres)   
            
            output_raster = gdal.GetDriverByName('GTiff').Create(path[:-3]+'\\precip'+str(fdate)+'_'+str(ensemble+1)+'.tif',ncols, nrows, 1 ,gdal.GDT_Float32)  # Open the file
            output_raster.SetGeoTransform(geotransform)  #Specify its coordinates
            srs = osr.SpatialReference()                 #Establish its coordinate encoding
            srs.ImportFromEPSG(4326)                     #specifies WGS84 lat long.
                                                         
            output_raster.SetProjection( srs.ExportToWkt() )   # Exports the coordinate system to the file
            output_raster.GetRasterBand(1).WriteArray(array)   # Writes array to the raster
            
            output_raster.FlushCache()
            sys.exit()
            ####################################################################################
            #write temp tif
            array=t
            
            #adding/subtracting 0.25 here since the lat/lon we have is from the pixel center
            xmin,ymin,xmax,ymax = [(lon.min()-0.25),(lat.min()-0.25),(lon.max()+0.25),(lat.max()+0.25)]
            nrows,ncols = np.shape(array)
            xres = ((xmax-xmin))/float(ncols)
            yres = ((ymax-ymin))/float(nrows)
            geotransform=(xmin,xres,0,ymax,0, -yres)   
            
            output_raster = gdal.GetDriverByName('GTiff').Create(path[:-3]+'\\temp'+str(fdate)+'_'+str(ensemble+1)+'.tif',ncols, nrows, 1 ,gdal.GDT_Float32)  # Open the file
            output_raster.SetGeoTransform(geotransform)  #Specify its coordinates
            srs = osr.SpatialReference()                 #Establish its coordinate encoding
            srs.ImportFromEPSG(4326)                     #specifies WGS84 lat long.
                                                         
            output_raster.SetProjection( srs.ExportToWkt() )   # Exports the coordinate system to the file
            output_raster.GetRasterBand(1).WriteArray(array)   # Writes array to the raster
            
            output_raster.FlushCache()
        except:
            pass
            
    
    
