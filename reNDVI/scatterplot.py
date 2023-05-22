'''
create scatter density plot from csv of eMODIS and sMODIS values
author: Sara Miller
'''

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from scipy.stats import kde
from scipy.interpolate import interpn


df = pd.read_csv(r'C:\Users\smiller\Downloads\pointstoplot.csv')
#drop any empty values
df = df.dropna(how='any') 

y = df['smodis']
x = df['emodis']
'''
# Evaluate a gaussian kde on a regular grid of nbins x nbins over data extents
nbins=300
k = kde.gaussian_kde([x,y])
xi, yi = np.mgrid[x.min():x.max():nbins*1j, y.min():y.max():nbins*1j]
zi = k(np.vstack([xi.flatten(), yi.flatten()]))
 
# Make the plot
plt.pcolormesh(xi, yi, zi.reshape(xi.shape))
plt.show()
 
# Change color palette
plt.pcolormesh(xi, yi, zi.reshape(xi.shape), cmap=plt.cm.inferno)


# Calculate the point density
xy = np.vstack([x,y])
z = gaussian_kde(xy)(xy)

# Sort the points by density, so that the densest points are plotted last
idx = z.argsort()
x, y, z = x[idx], y[idx], z[idx]


fig, ax = plt.subplots()
ax.scatter(x, y, s=50, c=z, edgecolor='none', cmap=plt.cm.viridis)


plt.hist2d(x, y, (100, 100), cmap=plt.cm.inferno)
plt.colorbar()
'''

def density_scatter( x , y, ax = None, sort = True, bins = 20, **kwargs )   :
    """
    Scatter plot colored by 2d histogram
    """
    if ax is None :
        fig , ax = plt.subplots()
    data , x_e, y_e = np.histogram2d( x, y, bins = bins)
    z = interpn( ( 0.5*(x_e[1:] + x_e[:-1]) , 0.5*(y_e[1:]+y_e[:-1]) ) , data , np.vstack([x,y]).T , method = "splinef2d", bounds_error = False )

    # Sort the points by density, so that the densest points are plotted last
    if sort :
        idx = z.argsort()
        x, y, z = x[idx], y[idx], z[idx]

    
    sc = plt.scatter( x, y, c=z, s=40, edgecolor='none', cmap=plt.cm.inferno_r, alpha=0.15)
    return sc


if "__main__" == __name__ :
    sc = density_scatter( x, y, bins = [1000,1000] )
    #plot colorbar and set colorbar to no transparency
    cbar = plt.colorbar()
    cbar.solids.set(alpha=1)
    cbar.set_label('Point Density')


#plot 1:1 line
plt.plot([0,1],[0,1], color='black')
 
plt.ylim(top=1, bottom=0)
plt.xlim(right=1, left=0)
plt.xlabel('eMODIS NDVI')
plt.ylabel('reNDVI')


fig = plt.gcf()
fig.set_size_inches(5.51181, 3.5)
plt.rcParams.update({'font.size': 8})

plt.savefig(r'C:\Users\smiller\Documents\paper\paperimages\FIG5a.png', format='png', dpi=1000, frameon=True, bbox_inches='tight')
plt.show()

