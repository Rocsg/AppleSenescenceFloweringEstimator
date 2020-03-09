#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Jun 30 23:42:25 2019

@author: fernandr
"""
from keras.models import Sequential
from keras.layers import Dense, Conv3D,Conv2D,Dropout,Flatten,MaxPooling3D,AveragePooling3D,BatchNormalization
import matplotlib.pyplot as plt
from keras import backend as K
from skimage import io
import numpy as np

def custom_loss():
    def loss(y_true,y_pred):
        return K.mean(K.sum(K.square(y_pred-y_true),axis=1),axis=0)
    return loss


#declaration donnees
dims=(64,64,64)
specimens=('B001_PAL','B031_NP','B032_NP','B041_DS','B042_DS','B051_CT')
days=('J0','J35','J70','J133','J218')
n_specs=6
n_days=5
n_rig=3
n_lig=3
n_den=3
n_sim=3
n_noi=3
rep_aug='/mnt/DD_COMMON/Data_VITIMAGE/Train_space_NN/Full_Exp/data_3_augmented/'
rep_source='/mnt/DD_COMMON/Data_VITIMAGE/Train_space_NN/Full_Exp/data_2_to_nn_geometry/'
rep_save='/mnt/DD_COMMON/Data_VITIMAGE/Train_space_NN/Full_Exp/data_4_results/'

# Collecter toutes les donnees depuis le .tif vers un vecteur source et un vecteur aug
X_source=np.zeros(( n_specs, n_days, dims[0],dims[1],dims[2]),dtype=float)
Y_source=np.zeros(( n_specs, n_days, 3),dtype=float)

X_aug=np.zeros(( n_specs, n_days, n_rig,n_lig,n_den,n_sim,n_noi,dims[0],dims[1],dims[2]),dtype=float)
Y_aug=np.zeros(( n_specs, n_days, n_rig,n_lig,n_den,n_sim,n_noi,3),dtype=float)


print('X_source, taille='+str(X_source.shape))
print('Y_source, taille='+str(Y_source.shape))
print('X_aug, taille='+str(X_aug.shape))
print('Y_aug, taille='+str(Y_aug.shape))

for ind_spec in range(n_specs):
    spec=specimens[ind_spec]
    for ind_day in range(n_days):
        day=days[ind_day]
        print('\nNew source = '+str(ind_spec+1)+'/'+str(n_specs)+' - '+str(ind_day+1)+'/'+str(n_days))
        Y_source[ind_spec,ind_day,:]=np.loadtxt(rep_source+'coordinates_normalized_'+spec+'_'+day+'_res1.txt')
        X_source[ind_spec,ind_day] = io.imread(rep_source+spec+'_'+day+'_res1.tif')
        for ind_rig in range(n_rig):
            for ind_lig in range(n_lig):
                for ind_den in range(n_den):
                    for ind_sim in range(n_sim):
                        for ind_noi in range(n_noi):
                            print('--'+str(ind_rig)+str(ind_lig)+str(ind_den)+str(ind_sim)+str(ind_noi))
                            suffix=spec+'_'+day+'_res1_aug__Rig'+str(ind_rig)+'_Lig'+str(ind_lig)+'_Den'+str(ind_den)+'_Sim'+str(ind_sim)+'_Noi'+str(ind_noi)
                            Y_aug[ind_spec,ind_day,ind_rig,ind_lig,ind_den,ind_sim,ind_noi:]=np.loadtxt(rep_aug+'coordinates_normalized_'+suffix+'.txt')
                            X_aug[ind_spec,ind_day,ind_rig,ind_lig,ind_den,ind_sim,ind_noi] = io.imread(rep_aug+suffix+'.tif')
        

np.save(rep_save+'X_source.npy', X_source)
np.save(rep_save+'Y_source.npy', Y_source)
np.save(rep_save+'X_aug_3.npy', X_aug)
np.save(rep_save+'Y_aug_3.npy', Y_aug)




#Charger tous les exemples
X_source=np.load(rep_save+'X_source.npy')
Y_source=np.load(rep_save+'Y_source.npy')
X_aug=np.load(rep_save+'X_aug_3.npy')
Y_aug=np.load(rep_save+'Y_aug_3.npy')
Y_source=Y_source-0.5
Y_aug=Y_aug-0.5
print('X_source, taille='+str(X_source.shape))
print('Y_source, taille='+str(Y_source.shape))
print('X_aug, taille='+str(X_aug.shape))
print('Y_aug, taille='+str(Y_aug.shape))
#
# Construire les sous-vecteurs train
spec_test=1
X_train,Y_train=get_training(X_aug,Y_aug,spec_test)
X_test,Y_test=get_test(X_source,Y_source,spec_test)




# Lancer un reseau de neurones sur le sujet
m_train=X_train.shape[0]
m_test=X_test.shape[0]
X_train=X_train.reshape(m_train,dims[0],dims[1],dims[2],1)
X_test=X_test.reshape(m_test,dims[0],dims[1],dims[2],1)
print('Shape of X_train '+str(X_train.shape))
print('Shape of Y_train '+str(Y_train.shape))
print('Shape of X_test '+str(X_test.shape))
print('Shape of Y_test '+str(Y_test.shape))
for i in range(X_train.shape[0]):
    X_train[i]=X_train[i]-(np.mean(X_train[i]))
    X_train[i]=X_train[i]/(2*(np.std(X_train[i])))
    X_train[i]=X_train[i]
for i in range(X_test.shape[0]):
    X_test[i]=X_test[i]-(np.mean(X_test[i]))
    X_test[i]=X_test[i]/(2*(np.std(X_test[i])))
    X_test[i]=X_test[i]


#create model and add model layers
padding='same'
activation='relu'
optimizer='nadam'
batch_size=32
dropout_rate=0
model = Sequential()
model.add(Conv3D(8, kernel_size=3, activation=activation,padding=padding))
model.add(Conv3D(8, kernel_size=3, activation=activation,padding=padding))
model.add(MaxPooling3D(pool_size=(2,2,2)))
#output=16 x 32 x 32 x 32  or 30

#model.add(Conv3D(8, kernel_size=3, activation='relu',padding='same'))
model.add(Dropout(rate=dropout_rate))
model.add(Conv3D(16, kernel_size=3, activation=activation,padding=padding))
model.add(Conv3D(16, kernel_size=3, activation=activation,padding=padding))
model.add(MaxPooling3D(pool_size=(2,2,2)))
#output=16 x 16 x 16 x 16   or 13

model.add(Conv3D(32, kernel_size=3, activation=activation,padding=padding))
model.add(Conv3D(32, kernel_size=3, activation=activation,padding=padding))
model.add(MaxPooling3D(pool_size=(2,2,2)))
#output=32 x 8 x 8 x 8   4


model.add(Flatten())
model.add(Dropout(rate=dropout_rate))
model.add(Dense(3, activation='linear'))
model.compile(optimizer=optimizer,batch_size=batch_size, loss=custom_loss(), metrics=['mse'])
history=model.fit(X_train, Y_train, batch_size=batch_size, epochs=20,verbose=1, validation_data=(X_test, Y_test))
Y_hat_train=model.predict(X_train)
Y_hat_test=model.predict(X_test)
X_train_resh=X_train.reshape(m_train,dims[0],dims[1],dims[2])
X_test_resh=X_test.reshape(m_test,dims[0],dims[1],dims[2])





Y_test_both=np.zeros((5,3,4))
Y_test_both[:,:,0]=Y_hat_test
Y_test_both[:,:,1]=Y_hat_test2
Y_test_both[:,:,2]=Y_hat_test3
Y_test_both[:,:,3]=Y_hat_test4
Y_hat_test_both=np.mean(Y_test_both,axis=2)
rms_measure_threshold_detector(Y_test,Y_hat_test,1)
rms_measure_threshold_detector(Y_test,Y_hat_test2,1)
rms_measure_threshold_detector(Y_test,Y_hat_test3,1)
rms_measure_threshold_detector(Y_test,Y_hat_test4,1)
rms_measure_threshold_detector(Y_test,Y_hat_test_both,1)




# summarize history for loss
plt.plot(np.log10(history.history['loss']))
plt.plot(np.log10(history.history['val_loss']))
plt.plot((0,15),(-3,-3))
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

plot_hat(Y_train,Y_hat_train,Y_test,Y_hat_test)





index=4; Slicer_3d(add_cube_norm(add_cube_norm(X_test_resh[index],Y_test[index]+0.5,8,3),Y_hat_test[index]+0.5,5,2))
    

# Sauvegarder le modele


# Sauvegarder les predictions et les attendus


# Afficherr les résultats