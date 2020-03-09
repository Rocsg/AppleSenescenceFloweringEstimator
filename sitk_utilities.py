#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 19:29:38 2019

@author: fernandr
"""
import matplotlib.pyplot as plt
import SimpleITK as sitk
import numpy as np


def get_training(X_aug,Y_aug,spec_test):
    size_X=X_aug.shape
    size_Y=Y_aug.shape
    print('Taille initiale X='+str(size_X))
    print('Taille initiale Y='+str(size_Y))
    m_total=(size_Y[0]-1)*size_Y[1]*size_Y[2]*size_Y[3]*size_Y[4]*size_Y[5]*size_Y[6]
    X_out=np.zeros((size_X[0]-1,size_X[1],size_X[2],size_X[3],size_X[4],size_X[5],size_X[6],size_X[7],size_X[8],size_X[9]))
    Y_out=np.zeros((size_X[0]-1,size_X[1],size_X[2],size_X[3],size_X[4],size_X[5],size_X[6],size_Y[7]))
    print('Train : Selection de : '+str(X_out.shape))
    print('m_total='+str(m_total))
    iter=0
    for sp in range (Y_aug.shape[0]):
        print('copie spec '+str(sp))
        if(sp==spec_test):
            print('Training : ommission de l element numero '+str(sp))
        else :
            print('Training : ajout de l element numero '+str(sp))
            X_out[iter]=X_aug[sp]
            Y_out[iter]=Y_aug[sp]
            iter=iter+1
    X_out=X_out.reshape(m_total,64,64,64)
    Y_out=Y_out.reshape(m_total,3)
    rand_index=np.arange(m_total)
    np.random.shuffle(rand_index)
    X_ret=X_out[rand_index]
    Y_ret=Y_out[rand_index]
    return X_ret,Y_ret


def get_test(X_source,Y_source,spec_test):
    size_X=X_source.shape
    size_Y=Y_source.shape
    m_total=1*size_Y[1]
    X_out=X_source[spec_test]
    Y_out=Y_source[spec_test]
    print('Test : Selection de : '+str(X_out.shape))
    print('m_total='+str(m_total))
    X_out=X_out.reshape(m_total,64,64,64)
    Y_out=Y_out.reshape(m_total,3)
    return X_out,Y_out



def ordered_shape(image):
    shap=(image.shape[1],image.shape[2],image.shape[0])
    return shap

def set_in_bounds(coordinates,image):
    coord2=np.copy(coordinates)
    shap=ordered_shape(image)
    for i in range(3):
        if coord2[i]<0:
            coord2[i]=0
        if coord2[i]>=shap[i]-0.5:
            coord2[i]=shap[i]-1
    return coord2


def add_cube_norm(image,point,size,value):
    shap=ordered_shape(image)
    pointBis=to_voxel_coordinates(point,image)
    return add_cube(image,pointBis,size,value)


def add_cube(image,point,size,value):
    img2=np.copy(image) 
    pointBis=np.copy(point)
    point_0=pointBis-size*np.ones(3)
    point_1=pointBis+(size+1)*np.ones(3)
    
    pointBis=set_in_bounds(pointBis,image)
    point_0=set_in_bounds(point_0,image)
    point_1=set_in_bounds(point_1,image)
 
    point_0=(np.round(point_0)).astype(int)
    point_1=(np.round(point_1)).astype(int)
    pointBis=(np.round(pointBis)).astype(int)
      
    #center
    img2[pointBis[2],pointBis[1],pointBis[0]]=value

    #axis ZY
    img2[point_0[2]:point_1[2],point_0[1]:point_1[1],point_0[0]]=value
    img2[point_0[2]:point_1[2],point_0[1]:point_1[1],point_1[0]-1]=value

    #axis XY
    img2[point_0[2],point_0[1]:point_1[1],point_0[0]:point_1[0]]=value
    img2[point_1[2],point_0[1]:point_1[1],point_0[0]:point_1[0]-1]=value

    #axis XZ
    img2[point_0[2]:point_1[2],point_0[1],point_0[0]:point_1[0]]=value
    img2[point_0[2]:point_1[2],point_1[1],point_0[0]:point_1[0]-1]=value
    return img2

def add_cross_norm(image,point,size,value):
    shap=ordered_shape(img2)
    pointBis=to_voxel_coordinates(point,image)
    return add_cross(image,pointBis,size,value)


def add_cross(image,point,size,value):
    img2=np.copy(image) 
    pointBis=np.copy(point)
    point_0=pointBis-size*np.ones(3)
    point_1=pointBis+(size+1)*np.ones(3)
    
    pointBis=set_in_bounds(pointBis,image)
    point_0=set_in_bounds(point_0,image)
    point_1=set_in_bounds(point_1,image)
 
    #axis Z, fixed X and Y
    point_0=(np.round(point_0)).astype(int)
    point_1=(np.round(point_1)).astype(int)
    pointBis=(np.round(pointBis)).astype(int)
      
    #axis ZY, fixed X
    img2[point_0[2]:point_1[2],point_0[1]:point_1[1],pointBis[0]]=value

    #axis XY, fixed Z
    img2[pointBis[2],point_0[1]:point_1[1],point_0[0]:point_1[0]]=value

    #axis XZ, fixed Y
    img2[point_0[2]:point_1[2],pointBis[1],point_0[0]:point_1[0]]=value
    return img2

def plot_two_images(img1,img2,slice):
    f, axarr = plt.subplots(1,2)
    axarr[0].imshow(img1[slice])
    axarr[1].imshow(img2[slice])
    
def plot_three_images(img1,img2,img3,slice):
    f, axarr = plt.subplots(1,3)
    axarr[0].imshow(img1[slice])
    axarr[1].imshow(img2[slice])
    axarr[2].imshow(img3[slice])

def plot_four_images(img1,img2,img3,img4,slice):
    f, axarr = plt.subplots(2,2)
    axarr[0,0].imshow(img1[slice])
    axarr[0,1].imshow(img2[slice])
    axarr[1,0].imshow(img3[slice])
    axarr[1,1].imshow(img4[slice])


def create_transform(tx,ty,tz,ax,ay,az,cx,cy,cz):
    basic_transform = sitk.Euler3DTransform()
    basic_transform.SetTranslation((tx,ty,tz))
    basic_transform.SetCenter((cx,cy,cz))
    basic_transform.SetRotation(ax,ay,az)
#    basic_transform.SetScale(k)
    return basic_transform

def transform_centered_image(im,tx,ty,tz,ax,ay,az):
    image=sitk.GetImageFromArray(im)
    cx=image.GetWidth()*image.GetSpacing()[0]/2
    cy=image.GetHeight()*image.GetSpacing()[1]/2
    cz=image.GetDepth()*image.GetSpacing()[2]/2
    trans=create_transform(tx,ty,tz,ax,ay,az,cx,cy,cz)
    img=resample(image,trans)
    img=sitk.GetArrayFromImage(img)
    return img,trans

def resample(image, transform):
    reference_image = image
    interpolator = sitk.sitkCosineWindowedSinc
    default_value = 0
    return sitk.Resample(image, reference_image, transform,
                         interpolator, default_value)


def resample_to_size_with_vox_reset(image,dims_fin):
    img=sitk.GetImageFromArray(image)
    print('st1')
    reference_image = sitk.Image(dims_fin, img.GetPixelIDValue())
    reference_image.SetOrigin(img.GetOrigin())
    reference_image.SetDirection(img.GetDirection())
    reference_image.SetSpacing([sz*spc/nsz for nsz,sz,spc in zip(dims_fin, img.GetSize(), img.GetSpacing())])
    interpolator = sitk.sitkCosineWindowedSinc
    print('st2')
    basic_transform = sitk.Transform(3, sitk.sitkIdentity)
    # Resample without any smoothing.
    img=sitk.Resample(img, reference_image,basic_transform,interpolator)
    print('st3')
    image=sitk.GetArrayFromImage(img)
    print('st4')
    return image    

def print_point(point):
    print('Point' + str(point))

def transform_point(transform, point):
    transformed_point = transform.GetInverse().TransformPoint(point)
    return transformed_point

def transform_centered_image_and_point_vect(img,p1,rand_vars,dim_img):
    img,p2,trans=transform_centered_image_and_point(img,p1,rand_vars[0],rand_vars[1],rand_vars[2],rand_vars[3],rand_vars[4],rand_vars[5],dim_img)
    return img,p2,trans

def to_voxel_coordinates(point,image):
    p1=np.copy(point)
    shap=ordered_shape(image)
    for i in range(3):
        p1[i]=p1[i]*shap[i]
    return p1

def to_normalized_coordinates(point,image):
    p1=np.copy(point)
    shap=ordered_shape(image)
    for i in range(3):
        p1[i]=p1[i]/shap[i]
    return p1
    
def transform_centered_image_and_point(img,p1,tx,ty,tz,ax,ay,az,dim_img):
    img,trans=transform_centered_image(img,tx,ty,tz,ax,ay,az)
    p2=transform_point(trans,to_voxel_coordinates(p1,img))
    p2=to_normalized_coordinates(p2,img)
    return img,p2,trans

def rms_measure(y_exp,y_pred):
    y=y_pred-y_exp
    y=np.multiply(y,y)
    y=np.sum(y,axis=1)
    y=np.sqrt(y)
    return y


def angle(x,y):
    return 0

def plot_hat(y_true_tr,y_pred_tr,y_true_tes,y_pred_tes):
    dists_train=rms_measure(y_true_tr,y_pred_tr)
    dists_test=rms_measure(y_true_tes,y_pred_tes)
    plt.subplot(2,1,1)
    plt.hist(dists_train,  bins=30)
    plt.ylabel('RMS distance Train');
    plt.subplot(2,1,2)
    plt.hist(dists_test,  bins=30)
    plt.ylabel('RMS distance Test');


def rms_measure_threshold_detector(y_exp,y_pred,thresh=10):
    y=y_pred-y_exp
    y=np.multiply(y,y)
    mec=np.mean(y)
    y=np.sum(y,axis=1)
    mep=np.mean(y)
    y=np.sqrt(y)
    me=np.mean(y)
  #  print('mean square indiv coord='+str(mec))
    print('mean square='+str(mep))
  #  print('mean dist='+str(me))
    for i in range(y.shape[0]):
        if y[i]>thresh:
            print('Indice '+str(i)+', valeur ='+str(y[i]))
    return mep

def generate_random_transform_factors(n_specs,n_days,augment_factor,vars):
    tab_vars=np.zeros((n_specs,n_days,1+augment_factor,6),dtype=float)
    for ind_spec in range(n_specs):
        for ind_day in range(n_days):
            tab_vars[ind_spec,ind_day,0]=np.zeros(6)
            for aug in range(augment_factor):
                vect_rand=np.random.rand(6)-0.5
                tab_vars[ind_spec,ind_day,aug+1]=np.multiply(vect_rand,vars)
    return tab_vars

# Check setup
#    index=50; Slicer_3d(add_cube_norm(tab_X_tmp[index],tab_Y_tmp[index],5,2))

# Check detection train set
#    index=50; Slicer_3d(add_cube_norm(add_cube_norm(X_train[index],Y_train[index],5,3)),Y_hat_train[index],3,2)
    
# Check detection test set
#    index=50; Slicer_3d(add_cube_norm(add_cube_norm(X_test[index],Y_test[index],5,3)),Y_hat_test[index],3,2)
    
    
    