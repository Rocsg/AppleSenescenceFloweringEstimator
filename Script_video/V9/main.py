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
source_rep=get_source_rep()
path_to_movie="/mnt/DD_COMMON/Data_VITIMAGE/Movie_maker_v2/Movie_export/Movie_V9"
version =3
day_max=3

z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
print('Starting rendering. Constants defined=z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z :'+str(z_begin_irm)+', '+str(z_end_irm)+', '+str(size_x)+', '+str(size_y)+', '+str(size_z))
mobile_rendering=0 # 0 = normal on personal computer, 1=1080p, 2= 4K TV, 3= mobile_phone
window_width,window_height,x_margin,text_width,y_margin,text_height,police_1,police_2,x_plus,space_between_texts=window_size_config(day_max,mobile_rendering)


framerate,timestep=25,0
nb_interp=120
interp_step=1


day_idle=0
frame_idle=0
type_interaction=2  #0=fix sur modele, 1=interactionmode sur modele,  2=video
type_view=0  # 0 = oblique 1=front, 2=right, 3 =up
day_i=day_idle
day_i_plus=day_idle+1
inter=frame_idle
basenom=str(day_i)+str(day_i_plus)+'_'+str(inter)
day_i=0
day_i_plus=1
inter=0









""" 
################################################################
#########  MISE EN PLACE SILHOUETTE ET VUE   ##############################
################################################################
 """
start = time.time()
print('Start.')

#SETUP CAMERA, RENDER WINDOW, LIGHTS AND MOVIE BUILDER

#WARNING : THESE TWO LINES HELPS BUILDING THE SETUP
actorSilhouetteN=build_silhouette(0,0,renderer,None,0) 
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


print('here0')


""" 
################################################################
#########  Partie 1 : Inoculation et methode de suivi  #########
################################################################
 """

#imagefilter,moviewriter=setup_movie(framerate,path_to_movie+"_intro_part_1_title_and_main_movie.ogg",renWin)
print('here1')
sequence_01_title(day_max,nb_interp,100,timestep,renWin,imagefilter,moviewriter,camera,renderer,mobile_rendering)
#moviewriter.End()

#imagefilter,moviewriter=setup_movie(framerate,path_to_movie+"_intro_part_2_inoculation_and_observation.ogg",renWin)
#sequence_02_retrait_ecorce(day_max, timestep,renWin,imagefilter,moviewriter,camera,renderer,mobile_rendering)
#sequence_03_mri_observations(day_max, timestep,nb_interp,renWin,imagefilter,moviewriter,camera,renderer,mobile_rendering)
#sequence_04_successive_volumes(day_max, nb_interp,timestep,renWin,imagefilter,moviewriter,camera,renderer,mobile_rendering)
#moviewriter.End()


""" 
################################################################
#########  Partie 2 : Recalage et interpolation  ###############
################################################################
 """
#imagefilter,moviewriter=setup_movie(framerate,path_to_movie+"_intro_part_3_registration_and_time_lapse.ogg",renWin)
#sequence_05_registration(day_max, timestep,nb_interp,renWin,imagefilter,moviewriter,camera,renderer,mobile_rendering)
#sequence_07_interpolation_volume(day_max, timestep,nb_interp,renWin,imagefilter,moviewriter,camera,renderer,mobile_rendering)
#moviewriter.End()

#imagefilter,moviewriter=setup_movie(framerate,path_to_movie+"_intro_part_4_vanishing_area_tracking.ogg",renWin)
#sequence_08_destruction_area(day_max, timestep,nb_interp,renWin,imagefilter,moviewriter,camera,renderer,mobile_rendering)
#sequence_09_interpolation_volume(day_max, timestep,nb_interp,renWin,imagefilter,moviewriter,camera,renderer,mobile_rendering)
#moviewriter.End()

#print('stop test')
#setup_rectangles(day_max,mobile_rendering,renderer)
##sequence_06_interpolation_slices(day_max, timestep,nb_interp,renWin,imagefilter,moviewriter,camera,renderer,actorPlane1,actorPlane2,mobile_rendering)

   

#sequence_idle(20,timestep,renWin,imagefilter,moviewriter,camera)        
#sequence_idle(10,timestep,renWin,imagefilter,moviewriter,camera)        
#actorImg0=build_mpr(day_i,inter,renderer,None,usePrecomputed)
###### TEST

#OBJET SEUL, PUIS DISPARITION DU QUART DE L OBJET, QUI LAISSE APPARAITRE L INTERIEUR
#sequence_idle(50,timestep,renWin,imagefilter,moviewriter,camera)        
#sequence_disappear_full(renderer,actorVesselsFull,actorMoelleFull,actorCambiumFull,actorVessels,actorMoelle,actorCambium,30,timestep,renWin,imagefilter,moviewriter,camera)            
#   sequence_idle(100,timestep,renWin,imagefilter,moviewriter,camera)        

#SEQUENCE ROTATIVE POUR SE FAIRE UN APERCU GLOBAL DE L OBJET
#sequence_turn_around_global(timestep,renWin,imagefilter,moviewriter,camera)
#sequence_idle(20,timestep,renWin,imagefilter,moviewriter,camera) 

#SEQUENCE EXPLICATIVE SUR L EXPERIENCE QUI SE DEROULE, AVEC APPARITION DU POINT D INOCULATION



#AFFICHAGE DE LA LEGENDE
#textActorMRI,textActorINTER,actP = setup_text_and_progress_bar(day_max,renderer,mobile_rendering)   
#sequence_idle(50,timestep,renWin,imagefilter,moviewriter,camera) 

       
