#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 18:09:56 2019

@author: fernandr
"""
from scene_3d_helper_functions import *
nb_interp=120
day_max=3
version =2

source_rep='/home/fernandr/Bureau/Test/Visu2/Compute/'
x_end,y_end,z_end=512,512,512
y_last,z_last=260,260
size,window_width,window_height=511 ,1200, 896
z_begin_irm,z_end_irm=180,370
framerate,timestep=40,0.025
type=0  #test
#type=1  #movie building



#Build mesh for v2
source_rep='/home/fernandr/Bureau/Test/Visu2/Compute/'
build_mesh_and_write_to_file(source_rep+'D0_mush_to_size.tif',source_rep+"D0_mesh.vtp",127.5,z_begin_irm,z_end_irm,y_last,z_last,size)
build_mesh_and_write_to_file(source_rep+'D1_mush_to_size.tif',source_rep+"D1_mesh.vtp",127.5,z_begin_irm,z_end_irm,y_last,z_last,size)
build_mesh_and_write_to_file(source_rep+'D2_mush_to_size.tif',source_rep+"D2_mesh.vtp",127.5,z_begin_irm,z_end_irm,y_last,z_last,size)
build_mesh_and_write_to_file(source_rep+'D3_mush_to_size.tif',source_rep+"D3_mesh.vtp",127.5,z_begin_irm,z_end_irm,y_last,z_last,size)

build_mesh_and_write_to_file(source_rep+'D0_moelle_gauss.tif',source_rep+"moe_mesh.vtp",127.5,z_begin_irm,z_end_irm,y_last,z_last,size)
build_mesh_and_write_to_file(source_rep+'D0_camb_gauss4.tif',source_rep+"camb_mesh.vtp",127.5,z_begin_irm,z_end_irm,y_last,z_last,size)
build_mesh_and_write_to_file(source_rep+'D0_vaisseaux_gauss2.tif',source_rep+"ves_mesh.vtp",127.5,z_begin_irm,z_end_irm,y_last,z_last,size)

