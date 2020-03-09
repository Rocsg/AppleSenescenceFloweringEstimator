#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec  6 15:08:39 2019

@author: fernandr
"""
import numpy as np
import matplotlib.pyplot as plt

def read_parameters():
    vox_max=800
    ray_max=60
    n_data=12
    specimens=['CEP011_AS1','CEP012_AS2','CEP013_AS3',  'CEP017_S1','CEP018_S2','CEP019_S3',  'CEP014_RES1','CEP015_RES2','CEP016_RES3',   'CEP020_APO1','CEP021_APO2','CEP022_APO3']
    categories=['AS','S','RES','APO']
    return vox_max,ray_max,n_data,specimens,categories



def prepare_bowl_and_sect():
    vox_max,ray_max,n_data,specimens,categories=read_parameters()
    for spec in specimens:
        repSource='/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_7_FIBERS/'+spec+'/Data_Fibers'
        fi1=np.loadtxt(repSource+'/N_BR.txt')
        print(fi1)
        nBr=int(fi1)
        nBri=np.zeros(nBr)
        nBri=nBri.astype(int)
        dataOut=np.zeros((nBr,vox_max,ray_max,n_data))    
        dataOut2=np.zeros((nBr,vox_max,ray_max,n_data))    
        for br in range(nBr):
            fi1=np.loadtxt(repSource+'/BR_'+str(br)+'PA_0_NPTS.txt')
            nBri[br]=int(fi1)
            for pt in range(nBri[br]):
                dataOut[br,pt]=np.loadtxt(repSource+'/valBowl_BR_'+str(br)+'__PA_0__PT_'+str(pt)+'.txt')
                dataOut2[br,pt]=np.loadtxt(repSource+'/valSect_BR_'+str(br)+'__PA_0__PT_'+str(pt)+'.txt')
        np.save(repSource+'/dataOut.npy',dataOut)
        np.save(repSource+'/dataOut2.npy',dataOut2)




def read_bowl_and_sect(spec,type):
    vox_max,ray_max,n_data,specimens,categories=read_parameters()
    repSource='/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_7_FIBERS/'+spec+'/Data_Fibers'
    if(type==0):
        return np.load(repSource+'/dataOut.npy')
    else:
        return np.load(repSource+'/dataOut2.npy')





def compute_limite_ray(index_spec,type,only_cond,stop_ratio):
    vox_max,ray_max,n_data,specimens,categories=read_parameters()
    spec=specimens[index_spec]
    data=read_bowl_and_sect(spec,type)
    n_br=np.shape(data)[0]
    limite_rays=np.zeros((n_br,vox_max))
    for br in range(n_br):
        for pt in range(vox_max):
            index=-1
            for rayMM in range(ray_max-2):
                rayM=rayMM+1
                diff_bad=data[br,pt,rayM+1,4]-data[br,pt,rayM,4] + data[br,pt,rayM+1,5]-data[br,pt,rayM,5]
                if(not only_cond):
                    diff_bad=diff_bad+data[br,pt,rayM+1,1]-data[br,pt,rayM,1] + data[br,pt,rayM+1,2]-data[br,pt,rayM,2]                
                diff_all=data[br,pt,rayM+1,3]-data[br,pt,rayM,3]
                if(not only_cond):
                    diff_bad+data[br,pt,rayM+1,0]-data[br,pt,rayM,0]
                if(index==-1):
                     if((diff_bad/diff_all) > stop_ratio):
                         index=rayM
            if(index==-1):
                index=ray_max
#            print('For pt='+str(pt)+' at the end, index='+str(index))
            limite_rays[br,pt]=index
            
    return limite_rays



def compute_limite_ray_cat(index_cat,type,only_cond,stop_ratio):
    vox_max,ray_max,n_data,specimens,categories=read_parameters()
    a0=compute_limite_ray(index_cat*3+0,type,only_cond,stop_ratio)
    a1=compute_limite_ray(index_cat*3+1,type,only_cond,stop_ratio)
    a2=compute_limite_ray(index_cat*3+2,type,only_cond,stop_ratio)
    n_lines=np.shape(a0)[0]+np.shape(a1)[0]+np.shape(a2)[0]
    tab_ret=np.zeros((n_lines,vox_max))
    tab_ret=np.concatenate((a0,a1))
    tab_ret=np.concatenate((tab_ret,a2))
    return tab_ret



def plot_limit_rays(type_disc,only_cond,stop_ratio):
    vox_max,ray_max,n_data,specimens,categories=read_parameters()
    colors=np.zeros((4,4))
    colors=colors.astype(str)
    colors=[
            ['#991111', '#BB1111', '#DD1111', '#FF1111'],
            ['#119911', '#11BB11', '#11DD11', '#11FF11'],
            ['#111199', '#1111BB', '#1111DD', '#1111FF'],
    ]
    alpha_sympt=[0.4,0.3,0.3,0.25]
    colors_cats=np.zeros((4))
    colors_cats=colors_cats.astype(str)
    colors_cats=['#238c00' ,          '#1111AA' ,         '#ad4eaf' ,        '#bb0e0e' ]
    my_dpi=100
    plt.close('all')
    plt.figure(figsize=(4*400/my_dpi, 3*300/my_dpi), dpi=my_dpi) 
    t=np.arange(0,vox_max,1)
    for index in range(12):
        pos_x=index//3
        pos_y=index%3
        ind_plot=4*pos_y+pos_x+1
        ax=plt.subplot(3,4,(ind_plot))
        spec=specimens[index]
        data=compute_limite_ray(index,type_disc,only_cond,stop_ratio)
    
        nBr=np.shape(data)[0]
        plt.ylim(0,70)
        plt.xlim(0,200)
        if(pos_y==2):
            plt.xlabel('Chebyshev distance from rootstock (mm)')
        else:
            plt.xlabel('')
        if(pos_x==0):
            plt.ylabel("healthy radius ")
        else:
            plt.ylabel(" ")
        mean_necr=np.mean(data[:,:],axis=0)
        st_necr=np.std(data[:,:],axis=0)
        plt.fill_between(t, mean_necr-st_necr,mean_necr+st_necr,color=colors[1][0], alpha=alpha_sympt[0])
        plt.plot(t,mean_necr,color=colors[1][0])
#        for nBr in range(np.shape(data)[0]):
#            val_necr=data[nBr,:,index_necr]
#           val_amad=data[nBr,:,index_amad]
            #plt.plot(t,val_necr,color=colors[1][nBr+1]) 
            #plt.plot(t,val_amad,color=colors[2][nBr+1]) 
        plt.title(spec+'__')
        plt.plot([200,200],[0,60],color='#AAAAAA')
        plt.plot([100,100],[0,60],color='#AAAAAA')
            
    
    my_dpi=100
    plt.figure(figsize=(800/my_dpi, 600/my_dpi), dpi=my_dpi) 
    ax=plt.subplot(1,1,1)
    for index in range(4):
        tab_ret=compute_limite_ray_cat(index,type_disc,only_cond,stop_ratio)
        mes=np.mean(tab_ret,axis=0)
        sts=np.std(tab_ret,axis=0)
        plt.ylim(0,70)
        plt.xlim(0,200)
        plt.xlabel('Chebyshev distance from rootstock (mm)')
        plt.ylabel("healthy radius")
        plt.fill_between(t, mes-sts, mes+sts,color=colors_cats[index], alpha=alpha_sympt[index])
        plt.plot(t,mes,color=colors_cats[index],label=categories[index])
        plt.title(categories[index]+'_Healthy radius_'+str(type))
    ax.legend(fontsize=11,loc=(0.7,0.8))
    plt.plot([200,200],[0,60],color='#AAAAAA')
    plt.plot([100,100],[0,60],color='#AAAAAA')
    

type_disc=0
only_cond=0
stop_ratio=0.66
plot_limit_rays(type_disc,only_cond,stop_ratio)
             
 
for sp in range(12):
    print(str(sp))
    a=compute_limite_ray(sp,1,1,0.1)
    print(np.min(a,axis=1))






def read_bowl_and_sect_mean_and_var_of_category(cat,type):
    vox_max,ray_max,n_data,specimens,categories=read_parameters()    
    data_agg=np.zeros((0,vox_max,ray_max,12))
    for sp in range(3):
        spec=specimens[cat*3+sp]
        data=read_bowl_and_sect(spec,type)
        data_agg=np.concatenate((data_agg,data))

    st=np.std(data_agg,axis=0)
    me=np.mean(data_agg,axis=0)
    st[np.isnan(st)] = 0
    return me,st



#def test_plot_2_by_categories():


def test_plot_1_all_specimens():
    plt.close('all')
    type=0
    val_r=59
    for index in range(12):
        spec=specimens[index]
        plot_amadou_death_star_specimen(spec,type,val_r)



def plot_amadou_death_star_categories(spec,type,r_val):
    dataOut=read_bowl_and_sect(spec,type)
    data=dataOut[:,:,r_val,:]
    if(type==0):
        y_max=200
    else:
        y_max=50

    nBr=np.shape(dataOut)[0]
    my_dpi=100
    plt.figure(figsize=(400/my_dpi, 300/my_dpi), dpi=my_dpi) 
    plt.ylim(0,y_max)
    plt.xlim(0,400)
    t=np.arange(0,len(data[0,:,0]),1)
    colors=np.zeros((3,4))
    colors=colors.astype(str)
    colors=[
            ['#991111', '#BB1111', '#DD1111', '#FF1111'],
            ['#119911', '#11BB11', '#11DD11', '#11FF11'],
            ['#111199', '#1111BB', '#1111DD', '#1111FF'],
    ]
    plt.xlabel('Influence factors')
    plt.ylabel("Distance to Necrose (mm)")
    mean_necr=np.mean(data[:,:,6],axis=0)
    mean_amad=np.mean(data[:,:,7],axis=0)
    print(np.shape(mean_necr))
    plt.plot(t,mean_necr,color=colors[1][0])
    plt.plot(t,mean_amad,color=colors[2][0])
    for nBr in range(np.shape(data)[0]):
        val_necr=data[nBr,:,6]
        val_amad=data[nBr,:,7]
        plt.plot(t,val_necr,color=colors[1][nBr+1]) 
        plt.plot(t,val_amad,color=colors[2][nBr+1]) 
    plt.title(spec+str(type)+'__'+str(r_val))




def plot_amadou_death_star_specimen_all(type,r_val,squared_law):
    vox_max,ray_max,n_data,specimens,categories=read_parameters()
    index_necr=9-squared_law*3
    index_amad=10-squared_law*3


    #Decroissance lineaire en distance, et mesure sur une boule
    if((squared_law==0) & (type==0)):
        y_max_necr=2000
        y_max_amad=500

    #Decroissance lineaire en distance, et mesure sur un disque
    if((squared_law==0) & (type==1)):
        y_max_necr=400
        y_max_amad=150

    #Decroissance quadratique en distance, et mesure sur une boule
    if((squared_law==1) & (type==0)):
        y_max_necr=200
        y_max_amad=50

    #Decroissance quadratique en distance, et mesure sur un disque
    if((squared_law==1) & (type==1)):
        y_max_necr=50
        y_max_amad=10


    colors=np.zeros((4,4))
    colors=colors.astype(str)
    colors=[
            ['#991111', '#BB1111', '#DD1111', '#FF1111'],
            ['#119911', '#11BB11', '#11DD11', '#11FF11'],
            ['#111199', '#1111BB', '#1111DD', '#1111FF'],
    ]
    alpha_sympt=[0.4,0.3,0.3,0.25]
    colors_cats=np.zeros((4))
    colors_cats=colors_cats.astype(str)
    colors_cats=['#238c00' ,          '#1111AA' ,         '#ad4eaf' ,        '#bb0e0e' ]

    my_dpi=100
    plt.close('all')
    plt.figure(figsize=(4*400/my_dpi, 3*300/my_dpi), dpi=my_dpi) 
    for index in range(12):
        pos_x=index//3
        pos_y=index%3
        ind_plot=4*pos_y+pos_x+1
        ax=plt.subplot(3,4,(ind_plot))
        spec=specimens[index]
        dataOut=read_bowl_and_sect(spec,type)
        data=dataOut[:,:,r_val,:]
    
        nBr=np.shape(dataOut)[0]
        plt.ylim(0,y_max_necr)
        plt.xlim(0,300)
        t=np.arange(0,len(data[0,:,0]),1)
        if(pos_y==2):
            plt.xlabel('Chebyshev distance from rootstock (mm)')
        else:
            plt.xlabel('')
        if(pos_x==0):
            plt.ylabel("Influence power ")
        else:
            plt.ylabel(" ")
        mean_necr=np.mean(data[:,:,index_necr],axis=0)
        mean_amad=np.mean(data[:,:,index_amad],axis=0)
        print(np.shape(mean_necr))
        plt.plot(t,mean_necr,color=colors[1][0])
        plt.plot(t,mean_amad,color=colors[2][0])
        for nBr in range(np.shape(data)[0]):
            val_necr=data[nBr,:,index_necr]
            val_amad=data[nBr,:,index_amad]
            #plt.plot(t,val_necr,color=colors[1][nBr+1]) 
            #plt.plot(t,val_amad,color=colors[2][nBr+1]) 
        plt.title(spec+str(type)+'__'+str(r_val))
        plt.plot([200,200],[0,y_max_necr],color='#AAAAAA')
        plt.plot([100,100],[0,y_max_necr],color='#AAAAAA')
            
    
    my_dpi=100
    plt.figure(figsize=(800/my_dpi, 600/my_dpi), dpi=my_dpi) 
    ax=plt.subplot(1,1,1)
    for index in range(4):
        means,stds=read_bowl_and_sect_mean_and_var_of_category(index,type)
        mes=means[:,r_val,index_necr]
        sts=stds[:,r_val,index_necr]
        plt.ylim(0,y_max_necr)
        plt.xlim(0,300)
        t=np.arange(0,len(data[0,:,0]),1)
        plt.xlabel('Chebyshev distance from rootstock (mm)')
        plt.ylabel("Mean influence power necrose")
        plt.fill_between(t, mes-sts, mes+sts,color=colors_cats[index], alpha=alpha_sympt[index])
        plt.plot(t,mes,color=colors_cats[index],label=categories[index])
        plt.title(categories[index]+'_NECROSE_INFLUENCE_'+str(type)+'__'+str(r_val))
    ax.legend(fontsize=11,loc=(0.7,0.8))
    plt.plot([200,200],[0,y_max_necr],color='#AAAAAA')
    plt.plot([100,100],[0,y_max_necr],color='#AAAAAA')
       
    my_dpi=100
    plt.figure(figsize=(800/my_dpi, 600/my_dpi), dpi=my_dpi) 
    for index in range(4):
        means,stds=read_bowl_and_sect_mean_and_var_of_category(index,type)
        mes=means[:,r_val,index_amad]
        sts=stds[:,r_val,index_amad]
        plt.ylim(0,y_max_amad)
        plt.xlim(0,300)
        t=np.arange(0,len(data[0,:,0]),1)
        plt.xlabel('Chebyshev distance from rootstock (mm)')
        plt.ylabel("Mean influence power amadou")
        plt.fill_between(t, mes-sts, mes+sts,color=colors_cats[index], alpha=alpha_sympt[index])
        plt.plot(t,mes,color=colors_cats[index],label=categories[index])
        plt.title(categories[index]+'_AMADOU_INFLUENCE_'+str(type)+'__'+str(r_val))
    ax.legend(fontsize=11,loc=(0.7,0.8))
    plt.plot([200,200],[0,y_max_amad],color='#AAAAAA')
    plt.plot([100,100],[0,y_max_amad],color='#AAAAAA')
           
#1 0 59 makes beatiful thing             
quadratic=1
disc_shape=0
ray_ref=39
plot_amadou_death_star_specimen_all(disc_shape,ray_ref,quadratic)



















def plot_amadou_la_force_specimen_all(type,r_val,only_cond,make_sum):
    plt.close(('all'))
    vox_max,ray_max,n_data,specimens,categories=read_parameters()


    #Decroissance lineaire en distance, et mesure sur une boule
    if((only_cond==0) & (type==0)):
        y_max_necr=3*r_val*r_val*r_val*(1+2*make_sum)
        y_max_sane=3*r_val*r_val*r_val*(1+2*make_sum)

    #Decroissance lineaire en distance, et mesure sur un disque
    if((only_cond==0) & (type==1)):
        y_max_necr=10*r_val*r_val*(1+2*make_sum)
        y_max_sane=10*r_val*r_val*(1+2*make_sum)

    #Decroissance quadratique en distance, et mesure sur une boule
    if((only_cond==1) & (type==0)):
        y_max_necr=20*r_val*r_val*(1+2*make_sum)
        y_max_sane=20*r_val*r_val*(1+2*make_sum)

    #Decroissance quadratique en distance, et mesure sur un disque
    if((only_cond==1) & (type==1)):
        y_max_necr=50*r_val*(1+2*make_sum)
        y_max_sane=50*r_val*(1+2*make_sum)


    colors=np.zeros((4,4))
    colors=colors.astype(str)
    colors=[
            ['#991111', '#BB1111', '#DD1111', '#FF1111'],
            ['#119911', '#11BB11', '#11DD11', '#11FF11'],
            ['#111199', '#1111BB', '#1111DD', '#1111FF'],
    ]
    alpha_sympt=[0.4,0.3,0.3,0.25]
    colors_cats=np.zeros((4))
    colors_cats=colors_cats.astype(str)
    colors_cats=['#238c00' ,          '#1111AA' ,         '#ad4eaf' ,        '#bb0e0e' ]

    my_dpi=100
    plt.close('all')
    plt.figure(figsize=(4*400/my_dpi, 3*300/my_dpi), dpi=my_dpi) 
    for index in range(12):
        pos_x=index//3
        pos_y=index%3
        ind_plot=4*pos_y+pos_x+1
        ax=plt.subplot(3,4,(ind_plot))
        spec=specimens[index]
        dataOut=read_bowl_and_sect(spec,type)
        data=dataOut[:,:,r_val,:]
        if(only_cond):
            dataSane=data[:,:,3]
            dataNecr=data[:,:,4]
        else:
            dataSane=data[:,:,3]+data[:,:,0]
            dataNecr=data[:,:,4]+data[:,:,1]
    
        nBr=np.shape(dataSane)[0]
        print(np.shape(dataSane))
        plt.ylim(0,y_max_sane)
        plt.xlim(0,200)
        t=np.arange(0,len(data[0,:,0]),1)
        if(pos_y==2):
            plt.xlabel('Chebyshev distance from rootstock (mm)')
        else:
            plt.xlabel('')
        if(pos_x==0):
            plt.ylabel("Surfaces ")
        else:
            plt.ylabel(" ")
        
        if(make_sum==0):
            mean_necr=np.mean(dataNecr[:,:],axis=0)
            mean_sane=np.mean(dataSane[:,:],axis=0)
        else:
            mean_necr=np.sum(dataNecr[:,:],axis=0)
            mean_sane=np.sum(dataSane[:,:],axis=0)
        print(np.shape(mean_necr))
        plt.plot(t,mean_necr,color=colors[1][0],label='mean necr')
        plt.plot(t,mean_sane,color=colors[2][0],label='mean sane')
        for nBr in range(np.shape(data)[0]):
            val_necr=dataSane[nBr,:]
            val_amad=dataNecr[nBr,:]
           # plt.plot(t,val_necr,color=colors[1][nBr+1],label='necr') 
           # plt.plot(t,val_amad,color=colors[2][nBr+1],label='sane') 
        plt.title(spec+str(type)+'__'+str(r_val))
        plt.plot([200,200],[0,y_max_necr],color='#AAAAAA')
        plt.plot([100,100],[0,y_max_necr],color='#AAAAAA')
            
type=1
only_cond=1 
r_val=15
make_sum=1
plot_amadou_la_force_specimen_all(type,r_val,only_cond,make_sum) 
           

























def plot_amadou_death_star_specimen(spec,type,r_val):
    dataOut=read_bowl_and_sect(spec,type)
    data=dataOut[:,:,r_val,:]
    if(type==0):
        y_max=200
    else:
        y_max=50
    nBr=np.shape(dataOut)[0]
    my_dpi=100
    plt.figure(figsize=(400/my_dpi, 300/my_dpi), dpi=my_dpi) 
    plt.ylim(0,y_max)
    t=np.arange(0,len(data[0,:,0]),1)
    colors=np.zeros((3,4))
    colors=colors.astype(str)
    colors=[
            ['#991111', '#BB1111', '#DD1111', '#FF1111'],
            ['#119911', '#11BB11', '#11DD11', '#11FF11'],
            ['#111199', '#1111BB', '#1111DD', '#1111FF'],
    ]
    plt.xlabel('Influence factors')
    plt.ylabel("Distance to Necrose (mm)")
    mean_necr=np.mean(data[:,:,6],axis=0)
    mean_amad=np.mean(data[:,:,7],axis=0)
    print(np.shape(mean_necr))
    plt.plot(t,mean_necr,color=colors[1][0])
    plt.plot(t,mean_amad,color=colors[2][0])
    for nBr in range(np.shape(data)[0]):
        val_necr=data[nBr,:,6]
        val_amad=data[nBr,:,7]
        plt.plot(t,val_necr,color=colors[1][nBr+1]) 
        plt.plot(t,val_amad,color=colors[2][nBr+1]) 
    plt.title(spec+'_'+str(type)+'__'+str(r_val))





    
           
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
    