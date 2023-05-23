# -*- coding: utf-8 -*-
"""
Created on Wed Aug 18 08:46:05 2021

author: Sara Miller
plot the average skill scores for precipitation forecasts compared to lead time
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r'C:\Users\smille25\Downloads\skillscoreslead.csv')
df = df.set_index('Lead Time')
print(df)

styles = ['-','-','--','--','-.','-.',':',':']
colors = ['orange','blue','orange','blue','orange','blue','orange','blue']

fig, ax = plt.subplots()
for col, style, color in zip(df.columns, styles, colors):
    df[col].plot(style=style, color=color,ax=ax)
#df.plot()
plt.xlabel('Lead Time')
plt.title('Forecast Skill')
plt.legend(loc='upper right')

plt.savefig(r'C:\Users\smille25\Downloads\forecasts\precip\skill\images\graphskill.png',dpi=300)