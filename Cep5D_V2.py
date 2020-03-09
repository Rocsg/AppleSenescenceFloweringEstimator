#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 22:09:03 2019

@author: fernandr
"""
import os
import numpy as np
import random
import os.path
import numpy as np
from keras.models import Sequential
from keras import optimizers
from keras.layers import Dense, Flatten,MaxPooling3D
from keras.layers import Dropout
from keras.constraints import maxnorm
import tensorflow as tf
import matplotlib.pyplot as plt
import time
import sklearn.metrics


###############################################################################################################################"
#####
##### Training routines, and main entry points
#

def perform_augmented_test(exp,crossmode):
    path=get_results_dir(exp)
    best_config=np.load(path+'Best_config.npy')
    confusion_matrices,accuracies,val_accuracies,hist_accuracies,hist_val_accuracies=evaluate_config(best_config,exp,1,crossmode,0,0)
    augmented_performance=mean_and_std_accuracy_over_cross_experiments(confusion_matrices)
    wash_screen()
    print('Performance with augmented data='+str(augmented_performance[0]))
    path=get_results_dir(exp)
    np.save(path+'Best_augmented_confusions_matrices'+exp+'.npy',confusion_matrices)
    np.save(path+'Best_augmented_hist_accuracies.npy',np.mean(hist_accuracies,axis=0))
    np.save(path+'Best_augmented_hist_val_accuracies.npy',np.mean(hist_val_accuracies,axis=0))
    return augmented_performance, confusion_matrices


    

def compute_augmented_scores(exp):
    path=get_results_dir(exp)
    confusion_matrices=np.load(path+'Best_augmented_confusions_matrices'+exp+'.npy')
    results=performances_scores_over_cross_experiments(confusion_matrices)
    print(results)

def show_learning_curves(exp,start,first_index,last_index,focus=2):
    indices_list=build_unique_index_list_for_exp(exp,first_index,last_index)
    path=get_data_debug_dir(exp)
    print('Results get with config=')
    print(config)
    plt.figure()
    for index in indices_list:
        config=np.load(path+'Best_config.npy')
        
    hist_accuracies=np.load(path+'Best_augmented_hist_accuracies.npy')
    hist_val_accuracies=np.load(path+'Best_augmented_hist_val_accuracies.npy')
    n_epochs=len(hist_accuracies)
    plt.plot(100*hist_accuracies)
    plt.plot(100*hist_val_accuracies)
    plt.plot([0,n_epochs],[91.6,91.6])
    plt.plot([0,n_epochs],[92.0,92.0])
    plt.plot([0,n_epochs],[92.4,92.4])
    plt.plot([0,n_epochs],[92.8,92.8])
    legends=['Training accuracy','Validation accuracy', 'Best random forest', 'Best without augmentation', 'High_score low', 'High_score high']
    plt.title('Model accuracy')
    plt.ylabel('% Good classification')
    plt.xlabel('Epoch')
    plt.ylim(0.8,1)
    if(focus==0):
        plt.ylim([60.0,100])
    if(focus==1):
        plt.ylim([80.0,95])
    if(focus==2):
        plt.ylim([90.0,94])
    if(focus==3):
        plt.ylim([90.7,93.3])
    plt.legend(legends)
    plt.show()


def build_unique_index_list_for_exp(exp,first_index,last_index):
    filenames = os.listdir(get_data_debug_dir(exp))
    unique_indices=[]
    for file in filenames:    
        val=int(file.split("_")[0])
        if((val>=first_index) & (val<=last_index)):
            unique_indices.append(val)
    return np.unique(unique_indices)



def configurations_comparisons(exp,unique_index_list,focus=1):
    #Collecter toutes les configurations
    n_param=8
    n_list=len(unique_index_list)
    configs=np.zeros((n_list,n_param))
    accs=np.zeros(n_list)
    val_accs=np.zeros(n_list)
    varying_parameters=np.zeros(n_param)
    #Collecter les variations sur les configurations
    for conf in range(n_list):
        configs[conf]=np.load(get_data_debug_dir(exp)+str(unique_index_list[conf])+'_config.npy')
        hist_val_acc=np.load(get_data_debug_dir(exp)+str(unique_index_list[conf])+'_hist_val_accuracies.npy')
        hist_acc=np.load(get_data_debug_dir(exp)+str(unique_index_list[conf])+'_hist_accuracies.npy')
        n_epochs=len(hist_val_acc)
        accs[conf]=100*np.mean(hist_acc[n_epochs-5:n_epochs])        
        val_accs[conf]=100*np.mean(hist_val_acc[n_epochs-5:n_epochs])        

    for param in range(n_param):
        val_init=configs[0,param]
        for conf in range(n_list):
            if(configs[conf,param] != val_init):
                varying_parameters[param]=1
                
    #Pour chaque variation, construire un plot
    for param in range(n_param):
        if(varying_parameters[param]==1):
            plt.figure()
            
            min=np.min(configs[:,param])
            max=np.max(configs[:,param])
            dminmax=max-min
            plt.scatter(configs[:,param],val_accs,c='coral')
            plt.scatter(configs[:,param],accs,c='blue')
            plt.title(param_names(param))
            print('')
            print('param numero '+str(param)+' je vais faire scatter de  :')
            print(configs[:,param])
            print(val_accs)
            print(accs)
           #Pour chaque valeur possible, faire une boxplot
            vals=np.unique(configs[:,param])
            for val in vals:
                index_confs_inside=list(filter(lambda i: configs[i,param]==val, range(n_list)))    
                values_inside=val_accs[index_confs_inside]
                print('indices=')
                print(index_confs_inside)
                print(values_inside)
                plt.boxplot(values_inside,positions=[val],widths=dminmax/20)
            plt.xlim(min-dminmax/10,max+dminmax/10)
            plt.ylim(0.8,1)
            if(focus==0):
                plt.ylim([60.0,100])
            if(focus==1):
                plt.ylim([80.0,95])
            if(focus==2):
                plt.ylim([90.0,94])
            if(focus==3):
                plt.ylim([92,93.5])
            plt.show()
 


    plt.figure()
    legends=[]
    for conf in range(n_list):
        configs=np.load(get_data_debug_dir(exp)+str(unique_index_list[conf])+'_config.npy')
        print('Je vais faire un plot')
        print(configs)
        strin='ACC BS='+str(configs[0])+' |LR='+str(configs[1])+' |NLAYS='+str(configs[2])+'|NAUG='+str(configs[6])
        legends.append(strin)
        strin='VAL ACC BS='+str(configs[0])+' |LR='+str(configs[1])+' |NLAYS='+str(configs[2])+'|NAUG='+str(configs[6])
        legends.append(strin)
        hist_val_acc=np.load(get_data_debug_dir(exp)+str(unique_index_list[conf])+'_hist_val_accuracies.npy')
        hist_acc=np.load(get_data_debug_dir(exp)+str(unique_index_list[conf])+'_hist_accuracies.npy')
        print(hist_val_acc)
        print(hist_acc)
        plt.plot(100*hist_acc)
        plt.plot(100*hist_val_acc)
    plt.plot([0,n_epochs],[90,90])
    plt.plot([0,n_epochs],[92.0,92.0])
    plt.plot([0,n_epochs],[94,94])
    plt.plot([0,n_epochs],[96,96])
    plt.title('Model accuracy')
    plt.ylabel('% Good classification')
    plt.xlabel('Epoch')
    plt.ylim(0.8,1)
    if(focus==0):
        plt.ylim([60.0,100])
    if(focus==1):
        plt.ylim([80.0,95])
    if(focus==2):
        plt.ylim([90.0,94])
    if(focus==3):
        plt.ylim([90.7,93.3])
    plt.legend(legends)
    plt.show()




    

def hyper_optimization(exp,crossmode):
    wash_screen()
    print("Starting hyper_optimization")
    configs=build_test_configurations()
    print(" test configs : ")
    print(configs)
    exit(0)
    max_perf=0
    ind_of_max=0
    unique_index_of_max=0
    for index_config in range(np.shape(configs)[0]):
        unique_exp_index=int(time.time()//1)
        wash_screen()
        print('PROCESSING HYPEREVAL OVER '+str(index_config)+' / '+str(np.shape(configs)[0])+' index='+str(unique_exp_index))        
        confusion_matrices,accuracies,val_accuracies,hist_accuracies,hist_val_accuracies=evaluate_config(configs[index_config],exp,0,crossmode,1,index_config)
        global_performance=mean_and_std_accuracy_over_cross_experiments(confusion_matrices)       
        print(' config '+str(index_config)+' gets performance of '+str(global_performance))
        np.save(get_data_debug_dir(exp)+str(unique_exp_index)+'_config.npy',configs[index_config])
        np.save(get_data_debug_dir(exp)+str(unique_exp_index)+'_confusion_matrices.npy',confusion_matrices)
        np.save(get_data_debug_dir(exp)+str(unique_exp_index)+'_hist_accuracies.npy',np.mean(hist_accuracies,axis=0))
        np.save(get_data_debug_dir(exp)+str(unique_exp_index)+'_hist_val_accuracies.npy',np.mean(hist_val_accuracies,axis=0))
        

        if(global_performance[0]>max_perf):
            print(' it s a new max !')
            max_perf=global_performance[0]
            ind_of_max=index_config
            unique_index_of_max=unique_exp_index

    print('Best performance of '+str(max_perf)+' achieved with config ')
    print(configs[ind_of_max])
    path=get_results_dir(exp)
    np.save(path+'Best_config.npy',configs[ind_of_max])
    np.save(path+'Best_unique_index.npy',unique_index_of_max)
    return configs[ind_of_max]




 

def train_model(X_train,Y_train,X_test,Y_test,n_epochs,params):
    n_batch=params["Batch_size"]
    learning_rate=params["Learning_rate"]
    layers_sizes=params["Network_layers_configuration"]
    dropout_rate=params["Dropout_rate"]
    weight_constraint=params["Weight_constraint"]
    print('Training a model built with the config ')
    print(layers_sizes)
    print(' training on data :')
    print(np.shape(X_train))
    print(np.shape(Y_train))
    print(np.shape(X_test))
    print(np.shape(Y_test))

    model = Sequential()
    model.add(Dropout(dropout_rate))
    first=1
    n_input=328
    for n_lay in layers_sizes:
        if(n_lay>0):
            if(first==1):
                model.add(Dense(n_lay, activation='sigmoid',kernel_initializer='glorot_normal',bias_initializer='zeros',input_dim=n_input, kernel_constraint=maxnorm(weight_constraint)))
                model.add(Dropout(dropout_rate))
                first=0
            else:
                model.add(Dense(n_lay, activation='sigmoid',kernel_initializer='glorot_normal',bias_initializer='zeros', kernel_constraint=maxnorm(weight_constraint)))
                model.add(Dropout(dropout_rate))
    model.add(Dense(5, activation='softmax'))
    nadam = optimizers.Adam(lr=learning_rate)  
    model.compile(nadam, loss='categorical_crossentropy', metrics=['accuracy'])

    #train and evaluate the model
    history=model.fit(X_train, Y_train, batch_size=n_batch, epochs=n_epochs,verbose=1, validation_data=(X_test, Y_test))
    Y_pred=model.predict(X_test)
    y_true=np.argmax(Y_test,1)
    y_pred=np.argmax(Y_pred,1)
    confusion_matrix=sklearn.metrics.confusion_matrix(y_pred,y_true)
    confusion_matrix=np.array(confusion_matrix)
    leng=len(history.history['acc'])
    acc=(history.history['acc'])[leng-1]
    val_acc=(history.history['val_acc'])[leng-1]
    hist_acc=np.asarray((history.history['acc']))
    hist_val_acc=np.asarray((history.history['val_acc']))
    del y_true,y_pred,Y_pred,X_train,Y_train,X_test,Y_test,nadam,model
    return confusion_matrix,acc,val_acc,hist_acc,hist_val_acc



def evaluate_config(config,exp,do_data_augmentation,cross_mode,is_tuning,n_config):
    n_test,training_specimens,test_specimens=cross_configurations(cross_mode)
    print('Evaluate config')
    if(do_data_augmentation==1):
        n_epochs=250
    else:
        n_epochs=250
    print(config)
    print('n_test='+str(n_test))
    print('training_specimens=')
    print(training_specimens)
    print('test_specimens=')
    print(test_specimens)
    confusion_matrices=np.zeros((n_test,5,5))
    accuracies=np.zeros(n_test)
    val_accuracies=np.zeros(n_test)
    hist_accuracies=np.zeros((n_test,n_epochs))
    hist_val_accuracies=np.zeros((n_test,n_epochs))
    for test in range(n_test):        
        #Load data according to exp
        print('Test number '+str(test)+' of config number '+str(n_config))
        X_train,Y_train=load_data(exp,0,training_specimens[test],do_data_augmentation,config[6],config[7]) # Training data
        print('X_train and Y_train shape=')
        print(np.shape(X_train))
        print(np.shape(Y_train))
        if(is_tuning==1):
            X_test,Y_test=load_data(exp,1,test_specimens[test],0) #Hyper tuning data
        else:
            X_test,Y_test=load_data(exp,2,test_specimens[test],0) #Testing data
        print('X_test and Y_test shape=')
        print(np.shape(X_test))
        print(np.shape(Y_test))

        
        params=parse_arguments(config)

        confusion_matrix,accuracy,val_accuracy,hist_accuracy,hist_val_accuracy=train_model(
                X_train,Y_train,X_test,Y_test,
                n_epochs,params)
        confusion_matrices[test]=np.copy(confusion_matrix)
        accuracies[test]=accuracy
        val_accuracies[test]=val_accuracy
        hist_accuracies[test]=hist_accuracy
        hist_val_accuracies[test]=hist_val_accuracy
        del X_train,Y_train,X_test,Y_test
    return confusion_matrices,accuracies,val_accuracies,hist_accuracies,hist_val_accuracies







###############################################################################################################################"
#####
##### Access to data and results via file storage, data preparation, train/test/valid/augment split
#
def get_main_dir():
    return '/home/fernandr/Bureau/ML_CEP/DATA_NN/'


def get_data_debug_dir(exp):
    return (get_main_dir()+'Data_debug/'+exp+'/')

def get_data_npy_dir(exp):
    return (get_main_dir()+'Data_npy/'+exp+'/')

def get_data_weka_dir(exp):
    return (get_main_dir()+'Data_weka/'+exp+'/')

def get_results_dir(exp):
    return (get_main_dir()+'Results/'+exp+'/')


def prepare_folders_for_experiment(exp):
    rep_debug=get_data_debug_dir(exp)
    os.makedirs(rep_debug)
    rep_data_npy=get_data_npy_dir(exp)
    os.makedirs(rep_data_npy)
    rep_data_weka=get_data_weka_dir(exp)
    os.makedirs(rep_data_weka)
    rep_results=get_results_dir(exp)
    os.makedirs(rep_results)


def transform_weka_data_to_normalized_npy_data(exp,balance_amadou):
    n_ceps=12
    n_feat=328
    n_sli_by_cep=7
    epsilon=0.000001
    index_starting_feat=5
    n_examples_ceps=np.zeros(n_ceps)
    global_data=np.zeros((0,n_feat+index_starting_feat))
    if(balance_amadou==1):
        range_classes=[0,1,2,3,3,4]
    else:
        range_classes=[0,1,2,3,4]
    
    #Count number of examples for each cep 
    print('Examples inventory')
    for cep in range(n_ceps):
        n_ex_tot=0
        for classe in range_classes:
            n_ex=0
            for sli in range(n_sli_by_cep):
                z=cep+n_ceps*sli  #The 12 ceps are interleaved in the file. Cep01 can be get in slices 0,12,24,...
                str_file=get_data_weka_dir(exp)+'data_all.txt_cl_'+str(classe)+'z_'+str(z)+'.txt'
                if(os.path.exists(str_file)):
                    tab=np.loadtxt(str_file,delimiter=';') ;
                    global_data=np.append(global_data,tab,axis=0)
                    n_ex=n_ex+np.shape(tab)[0]
            n_ex_tot=n_ex_tot+n_ex
            print('   cep '+str(cep)+' classe '+str(classe)+' a '+str(n_ex)+' examples')
        print('Cep '+str(cep)+' a '+str(n_ex_tot)+' examples')
        n_examples_ceps[cep]=n_ex_tot

    #Compute global mean and std for each feature
    print('shape de global_data')
    print(np.shape(global_data))
    glob_means_all=np.mean(global_data,axis=0)
    print('shape de means')
    print(np.shape(glob_means_all))
#    glob_stds_all=np.std(global_data,axis=0)
    glob_stds_all=(np.max(global_data,axis=0)-np.min(global_data,axis=0))/2
    glob_means=glob_means_all[index_starting_feat:n_feat+index_starting_feat]
    glob_stds=glob_stds_all[index_starting_feat:n_feat+index_starting_feat]
    for i in range(len(glob_stds)):
        if(glob_stds[i]<epsilon):
            glob_stds[i]=1
 
    #Build the corresponding data
    print('Data building')
    for cep in range(n_ceps):
        data_cep=np.zeros((int(round(n_examples_ceps[cep])),n_feat+1))
        data_coords=np.zeros((int(round(n_examples_ceps[cep])),3))
        n_ex=0 
        for classe in range_classes:
            for sli in range(n_sli_by_cep):
                z=cep+n_ceps*sli #as explained ten lines below
                str_file=get_data_weka_dir(exp)+'data_all.txt_cl_'+str(classe)+'z_'+str(z)+'.txt'
                if(os.path.exists(str_file)): 
                    tab=np.loadtxt(str_file,delimiter=';') ;
                    dataX=(tab[:,index_starting_feat:n_feat+index_starting_feat]-glob_means)/glob_stds
                    dataY=tab[:,3]
                    dataZ=tab[:,0:3]
                    start=n_ex
                    stop=n_ex+np.shape(dataX)[0]
                    data_cep[start:stop,0:n_feat]=dataX[:,:]
                    data_cep[start:stop,n_feat]=dataY[:]                    
                    data_coords[start:stop,:]=dataZ[:]                    
                    n_ex=stop                    
                    #print('prochain indice start='+str(n_ex)+' / '+ str(n_examples_ceps[cep]))
        print ('saving '+str(n_ex)+' examples in dir '+get_data_npy_dir(exp)+'cep_'+str(cep)+'_global.npy')
        np.save(get_data_npy_dir(exp)+'cep_'+str(cep)+'_global.npy',data_cep)
        np.save(get_data_npy_dir(exp)+'cep_'+str(cep)+'_global_coords.npy',data_coords)
        del data_cep        
    
    
    
    
    
    
    

    
def split_training_augmented_crossvalidation_test_sets(exp,n_augmentation_max,sigma_power_max):
    seed=7
    np.random.seed(seed)  
    n_feat=328
    train_ratio=50
    valid_ratio=25
    for cep in range(12):
        print('Building sets for cep '+str(cep))
        np.random.seed(seed)  
        global_set=np.load(get_data_npy_dir(exp)+'cep_'+str(cep)+'_global.npy')
        np.random.shuffle(global_set)
        n_glob=np.shape(global_set)[0]
        last_train=(n_glob*train_ratio)//100
        last_valid=last_train+(n_glob*valid_ratio)//100
        training_set=np.copy(global_set[0:last_train,:])
        valid_set=np.copy(global_set[last_train:last_valid,:])
        test_set=np.copy(global_set[last_valid:n_glob,:])
        np.save(get_data_npy_dir(exp)+'cep_'+str(cep)+'_train.npy',training_set)
        print('saving '+get_data_npy_dir(exp)+'cep_'+str(cep)+'_train.npy')

        np.save(get_data_npy_dir(exp)+'cep_'+str(cep)+'_valid.npy',valid_set)
        print('saving '+get_data_npy_dir(exp)+'cep_'+str(cep)+'_valid.npy')

        np.save(get_data_npy_dir(exp)+'cep_'+str(cep)+'_test.npy',test_set)
        print('saving '+get_data_npy_dir(exp)+'cep_'+str(cep)+'_test.npy')


        for n_aug in range(n_augmentation_max):
            for n_sig in range(sigma_power_max):
                sigma_max_augment=0.1+n_sig*0.1
                augmented_training_set=np.zeros((last_train*n_aug,n_feat+1))
                for repet in range(n_aug):
                    sigma=sigma_max_augment*((repet+1)/n_aug)
                    augmented_training_set[repet*last_train:(repet+1)*last_train,:]=np.copy(training_set)
                    augmented_training_set[repet*last_train:(repet+1)*last_train,0:n_feat]=augmented_training_set[repet*last_train:(repet+1)*last_train,0:n_feat]+np.random.normal(0,sigma,(last_train,n_feat)) 
         
                np.save(get_data_npy_dir(exp)+'cep_'+str(cep)+'_train_augmented_'+str(n_aug)+'_'+str(n_sig)+'.npy',augmented_training_set)
                print('saving '+get_data_npy_dir(exp)+'cep_'+str(cep)+'_train_augmented.npy')
                del augmented_training_set,training_set,valid_set,test_set


def manhatan_distance(vect1,vect2):
    return np.max(np.abs(vect1-vect2))


def split_training_augmented_crossvalidation_test_sets_interpolation(exp,n_augmentation_max,sigma_power):
    seed=7
    np.random.seed(seed)  
    n_feat=328
    train_ratio=50
    valid_ratio=25
    for cep in range(12):
        print('Building sets for cep '+str(cep))
        np.random.seed(seed)  
        global_set=np.load(get_data_npy_dir(exp)+'cep_'+str(cep)+'_global.npy')
        global_coords=np.load(get_data_npy_dir(exp)+'cep_'+str(cep)+'_global_coords.npy')
        if(n_augmentation_max>0):
            n_init=np.shape(global_set)[0]
            list_new_vect=np.zeros((n_init*(n_augmentation_max+4),n_feat+1))
            incr=0
            for n in range(n_init-1):
                if((n%2000)==0):
                    print('')
                    print('processing '+str(n)+' / '+str(n))
                    print(global_coords[n,:])
                    print(global_coords[n+1,:])
                if((manhatan_distance(global_coords[n,:],global_coords[n+1,:]) < 2)):
                    if((n%2000)==0):
                        print('manhatan ok')
                    if((global_set[n,n_feat]==global_set[n+1,n_feat])):
                        if((n%2000)==0):
                            print('classe ok')
                            print('vals start i0 :')
                            print(global_set[n,0:4])
                            print('vals start i1 :')
                            print(global_set[n+1,0:4])
                        for indx in range(n_augmentation_max):
                            vect_new=((indx+1)/(n_augmentation_max+1))*global_set[n+1]+((n_augmentation_max-indx)/(n_augmentation_max+1)*global_set[n])
                            list_new_vect[incr]=vect_new
                            if((n%2000)==0):
                                print('ajout : ')
                                print(list_new_vect[incr,0:4])
                            incr=incr+1
                if((n%2000)==0):
                    print('etat list sup : '+str(np.shape(list_new_vect)[0]))
                    
        list_new_vect=list_new_vect[0:incr,:]
        print('Avant ajout : global set='+str(np.shape(global_set)[0]))
        print('Incr='+str(incr))
        global_set=np.concatenate((global_set,list_new_vect),axis=0)
        print('Apres ajout : global set='+str(np.shape(global_set)[0]))
        np.random.shuffle(global_set)
        n_glob=np.shape(global_set)[0]
        last_train=(n_glob*train_ratio)//100
        last_valid=last_train+(n_glob*valid_ratio)//100
        training_set=np.copy(global_set[0:last_train,:])
        valid_set=np.copy(global_set[last_train:last_valid,:])
        test_set=np.copy(global_set[last_valid:n_glob,:])
        np.save(get_data_npy_dir(exp)+'cep_'+str(cep)+'_train.npy',training_set)
        print('saving '+get_data_npy_dir(exp)+'cep_'+str(cep)+'_train.npy')

        np.save(get_data_npy_dir(exp)+'cep_'+str(cep)+'_valid.npy',valid_set)
        print('saving '+get_data_npy_dir(exp)+'cep_'+str(cep)+'_valid.npy')

        np.save(get_data_npy_dir(exp)+'cep_'+str(cep)+'_test.npy',test_set)
        print('saving '+get_data_npy_dir(exp)+'cep_'+str(cep)+'_test.npy')







def load_data(exp,type,cep_list,do_data_augmentation,n_augmentation=0,sigma_power=0):
    print('Building data for the test')
    print(cep_list)
    seed=7
    n_feat=328
    global_set=np.zeros((0,n_feat+1))
    print(cep_list)
    print(np.shape(cep_list))
    for i in range (12):
        if(cep_list[i]==1):
            if(type==0):
                new_set=np.load(get_data_npy_dir(exp)+'cep_'+str(i)+'_train.npy')
                print(np.shape(new_set)[0])
                global_set=np.append(global_set,new_set,axis=0)
                del new_set
                if(do_data_augmentation==1):
                    new_set=np.load(get_data_npy_dir(exp)+'cep_'+str(i)+'_train_augmented_'+str(int(n_augmentation))+'_'+str(int(sigma_power))+'.npy')
                    print(np.shape(new_set)[0])
                    global_set=np.append(global_set,new_set,axis=0)
                    del new_set
            if(type==1):
                new_set=np.load(get_data_npy_dir(exp)+'cep_'+str(i)+'_valid.npy')
                print(np.shape(new_set)[0])
                global_set=np.append(global_set,new_set,axis=0)
                del new_set
            if(type==2):
                new_set=np.load(get_data_npy_dir(exp)+'cep_'+str(i)+'_test.npy')
                print(np.shape(new_set)[0])
                global_set=np.append(global_set,new_set,axis=0)
                del new_set
    print(np.shape(global_set))
    np.random.seed(seed)
    np.random.shuffle(global_set)
    X_set=global_set[:,0:n_feat]
    Y_set=global_set[:,n_feat]
    Y_set=tf.keras.utils.to_categorical(Y_set)
    del global_set
    return X_set,Y_set



###############################################################################################################################"
#####
##### Functions for performance evaluation
#
def mean_and_std_accuracy_over_cross_experiments(confusion_matrices):
    accs=np.zeros(np.shape(confusion_matrices)[0])
    for i in range (len(accs)):
        accs[i]=accuracy(confusion_matrices[i])
    mean_acc=np.mean(accs)
    std_acc=np.std(accs)
    return mean_acc,std_acc

def performances_scores_over_cross_experiments(confusion_matrices):
    accs=np.zeros(np.shape(confusion_matrices)[0])
    precs=np.zeros((np.shape(confusion_matrices)[0],5))
    recs=np.zeros((np.shape(confusion_matrices)[0],5))
    f1ss=np.zeros((np.shape(confusion_matrices)[0],5))
    for i in range (len(accs)):
        accs[i]=accuracy(confusion_matrices[i])
        precs[i]=precisions(confusion_matrices[i])
        recs[i]=recalls(confusion_matrices[i])
        f1ss[i]=f1s(confusion_matrices[i])
    mean_acc=np.mean(accs)
    mean_precs=np.mean(precs,axis=0)
    mean_precs=np.mean(precs,axis=0)
    mean_recs=np.mean(recs,axis=0)
    mean_f1s=np.mean(f1ss,axis=0)
    results=np.zeros(16)
    results[0]=mean_acc
    for clas in range(5):
        results[clas*3+1]=mean_f1s[clas]
        results[clas*3+2]=mean_precs[clas]
        results[clas*3+3]=mean_recs[clas]
    return results



def accuracy(confusion_matrix):
    return np.sum(np.sum(np.diagonal(confusion_matrix)))/np.sum(np.sum(confusion_matrix))

        
def precisions(confusion_matrix):
    return np.diagonal(confusion_matrix)/np.sum(confusion_matrix,1)
        
def recalls(confusion_matrix):
    return np.diagonal(confusion_matrix)/np.sum(confusion_matrix,0)
        
def f1s(confusion_matrix):
    prec=precisions(confusion_matrix)
    rec=recalls(confusion_matrix)
    return (2*rec*prec/(rec+prec))



def wash_screen():
    for i in range(20):
        print('')







###############################################################################################################################"
#####
##### Functions for cross_validation experiment settings and hyperparameter configurations
#
def parse_arguments(config):
    n_batch=int(config[0])
    print('n_batch='+str(n_batch))
    learning_rate=config[1]
    print('learning_rate='+str(learning_rate))
    n_layers=int(config[2])
    print('n_layers='+str(n_layers))
    layers_power=int(config[3])
    print('layers_power='+str(layers_power))

    dropout_rate=config[4]
    print('dropout_rate='+str(dropout_rate))
    weight_constraint=int(config[5])
    print('weight_constraint='+str(weight_constraint))
    n_augmentation=int(config[6])
    sigma_power=int(config[7])



    configs_nn=np.asarray([
                [[10],
                [50],
                [200]],

                [[200,20],
                [100,35],
                [200,50]],

                [[200,60,20],
                [350,80,20],
                [500,100,20]],

                [[500,200,60,15],
                [750,350,80,17],
                [1000,500,100,20]],

                [[500,200,200,60,15],
                [750,350,200,60,15],
                [1000,500,200,60,15]],

                [[500,300,200,100,60,15],
                [750,400,250,120,60,15],
                [1000,500,300,150,60,15]],

                [[500,300, 200,100,60,30,15],
                [700,450,200,150,70,45,17],
                [1000,600,400,200,100,60,20]]

                ])
    
    layers_sizes=configs_nn[n_layers,layers_power]
    return {"Batch_size" : n_batch,"Learning_rate" : learning_rate,"Network_layers_configuration" : layers_sizes,
            "Dropout_rate" : dropout_rate,  "Weight_constraint" : weight_constraint,
            "N_augmentation" : n_augmentation, "Sigma_power" : sigma_power}


def param_names(index):
    legends=['Batch_size','Learning_rate','Nb_layers','Decreasing_layers','Dropout_rate','Weight_constraint','N_augmentation','Sigma_power']
    return legends[index]

def cross_configurations(cross_mode):
    n_ceps=12
    if(cross_mode==0):
        n_test=1
        test_specimens=np.zeros((1,12))
        test_specimens[0,0]=1 
        test_specimens[0,1]=1 

    if(cross_mode==1):
        n_test=6
        test_specimens=np.zeros((6,12))
        for i in range(6):
            test_specimens[i,i*2]=1
            test_specimens[i,i*2+1]=1 

    if(cross_mode==2):
        n_test=66
        test_specimens=np.zeros((66,12))
        incr=-1
        for c1 in range(12):
            for c2 in range(12):
                if(c2>c1):
                    incr=incr+1
                    test_specimens[incr,c1]=1
                    test_specimens[incr,c2]=1 
                
    if(cross_mode==3):
        #01 27 36 4-10 5-11 89        04   1-11  2-10  56  38  79
        n_test=12
        test_specimens=np.zeros((12,12))
        test_specimens=[
                [ 1, 1, 0,     0, 0, 0,     0, 0, 0,     0, 0, 0],
                [ 0, 0, 1,     0, 0, 0,     0, 1, 0,     0, 0, 0],
                [ 0, 0, 0,     1, 0, 0,     1, 0, 0,     0, 0, 0],
                [ 0, 0, 0,     0, 1, 0,     0, 0, 0,     0, 1, 0],
                [ 0, 0, 0,     0, 0, 1,     0, 0, 0,     0, 0, 1],
                [ 0, 0, 0,     0, 0, 0,     0, 0, 1,     1, 0, 0],
                [ 1, 0, 0,     1, 0, 0,     0, 0, 0,     0, 0, 0],
                [ 0, 1, 0,     0, 0, 0,     0, 0, 0,     0, 0, 1],
                [ 0, 0, 1,     0, 0, 0,     0, 0, 0,     0, 1, 0],
                [ 0, 0, 0,     0, 0, 1,     1, 0, 0,     0, 0, 0],
                [ 0, 0, 0,     0, 1, 0,     0, 0, 1,     0, 0, 0],
                [ 0, 0, 0,     0, 0, 0,     0, 1, 0,     1, 0, 0],
                ]
        test_specimens=np.array(test_specimens)
        test_specimens=test_specimens.astype(int)
    training_specimens=1-test_specimens
    training_specimens=training_specimens.astype(int)
    test_specimens=test_specimens.astype(int)
    return n_test,training_specimens,test_specimens


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
        configs=np.zeros((nb_new_configs,n_param))
        for config in range(nb_new_configs):
            print()
            val=config
            for param in range(n_param):
                values=np.asarray(vars[n_param-1-param])
                configs[config,n_param-1-param]=values[(val//multiples[n_param-1-param])]
                val=val%multiples[n_param-1-param]
        configs=np.array(configs)
        print (configs)
        
        return configs
        


def build_test_configurations():
#    [512,768,1024],
 #   [0.000125,0.00015,0.000175],
    #0 : batch       1 : LR       2 : nlays      3 : decLay   4 : dropout  5: max_weight  6 : n_augmentation  7 : Sigma_power
    vars=[
    [768],
    [0.00015],
    [5,4],
    [2],
    [0.2,0.25,0.3],
    [6],
    [0],
    [0]
    ]

    return build_configs(0,vars,0) #return all possible configurations of hyperparameters


