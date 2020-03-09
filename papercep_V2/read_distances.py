#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 15:08:39 2019

@author: fernandr
"""
import numpy as np
import matplotlib.pyplot as plt





def read_data_out(spec):
    print('Reading '+spec)
    repSource='/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_7_FIBERS/'+spec
    fi1=np.loadtxt(repSource+'/nBranches.txt')
    print(fi1)
    nBr=int(fi1)
    nBri=np.zeros(nBr)
    nBri=nBri.astype(int)
    nMax=0
    print('Nbranches='+str(nBr))
    for br in range(nBr):
        fi1=np.loadtxt(repSource+'/nBranches_nb_'+str(br)+'.txt')
        nBri[br]=int(fi1)
        for pa in range(nBri[br]):
            fi1=np.loadtxt(repSource+'/dataOut_'+str(br)+'_'+str(pa)+'.txt')
            if( (np.shape(fi1)[1])>nMax):
                nMax=np.shape(fi1)[1]
    
    maxnBri=np.max(nBri)
    dataOut=np.zeros((nBr,maxnBri,3,nMax))    
    for br in range(nBr):
        fi1=np.loadtxt(repSource+'/nBranches_nb_'+str(br)+'.txt')
        nBri[br]=int(fi1)
        for pa in range(nBri[br]):
            fi1=np.loadtxt(repSource+'/dataOut_'+str(br)+'_'+str(pa)+'.txt')
            n=np.shape(fi1)[1]
            dataOut[br,pa,:,0:n]=np.copy(fi1)
    return dataOut

def plot_specimen(spec):
    data=read_data_out(spec)
    my_dpi=100
    plt.figure(figsize=(750/my_dpi, 500/my_dpi), dpi=my_dpi) 
    plt.ylim(0,50)
    t=np.arange(0,len(data[0,0,0]),1)
    colors=np.zeros((3,4))
    colors=colors.astype(str)
    colors=[
            ['#991111', '#BB1111', '#DD1111', '#FF1111'],
            ['#119911', '#11BB11', '#11DD11', '#11FF11'],
            ['#111199', '#1111BB', '#1111DD', '#1111FF'],
    ]
    plt.xlabel('Path from rootstock to branches')
    plt.ylabel("Distance to Necrose (mm)")
    mean_irm=np.mean(data[:,0,0,:],axis=0)
    mean_necr=np.mean(data[:,0,1,:],axis=0)
    mean_amad=np.mean(data[:,0,2,:],axis=0)
    print(np.shape(mean_irm))
#    plt.plot(t,mean_irm,color=colors[0][0])
    plt.plot(t,mean_necr,color=colors[1][0])
    plt.plot(t,mean_amad,color=colors[2][0])
    for nBr in range(np.shape(data)[0]):
        val_irm=data[nBr,0,0,:]
        val_necr=data[nBr,0,1,:]
        val_amad=data[nBr,0,2,:]
#        plt.plot(t,val_irm,color=colors[0][nBr+1]) 
        plt.plot(t,val_necr,color=colors[1][nBr+1]) 
        plt.plot(t,val_amad,color=colors[2][nBr+1]) 
    plt.title(spec)
                
def plot_specimens():
    spec='CEP011_AS1'
    data=read_data_out(spec)
    my_dpi=80
    plt.figure(figsize=(750/my_dpi, 500/my_dpi), dpi=my_dpi) 
    plt.ylim(-50,50)
    t=np.arange(-20, 5, 25/len(data[0,0,0]))
    colors=np.zeros((3,4))
    colors=colors.astype(str)
    colors=[
            ['#991111', '#BB1111', '#DD1111', '#FF1111'],
            ['#119911', '#11BB11', '#11DD11', '#11FF11'],
            ['#111199', '#1111BB', '#1111DD', '#1111FF'],
    ]
    plt.xlabel('Path from rootstock to branches')
    plt.ylabel("Distance to Necrose (mm)")
    mean_irm=np.mean(data[:,0,0,:],axis=0)
    mean_necr=np.mean(data[:,0,1,:],axis=0)
    mean_amad=np.mean(data[:,0,2,:],axis=0)
    print(np.shape(mean_irm))
#    plt.plot(t,mean_irm,color=colors[0][0])
    plt.plot(t,mean_necr,color=colors[1][0])
    plt.plot(t,mean_amad,color=colors[2][0])
    for nBr in range(np.shape(data)[0]):
        val_irm=data[nBr,0,0,:]
        val_necr=data[nBr,0,1,:]
        val_amad=data[nBr,0,2,:]
#        plt.plot(t,val_irm,color=colors[0][nBr+1]) 
        plt.plot(t,val_necr,color=colors[1][nBr+1]) 
        plt.plot(t,val_amad,color=colors[2][nBr+1]) 
    plt.title(spec)
    
                    
def plot_categories():
    specimens=['CEP011_AS1','CEP012_AS2','CEP013_AS3',   'CEP014_RES1','CEP015_RES2','CEP016_RES3',  'CEP017_S1','CEP018_S2','CEP019_S3',  'CEP020_APO1','CEP021_APO2','CEP022_APO3']
    cats=['AS','RES','S','APO']
    txt=['to necrose','to amadou']
    indmax=400
    colors=np.zeros(8)
    colors=colors.astype(str)
    colors=['#238c00' , '#51f500',         '#1111AA' , '#4444FF' ,         '#ad4eaf' , '#f34efa' ,          '#bb0e0e' , '#fb0e0e']
    my_dpi=80
    plt.figure(figsize=(750/my_dpi, 500/my_dpi), dpi=my_dpi) 
    ax=plt.subplot(1,1,1)
    plt.ylim(0,30)
    plt.xlabel('Path from rootstock to branches')
    plt.ylabel("Distance to Necrose (mm)")
    plt.title('Distance to necrose, mean over categories (mm)')
    for cat in range(4):
        data=np.zeros((3,indmax))
        incr=0
        for sp in range(3):
            index=cat*3+sp
            data0=read_data_out(specimens[index])
            mxsp=len(data0[0,0,0])
            data[0,0:mxsp]= data[0,0:mxsp]+0.25*np.mean(data0[:,0,0,:],axis=0)
            data[1,0:mxsp]= data[1,0:mxsp]+0.25*np.mean(data0[:,0,1,:],axis=0)
            data[2,0:mxsp]= data[2,0:mxsp]+0.25*np.mean(data0[:,0,2,:],axis=0)
        t=np.arange(-20, 5, 25/indmax)
#    plt.plot(t,mean_irm,color=colors[0][0])
        tt=cats[cat]+' '+txt[0]
        plt.plot(t,data[1],color=colors[2*cat+0],label=tt)
    ax.legend(fontsize=11,loc=(0.7,0.8))


    plt.figure(figsize=(750/my_dpi, 500/my_dpi), dpi=my_dpi) 
    ax=plt.subplot(1,1,1)
    plt.ylim(0,80)
    plt.xlabel('Path from rootstock to branches')
    plt.ylabel("Distance to Amadou (mm)")
    plt.title('Distance to amadou, mean over categories (mm)')
    for cat in range(4):
        data=np.zeros((3,indmax))
        incr=0
        for sp in range(3):
            index=cat*3+sp
            data0=read_data_out(specimens[index])
            mxsp=len(data0[0,0,0])
            data[0,0:mxsp]= data[0,0:mxsp]+0.25*np.mean(data0[:,0,0,:],axis=0)
            data[1,0:mxsp]= data[1,0:mxsp]+0.25*np.mean(data0[:,0,1,:],axis=0)
            data[2,0:mxsp]= data[2,0:mxsp]+0.25*np.mean(data0[:,0,2,:],axis=0)
        t=np.arange(-20, 5, 25/indmax)
#    plt.plot(t,mean_irm,color=colors[0][0])
        tt=cats[cat]+' '+txt[1]
        plt.plot(t,data[2],color=colors[2*cat+1],label=tt)
    ax.legend(fontsize=11,loc=(0.7,0.8))
    

specimens=['CEP011_AS1','CEP012_AS2','CEP013_AS3',   'CEP014_RES1','CEP015_RES2','CEP016_RES3',  'CEP017_S1','CEP018_S2','CEP019_S3',  'CEP020_APO1','CEP021_APO2','CEP022_APO3']
plt.close('all')
#for spec in specimens:
index=0
spec=specimens[index]
print('Processing '+spec)
plot_specimen(spec)    

plot_categories()
    