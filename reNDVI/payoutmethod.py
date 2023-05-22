# -*- coding: utf-8 -*-
"""
Created on Fri Nov  1 08:25:14 2019

author: Sara Miller
create figure showing index insurance payout method:
    ndvi percentiles, payout trigger, and payout percentages
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

plt.rcParams.update({'font.size': 8})
fig, ax = plt.subplots(figsize=(5,3))

plt.vlines(x=0.01, ymin=0, ymax=100, linestyles='dotted', color='red', label='Exit')
plt.vlines(x=0.2, ymin=0, ymax=100, linestyles='dashed', color='red', label='Trigger')
plt.hlines(y=5, xmin=0.19, xmax=0.2)
plt.plot([0.01, 0.19], [100, 5], color='black', label='Payout Percent')
plt.plot([0.2, 1], [0, 0], color='black')
plt.xlabel('NDVI Percentile')
plt.ylabel('Payout Percent')
plt.legend(loc='upper right')
plt.tight_layout()
plt.savefig(r'C:\Users\smille25\Downloads\paperimages\FIG3optionhi.png', format='png', dpi=1000, frameon=True, bbox_inches='tight')
plt.show()