#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jun 26 13:36:25 2019

@author: fernandr
"""
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Conv3D, Dropout,Flatten,MaxPooling3D,AveragePooling3D,BatchNormalization
import matplotlib.pyplot as plt
from keras import backend as K
def custom_loss():
    def loss(y_true,y_pred):
        return K.mean(K.sum(K.square(y_pred-y_true),axis=1),axis=0)
    return loss
dim_img=128
dim_crop=64
augment_factor=100
tab_X_tmp=np.load('/mnt/DD_COMMON/Data_VITIMAGE/Train_space_NN/Test_data_detect_IP/export/tab_X_IP_'+str(dim_img)+'_'+str(dim_crop)+'_'+str(augment_factor)+'.npy')
tab_Y_tmp=np.load('/mnt/DD_COMMON/Data_VITIMAGE/Train_space_NN/Test_data_detect_IP/export/tab_Y_IP_'+str(dim_img)+'_'+str(dim_crop)+'_'+str(augment_factor)+'.npy')
print('Shape of tab_X '+str(tab_X_tmp.shape))
print('Shape of tab_Y '+str(tab_Y_tmp.shape))
tab_Y_tmp=tab_Y_tmp-0.5

#Populations 
m_total=(tab_X_tmp.shape)[0]
m_train=int(((tab_X_tmp.shape)[0]*8)/10)
m_test=m_total-m_train
dim_img=(tab_X_tmp.shape)[1]
rand_index=np.arange(m_total)
np.random.shuffle(rand_index)
tab_X=np.copy(tab_X_tmp)
tab_Y=np.copy(tab_Y_tmp)
for i in range(m_total):
    print('copie : '+str(i+1)+'/'+str(m_total))
    tab_X[rand_index[i]]=tab_X_tmp[i]
    tab_Y[rand_index[i]]=tab_Y_tmp[i]

X_train=tab_X[0:m_train,:,:,:].reshape(m_train,dim_img,dim_img,dim_img,1)
X_test=tab_X[m_train:tab_Y.shape[0],:,:,:].reshape(m_test,dim_img,dim_img,dim_img,1)
Y_train=tab_Y[0:m_train,:]
Y_test=tab_Y[m_train:tab_Y.shape[0],:]
print('Shape of X_train '+str(X_train.shape))
print('Shape of Y_train '+str(Y_train.shape))
print('Shape of X_test '+str(X_test.shape))
print('Shape of Y_test '+str(Y_test.shape))


#create model and add model layers
model = Sequential()
model.add(Conv3D(8, kernel_size=3, activation='relu',padding='same'))
model.add(Conv3D(8, kernel_size=3, activation='relu',padding='same'))
model.add(MaxPooling3D(pool_size=(2,2,2)))
#output=16 x 16 x 16 x 16

model.add(Conv3D(16, kernel_size=3, activation='relu',padding='same'))
model.add(Conv3D(16, kernel_size=3, activation='relu',padding='same'))
model.add(MaxPooling3D(pool_size=(2,2,2)))
#output=64 x 8 x 8 x 8

model.add(Conv3D(32, kernel_size=3, activation='relu',padding='same'))
model.add(Conv3D(32, kernel_size=3, activation='relu',padding='same'))
model.add(MaxPooling3D(pool_size=(2,2,2)))
#output=64 x 8 x 8 x 8

model.add(Flatten())
model.add(Dense(3, activation='linear'))
batch_size=32
model.compile(optimizer='adam',batch_size=batch_size, loss=custom_loss(), metrics=['mse'])
history=model.fit(X_train, Y_train, batch_size=batch_size, epochs=15,verbose=1, validation_data=(X_test, Y_test))
score = model.evaluate(X_test, Y_test, verbose=1)

# summarize history for loss
plt.plot(np.log10(history.history['loss']))
plt.plot(np.log10(history.history['val_loss']))
plt.plot((0,15),(-3,-3))
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()

Y_hat_train=model.predict(X_train)
Y_hat_test=model.predict(X_test)
plot_hat(Y_train,Y_hat_train,Y_test,Y_hat_test)

for i in range(50):
    print('next')



#create model and add model layers
model = Sequential()


model.add(Conv3D(8, kernel_size=3, activation='relu',padding='same'))
model.add(Conv3D(8, kernel_size=3, activation='relu',padding='same'))
#model.add(BatchNormalization())
model.add(MaxPooling3D(pool_size=(2,2,2)))
#output=16 x 16 x 16 x 16

model.add(Conv3D(8, kernel_size=3, activation='relu',padding='same'))
model.add(Conv3D(16, kernel_size=3, activation='relu',padding='same'))
#model.add(BatchNormalization())
model.add(MaxPooling3D(pool_size=(2,2,2)))
#output=64 x 8 x 8 x 8

model.add(Conv3D(32, kernel_size=3, activation='relu',padding='same'))
model.add(Conv3D(32, kernel_size=3, activation='relu',padding='same'))
#model.add(BatchNormalization())
model.add(MaxPooling3D(pool_size=(2,2,2)))
#output=64 x 8 x 8 x 8


model.add(Flatten())
model.add(Dense(3, activation='linear'))
batch_size=32
#compile model using accuracy to measure model performance
model.compile(optimizer='adam',batch_size=batch_size, loss=custom_loss(), metrics=['mse'])


#train the model
history=model.fit(X_train, Y_train, batch_size=batch_size, epochs=50,verbose=1, validation_data=(X_test, Y_test))
score = model.evaluate(X_test, Y_test, verbose=1)



def cos_distance():
    def l2_normalize(x, axis):
        norm = K.sqrt(K.sum(K.square(x), axis=axis, keepdims=True))
        return K.sign(x) * K.maximum(K.abs(x), K.epsilon()) / K.maximum(norm, K.epsilon())
    def loss(y_true,y_pred):
        y_true = l2_normalize(y_true, axis=-1)
        y_pred = l2_normalize(y_pred, axis=-1)
        return K.mean(1-y_true * y_pred, axis=-1)
    return loss



print('Test score:', score[0])
print('Test accuracy:', score[1])
model.summary()
X_train_resh=X_train.reshape(m_train,dim_img,dim_img,dim_img)
X_test_resh=X_test.reshape(m_test,dim_img,dim_img,dim_img)


erreur_train=cosinus_error_norm(Y_train,Y_hat_train)
erreur_test=cosinus_error_norm(Y_test,Y_hat_test)

#Before checking
# Check setup
#    index=50; Slicer_3d(add_cube_norm(tab_X_tmp[index],tab_Y_tmp[index],5,2))

# Check detection train set
#    index=50; Slicer_3d(add_cube_norm(add_cube_norm(X_train_resh[index],Y_train[index],5,3),Y_hat_train[index],3,2))
    
# Check detection test set
#    index=10; Slicer_3d(add_cube_norm(add_cube_norm(X_test_resh[index],Y_test[index],8,3),Y_hat_test[index],5,2))
    



def cosinus_error_norm_mat(y_true,y_pred):
    mat=np.zeros(y_true.shape[0])
    for i in range(y_true.shape[0]):
        mat[i]=cosinus_error_norm(y_true[i],y_pred[i])
    return np.mean(mat)
    


def cosinus_error_norm(y_true,y_pred):
    doab=np.dot(y_true,np.transpose(y_pred))
    nora=np.sqrt(np.dot(y_true,np.transpose(y_true)))
    norb=np.sqrt(np.dot(y_pred,np.transpose(y_pred)))
    norab=np.dot(nora,norb)
    return (1-np.divide(doab, norab))
    

def norm(vect_horiz):
    return 


def custom_cosine_loss():
    def loss(y_true,y_pred):
        doab=K.dot(y_true,K.transpose(y_pred))
        nora=K.sqrt(K.dot(y_true,K.transpose(y_true)))
        norb=K.sqrt(K.dot(y_pred,K.transpose(y_pred)))
        norab=K.dot(1/nora,1/norb)
        return (1-K.dot(norab,doab))
#        return (1-K.division(doab, norab))
    return loss


def mahalanobis_loss():
    def loss(y_true,y_pred):
        z_t=y_true[2]
        z_p=y_pred[2]
        ro_t=np.sqrt((y_true[0]-0.5)*(y_true[0]-0.5)+(y_true[1]-0.5)*(y_true[1]-0.5))
        ro_p=np.sqrt((y_pred[0]-0.5)*(y_pred[0]-0.5)+(y_pred[1]-0.5)*(y_pred[1]-0.5))
        teta_t=angle(y_true[0],y_true[1])
        teta_p=angle(y_pred[0],y_pred[1])
        acceptability_dz=2
        acceptability_dteta=0.1
        acceptability_dro=ro_p/3

        dz=np.abs(z_t-z_p)
        dro=np.abs(ro_t-ro_p)
        dteta=np.abs(teta_t-teta_p)
        if dteta>np.pi:
            dteta=2*np.pi-dteta
        vect_d=(dz/acceptability_dz,dro/acceptability_dro,dteta/acceptability_dteta)
        return K.mean(K.sum(K.square(vect_d),axis=1),axis=0)
    return loss



# summarize history for accuracy
plt.plot(history.history['acc'])
plt.plot(history.history['val_acc'])
plt.title('model accuracy')
plt.ylabel('accuracy')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()
# summarize history for loss
plt.plot(history.history['loss'])
plt.plot(history.history['val_loss'])
plt.title('model loss')
plt.ylabel('loss')
plt.xlabel('epoch')
plt.legend(['train', 'test'], loc='upper left')
plt.show()


Y_dep=Y_hat-Y_test
nor=np.multiply(Y_dep,Y_dep)
nor2=np.sum(nor,axis=1)
nor=np.sqrt(nor2)
print(nor)




























#create model and add model layers
model1 = Sequential()


model1.add(Conv3D(8, kernel_size=3, activation='relu',padding='same'))
model1.add(Conv3D(8, kernel_size=3, activation='relu',padding='same'))
#model.add(BatchNormalization())
model1.add(MaxPooling3D(pool_size=(2,2,2)))
#output=16 x 16 x 16 x 16

model1.add(Conv3D(32, kernel_size=3, activation='relu',padding='same'))
model1.add(Conv3D(32, kernel_size=3, activation='relu',padding='same'))
#model.add(BatchNormalization())
model1.add(MaxPooling3D(pool_size=(2,2,2)))
#output=64 x 8 x 8 x 8

model1.add(Conv3D(64, kernel_size=3, activation='relu',padding='same'))
model1.add(Conv3D(64, kernel_size=3, activation='relu',padding='same'))
#model.add(BatchNormalization())
model1.add(MaxPooling3D(pool_size=(2,2,2)))
#output=64 x 8 x 8 x 8


model1.add(Flatten())
model1.add(Dense(3, activation='linear'))
batch_size=16
#compile model using accuracy to measure model performance
model1.compile(optimizer='adam',batch_size=batch_size, loss=custom_loss(), metrics=['mse'])


#train the model
history=model1.fit(X_train, Y_train, batch_size=batch_size, epochs=50,verbose=1, validation_data=(X_test, Y_test))





#create model and add model layers
model2 = Sequential()


model2.add(Conv3D(8, kernel_size=3, activation='relu',padding='same'))
model2.add(Conv3D(8, kernel_size=3, activation='relu',padding='same'))
#model.add(BatchNormalization())
model2.add(MaxPooling3D(pool_size=(2,2,2)))
#output=16 x 16 x 16 x 16

model2.add(Conv3D(32, kernel_size=3, activation='relu',padding='same'))
model2.add(Conv3D(32, kernel_size=3, activation='relu',padding='same'))
#model.add(BatchNormalization())
model2.add(MaxPooling3D(pool_size=(2,2,2)))
#output=64 x 8 x 8 x 8

model2.add(Conv3D(64, kernel_size=3, activation='relu',padding='same'))
model2.add(Conv3D(64, kernel_size=3, activation='relu',padding='same'))
#model.add(BatchNormalization())
model2.add(MaxPooling3D(pool_size=(2,2,2)))
#output=64 x 8 x 8 x 8


model2.add(Flatten())
model2.add(Dense(3, activation='linear'))
batch_size=16
#compile model using accuracy to measure model performance
model2.compile(optimizer='adam',batch_size=batch_size, loss=custom_loss(), metrics=['mse'])


#train the model
history=model2.fit(X_train, Y_train, batch_size=batch_size, epochs=50,verbose=1, validation_data=(X_test, Y_test))




#create model and add model layers
model3 = Sequential()


model3.add(Conv3D(8, kernel_size=3, activation='relu',padding='same'))
model3.add(Conv3D(8, kernel_size=3, activation='relu',padding='same'))
#model.add(BatchNormalization())
model3.add(MaxPooling3D(pool_size=(2,2,2)))
#output=16 x 16 x 16 x 16

model3.add(Conv3D(32, kernel_size=3, activation='relu',padding='same'))
model3.add(Conv3D(32, kernel_size=3, activation='relu',padding='same'))
#model.add(BatchNormalization())
model3.add(MaxPooling3D(pool_size=(2,2,2)))
#output=64 x 8 x 8 x 8

model3.add(Conv3D(64, kernel_size=3, activation='relu',padding='same'))
model3.add(Conv3D(64, kernel_size=3, activation='relu',padding='same'))
#model.add(BatchNormalization())
model3.add(MaxPooling3D(pool_size=(2,2,2)))
#output=64 x 8 x 8 x 8


model3.add(Flatten())
model3.add(Dense(3, activation='linear'))
batch_size=16
#compile model using accuracy to measure model performance
model3.compile(optimizer='adam',batch_size=batch_size, loss=custom_loss(), metrics=['mse'])


#train the model
history=model3.fit(X_train, Y_train, batch_size=batch_size, epochs=50,verbose=1, validation_data=(X_test, Y_test))







#create model and add model layers
model4 = Sequential()


model4.add(Conv3D(8, kernel_size=3, activation='relu',padding='same'))
model4.add(Conv3D(8, kernel_size=3, activation='relu',padding='same'))
#model.add(BatchNormalization())
model4.add(MaxPooling3D(pool_size=(2,2,2)))
#output=16 x 16 x 16 x 16

model4.add(Conv3D(32, kernel_size=3, activation='relu',padding='same'))
model4.add(Conv3D(32, kernel_size=3, activation='relu',padding='same'))
#model.add(BatchNormalization())
model4.add(MaxPooling3D(pool_size=(2,2,2)))
#output=64 x 8 x 8 x 8

model4.add(Conv3D(64, kernel_size=3, activation='relu',padding='same'))
model4.add(Conv3D(64, kernel_size=3, activation='relu',padding='same'))
#model.add(BatchNormalization())
model4.add(MaxPooling3D(pool_size=(2,2,2)))
#output=64 x 8 x 8 x 8


model4.add(Flatten())
model4.add(Dense(3, activation='linear'))
batch_size=16
#compile model using accuracy to measure model performance
model4.compile(optimizer='adam',batch_size=batch_size, loss=custom_loss(), metrics=['mse'])


#train the model
history=model4.fit(X_train, Y_train, batch_size=batch_size, epochs=50,verbose=1, validation_data=(X_test, Y_test))








Y_hat_train_md1=model1.predict(X_train)
Y_hat_train_md2=model2.predict(X_train)
Y_hat_train_md3=model3.predict(X_train)
Y_hat_train_md4=model4.predict(X_train)
Y_train_both=np.zeros((336,3,4))
Y_train_both[:,:,0]=Y_hat_train_md1
Y_train_both[:,:,1]=Y_hat_train_md2
Y_train_both[:,:,2]=Y_hat_train_md3
Y_train_both[:,:,3]=Y_hat_train_md4
Y_hat_train_both=np.mean(Y_train_both,axis=2)
rms_measure_threshold_detector(Y_train,Y_hat_train_md1,1)
rms_measure_threshold_detector(Y_train,Y_hat_train_md2,1)
rms_measure_threshold_detector(Y_train,Y_hat_train_md3,1)
rms_measure_threshold_detector(Y_train,Y_hat_train_md4,1)
rms_measure_threshold_detector(Y_train,Y_hat_train_both,1)

Y_hat_test_md1=model1.predict(X_test)
Y_hat_test_md2=model2.predict(X_test)
Y_hat_test_md3=model3.predict(X_test)
Y_hat_test_md4=model4.predict(X_test)
Y_test_both=np.zeros((84,3,4))
Y_test_both[:,:,0]=Y_hat_test_md1
Y_test_both[:,:,1]=Y_hat_test_md2
Y_test_both[:,:,2]=Y_hat_test_md3
Y_test_both[:,:,3]=Y_hat_test_md4
Y_hat_test_both=np.mean(Y_test_both,axis=2)
rms_measure_threshold_detector(Y_test,Y_hat_test_md1,1)
rms_measure_threshold_detector(Y_test,Y_hat_test_md2,1)
rms_measure_threshold_detector(Y_test,Y_hat_test_md3,1)
rms_measure_threshold_detector(Y_test,Y_hat_test_md4,1)
rms_measure_threshold_detector(Y_test,Y_hat_test_both,1)

  
#    index=10; Slicer_3d(add_cube_norm(add_cube_norm(X_test_resh[index],Y_test[index],8,3),Y_hat_test_both[index],5,2))
    