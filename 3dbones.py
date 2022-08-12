#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Aug 12 13:32:31 2022

@author: bradleyrauscher
"""

import pandas as pd
import os
import numpy as np
from matplotlib import pyplot as plt

def calclength(point1,point2):
    length = np.sqrt((point1[0]-point2[0])**2+(point1[1]-point2[1])**2+(point1[2]-point2[2])**2)
    return length

totdatafiles = os.listdir()
datafiles = []

for i in totdatafiles:
    if i[-4:] == '.csv':
        datafiles.append(i)

lengths = []

data = pd.read_csv(datafiles[0])

for i in range(len(data)):
    point1 = [data['x1'][i],data['y1'][i],data['z1'][i]]
    point2 = [data['x2'][i],data['y2'][i],data['z2'][i]]
    lengths.append(calclength(point1,point2))

plt.plot(range(len(lengths)),lengths)
plt.show()
