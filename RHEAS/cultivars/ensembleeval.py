# -*- coding: utf-8 -*-
"""
Created on Fri Oct 28 12:48:44 2022

author: Sara Miller
script to test how many ensembles are needed to get consistent yield results
need to read all yields from all files randomly with different numbers of ensembles
then print out avg yields per season for each ensemble # maybe 5 times
"""

import pandas as pd
import matplotlib.pyplot as plt
import matplotlib
import numpy as np
import sys

culeval = pd.DataFrame(columns=['county','season','run#','rmse','%rmse','unbiased rmse','bias','correlation'])


df1 = pd.read_csv(r'C:\Users\smille25\Downloads\cultivartests\nowcasts_update_samerun30timesHPMLR.csv')
yielddif = pd.DataFrame()
statsdif = pd.DataFrame()
culeval = pd.DataFrame()
#loop through each # of ensembles per county/season and select x ensembles randomly
for c in df1.cname.unique():
    #for t in range(5):
        avg_yields1 = pd.DataFrame()
        for yr in range(2015,2020):
            df2 = pd.DataFrame()
            yields = pd.DataFrame()
            for ens in range(50, 850, 50):   

                #get specific county and year
                df = df1.loc[(df1['cname']==c)&(df1['Year']==yr)]


                #select n random ensembles from all data
                df = df['gwad'].sample(n=50, replace = True)
                if (ens>50):
                    df = pd.concat([df,df2],ignore_index=True)

                df2 = df
                df = df.rename(ens)
                #sys.exit()
                df['ens'] = ens
                df = df.reset_index(drop=True)
                #get mean/min/max/med yields
                #avg_yield = df['gwad'].mean()
                #min_yield = df['gwad'].min()
                #max_yield = df['gwad'].max()
                #med_yield = df['gwad'].median()
                #yields = yields.append({'County':c,'Year':yr, 'run#':t,'avg_yield':avg_yield, 'min_yield':min_yield,'max_yield':max_yield, 'med_yield':med_yield, 'ens#':ens}, ignore_index=True)
                yields = pd.concat([yields,df],axis=1)
                
            r'''    
            # read csv with FAO yields
            fao = pd.read_csv(r'C:\Users\smille25\Downloads\Kenya_seasonal_yield_MOA.csv')
            fao = fao.set_index(['Season','season1'])
            
            # convert to kg/ha 
            fao = (fao * 1000)
            fao = fao.reset_index()
            fao['Year'] = fao['Year'] / 1000
            fao = fao.set_index('Year')
            #fao['COUNTY'] = fao['COUNTY'].str.lower()
        
        
            #df = df75
            # get seasonal yields for selected cultivar
            df = yields.loc[((yields['County']==c)&(yields['run#']==t))&(yields['ens#']==ens)]
            df = df.set_index(['County','Year'])
            # remove unnamed column, ensemble column, and gid column
            df = df.loc[:, ~df.columns.str.contains('^Unnamed')]
            df = df['avg_yield']
        
            df = df.unstack(level=0)


            fao1 = fao[c].loc[fao['season1']=='LR']
            
            #use 2002-09 for calibration
            #use 2015 onward for validation
            stddev = fao1.std()
            #print(fao1,df2)
            #sys.exit()

            fao2 = fao1.iloc[-5:]
            df3 = df.iloc[-5:]
            df3 = df3[c]
            stddev = fao1.std()


            if (df3.shape[0] >= fao2.shape[0]):
                #print(df3,fao2)
                #   calculate correlation and RMSE for that cultivar with the FAO data
                corr = df3.corr(fao2)
                rmse = np.sqrt(((df3-fao2)**2).mean())
                perrmse = np.sqrt(((df3-fao2)**2).mean())/(fao2.mean())*100
                ubrmse = np.sqrt((((df3-df3.mean())-(fao2-fao2.mean()))**2).mean())
                bias = (df3-fao2).mean()
                
                culeval = culeval.append({'County':c,'season':'LR','run#':t, 'rmse':rmse, '%rmse':perrmse,'unbiased rmse':ubrmse, 'bias':bias, 'correlation':corr, 'ens#':ens}, ignore_index=True)
            '''
            #plot a line graph of avg yields for each year
            #print(yields)
            #yields = yields.stack()
            #print(yields)
            #sys.exit()
            avg_yields = yields.mean()
            avg_yields  = avg_yields.rename(yr)
            avg_yields1 = pd.concat([avg_yields1,avg_yields], axis=1)
        fig,ax = plt.subplots()
        avg_yields1.plot(ax=ax)
        plt.title('{0}'.format(c))
        plt.xlabel('Number of Ensembles')
        plt.ylabel('Yield')
        #sys.exit()
        #get range in correlation/rmse between the 10 random selections
        #meanrange = yields['avg_yield'].loc[((yields['County']==c)&(yields['Year']==yr))&(yields['ens#']==ens)].max() - yields['avg_yield'].loc[((yields['County']==c)&(yields['Year']==yr))&(yields['ens#']==ens)].min()
        #medrange = yields['med_yield'].loc[((yields['County']==c)&(yields['Year']==yr))&(yields['ens#']==ens)].max() - yields['med_yield'].loc[((yields['County']==c)&(yields['Year']==yr))&(yields['ens#']==ens)].min()
        #corrrange = culeval['correlation'].loc[((culeval['County']==c))&(culeval['ens#']==ens)].max() - culeval['correlation'].loc[((culeval['County']==c))&(culeval['ens#']==ens)].min()
        #rmserange = culeval['rmse'].loc[((culeval['County']==c))&(culeval['ens#']==ens)].max() - culeval['rmse'].loc[((culeval['County']==c))&(culeval['ens#']==ens)].min()            
        #yielddif = yielddif.append({'County':c,'Year':yr, 'meanrange':meanrange, 'medrange':medrange,'ens#':ens}, ignore_index=True)
        #statsdif = statsdif.append({'County':c,'ens#':ens,'correlation range':corrrange,'rmse range':rmserange}, ignore_index=True)
        #sys.exit()
           


#print(culeval)
#culeval.to_csv(r'C:\Users\smille25\Downloads\cultivartests\seasonalcultivareval.csv')
#culeval = culeval.set_index(['County','season'])
#print(culeval)
#culeval.to_csv(r'C:\Users\smille25\Downloads\cultivartests\culeval_ensrange.csv')
#statsdif.to_csv(r'C:\Users\smille25\Downloads\cultivartests\culevalens_differences.csv')
