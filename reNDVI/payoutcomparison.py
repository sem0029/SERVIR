# -*- coding: utf-8 -*-
"""
Created on Tue Apr  7 10:55:15 2020

author: Sara Miller
compare calculated payouts from eMODIS as compared to reNDVI (smodis)
compare payouts over the unit areas of insurance with highest cloud cover
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

smodislrdf = pd.read_csv(r'C:\Users\smille25\Downloads\smodislrdf.csv').set_index('gridcode')
emodislrdf = pd.read_csv(r'C:\Users\smille25\Downloads\emodislrdf.csv').set_index('gridcode')
smodissrdf = pd.read_csv(r'C:\Users\smille25\Downloads\smodissrdf.csv').set_index('gridcode')
emodissrdf = pd.read_csv(r'C:\Users\smille25\Downloads\emodissrdf.csv').set_index('gridcode')
cloud = pd.read_csv(r'C:\Users\smille25\Downloads\cloudcover.csv').set_index('gridcode')

#get top 25% (top 43 uais) with most clouds
uais = cloud.nlargest(32, 'MEAN')

smodislrdf = pd.concat([smodislrdf, cloud], axis=1).nlargest(26, 'MEAN')
smodissrdf = pd.concat([smodissrdf, cloud], axis=1).nlargest(26, 'MEAN')
emodislrdf = pd.concat([emodislrdf, cloud], axis=1).nlargest(26, 'MEAN')
emodissrdf = pd.concat([emodissrdf, cloud], axis=1).nlargest(26, 'MEAN')


#compare payouts

lrcomparison = pd.DataFrame()

for yr in range(2003, 2017):
  lrcomparison['difference'+str(yr)] = np.where(((smodislrdf['payout'+str(yr)]==0)&(emodislrdf['payout'+str(yr)]==0)) | ((smodislrdf['payout'+str(yr)]!=0)&(emodislrdf['payout'+str(yr)]!=0)), 0, 1)
  #when one product triggers a payout and the other doesn't it assigns a 1 to that UAI for the year
  if yr ==2003:
    lrcomparison.index = emodislrdf.index
  lrcomparison['falsepos'+str(yr)] = np.where((lrcomparison['difference'+str(yr)]==1)&(smodislrdf['payout'+str(yr)]>emodislrdf['payout'+str(yr)]), smodislrdf['payout'+str(yr)]-emodislrdf['payout'+str(yr)], 0)
  #gets how far off the payouts are when one product triggered a payout and the other didn't
  lrcomparison['falseneg'+str(yr)] = np.where((lrcomparison['difference'+str(yr)]==1)&(smodislrdf['payout'+str(yr)]<emodislrdf['payout'+str(yr)]), emodislrdf['payout'+str(yr)]-smodislrdf['payout'+str(yr)], 0)

  
#sum number of differences and set index to gridcode
differencecolumns = ['difference2003', 'difference2004', 'difference2005', 'difference2006', 'difference2007', 'difference2008', 'difference2009', 'difference2010', 'difference2011', 'difference2012', 'difference2013', 'difference2014', 'difference2015', 'difference2016']
lrcomparison['totaldifference'] = lrcomparison[differencecolumns].sum(axis = 1)


#sum of false positives and negatives
#false positives are when smodis triggered a payout and emodis did not
#false negatives are when emodis triggered a payout and smodis did not
columnlist2 = ['falsepos2003', 'falsepos2004', 'falsepos2005', 'falsepos2006', 'falsepos2007', 'falsepos2008', 'falsepos2009', 'falsepos2010', 'falsepos2011', 'falsepos2012', 'falsepos2013', 'falsepos2014', 'falsepos2015', 'falsepos2016']
columnlist3 = ['falseneg2003', 'falseneg2004', 'falseneg2005', 'falseneg2006', 'falseneg2007', 'falseneg2008', 'falseneg2009', 'falseneg2010', 'falseneg2011', 'falseneg2012', 'falseneg2013', 'falseneg2014', 'falseneg2015', 'falseneg2016']
lrcomparison['sumfalsepos'] = lrcomparison[columnlist2].sum(axis=1) #sum only the positive values
lrcomparison['sumfalseneg'] = lrcomparison[columnlist3].sum(axis=1) #sum only negatives

#plot total differences, sum of false positives, and sum of false negatives
#lrcomparison['geometry'] = map(lambda s: shape(s), emodislrdf.geometry)
#lrcomparison.plot(column='totaldifference', cmap='OrRd', legend=True, edgecolor='#a9a9a9').set_title('Long Rains Total Differences')
#lrcomparison.plot(column='sumfalsepos', cmap='Blues', legend=True, edgecolor='#a9a9a9').set_title('Long Rains Sum of False Positives')
#lrcomparison.plot(column='sumfalseneg', cmap='Reds', legend=True, edgecolor='#a9a9a9').set_title('Long Rains Sum of False Negatives')



#do the same for short rains
srcomparison = pd.DataFrame()

for yr in range(2003, 2017):
  srcomparison['difference'+str(yr)] = np.where(((smodissrdf['payout'+str(yr)]==0)&(emodissrdf['payout'+str(yr)]==0)) | ((smodissrdf['payout'+str(yr)]!=0)&(emodissrdf['payout'+str(yr)]!=0)), 0, 1)
  if yr ==2003:
    srcomparison.index = emodissrdf.index
  srcomparison['falsepos'+str(yr)] = np.where((srcomparison['difference'+str(yr)]==1)&(smodissrdf['payout'+str(yr)]>emodissrdf['payout'+str(yr)]), smodissrdf['payout'+str(yr)]-emodissrdf['payout'+str(yr)], 0)
  #gets how far off the payouts are when one product triggered a payout and the other didn't
  srcomparison['falseneg'+str(yr)] = np.where((srcomparison['difference'+str(yr)]==1)&(smodissrdf['payout'+str(yr)]<emodissrdf['payout'+str(yr)]), emodissrdf['payout'+str(yr)]-smodissrdf['payout'+str(yr)], 0)

srcomparison['totaldifference'] = srcomparison[differencecolumns].sum(axis = 1)
#srcomparison['geometry'] = map(lambda s: shape(s), emodissrdf.geometry)
#srcomparison.plot(column='totaldifference', cmap='OrRd', legend=True, edgecolor='#a9a9a9').set_title('Short Rains Total Differences')

#sum of false positives and negatives
srcomparison['sumfalsepos'] = (srcomparison[columnlist2].sum(axis=1)) #average only the positive values
srcomparison['sumfalseneg'] = (srcomparison[columnlist3].sum(axis=1)) #sum only negatives
#srcomparison.plot(column='sumfalsepos', cmap='Blues', legend=True, edgecolor='#a9a9a9').set_title('Short Rains Sum of False Positives')
#srcomparison.plot(column='sumfalseneg', cmap='Reds', legend=True, edgecolor='#a9a9a9').set_title('Short Rains Sum of False Negatives')


#count number of UAIs with 0, 2, 4, and 6 payouts triggered at different times
countlr = pd.value_counts(lrcomparison['totaldifference'].values, sort=False)
print('Number of UAIs with 0, 2, 4, and 6 payouts triggered at different times for long rains:')
print(countlr/26*100)
countsr = pd.value_counts(srcomparison['totaldifference'].values, sort=False)
print('Number of UAIs with 0, 2, 4, and 6 payouts triggered at different times for short rains:')
print(countsr/26*100)
