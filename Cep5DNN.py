#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 22:54:15 2019
From
@author: fernandr
"""
import random
import os.path
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten,MaxPooling3D
from keras.layers import Dropout
from keras.constraints import maxnorm
import tensorflow as tf
import matplotlib.pyplot as plt
import time
import sklearn.metrics
from keras import optimizers
n_sli_by_cep=7
n_ceps=12
n_classes=5
index_starting_feat=5
n_feat=328
n_examples=0
prepare_data=0
normalisation_mode=2  #2=global, 0 = chaque cep a part , 1= normalisation separee de train et test set
prefix_dir='/home/fernandr/Bureau/ML_CEP/DATA_NN/'

def do_it():
    if(prepare_data==1):
        build_data()
    
                
    #n_batch=128 # VAR 0   128
    #n_init=0# VAR 1    0
    #learning_rate=0.00003 #VAR 2  0.00003
    #type_activ=2#VAR 3  2
    #n_layers=6#VAR 4   6
    #layers_power=0#VAR 5   0
    # dropout_rate=0.2 #VAR 6   0.2
    #normalisation_mode=2 #VAR 7 2  #2=global, 0 = chaque cep a part , 1= normalisation separee de train et test set
    n_epochs=300
    vars=[
          [256,320,384,448,512],
          [3],
          [0.00007,0.000084,0.0001,0.000125,0.00015],
          [2],
          [3,4,5],
          [0,1,2],
          [0.15,0.175,0.2,0.225,0.25,0.275,0.3,0.325,0.35],
          [5,6,7],
          [2],
          [1]
          ]

    ####NM3
    vars=[
    [384,512,768],
    [3],
    [0.000125,0.00015,0.000175],
    [2],
    [4],
    [1],
    [0.25],
    [6],
    [2],
    [1]
    ]
   
    #n_batch=64
    #type_initialisation=0
    #learning_rate=0.0002
    #type_activation=2
    #n_layers=5
    #layers_power=1
    #dropout_rate=0
    #normalisation_mode=2
    #optimizer=0
    random=0
    percentage_keep=40
    n_configs=9
    n_repet=2
    tab_acc_vs_epoch=np.zeros((n_configs,n_epochs))
    tab_val_acc_vs_epoch=np.zeros((n_configs,n_epochs))
    tab_mean_std_ending=np.zeros(n_configs)
    tab_std_between_repet=np.zeros(n_configs)
    tab_growing=np.zeros(n_configs)
    
    configs,n_configs_new=build_configs(n_configs,vars,random)
    for index_config in range(n_configs_new):
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print("NEXT TRIAL")
        print()
        print()
        print(str(index_config)+'/'+str(n_configs_new))    
        config=configs[index_config]
        print(config)
        acc_vs_epoch,val_acc_vs_epoch,mean_std_ending,std_between_repet,growing=scores_nn(config,n_epochs,percentage_keep,index_config,n_repet)
        tab_acc_vs_epoch[index_config]=acc_vs_epoch
        tab_val_acc_vs_epoch[index_config]=val_acc_vs_epoch
        tab_mean_std_ending[index_config]=mean_std_ending
        tab_std_between_repet[index_config]=std_between_repet
        tab_growing[index_config]=growing
    
    return tab_acc_vs_epoch,tab_val_acc_vs_epoch,tab_mean_std_ending,tab_std_between_repet,tab_growing,configs



def build_configs(n_configs,vars,rand):
    if(rand==1):
        n_param=np.shape(vars)[0]
        configs=np.zeros((n_configs,n_param))
        for config in range(n_configs):
            for param in range(n_param):
                nb=len(vars[param])
                values=np.asarray(vars[param])
                configs[config,param]=values[int(random.randint(0,nb-1))]
                
        configs=np.array(configs)
    #    configs=configs.astype(int)
        return configs,n_configs
    else:
        n_param=np.shape(vars)[0]
        nb_new_configs=1
        multiples=np.ones((n_param,1))
        multiples=multiples.astype(int)
        for param in range(n_param):
            multiples[param,0]=nb_new_configs            
            nb_new_configs=nb_new_configs*len(vars[param])
            print('gestion de param='+str(param)+' nb vaut'+str(nb_new_configs))
        configs=np.zeros((nb_new_configs,n_param))
        for config in range(nb_new_configs):
            print()
            print('traitement config '+str(config))
            val=config
            for param in range(n_param):
                print('  param'+str(param))
                print('  val '+str(val))
                print('  multiples '+str(multiples[n_param-1-param]))
                print('  case select '+str((val//multiples[n_param-1-param])))
                values=np.asarray(vars[n_param-1-param])
                configs[config,n_param-1-param]=values[(val//multiples[n_param-1-param])]
                val=val%multiples[n_param-1-param]
        configs=np.array(configs)
        print (configs)
        
        return configs,nb_new_configs
        

def scores_nn(config,n_epochs,percentage_keep,index_config,n_repet):
    print('')
    print('')
    print('')
    print('')
    print('')
    print('Testing config :'+str(index_config)+' 1/3')
    t0=time.time()
    n_batch=int(config[0])
    print('n_batch='+str(n_batch))
    n_init=int(config[1])
    learning_rate=config[2]
    print('learning_rate='+str(learning_rate))
    type_activ=int(config[3])
    n_layers=int(config[4])
    print('n_layers='+str(n_layers))
    layers_power=int(config[5])
    print('layers_power='+str(layers_power))
    dropout_rate=config[6]
    print('dropout_rate='+str(dropout_rate))
    weight_constraint=int(config[7])
    print('weight_constraint='+str(weight_constraint))
    normalisation_mode=int(config[8])
    optimizer_mode=int(config[9])
    print('normalisation_mode='+str(normalisation_mode))
    initialisations=['glorot_uniform', 'random_uniform', 'random_normal','glorot_normal']
    activations=['relu','elu','sigmoid','tanh']
    configs_nn=np.asarray([
                [[1000,600,400,200,100,60,20],
                [700,450,200,150,70,45,17],
                [500,300, 200,100,60,30,15]],
     
                [[1000,500,300,150,60,15],
                [750,400,250,120,60,15],
                [500,300,200,100,60,15]],
        
                [[1000,500,200,60,15],
                [750,350,200,60,15],
                [500,200,200,60,15]],
    
                [[1000,500,100,20],
                [750,350,80,17],
                [500,200,60,15]],
    
                [[500,100,20],
                [350,80,20],
                [200,60,20]],
    
                [[200,50],
                [100,35],
                [200,20]],
    
                [[200],
                [50],
                [10]]
                ])
    
    type_init=initialisations[n_init] 
    print('type_initialisation='+type_init)
    type_activation=activations[type_activ]
    print('type_activation='+type_activation)
    layers_sizes=configs_nn[n_layers,layers_power]
    val_acc_vs_epoch=np.zeros(n_epochs)
    acc_vs_epoch=np.zeros(n_epochs)

    mean_f1score=np.zeros(5)
    mean_rec=np.zeros(5)
    mean_prec=np.zeros(5)
    mean_val_acc=0
    mean_std_ending=0
    acc_fin=np.zeros(n_repet)
    std_between_repet=0
    mean_acc=0
    incr=0
    n_exp=1
    n_tot_exp=n_exp*n_repet
    for test_0 in range(n_exp):
        for rep in range(n_repet):
            cep_test_0=test_0*2
            cep_test_1=test_0*2+1
            print('testing '+str(cep_test_0)+' '+str(cep_test_1)+' config'+str(index_config)+' at incr '+str(incr)+'/'+str(n_tot_exp))
            X_train,Y_train,X_test,Y_test=load_data(cep_test_0,cep_test_1,normalisation_mode,percentage_keep)
            confusion,accuracy,val_accuracy,f1score,rec,prec,hist_acc,hist_val_acc=train_model(X_train,Y_train,X_test,Y_test,n_epochs,n_batch,dropout_rate,weight_constraint,type_init,learning_rate,type_activation,layers_sizes,optimizer_mode)
            mean_val_acc=mean_val_acc+val_accuracy/((n_tot_exp))
            mean_acc=mean_acc+accuracy/(n_tot_exp)
            mean_f1score=mean_f1score+(1/(n_tot_exp))*f1score
            mean_rec=mean_rec+(1/(n_tot_exp))*mean_rec
            mean_prec=mean_prec+(1/(n_tot_exp))*mean_prec
            acc_vs_epoch=val_acc_vs_epoch+(1/n_tot_exp)*hist_acc
            val_acc_vs_epoch=val_acc_vs_epoch+(1/n_tot_exp)*hist_val_acc
            mean_std_ending=mean_std_ending+(1/n_tot_exp)*np.std(val_acc_vs_epoch[n_epochs-10:n_epochs])
            acc_fin[incr]=val_accuracy
            incr=incr+1
    std_between_repet=np.std(acc_fin)    
    growing=np.std(val_acc_vs_epoch[n_epochs-10:n_epochs])-np.std(val_acc_vs_epoch[n_epochs-20:n_epochs-10])
    t1=time.time()
    delta_time=int(t1-t0)
    print('TIMING')
    print('TIMING')
    print(delta_time)
    return acc_vs_epoch,val_acc_vs_epoch,mean_std_ending,std_between_repet,growing
 



def train_model(X_train,Y_train,X_test,Y_test,n_epochs,n_batch,dropout_rate,weight_constraint,type_init,learning_rate,type_activation,layers_sizes,optim):
    print('config=')
    print(layers_sizes)
    mean_valacc=np.zeros(n_epochs)
    mean_acc=np.zeros(n_epochs)
    model = Sequential()
    model.add(Dropout(dropout_rate))
    first=1
    n_input=328
    for n_lay in layers_sizes:
        if(n_lay>0):
            if(first==1):
                model.add(Dense(n_lay, activation=type_activation,kernel_initializer=type_init,bias_initializer='zeros',input_dim=n_input, kernel_constraint=maxnorm(weight_constraint)))
                model.add(Dropout(dropout_rate))
                first=0
            else:
                model.add(Dense(n_lay, activation=type_activation,kernel_initializer=type_init,bias_initializer='zeros', kernel_constraint=maxnorm(weight_constraint)))
                model.add(Dropout(dropout_rate))
    model.add(Dense(5, activation=type_activation))
    if(optim==0):
        adam = optimizers.Adam(lr=learning_rate)  
    else:
        adam = optimizers.Nadam(lr=learning_rate)  
    model.compile(adam, loss='categorical_crossentropy', metrics=['accuracy'])
    #train and evaluate the model
    history=model.fit(X_train, Y_train, batch_size=n_batch, epochs=n_epochs,verbose=1, validation_data=(X_test, Y_test))
    Y_pred=model.predict(X_test)
    y_true=np.argmax(Y_test,1)
    y_pred=np.argmax(Y_pred,1)
    conf=sklearn.metrics.confusion_matrix(y_pred,y_true)
    conf=np.array(conf)
    f1score=f1s(conf)
    prec=precisions(conf)
    rec=recalls(conf)
    leng=len(history.history['acc'])
    acc=(history.history['acc'])[leng-1]
    val_acc=(history.history['val_acc'])[leng-1]
    hist_acc=np.asarray((history.history['acc']))
    hist_val_acc=np.asarray((history.history['val_acc']))
    return conf,acc,val_acc,f1score,rec,prec,hist_acc,hist_val_acc


def mean_and_std_accuracy_over_cross_experiments(confusion_matrices):
    accs=np.zeros(np.shape(confusion_matrices)[0])
    for i in range (len(accs)):
        accs[i]=accuracy(confusion_matrices[i])
    mean_acc=np.mean(accs)
    std_acc=np.std(accs)
    return mean_acc,std_acc

def accuracy(confusion_matrix):
    return np.diagonal(confusion_matrix)/np.sum(confusion_matrix,1)
        
def precisions(confusion_matrix):
    return np.diagonal(confusion_matrix)/np.sum(confusion_matrix,1)
        
def recalls(confusion_matrix):
    return np.diagonal(confusion_matrix)/np.sum(confusion_matrix,0)
        
def f1s(confusion_matrix):
    prec=precisions(confusion_matrix)
    rec=recalls(confusion_matrix)
    return (2*rec*prec/(rec+prec))


def testFunc(tab1,tab2):
    compteurTrue=0
    compteurFalse=0
    for i in range(len(tab1)):
        if tab1[i]==tab2[i]:
            compteurTrue=compteurTrue+1
        else:
            compteurFalse=compteurFalse+1

    print(compteurTrue)
    print(compteurFalse)








def build_data():
    #Inventory examples files, and count data available for each cep and classe
    n_examples_ceps=np.zeros((n_ceps))
    if(prepare_data==1):
        for cep in range(n_ceps):
            n_ex_tot=0
            for classe in range(n_classes):
                n_ex=0 
                for sli in range(n_sli_by_cep):
                    z=cep+n_ceps*sli  #The 12 ceps are interleaved in the file. Cep01 can be get in slices 0,12,24,...
                    str_file=prefix_dir+'Data_txt/data_all.txt_cl_'+str(classe)+'z_'+str(z)+'.txt'
                    if(os.path.exists(str_file)): 
                        tab=np.loadtxt(str_file,delimiter=';') ;
                        n_ex=n_ex+np.shape(tab)[0]
                n_ex_tot=n_ex_tot+n_ex
                print('   cep '+str(cep)+' classe '+str(classe)+' a '+str(n_ex)+' examples')
            print('Cep '+str(cep)+' a '+str(n_ex_tot)+' examples')
            n_examples=n_examples+n_ex_tot
            n_examples_ceps[cep]=n_ex_tot
        print('Nombre total examples='+str(n_examples))
        print(n_examples_ceps)
    
        #Build feature and output vector for each cep
        for cep in range(n_ceps):
            data_cep=np.zeros((int(round(n_examples_ceps[cep])),n_feat+1))
            n_ex=0 
            for classe in range(n_classes):
                for sli in range(n_sli_by_cep):
                    z=cep+n_ceps*sli #as explained ten lines below
                    str_file=prefix_dir+'Data_txt/data_all.txt_cl_'+str(classe)+'z_'+str(z)+'.txt'
                    if(os.path.exists(str_file)): 
                        tab=np.loadtxt(str_file,delimiter=';') ;
                        dataX=tab[:,index_starting_feat:n_feat+index_starting_feat]
                        dataY=tab[:,3]
                        start=n_ex
                        stop=n_ex+np.shape(dataX)[0]
                        data_cep[start:stop,0:n_feat]=dataX[:,:]
                        data_cep[start:stop,n_feat]=dataY[:]
    
                        print('')
                        print('cep='+str(cep)+' sli='+str(sli)+' classe='+str(classe))
                        print('tab shape=')
                        print(np.shape(tab))
                        print(tab[0,0:8])
                        print(tab[0,325:333])
                        print('data_cep shape=')
                        print(np.shape(data_cep))
                        print(data_cep[n_ex,0:8])
                        print(data_cep[n_ex,321:329])
                        n_ex=stop                    
                        print('prochain indice start='+str(n_ex)+' / '+ str(n_examples_ceps[cep]))
    #                    time.sleep(100000)
     #                   print(data_cep[0,:])
            print ('saving cep data in '+prefix_dir+'Data_npy/data_cep_'+str(cep)+'.npy')
    #        print ('first line contents :')
    #        print(data_cep[0,:])
    #        print ('second line contents :')
    #        print(data_cep[1,:])
            np.save(prefix_dir+'Data_npy/data_cep_'+str(cep)+'.npy',data_cep)
            print ('saving ok.')
            print('')





def load_data(test_cep_0,test_cep_1,normalisation_mode,percentage_keep):
    n_examples_ceps=np.zeros(n_ceps)
    for cep in range(n_ceps):
        data=np.load(prefix_dir+'Data_npy/data_cep_'+str(cep)+'.npy')         
        n_examples_ceps[cep]=int(round(np.shape(data)[0]))
    #        print('reading cep '+str(cep)+' with '+str(n_examples_ceps[cep])+' examples')
    n_examples_ceps=n_examples_ceps.astype(int)
    print('Cardinal of examples from each cep :')
    print(n_examples_ceps)
    
    
    ### Choisir ceux qui sont experimentés
    test_specimens=np.zeros(12)
    test_specimens[test_cep_0]=1 
    test_specimens[test_cep_1]=1 
    training_specimens=1-test_specimens
    training_specimens=training_specimens.astype(int)
    test_specimens=test_specimens.astype(int)
    print('training specimens=')
    print(training_specimens)
    print('test specimens=')
    print(test_specimens)


    # Construire X_test, X_train, Y_test, Y_train
    n_test=0
    n_train=0
    for cep in range(n_ceps):
        if(test_specimens[cep]==1):
            n_test=n_test+n_examples_ceps[cep]
        if(training_specimens[cep]==1):
            n_train=n_train+n_examples_ceps[cep]
    print('training examples='+str(n_train))
    print('test examples='+str(n_test))
    
    train_set=np.zeros((n_train,n_feat+1))
    test_set=np.zeros((n_test,n_feat+1))
    index_train=0
    index_test=0
    for cep in range(n_ceps):
        if(test_specimens[cep]==1):
            start=index_test
            stop=index_test+n_examples_ceps[cep]
            test_set[start:stop,:]=np.load(prefix_dir+'Data_npy/data_cep_'+str(cep)+'.npy')
            index_test=stop
    
            #Normaliser à la volee
            if(normalisation_mode==0):#Normalisation interne à chaque cep
                test_set[start:stop,0:n_feat]=np.nan_to_num(((test_set[start:stop,0:n_feat]-np.mean(test_set[start:stop,0:n_feat],0))/np.std(test_set[start:stop,0:n_feat],0)))
        if(training_specimens[cep]==1):
            start=index_train
            stop=index_train+n_examples_ceps[cep]
            train_set[start:stop,:]=np.load(prefix_dir+'Data_npy/data_cep_'+str(cep)+'.npy')
            index_train=stop
            #Normaliser à la volee
            if(normalisation_mode==0):#Normalisation interne à chaque cep
                train_set[start:stop,0:n_feat]=np.nan_to_num(((train_set[start:stop,0:n_feat]-np.mean(train_set[start:stop,0:n_feat],0))/np.std(train_set[start:stop,0:n_feat],0)))
   
    #Shuffling, then divide in inputs X and outputs Y
    np.random.shuffle(train_set)
    np.random.shuffle(test_set)
    X_train=train_set[:,0:n_feat]
    Y_train=train_set[:,n_feat]
    X_test=test_set[:,0:n_feat]
    Y_test=test_set[:,n_feat]
    if(normalisation_mode==1):#Normalisation sur une moyenne globale train entre eux, et test entre eux
        X_train=np.nan_to_num((X_train-np.mean(X_train,0))/np.std(X_train,0))
        X_test=np.nan_to_num((X_test-np.mean(X_test,0))/np.std(X_test,0))
    if(normalisation_mode==2):
        X_glob=np.append(X_train,X_test,axis=0)
        X_train=np.nan_to_num((X_train-np.mean(X_glob,0))/np.std(X_glob,0))
        X_test=np.nan_to_num((X_test-np.mean(X_glob,0))/np.std(X_glob,0))
        
    
    #Set the output to categorical mode  ( 4 = [0 0 0 0 1])
    Y_train = tf.keras.utils.to_categorical(Y_train)
    Y_test = tf.keras.utils.to_categorical(Y_test)
    n_keep_train=(np.shape(X_train)[0]*percentage_keep)//100
    print(n_keep_train)
#    n_keep_test=(np.shape(X_test)[0]*percentage_keep)//100
    X_train=X_train[0:n_keep_train,:]
    Y_train=Y_train[0:n_keep_train,:]
#    X_test=X_test[0:n_keep_test,:]
#    Y_test=Y_test[0:n_keep_test,:]

    feat_imp=np.loadtxt('/home/fernandr/Bureau/temp/feat_imp_python.txt')
    mean=np.mean(feat_imp[:,4])

    sequence_feats = list(filter(lambda i: feat_imp[i,4]>=0, range(np.shape(feat_imp)[0])))    
    X_train=X_train[:,sequence_feats]
    X_test=X_test[:,sequence_feats]

    return X_train,Y_train,X_test,Y_test












def do_some():
    if(prepare_data==1):
        build_data()
    
                
    #n_batch=128 # VAR 0   128
    #n_init=0# VAR 1    0
    #learning_rate=0.00003 #VAR 2  0.00003
    #type_activ=2#VAR 3  2
    #n_layers=6#VAR 4   6
    #layers_power=0#VAR 5   0
    # dropout_rate=0.2 #VAR 6   0.2
    #normalisation_mode=2 #VAR 7 2  #2=global, 0 = chaque cep a part , 1= normalisation separee de train et test set
    #Optimizer=0 #VAR 8 
    n_epochs=300
    percentage_keep=50
    n_configs=1
    n_repet=3
    tab_acc_vs_epoch=np.zeros((n_configs,n_epochs))
    tab_val_acc_vs_epoch=np.zeros((n_configs,n_epochs))
    tab_mean_std_ending=np.zeros(n_configs)
    tab_std_between_repet=np.zeros(n_configs)
    tab_growing=np.zeros(n_configs)
    
    configs=[[128,3,0.00004,2,5,1,0.25,4,2]]
    for index_config in range(n_configs):
        print()
        print()
        print()
        print()
        print()
        print()
        print()
        print("NEXT TRIAL")
        print()
        print()
        print(str(index_config)+'/'+str(n_configs))    
        config=configs[index_config]
        print(config)
        acc_vs_epoch,val_acc_vs_epoch,mean_std_ending,std_between_repet,growing=scores_nn(config,n_epochs,percentage_keep,index_config,n_repet)
        tab_acc_vs_epoch[index_config]=acc_vs_epoch
        tab_val_acc_vs_epoch[index_config]=val_acc_vs_epoch
        tab_mean_std_ending[index_config]=mean_std_ending
        tab_std_between_repet[index_config]=std_between_repet
        tab_growing[index_config]=growing
    
    return tab_acc_vs_epoch,tab_val_acc_vs_epoch,tab_mean_std_ending,tab_std_between_repet,tab_growing,configs


