#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 22:54:15 2019
From
@author: fernandr
"""

import numpy as np

#download mnist data and split into train and test sets
#tab_X=np.load('/home/fernandr/Bureau/Test/Test_NN/python_data/export/tab_X.npy')
#tab_Y=np.load('/home/fernandr/Bureau/Test/Test_NN/python_data/export/tab_Y.npy')
tab_X=np.load('/mnt/DD_COMMON/Data_VITIMAGE/Temp/tab_X.npy')
tab_Y=np.load('/mnt/DD_COMMON/Data_VITIMAGE/Temp/tab_Y.npy')

dim=32
nb_elems=(tab_X.shape)[0]
nb_train=int(((tab_Y.shape)[0]*8)/10)
nb_test=nb_elems-nb_train

print ('tab_X shape=')
print(tab_X.shape)
print ('tab_Y shape=')
print(tab_Y.shape)
print('Nb elements to train ')
print(nb_train)
print('Nb elements to test ')
print(nb_test)
X_train=tab_X[0:nb_train,:,:,:]
X_train=X_train.reshape(nb_train,dim,dim,dim,1)
X_test=tab_X[nb_train:tab_Y.shape[0],:,:,:].reshape(nb_test,dim,dim,dim,1)
Y_train=tab_Y[0:nb_train,:]
Y_test=tab_Y[nb_train:tab_Y.shape[0],:]
print ('X_train shape=')
print(X_train.shape)
print ('Y_train shape=')
print(Y_train.shape)
print ('X_test shape=')
print(X_test.shape)
print ('Y_test shape=')
print(Y_test.shape)

#create model
from keras.models import Sequential
from keras.layers import Dense, Conv2D, Conv3D, Flatten,MaxPooling3D
model = Sequential()

#add model layers
model.add(Conv3D(20, kernel_size=3, activation='relu',padding='same'))
model.add(MaxPooling3D(pool_size=(2,2,2)))
#output=32 x 16 x 16 x 16

model.add(Conv3D(10, kernel_size=3, activation='relu',padding='same'))
model.add(MaxPooling3D(pool_size=(2,2,2)))
#output=32 x 8 x 8 x 8

model.add(Conv3D(5, kernel_size=3, activation='relu',padding='same'))
model.add(MaxPooling3D(pool_size=(2,2,2)))
#output=32 x 4 x 4 x 4

model.add(Conv3D(3, kernel_size=3, activation='relu',padding='same'))
model.add(MaxPooling3D(pool_size=(2,2,2)))
#output=32 x 2 x 2 x 2

model.add(Flatten())
model.add(Dense(2, activation='softmax'))

#compile model using accuracy to measure model performance
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])


#train the model
model.fit(X_train, Y_train, batch_size=32, epochs=3,verbose=1, validation_data=(X_test, Y_test))
score = model.evaluate(X_test, Y_test, verbose=1)

print('Test score:', score[0])
print('Test accuracy:', score[1])


model.summary()
