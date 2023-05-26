'''
wrapper to go through all forecasts
extract vic variables to tif files
cumulative then average by county
then store as csv, delete tifs
then move to next forecast date
author: Sara Miller
'''

import os
import sys
import time
from datetime import datetime
from datetime import timedelta
import psycopg2
from calendar import monthrange
import glob
import pandas as pd
import csv
import numpy as np
from rasterstats import zonal_stats
import matplotlib.pyplot as plt
import geopandas as gpd
import sys


start_time = time.time()
wrkdir = '/home/Socrates/rheas/RHEAS/'
varlist = ['evap','net_long', 'net_short', 'rootmoist', 'rainf', 'tmax', 'tmin']
varilist = ['evap','net_long', 'net_short', 'rootmoist', 'rainf', 'tmax', 'tmin', 'soil_moist_1','soil_moist_2','soil_moist_3']
outdir = '/home/Socrates/rheas/RHEAS/vicforecast/'

for year in range(2015,2016):
    for month in range(1,13):
        for day in [15,30]: 
    
            #year = 2000+int(date[-2:]) 
            #month = int(date[:2])
            #day = int(date[3:5])        
            date = str(month).zfill(2)+'_'+str(day)+'_'+str(year)[2:]
            date2 = str(month).zfill(2)+'_'+str(15)+'_'+str(year)[2:]
            yr = str(year)
            m = str(month)
            d = str(day)
            print(date)
            
            if((month==12) and (day==30)):
                latestgefs = datetime((year+1),1,10)
            elif(day==30):
                latestgefs = datetime((year),(month+1),10)
            else:
                latestgefs = datetime(year,month,20)
            gefsyr = latestgefs.strftime('%Y')
            gefsm = latestgefs.strftime('%m')
            gefsd = latestgefs.strftime('%d')
            latestgefs1 = str(gefsyr)+'-'+str(gefsm).zfill(2)+'-'+str(gefsd)
            
            # declare variable information 
            db = 'forecast{0}'.format(str(date2))          # database name
            hst = 'localhost'                # host name
            pwd = 'Servir2019!'                     # password
            usr = 'smiller'                    # username
            schema = 'forecast1{0}gefs'.format(date)

            try:
                # setup connection to the database using username and password
                conn = psycopg2.connect("dbname={0} user={1} host={2} password={3}".format(db,usr,hst,pwd))
                conn.autocommit = True
                cur = conn.cursor()
                
                for var in (varlist):
                
                    # sql query to obtain min, max id as well as total row count for table 1 
                    sql = 'SELECT count(*), min(id), max(id) from {0}.{1} where fdate<\'{2}\' '.format(schema,var,latestgefs1)
                    cur.execute(sql)
                    d = cur.fetchall()
                    miny = d[0][1]
                    maxy = d[0][2]
                    count = d[0][0] 
                    # creating tiff of table1
    
                    # loop through min and max id values
                    for k in range(miny,maxy+1):
                        
                        #sql query to get id, date from variable 1
                        sql = "SELECT id, fdate from {0}.{1} where id = {2}".format(schema,var,k)
                        cur.execute(sql)        # executes the sql command
                        g = cur.fetchall()      # captures the result of command into variable g
                        
                        # check to see if sql command resulted in any value - if length of g is > 0 
                        # indicates there are values under variable g else its empty
                        if len(g) > 0:
                            sid = k
                            dt = g[0][1]
                            dt = str(dt)
                            dt = dt.replace("-","")
                            
                            # print value if id, id, date to see if they are consistent  
                            print(sid, g[0][0], dt)
                            
                            # using gdal to translate extracted raster to GTiff 
                            t1 = "gdal_translate -of GTiff"
                            t2 = """ "PG:host='{0}' dbname='{1}' user='{2}' password='{3}' schema='{4}' table='{5}' where='id={6}' mode=1" """.format(hst,db,usr,pwd,schema,var,sid)
                            t3 = "{0}{1}_{2}.tiff".format(outdir,var,dt)
                            os.system(t1+t2+t3)
                    
                # sql query to obtain min, max id as well as total row count for table 1 
                sql = 'SELECT count(*), min(id), max(id) from {0}.soil_moist where fdate<\'{1}\''.format(schema,latestgefs1)
                cur.execute(sql)
                d = cur.fetchall()
                miny = d[0][1]
                maxy = d[0][2]
                count = d[0][0]  
                # Tiffs of soil moisture
                # layers 1,2 and 3
                
                # loop through the range of ids in variable 2 table
                for i in range(miny,maxy+1):
                    # sql query to get layer and fdate from id
                    sql = "SELECT id, layer, fdate from {0}.soil_moist where id = {1}". format(schema,i)
                    cur.execute(sql)
                    h = cur.fetchall()
                    if len(h) > 0:
                        sid = i    
                        lyr = h[0][1]
                        dtt = h[0][2]
                        dtt = str(dtt)
                        dtt = dtt.replace("-","")
                    
                        t1 = "gdal_translate -of GTiff"
                        t2 = """ "PG:host='{0}' dbname='{1}' user='{2}' password='{3}' schema='{4}' table='soil_moist' where='id={5}' mode=1" """.format(hst,db,usr,pwd,schema,sid)
                        t3 = "{0}soil_moist_{1}_{2}.tiff".format(outdir,lyr,dtt)
                        os.system(t1+t2+t3)   
                


                cur.close()
                for vari in varilist:
                    # Access randomized rasters
                    flist = glob.glob('/home/Socrates/rheas/RHEAS/vicforecast/{0}*.tiff'.format(vari)) #change to schema name, table1 name /* .tif (or .tiff)
                    flist = np.sort(flist)
                    #print(flist)
                    
                    counties = gpd.read_file('data_original/Ken/Kenya_County_Clip.shp')
                    c = counties['COUNTY']
                    print(c)
                    
                    # set up dataframe 
                    df = pd.DataFrame()
                    # Find mean of each raster
                    for r in flist:
                        result = zonal_stats('data_original/Ken/Kenya_County_Clip.shp', r, stats='mean', all_touched=True)
                        datedf = datetime.strptime(r[-13:-5], '%Y%m%d')
                        print(date)
                        # Store results in pandas dataframe
                        data = {'Meanresult': result}
                        df1 = pd.DataFrame(data)
                        # convert result of zonal stats to a string
                        df1['Meanresultstr'] = df1['Meanresult'].apply(str)
                        # extract only the number from the results of zonal stats mean
                        df1['Mean'] = df1['Meanresultstr'].str.extract('([-+]?\d*\.*\d+)').astype(float)
                        df1 = df1.drop(['Meanresult','Meanresultstr'], axis=1).transpose()
                        # set column 
                        df1.columns = c
                        df1['Date'] = datedf
                        # append mean from each day to one dataframe
                        df = df.append(df1)
                        print(df)
                        #sys.exit()
                    
                    # set dataframe index as date    
                    df = df.set_index('Date')
                    #print(df)
                    
                    # save dataframe as csv
                    df.to_csv('/home/Socrates/rheas/RHEAS/vicforecastcsv/{0}_{1}.csv'.format(vari,date)) # change path to wherever you want it saved
                os.system('rm -r vicforecast/*.tiff')

            except:
                print('Could not extract for date {0}. Continuing.'.format(date))
                pass

            
print("--- %s hrs ---" %str((time.time() - start_time)/3600.0))