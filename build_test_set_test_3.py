#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 10:10:37 2019

@author: fernandr
"""
#repSource='/home/fernandr/Bureau/Test/Test_NN/python_data/source'
#repExport='/home/fernandr/Bureau/Test/Test_NN/python_data/export'
#import tempfile
#import os
# Create a temporary directory
#d = tempfile.mkdtemp()
#import nibabel
#irm = nibabel.load(os.path.join(repSource, 'IRM.hdr'))
#irm_arr = irm.get_data()

    
import matplotlib.pyplot as plt
from skimage import io
import numpy as np
irm_data = io.imread('/home/fernandr/Bureau/Test/Test_NN/python_data/source/IRM_small.tif')
plt.imshow(irm_data[10])

rx_data = io.imread('/home/fernandr/Bureau/Test/Test_NN/python_data/source/RX_small.tif')
plt.imshow(rx_data[10])

dimX=40
dimY=40
dimZ=40
transFact=8
dimMaxTrans=dimX-transFact
n_trans=50

vect_trans_double=np.random.rand(n_trans,3)*5
vect_trans_int=vect_trans_double.astype(int)
print(vect_trans_int.shape)

tab_X=np.zeros((n_trans*2,dimMaxTrans,dimMaxTrans,dimMaxTrans),dtype=int)
print(tab_X.shape)
tab_Y=np.zeros((n_trans*2,2),dtype=int)
print(tab_Y.shape)

for i in range(0,n_trans):
    print (i) 
   #Copier l image RX translatee
    tab_X[i*2 , :, :,:]=irm_data[vect_trans_int[i][0]:vect_trans_int[i][0]+dimMaxTrans  , vect_trans_int[i][1]:vect_trans_int[i][1]+dimMaxTrans , vect_trans_int[i][2]:vect_trans_int[i][2]+dimMaxTrans]
    tab_X[i*2+1 , :, :,:]=rx_data[vect_trans_int[i][0]:vect_trans_int[i][0]+dimMaxTrans  , vect_trans_int[i][1]:vect_trans_int[i][1]+dimMaxTrans , vect_trans_int[i][2]:vect_trans_int[i][2]+dimMaxTrans]
    tab_Y[i*2,0]=1
    tab_Y[i*2+1,0]=1


np.save('/mnt/DD_COMMON/Data_VITIMAGE/Train_space_NN/tab_X.npy', tab_X)
np.savetxt('/mnt/DD_COMMON/Data_VITIMAGE/Train_space_NN/tab_Y.txt', tab_Y)
#np.save('/home/fernandr/Bureau/Test/Test_NN/python_data/export/tab_X.npy', tab_X)
#np.save('/home/fernandr/Bureau/Test/Test_NN/python_data/export/tab_Y.npy', tab_Y)
print('IRM=')
plt.imshow(tab_X[0,10])
print('tab_Y')
print(tab_Y)