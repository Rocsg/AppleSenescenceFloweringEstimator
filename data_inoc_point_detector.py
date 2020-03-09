#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 13:36:42 2019

@author: fernandr
"""
from skimage import io
import numpy as np

# Get general parameters
#tab_parameters=np.load('/mnt/DD_COMMON/Data_VITIMAGE/Train_space_NN/Foutoir_temp/tab_parameters.txt')
specimens=('B001_PAL','B031_NP','B032_NP','B051_CT')
n_specs=4
n_days=5
dim_img=128
dim_crop=64
dim_x_full=dim_img
dim_y_full=dim_img
dim_z_full=dim_img
dim_x=dim_crop
dim_y=dim_crop
dim_z=dim_crop
remove_band=int((dim_img-dim_crop)/2)
augment_factor=100
var_tx=1
var_ty=1
var_tz=12
var_ax=0.02
var_ay=0.02
var_az=2
vars=(var_tx,var_ty,var_tz,var_ax,var_ay,var_az)


tab_X_init=np.zeros((n_specs,n_days,dim_x,dim_y,dim_z),dtype=float)
tab_Y_init=np.zeros((n_specs,n_days,3),dtype=float)
print('Shape of tab_X_init '+str(tab_X_init.shape))
print('Shape of tab_Y_init '+str(tab_Y_init.shape))

#batch_size=32


#Get initial images and initial expected outputs
for ind_spec in range(n_specs):
    print('ind_spec='+str(ind_spec))
    spec=specimens[ind_spec]
    for ind_day in range(n_days):
        print('data preparation '+str(ind_spec)+'/'+str(n_specs-1)+' - '+str(ind_day)+'/'+str(n_days-1))
        print('step1')
        tab_Y_init[ind_spec,ind_day,:]=np.loadtxt('/mnt/DD_COMMON/Data_VITIMAGE/Train_space_NN/Test_data_detect_IP/source/'+spec+'_tab_coordinates.txt')
        print('step2')
        str_data='/mnt/DD_COMMON/Data_VITIMAGE/Train_space_NN/Test_data_detect_IP/source/'+str(spec)+'_D'+str(ind_day+1)+'.tif'
        data = io.imread(str_data)
        print('step3')
        data_sized=resample_to_size_with_vox_reset(data,(dim_x_full,dim_y_full,dim_z_full))
        print('step4')
        data_sized=data_sized[remove_band:dim_img-remove_band,remove_band:dim_img-remove_band,remove_band:dim_img-remove_band]
        print('step5')
        tab_X_init[ind_spec, ind_day, :,:,:]=data_sized[:,:,:]

#With band
tab_Y_init=(tab_Y_init-0.5)*2+0.5
np.save('/mnt/DD_COMMON/Data_VITIMAGE/Train_space_NN/Test_data_detect_IP/export/tab_X_init_IP_'+str(dim_img)+'_'+str(dim_crop)+'.npy', tab_X_init)
np.save('/mnt/DD_COMMON/Data_VITIMAGE/Train_space_NN/Test_data_detect_IP/export/tab_Y_init_IP_'+str(dim_img)+'_'+str(dim_crop)+'.npy', tab_Y_init)

tab_X_init=np.load('/mnt/DD_COMMON/Data_VITIMAGE/Train_space_NN/Test_data_detect_IP/export/tab_X_init_IP_'+str(dim_img)+'_'+str(dim_crop)+'.npy')
tab_Y_init=np.load('/mnt/DD_COMMON/Data_VITIMAGE/Train_space_NN/Test_data_detect_IP/export/tab_Y_init_IP_'+str(dim_img)+'_'+str(dim_crop)+'.npy')

#augment data
tab_X=np.zeros((n_specs*n_days*(1+augment_factor),dim_x,dim_y,dim_z),dtype=float)
tab_Y=np.zeros((n_specs*n_days*(1+augment_factor),3),dtype=float)
tab_rand=generate_random_transform_factors(n_specs,n_days,augment_factor,vars)
print('Shape of tab_X '+str(tab_X.shape))
print('Shape of tab_Y '+str(tab_Y.shape))
print('Shape of tab_rand '+str(tab_rand.shape))
for ind_spec in range(n_specs):
    for ind_day in range(n_days):
        point_init=tab_Y_init[ind_spec,ind_day,:]
        img_init=tab_X_init[ind_spec, ind_day, :,:,:]        
        for aug in range(augment_factor+1):
            print('augmentation '+str(ind_spec+1)+'/'+str(n_specs)+' - '+str(ind_day+1)+'/'+str(n_days)+' - '+str(aug+1)+'/'+str(augment_factor))
            rand_vars=tab_rand[ind_spec,ind_day,aug,:]
            img_aug,point_aug,trans=transform_centered_image_and_point_vect(img_init,point_init,rand_vars,dim_x)
            tab_X[ind_spec*n_days*(augment_factor+1)+ ind_day*(augment_factor+1) +aug,:,:,:]=img_aug[:,:,:]
            tab_Y[ind_spec*n_days*(augment_factor+1)+ ind_day*(augment_factor+1) +aug,:]=point_aug[:]

np.save('/mnt/DD_COMMON/Data_VITIMAGE/Train_space_NN/Test_data_detect_IP/export/tab_X_IP_'+str(dim_img)+'_'+str(dim_crop)+'_'+str(augment_factor)+'.npy', tab_X)
np.save('/mnt/DD_COMMON/Data_VITIMAGE/Train_space_NN/Test_data_detect_IP/export/tab_Y_IP_'+str(dim_img)+'_'+str(dim_crop)+'_'+str(augment_factor)+'.npy', tab_Y)



