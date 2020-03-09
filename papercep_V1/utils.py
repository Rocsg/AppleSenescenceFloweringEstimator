#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Oct 15 18:06:11 2019

@author: fernandr
"""
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from math import pi
from scipy import *
from matplotlib.patches import Rectangle
 


def compute_red_tab():
    exp='RESULTS_V3__1-128_SYMPTFEAT_14__NTREE_250__KIND_5_CL/1-128_SYMPTFEAT_14__NTREE_250__KIND_5_CL__'
    confusions=np.zeros((4,5,5))
    globAcc=np.zeros((4))
    accuracies=np.zeros((4,5))
    precisions=np.zeros((4,5))
    recalls=np.zeros((4,5))
    fscores=np.zeros((4,5))
    for i in range(4):
        confusions[i]=read_confusion_mat_from_full_text(exp,i,i)
        globAcc[i]=accuracy(confusions[i,:,:])
        for cl in range(5):
            accuracies[i,cl]=accuracy_class(confusions[i,:,:],cl)
            precisions[i,cl]=precision_class(confusions[i,:,:],cl)
            recalls[i,cl]=recall_class(confusions[i,:,:],cl)
            fscores[i,cl]=harmonic_mean(precisions[i,cl],recalls[i,cl])

    valsGlob=np.zeros((4,21))
    valsGlob[:,0]=globAcc
    for cl in range(5):
        valsGlob[:,1+4*cl]=accuracies[:,cl]    
        valsGlob[:,2+4*cl]=precisions[:,cl]
        valsGlob[:,3+4*cl]=recalls[:,cl]
        valsGlob[:,4+4*cl]=harmonic_mean(valsGlob[:,2+4*cl],valsGlob[:,3+4*cl])

    valsGlob2=np.zeros((6,21))
    valsGlob2[0:4,:]=valsGlob
    valsGlob2[4:6,:]=stats_vect(valsGlob)
    write_vals_tab2d_in_file_with_percent( valsGlob2,'/home/fernandr/Bureau/Tabs/tab_red.txt')






def compute_brown_tab():
    brown_ret=np.zeros((16,2,21))
    for sb in range(16):
        sub=sb+1
        brown_ret[sb,:,:]=compute_purple_tab('EXP_5_RESOLUTIONS/SUB_'+str(sub)+'/')
    write_vals_tab2d_in_file_with_percent( tab3d_to_tab2d(brown_ret),'/home/fernandr/Bureau/Tabs/tab_brown.txt')
    return brown_ret


def compute_yellow_tab():
    yellow_ret=np.zeros((16,2,21))
    yellow_vals=np.zeros((16,2,5))
    for rx in range(2):
        for t1 in range(2):
            for t2 in range(2):
                for dp in range(2):
                    config=str(rx)+str(t1)+str(t2)+str(dp)
                    config_num=rx*8+t1*4+t2*2+dp
                    yellow_ret[config_num,:,:]=compute_purple_tab(config)
    write_vals_tab2d_in_file_with_percent( tab3d_to_tab2d(yellow_ret),'/home/fernandr/Bureau/Tabs/tab_yellow.txt')
    yellow_vals[:,:,0]=yellow_ret[:,:,4]
    yellow_vals[:,:,1]=yellow_ret[:,:,8]
    yellow_vals[:,:,2]=yellow_ret[:,:,12]
    yellow_vals[:,:,3]=yellow_ret[:,:,16]
    yellow_vals[:,:,4]=yellow_ret[:,:,20]
    return yellow_vals


def compute_purple_tab(dir):     
     exp='/home/fernandr/Bureau/ML_CEP/RESULTS/'+dir
     if(exp_existe(exp)!=1):
         return np.zeros((2,21))
     print('ok')
     confusions=np.zeros((12,12,5,5))
     globAcc=np.zeros((12,12))
     accuracies=np.zeros((5,12,12))
     precisions=np.zeros((5,12,12))
     recalls=np.zeros((5,12,12))
     fscores=np.zeros((5,12,12))
     for i1 in range (12):
         for i2 in range (12):
             if(i2>i1):
                 confusions[i1,i2]=read_confusion_mat_from_full_text(exp,i1,i2)
                 globAcc[i1,i2]=accuracy(confusions[i1,i2,:,:])
                 confusions[i2,i1]=read_confusion_mat_from_full_text(exp,i1,i2)
                 globAcc[i2,i1]=accuracy(confusions[i1,i2,:,:])
                 for cl in range(5):
                     accuracies[cl,i1,i2]=accuracy_class(confusions[i1,i2,:,:],cl)
                     precisions[cl,i1,i2]=precision_class(confusions[i1,i2,:,:],cl)
                     recalls[cl,i1,i2]=recall_class(confusions[i1,i2,:,:],cl)
                     fscores[cl,i1,i2]=harmonic_mean(precisions[cl,i1,i2],recalls[cl,i1,i2])
                     accuracies[cl,i2,i1]=accuracy_class(confusions[i1,i2,:,:],cl)
                     precisions[cl,i2,i1]=precision_class(confusions[i1,i2,:,:],cl)
                     recalls[cl,i2,i1]=recall_class(confusions[i1,i2,:,:],cl)
                     fscores[cl,i2,i1]=harmonic_mean(precisions[cl,i1,i2],recalls[cl,i1,i2])
     vals_spec=np.zeros(12)
     for sp in range(12):
         vals_spec[sp]=np.mean(valeurs_line_no_diag(globAcc,sp))
     
     #Meilleur = S2
     max=7
     #Pire = RES2
     min=4

     valsGlob=np.zeros((21,2))
     valsMeilleur=np.zeros((21,2))
     valsPire=np.zeros((21,2))

     valsGlob[0]=stats(valeurs_no_diag(globAcc))
     valsMeilleur[0]=stats(valeurs_line_no_diag(globAcc,max))
     valsPire[0]=stats(valeurs_line_no_diag(globAcc,min))
    
     for cl in range(5):
         valsGlob[1+4*cl]=stats(valeurs_no_diag(accuracies[cl,:,:]))
         valsMeilleur[1+4*cl]=stats(valeurs_line_no_diag(accuracies[cl,:,:],max))
         valsPire[1+4*cl]=stats(valeurs_line_no_diag(accuracies[cl,:,:],min))
    
         valsGlob[2+4*cl]=stats(valeurs_no_diag(precisions[cl,:,:]))
         valsMeilleur[2+4*cl]=stats(valeurs_line_no_diag(precisions[cl,:,:],max))
         valsPire[2+4*cl]=stats(valeurs_line_no_diag(precisions[cl,:,:],min))
    
         valsGlob[3+4*cl]=stats(valeurs_no_diag(recalls[cl,:,:]))
         valsMeilleur[3+4*cl]=stats(valeurs_line_no_diag(recalls[cl,:,:],max))
         valsPire[3+4*cl]=stats(valeurs_line_no_diag(recalls[cl,:,:],min))
    
         valsGlob[4+4*cl]=harmonic_mean(valsGlob[2+4*cl],valsGlob[3+4*cl])
         valsMeilleur[4+4*cl]=harmonic_mean(valsMeilleur[2+4*cl],valsMeilleur[3+4*cl])
         valsPire[4+4*cl]=harmonic_mean(valsPire[2+4*cl],valsPire[3+4*cl])
    
     a=np.zeros((6,21))
     a[0,:]=valsGlob[:,0]
     a[1,:]=valsGlob[:,1]
     a[2,:]=valsPire[:,0]
     a[3,:]=valsPire[:,1]
     a[4,:]=valsMeilleur[:,0]
     a[5,:]=valsMeilleur[:,1]
     ta=dir.split("/")
     ta=ta[len(ta)-2]
     write_vals_tab2d_in_file_with_percent( a,'/home/fernandr/Bureau/Tabs/tab_purple_'+ta+'.txt')
     return a[0:2,:]




def tab3d_to_tab2d(tab3d):
    return np.reshape(tab3d,(np.shape(tab3d)[0]*np.shape(tab3d)[1],np.shape(tab3d)[2]))
    
def exp_existe(exp):
   
    try:
        with open(exp+'TWOFOLD_'+str(10)+'-'+str(11)+'__stats_test.txt'): return 1
    except IOError:
        return 0
    
def write_vals_tab2d_in_file_with_percent(tab,nomfich):
    st=''
    for x in range (np.shape(tab)[0]):
        for y in range (np.shape(tab)[1]):
            st=st+toPourcent(tab[x,y])+' '
        st=st+'\n'
    fichier = open(nomfich, "w")
    fichier.write(st)
    fichier.close()
    print('tab was written in '+nomfich)        

    
def stats(vals):
    ret=np.zeros(2)
    ret[0]=np.mean(vals)
    ret[1]=np.std(vals)
    return ret

def stats_vect(vals):
    ret=np.zeros((2,np.shape(vals)[1]))
    ret[0,:]=np.mean(vals,0)
    ret[1,:]=np.std(vals,0)
    return ret




def harmonic_mean(a,b):
    return (2*a*b/(a+b))

def toPourcent(ratio):
    return str((int(round(ratio*1000))/10))+' %W'
    
def read_confusion_mat_from_full_text(exp,spec1,spec2):    
    fichier=open(exp+'TWOFOLD_'+str(spec1)+'-'+str(spec2)+'__stats_test.txt')
    contents=fichier.read()
    l1=contents.split("\n")[1].split(" ")
    l2=contents.split("\n")[2].split(" ")
    l3=contents.split("\n")[3].split(" ")
    l4=contents.split("\n")[4].split(" ")
    l5=contents.split("\n")[5].split(" ")

    mat=np.zeros((5,5))
    mat[0,:]=(l1[1],l1[3],l1[5],l1[7],l1[9])
    mat[1,:]=(l2[1],l2[3],l2[5],l2[7],l2[9])
    mat[2,:]=(l3[1],l3[3],l3[5],l3[7],l3[9])
    mat[3,:]=(l4[1],l4[3],l4[5],l4[7],l4[9])
    mat[4,:]=(l5[1],l5[3],l5[5],l5[7],l5[9])
    return mat
    


def read_confusion_stats_from_full_text(exp,spec1,spec2):
    rep='/home/fernandr/Bureau/EX_CEDRIC/V3/RESULTS/'
    fichier=open(rep+exp+'_'+str(spec1)+'-'+str(spec2)+'__stats_test.txt')
    contents=fichier.read()
    prec=contents.split("\n")[6].split(" ")
    precisions=(prec[4],prec[6],prec[8],prec[10],prec[12])

    prec=contents.split("\n")[7].split(" ")
    recall=(prec[4],prec[6],prec[8],prec[10],prec[12])

    prec=contents.split("\n")[8].split(" ")
    accuracies=(prec[4],prec[6],prec[8],prec[10],prec[12])

    prec=contents.split("\n")[11].split("=")
    accuracy=(prec[1])



  
  



def afficher_experiences(exps):
    VminGlob=0.7
    VmaxGlob=0.9
    VminClas=0.75
    VmaxClas=0.92
    n_exp=len(exps)
    vals=np.zeros((n_exp,6))
    valsNo3=np.zeros((n_exp,6))
    valsNo4=np.zeros((n_exp,6))
    valsNo5=np.zeros((n_exp,6))
    fig, axes = plt.subplots(n_exp,6)
    for n in range(n_exp):
        exp=exps[n]
        summary=summary_accuracy_twofold(exp)
        vals[n,0]=mean_no_diag(summary)
        valsNo4[n,0]=mean_no_diag_no_i(summary,4)
        axes[n,0].imshow(summary,vmin=VminGlob,vmax=VmaxGlob)
        for i in range(5):
            summary=summary_accuracy_class_twofold(exp,i)
            vals[n,i+1]=mean_no_diag(summary)
            valsNo4[n,i+1]=mean_no_diag_no_i(summary,4)
            axes[n,1+i].imshow(summary,vmin=VminClas,vmax=VmaxClas)
    print('vals=')
    print(vals)
    print('valsNo4=')
    print(valsNo4)
    return fig



def valeurs_no_diag(mat):
    ret=np.ones(12*11)
    incr=0
    for spec1 in range(12):
        for spec2 in range(12):
            if(spec1!=spec2):
                ret[incr]=mat[spec1,spec2]
                incr=incr+1
    return ret
                
def valeurs_line_no_diag(mat,spec1):
    ret=np.ones(11)
    incr=0
    for spec2 in range(12):
        if(spec1!=spec2):
            ret[incr]=mat[spec1,spec2]
            incr=incr+1
    return ret              
                
                
def valeurs_column_no_diag(mat,spec1):
    ret=np.ones(11)
    incr=0
    for spec2 in range(12):
        if(spec1!=spec2):
            ret[incr]=mat[spec2,spec1]
            incr=incr+1
    return ret              

def mean_no_diag(summary):
    dims=summary.shape
    N_elems=dims[0]*(dims[1]-1)
    return (np.sum(summary)-np.trace(summary))/N_elems

def mean_no_diag_no_i(summary,i):
    dims=summary.shape
    N_elems=(dims[0])*(dims[1]-1)-(dims[0]*2-2)
    print ('elements :')
    print (N_elems)
    return (np.sum(summary)-np.trace(summary)-np.sum(summary[i,:])-np.sum(summary[:,i])+2*summary[i,i]  )  /N_elems


def summary_accuracy_twofold(exp):
    res_acc=np.zeros((12,12))
    for spec1 in range(12):
        for spec2 in range(12):
            if(spec1>=spec2):
                continue
            res_acc[spec1,spec2]=accuracy(read_confusion(exp,spec1,spec2))
            res_acc[spec2,spec1]=accuracy(read_confusion(exp,spec1,spec2))
            
    return res_acc




def summary_accuracy_class_twofold(exp,i):
    res_acc=np.zeros((12,12))
    for spec1 in range(12):
        for spec2 in range(12):
            if(spec1>=spec2):
                continue
            res_acc[spec1,spec2]=accuracy_class(read_confusion(exp,spec1,spec2),i)
            res_acc[spec2,spec1]=accuracy_class(read_confusion(exp,spec1,spec2),i)
            
    return res_acc



def read_confusion(exp,spec1,spec2):
    rep='/home/fernandr/Bureau/EX_CEDRIC/V3/RESULTS/'
    return np.loadtxt(rep+exp+'_'+str(spec1)+'-'+str(spec2)+'__stats_test.mat.python.txt')


def accuracy(confusion):
    su=np.sum(confusion)
    s=np.trace(confusion)
    return s/su

def accuracy_class(confusion,i):
    su=np.sum(confusion)
    li=np.sum(confusion[i,:])
    ci=np.sum(confusion[:,i])
    lici=confusion[i,i]
    return (su-li-ci+2*lici)/su

def precision_class(confusion,i):
    li=np.sum(confusion[i,:])
    lici=confusion[i,i]
    return (lici)/li


def recall_class(confusion,i):
    ci=np.sum(confusion[:,i])
    lici=confusion[i,i]
    return (lici)/ci








# Libraries
# Set data
df = pd.DataFrame({
'group': ['A','B','C','D'],
'var1': [38, 1.5, 30, 4],
'var2': [29, 10, 9, 34],
'var3': [8, 39, 23, 24],
'var4': [7, 31, 33, 14],
'var5': [28, 15, 32, 14]
})
 
# ------- PART 1: Define a function that do a plot for one line of the dataset!
 
def make_spider( data,min,max,classes,categories, titles, colors):
    print(categories)
    print(titles)
    NC = len(categories)
    NM = len(titles)
    print('NC='+str(NC))
    print('NM='+str(NM))
    alphas=(0.0,0,0,0.0)
    # What will be the angle of each axis in the plot? (we divide the plot / number of variable)
    angles = [n / float(NC) * 2 * pi for n in range(NC)]
    angles += angles[:1]
    vals=np.zeros((NM,NC+1))
    vals[:,0:NC]=data
    vals[:,NC]=data[:,0]
 
    # Initialise the spider plot
    ax = plt.subplot(1,1,1, polar=True)
 
    # If you want the first axis to be on top:
    ax.set_theta_offset(pi / 2)
    ax.set_theta_direction(-1)
 
    # Draw one axe per variable + add labels labels yet
    plt.xticks(angles[:-1], categories, color='black', size=6)
 
    # Draw ylabels
    ax.set_rlabel_position(0)
    plt.yticks([20,40,60,80,100], ["20","40","60","80","100"], color="black", size=5)
    plt.ylim(min,max)
 
    # Ind1
    for m in range(NM):
        print('traitement plot numero '+str(m)+' parmi '+str(NM))
        if(titles[m]!='No data used'):
            ax.plot(angles, vals[m,:], color=colors[m], linewidth=1, linestyle='solid',label=titles[m])
        #ax.fill(angles, vals[m,:], color=colors[m], alpha=alphas[m])
 
    # Add a title and legend
    ax.legend(fontsize=6,loc=(1.2,0.5))
    plt.title('Classification scores VS Imaging devices' , size=8, color='k', y=1.0)
   


def compute_spiders(config,valsYellow,min,max,classes):
    titles=('No data used','IrmPD only',  'IrmT2 only','IrmT2 and IrmPD',     'IrmT1 only','IrmT1 and IrmPD',    'IrmT1 and IrmT2', 'All but X-rays',
            'X-rays only','X-rays and IrmPD',  'X-rays and IrmT2','All but IrmT1',     'X-rays and IrmT1','All but IrmT2',    'All but IrmPD', 'All Irm and X-rays',)
    tit=()
    cols=('#d62728','#1f77b4','#8c564b','#2ca02c','#ff7f0e')
    my_dpi=200
    plt.figure(figsize=(1500/my_dpi, 800/my_dpi), dpi=my_dpi) 
    N_mods=5
    if(config==0):
        selected_mods=(8,4,2,1,15)
    if(config==1):
        selected_mods=(7,11,13,14,15)
    if(config==2):
        selected_mods=(7,8,0,0,15)
    if(config==99):
        selected_mods=(8,12,0,0,15)

    valuesMean=np.zeros((N_mods,5))
    valuesStd=np.zeros((N_mods,5))
    tit=(titles[selected_mods[0]] ,titles[selected_mods[1]] ,titles[selected_mods[2]],titles[selected_mods[3]],titles[selected_mods[4]]   )
    for m in range(N_mods):
        valuesMean[m]=valsYellow[selected_mods[m],0,:]*100
        valuesStd[m]=valsYellow[selected_mods[m],1,:]*100
        print(valuesMean[m])

    cat=('Background','Healthy wood','Deteriorated wood','Amadou','Bark')
    if(classes==4):
        cat=('Healthy wood','Deteriorated wood','Amadou','Bark')
        valuesMean=valuesMean[:,1:5]
        
    make_spider( valuesMean,min,max,classes,categories=cat, titles=tit ,colors=cols)



def compute_decreasing_plot_with_resolution(valsBrown):
    print(valsBrown)
#    cols=('#1f77b4','#8c564b','#2ca02c','#ff7f0e')
    titles=('Healthy wood','Deteriorated wood','Amadou','Bark')
    
    my_dpi=200
    plt.figure(figsize=(1350/my_dpi, 1000/my_dpi), dpi=my_dpi) 
    ax = plt.subplot(1,1,1)

    plt.ylim(0,100)
    plt.xlim(0,18)
    plt.xticks([1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16],
               ["1\n\nOriginal pixel size\n0.6 mm","2","3","4\n\nPixel size\n2.5 mm","5","6","7","8\n\nPixel size\n5 mm","9","10","11","12","13","14","15","16\n\nPixel size\n1 cm"],color="black", size=5) 
    plt.yticks([20,40,60,80,100], ["20","40","60","80","100"], color="black", size=5)

    #Draw horizontal lines
    for i in range(4):
        plt.plot([0,17], [20*(i+1),20*(i+1)], color='#cccccc',linewidth=0.6)

    #Draw Squares
    sizes=[1,2,4,8,16]
    ym=10
    fact_ech_X=0.06
    fact_ech_Y=fact_ech_X*8
    for i in range(5):
        xm=sizes[i]
        plt.plot([xm,xm], [0.7,ym-sizes[i]*fact_ech_Y-0.7], color='#333333',linewidth=0.6)
        if(i==0):
            ax.add_patch(Rectangle((xm-sizes[i]*fact_ech_X, ym-sizes[i]*fact_ech_Y), 
                               2*sizes[i]*fact_ech_X, 2*sizes[i]*fact_ech_Y,alpha=1,
                               facecolor='#dddddd',edgecolor='#333333',label='Pixel size'))      
        else:
            ax.add_patch(Rectangle((xm-sizes[i]*fact_ech_X, ym-sizes[i]*fact_ech_Y), 
                               2*sizes[i]*fact_ech_X, 2*sizes[i]*fact_ech_Y,alpha=1,
                               facecolor='#dddddd',edgecolor='#333333'))      
    t=np.arange(1, 17, 1)
    vals_healthy=valsBrown[:,0,8]*100
    vals_deter=valsBrown[:,0,12]*100
    vals_amad=valsBrown[:,0,16]*100
    vals_bark=valsBrown[:,0,20]*100
    plt.plot(t, vals_healthy, 'go',label=titles[0])
    plt.plot(t, vals_deter, 'rs', label=titles[1])
    plt.plot(t, vals_amad, 'b^',label=titles[2])
    plt.plot(t, vals_bark, 'kX',label=titles[3])

    ax.legend(fontsize=6)#    loc=(1.2,0.5)
    plt.title('Tissues classification scores VS images subsampling factor' , size=8, color='k', y=1.0)








