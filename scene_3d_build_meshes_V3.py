#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 18:09:56 2019

@author: fernandr
"""
from scene_3d_helper_functions import *
nb_interp=120
day_max=3
version =3
interp_step=20

source_rep=get_source_rep()
x_end,y_end,z_end,z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_y,size_z=get_image_constants()
window_width,window_height=1200, 896
framerate,timestep=40,0
type=0  #test
#type=1  #movie building


for day_i in range(day_max):
    day_i_plus=day_i+1
    for inter in range(nb_interp):
        print('Building meshes for time '+str(day_i)+'_'+str(inter))
        if inter%interp_step!=0:
            continue
        basenom=str(day_i)+str(day_i_plus)+'_'+str(inter)
        print('1...')
        build_mesh_and_write_to_file(source_rep+'/images/camb'+basenom+'.tif',source_rep+'/mesh/camb'+basenom+'.vtp',57.5)
        print('2...')
        build_mesh_and_write_to_file(source_rep+'/images/moe'+basenom+'.tif',source_rep+'/mesh/moe'+basenom+'.vtp',127.5)
        print('3...')
        build_mesh_and_write_to_file(source_rep+'/images/ves'+basenom+'.tif',source_rep+'/mesh/ves'+basenom+'.vtp',192.5)
        

