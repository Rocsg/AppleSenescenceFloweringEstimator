#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 21 16:34:19 2019

@author: fernandr
"""
tab_acc_vs_epoch_some,tab_val_acc_vs_epoch_some,tab_mean_std_ending_some,tab_std_between_repet_some,tab_growing_some,configs_some=do_some()

test_version='4_b'
tab_acc_vs_epoch,tab_val_acc_vs_epoch,tab_mean_std_ending,tab_std_between_repet,tab_growing,configs=do_it()
np.save('/home/fernandr/Bureau/tab_acc_vs_epoch_v'+test_version+'.npy',tab_acc_vs_epoch)
np.save('/home/fernandr/Bureau/tab_val_acc_vs_epoch_v'+test_version+'.npy',tab_val_acc_vs_epoch)
np.save('/home/fernandr/Bureau/tab_mean_std_ending_v'+test_version+'.npy',tab_mean_std_ending)
np.save('/home/fernandr/Bureau/tab_std_between_repet_v'+test_version+'.npy',tab_std_between_repet)
np.save('/home/fernandr/Bureau/tab_growing_v'+test_version+'.npy',tab_growing)
np.save('/home/fernandr/Bureau/configs_v'+test_version+'.npy',configs)

import matplotlib.pyplot as plt
import numpy as np
import seaborn

test_version='_v4_a'
test_version2='_v4_b'
tab_acc_vs_epoch0=100*np.load('/home/fernandr/Bureau/tab_acc_vs_epoch'+test_version+'.npy')
tab_val_acc_vs_epoch0=100*np.load('/home/fernandr/Bureau/tab_val_acc_vs_epoch'+test_version+'.npy')
tab_mean_std_ending0=100*np.load('/home/fernandr/Bureau/tab_mean_std_ending'+test_version+'.npy')
tab_std_between_repet0=100*np.load('/home/fernandr/Bureau/tab_std_between_repet'+test_version+'.npy')
tab_configs0=np.load('/home/fernandr/Bureau/configs'+test_version+'.npy')

tab_acc_vs_epoch=np.append(tab_acc_vs_epoch0,100*np.load('/home/fernandr/Bureau/tab_acc_vs_epoch'+test_version2+'.npy'),axis=0)
tab_val_acc_vs_epoch=np.append(tab_val_acc_vs_epoch0,100*np.load('/home/fernandr/Bureau/tab_val_acc_vs_epoch'+test_version2+'.npy'),axis=0)
tab_mean_std_ending=np.append(tab_mean_std_ending0,100*np.load('/home/fernandr/Bureau/tab_mean_std_ending'+test_version2+'.npy'),axis=0)
tab_std_between_repet=np.append(tab_std_between_repet0,100*np.load('/home/fernandr/Bureau/tab_std_between_repet'+test_version2+'.npy'),axis=0)
tab_configs=np.append(tab_configs0,np.load('/home/fernandr/Bureau/configs'+test_version2+'.npy'),0)




n_epochs=np.shape(tab_acc_vs_epoch)[1]
n_configs=np.shape(tab_acc_vs_epoch)[0]
n_params=np.shape(tab_configs)[1]
tab_means=np.mean(tab_val_acc_vs_epoch[:,n_epochs-20:n_epochs],1)
tab_growing=np.mean(tab_val_acc_vs_epoch[:,n_epochs-15:n_epochs-1],1)-np.mean(tab_val_acc_vs_epoch[:,n_epochs-29:n_epochs-15],1)
data=np.zeros((n_configs,n_params+6))
data[:,0:n_params]=tab_configs
data[:,n_params]=tab_means
data[:,n_params+1]=tab_acc_vs_epoch[:,n_epochs-1]
data[:,n_params+2]=tab_mean_std_ending #Oscillations
data[:,n_params+3]=tab_std_between_repet #Repetability
data[:,n_params+4]=tab_means-tab_acc_vs_epoch[:,n_epochs-1] #Overfitting
data[:,n_params+5]=tab_growing #Progression still possible
    
strings=['' for i in range(n_configs)]
for i in range(n_configs):
    string='Conf '+str(i)+' |Bat='+str(int(tab_configs[i,0]))
    string=string+'|lr='+str(tab_configs[i,2])
    string=string+'|Nlay='+str(int(tab_configs[i,4]))
    string=string+'|PowL='+str(tab_configs[i,5])
    string=string+'|Drop='+str(tab_configs[i,6])
    string=string+'|MaxV='+str(tab_configs[i,7])
    string=string+'|Normd='+str(tab_configs[i,8])+'|'
    string=string+'|opt='+str(tab_configs[i,9])+'|'
    strings[i]=string

#View correlation matrix between various parameters and output    
corr_mat=np.corrcoef(data.T)
seaborn.heatmap(corr_mat,cmap='RdYlGn_r', vmax=1.0, vmin=-1.0)
print('0 = Batch')
print('1 = Glorot')
print('2 = Learning rate')
print('3 = Activation')
print('4 = N layers')
print('5 = Pow layers')
print('6 = Dropout')
print('7 = Max weight')
print('8 = Normalisation mode')
print('9 = Optimizer (adam or nadam)')
print('10 = Means val_acc')
print('11= Means acc')
print('12 = Std Oscillation')
print('13 = Std Repetitions')
print('14 = Mean acc - mean val_acc')
print('15 = Growing over 15 last epochs')


#View point cloud of values of a parameter along the value of a parameter    
focus=3
index_param_view=0 # 0 =batch  2=lr  4=nlayers 5=powlayers  6=dropout 7=maxweight 8=normalisation 
min=np.min(data[:,index_param_view])
max=np.max(data[:,index_param_view])
dminmax=max-min
plt.figure()
plt.xlim([min-dminmax/10,max+dminmax/10])
if(focus==0):
    plt.ylim([60.0,100])
if(focus==1):
    plt.ylim([80.0,95])
if(focus==2):
    plt.ylim([90.0,94])
if(focus==3):
    plt.ylim([92,93.5])
#plt.scatter(data[:,index_param_view],data[:,n_params],c='coral',s=50*(np.abs(data[:,n_params+2])+np.abs(data[:,n_params+3])))
plt.scatter(data[:,index_param_view],data[:,n_params],c='coral')
#plt.scatter(data[:,index_param_view],data[:,n_params+1],c='lightblue')
plt.plot([min-dminmax/10,max+dminmax/10],[92,92])
plt.plot([min-dminmax/10,max+dminmax/10],[90,90])
plt.plot([min-dminmax/10,max+dminmax/10],[94,94])
plt.plot([min-dminmax/10,max+dminmax/10],[93,93])
vals=np.unique(data[:,index_param_view])
for val in vals:
    index_confs_inside=list(filter(lambda i: data[i,index_param_view]==val, range(n_configs)))    
    values_inside=data[index_confs_inside,n_params]
    plt.boxplot(values_inside,positions=[val],widths=dminmax/20)
    print('for '+str(val))
    print(index_confs_inside)
    print(values_inside)






    
#View all of a value of a parameter    
focus=2
plt.figure()
index_param_view=0 # 0 =batch  2=lr  4=nlayers 5=powlayers  6=dropout 7=maxweight 8=normalisation 
val_param_view= 512
sequence_view = list(filter(lambda i: data[i,index_param_view]==val_param_view, range(n_configs)))    

#sequence_view=list(filter(lambda i : ((data[i,14] > 0.1) & (data[i,9] > 91)), range(n_configs)))
legends=['' for i in range(len(sequence_view)+1)]
for i in range(len(sequence_view)):
    index=sequence_view[i]
    plt.plot(tab_val_acc_vs_epoch[index])
    legends[i]=strings[index]
    plt.title('Model accuracy')
    plt.ylabel('Accuracy')
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
plt.plot([0,n_epochs],[92,92])
plt.plot([0,n_epochs],[91,91])
plt.plot([0,n_epochs],[93,93])
legends[len(legends)-1]="Opti tree"
plt.legend(legends)
plt.show()











