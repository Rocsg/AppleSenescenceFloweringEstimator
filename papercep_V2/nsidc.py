#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Dec 12 13:16:54 2019

@author: fernandr
"""

import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
import scipy
plt.close('all')

def smooth(y, box_pts):
    box = np.ones(box_pts)/box_pts
    y_smooth = np.convolve(y, box, mode='same')
    return y_smooth


def rsquared(x, y):
    """ Return R^2 where x and y are array-like."""

    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
    return r_value**2

def rnosquared(x, y):
    """ Return R^2 where x and y are array-like."""

    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(x, y)
    return r_value

def r_rat(south,north,begin,end,pts):
    N=np.shape(north)[0]
    ret=np.zeros(N)
    for i in range (end-begin):
        incr=i+begin
        ret[incr]=rnosquared(south[incr-pts//2:incr+pts//2],north[incr-pts//2:incr+pts//2])
        
    return ret
 
#plt.figure()
plt.close('all')
No= smooth(data_north[:,3],ye_sm)
So= smooth(data_south[:,3],ye_sm)
NN=13369
delta=365*10
xmin=delta//2+100
xmax=NN-delta//2-100
print(str(xmin))
print(str(xmax))
y=data_north[xmin:xmax,0]+(1/12)*data_north[xmin:xmax,1]+(1/365)*data_north[xmin:xmax,2]    
print(y[0])
print(y[len(y)-1])
Co=r_rat(No,So,xmin,xmax,delta)    
plt.plot(data_north[xmin:xmax,0]+(1/12)*data_north[xmin:xmax,1]+(1/365)*data_north[xmin:xmax,2],Co[xmin:xmax],label='10-years sliding window correlation coefficient between 365-days-averaged-north sea ice surface and 365-days-averaged-south sea ice surface (Mkm²)')
plt.plot([y[0],y[len(y)-1]],[0,0],'k')
plt.legend()

ye_sm=365
mo_sm=30
data_north=np.loadtxt('/home/fernandr/Bureau/data_north.csv')
data_south=np.loadtxt('/home/fernandr/Bureau/data_south.csv')
#plt.plot(data_north[:,0]+(1/12)*data_north[:,1]+(1/365)*data_north[:,2],smooth(data_north[:,3],mo_sm),label='North sea ice in Mkm² (30-days averaging)',color='r')
#plt.plot(data_south[:,0]+(1/12)*data_south[:,1]+(1/365)*data_south[:,2],smooth(data_south[:,3],mo_sm),label='South sea ice in Mkm² (30-days averaging)',color='b')
#plt.plot(data_north[:,0]+(1/12)*data_north[:,1]+(1/365)*data_north[:,2],smooth(data_south[:,3]+data_north[:,3],30),label='sum',color='g')
#plt.plot(data_north[:,0]+(1/12)*data_north[:,1]+(1/365)*data_north[:,2],smooth(data_south[:,3]+data_north[:,3],730),label='sum',color='k')
plt.plot(data_south[:,0]+(1/12)*data_south[:,1]+(1/365)*data_south[:,2],smooth(data_south[:,3],ye_sm),label='North sea ice in Mkm² (365-days averaging)',color='k')
plt.plot(data_north[:,0]+(1/12)*data_north[:,1]+(1/365)*data_north[:,2],smooth(data_north[:,3],ye_sm),label='South sea ice in Mkm² (365-days averaging)',color='g')
#plt.plot(data_north[:,0]+(1/12)*data_north[:,1]+(1/365)*data_north[:,2],0.5*smooth(data_south[:,3],ye_sm)+0.5*smooth(data_north[:,3],mo_sm),label='Mean between north and south (30-days averaging)',color='m')
plt.plot(data_north[:,0]+(1/12)*data_north[:,1]+(1/365)*data_north[:,2],0.5*smooth(data_south[:,3],ye_sm)+0.5*smooth(data_north[:,3],ye_sm),label='Mean between north and south (365-days averaging)',color='m')
plt.xlim([1979.9,2019.5])
plt.ylim([5,15])
#plt.plot(data_north[3])
#plt.plot(data_south[0]+(1/12)*data_south[1]+(1/365)*data_south[2],data_south[3])
plt.plot([1979,2020],[10,10])
plt.plot([1979,2020],[10,10],'#999999')
plt.plot([1979,2020],[11,11],'#999999')
plt.plot([1979,2020],[12,12],'#999999')
plt.plot([1979,2020],[13,13],'#999999')
plt.legend()


#plt.plot(data_north[:,0]+(1/12)*data_north[:,1]+(1/365)*data_north[:,2],smooth(data_north[:,3],30),label='north',color='r')
#plt.plot(data_south[:,0]+(1/12)*data_south[:,1]+(1/365)*data_south[:,2],smooth(data_south[:,3],30),label='south',color='b')
#plt.plot(data_north[:,0]+(1/12)*data_north[:,1]+(1/365)*data_north[:,2],smooth(data_south[:,3]+data_north[:,3],30),label='sum',color='g')
#plt.plot(data_north[:,0]+(1/12)*data_north[:,1]+(1/365)*data_north[:,2],smooth(data_south[:,3]+data_north[:,3],730),label='sum',color='k')
#plt.plot(data_north[:,0]+(1/12)*data_north[:,1]+(1/365)*data_north[:,2],smooth(data_south[:,3],730),label='sum',color='k')
#plt.plot(data_north[:,0]+(1/12)*data_north[:,1]+(1/365)*data_north[:,2],smooth(data_north[:,3],730),label='sum',color='g')
#plt.plot(data_north[3])
#plt.plot(data_south[0]+(1/12)*data_south[1]+(1/365)*data_south[2],data_south[3])
