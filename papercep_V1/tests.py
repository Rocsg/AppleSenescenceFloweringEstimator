#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 10:53:18 2019
@author: fernandr
"""
from sequences import *

""" 
################################################################
#########  SETUP GENERAL  ######################################
################################################################
 """


renderer = vtk.vtkRenderer()
renderer.SetBackground(0,0,0)

#AJOUT DES DONNEES, GESTION CAMERA ET LUMIERE
specimen="CEP011_AS1"
dirSeg='/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'+specimen+'/
#path_to_movie="/mnt/DD_COMMON/Data_VITIMAGE/Movie_maker_v2/Movie_export/Movie_V9"

z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
print('Starting rendering. Constants defined=z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z :'+str(z_begin_irm)+', '+str(z_end_irm)+', '+str(size_x)+', '+str(size_y)+', '+str(size_z))
mobile_rendering=0 # 0 = normal on personal computer, 1=1080p, 2= 4K TV, 3= mobile_phone
window_width,window_height,x_margin,text_width,y_margin,text_height,police_1,police_2,x_plus,space_between_texts=window_size_config(day_max,mobile_rendering)


framerate,timestep=25,0
type_interaction=2  #0=fix sur modele, 1=interactionmode sur modele,  2=video
type_view=0  # 0 = oblique 1=front, 2=right, 3 =up








""" 
################################################################
#########  MISE EN PLACE SILHOUETTE ET VUE   ##############################
################################################################
 """
start = time.time()
print('Start.')
#SETUP CAMERA, RENDER WINDOW, LIGHTS AND MOVIE BUILDER

#WARNING : THESE TWO LINES HELPS BUILDING THE SETUP
actorSilhouetteN=build_cep_silhouette(spec,renderer,None,0) 
actorSilhouetteN.GetProperty().SetOpacity(0)
#WARNING : THESE TWO LINES HELPS BUILDING THE SETUP
renderer.ResetCamera()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)
renWin.Render()
camera=renderer.GetActiveCamera()
renWin.SetSize(window_width,window_height)
light_green,light_green2,light_green3=start_lights(renderer)
imagefilter,moviewriter=setup_movie(framerate,path_to_movie+"_intro_sigma_5.ogg",renWin)
setup_camera_initial_position(camera)
set_lights_on_normal_mode(light_green,light_green2,light_green3)
light=add_light_right_vr(renderer)
#add_lights_aliasing(renderer)
print('here0')












zo=120
zf=315
subFactor=1
camera.Elevation(5)
camera.Pitch(0.5)
camera.Azimuth(35)
camera.Zoom(1.3)






sigma_level=0
da=2
intee=110
inte=intee*subFactor
actorVolume=None
actorInoc=None
#camera.Zoom(2)    
to_front_view_intro(camera)
camera.Azimuth(10)
for sig in range (1):
    print("evaluation sigma="+str(sig))
    actorVolume=build_vr(da,inte,nb_interp,renderer,actorVolume,2,zo,zf)
    actorInoc=build_mushroom(da,inte,nb_interp,renderer,actorInoc,sig)
    actorInoc.GetProperty().SetOpacity(1)
    #to_front_view_intro(camera)
    actorInoc.GetProperty().SetInterpolationToPhong()
    renWin.Render()
    print('vue 1')
    time.sleep(3)

