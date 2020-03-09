#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 10:53:18 2019
@author: fernandr
"""
from scene_3d_helper_functions_v6 import *
#CREATION DU RENDERER
renderer = vtk.vtkRenderer()
renderer.SetBackground(0,0,0)

#AJOUT DES DONNEES, GESTION CAMERA ET LUMIERE
source_rep=get_source_rep()
path_to_movie="/mnt/DD_COMMON/Data_VITIMAGE/Movie_maker_v2/Movie_V6"
version =3
day_max=3

z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
window_width,window_height=1200, 896
framerate,timestep=40,0
nb_interp=120
interp_step=20

day_idle=0
frame_idle=0
type_interaction=2  #0=fix sur modele, 1=interactionmode sur modele,  2=video
type_view=0  # 0 = oblique 1=front, 2=right, 3 =up

usePrecomputed=False
view_silhouette=False
view_mushroom=True
mobile_rendering=False


start = time.time()
print('time='+str(start))
day_i=day_idle
day_i_plus=day_idle+1
inter=frame_idle
basenom=str(day_i)+str(day_i_plus)+'_'+str(inter)


# ELEMENTS DU TISSU DANS L IMAGE INITIALEa
print('')
print('Ajout de moelle...')
actorMoelle= build_moelle(day_i,inter,renderer,None,usePrecomputed)

print('')
print('Ajout de cambium...')
actorCambium= build_cambium(day_i,inter,renderer,None,usePrecomputed)

print('')
print('Ajout de vaisseaux...')
actorVessels= build_vessels(day_i,inter,renderer,None,usePrecomputed)

if(view_silhouette):
    print('')
    print('Ajout de la silhouette...')
    actorSilhouette= build_silhouette(day_i,inter,renderer,None,usePrecomputed)

if(view_mushroom):
    print('')
    print('Ajout du champignon...')
    if(type_interaction !=2):
        actorMushroom= build_mushroom(day_i,inter,nb_interp,renderer,None)

stop = time.time()
print('time='+str(stop-start))




if(type_interaction==2):
    day_i=0
    day_i_plus=1
    inter=0
    actorVessels=build_vessels(day_i,inter,renderer,actorVessels,usePrecomputed)
    actorMoelle=build_moelle(day_i,inter,renderer,actorMoelle,usePrecomputed)
    actorCambium=build_cambium(day_i,inter,renderer,actorCambium,usePrecomputed)
    if(view_silhouette):
        actorSilhouette=build_silhouette(day_i,inter,renderer,actorSilhouette,usePrecomputed)
     #SETUP CAMERA, RENDER WINDOW, LIGHTS AND MOVIE BUILDER
    renderer.ResetCamera()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(renderer)
    renWin.Render()
    camera=renderer.GetActiveCamera()
    renWin.SetSize(window_width,window_height)
    light_green,light_green2,light_green3=start_lights(renderer)
    imageFilter,movieWriter=setup_movie(framerate,path_to_movie+"_oblique.ogg",renWin)
    imageFilterUp,movieWriterUp=setup_movie(framerate,path_to_movie+"_up.ogg",renWin)
    imageFilterFront,movieWriterFront=setup_movie(framerate,path_to_movie+"_front.ogg",renWin)
    imageFilterRight,movieWriterRight=setup_movie(framerate,path_to_movie+"_right.ogg",renWin)
    setup_camera_initial_position(camera)

    set_lights_on_normal_mode(light_green,light_green2,light_green3)
    if(type_view==1):
        to_front_view(camera)
    if(type_view==2):
        to_right_view(camera)
    if(type_view==3):
        to_up_view(camera)
        set_lights_on_upper_mode(light_green,light_green2,light_green3)
       
    
    
    
    

    
    sequence_idle(100,timestep,renWin,imageFilter,movieWriter,camera)        
    sequence_turn_around_global(timestep,renWin,imageFilter,movieWriter,camera)
    sequence_idle(20,timestep,renWin,imageFilter,movieWriter,camera) 
    actorMushroom=sequence_idle_with_red_text(timestep,renWin,imageFilter,movieWriter,camera,renderer,mobile_rendering) 


    x_margin,text_width,y_margin,text_height=window_size_config()
    setup_rectangle(window_width,window_height,x_margin,y_margin,renderer)
    textActorMRI,textActorINTER,actP,x_margin,space_between_texts,y_margin,x_plus=setup_text_and_progress_bar(day_max,window_width,window_height,renderer)   
    sequence_idle(50,timestep,renWin,imageFilter,movieWriter,camera) 
    
    for day_i in range(day_max):
        day_i_plus=day_i+1
        if day_i==day_max-1:
            nbfra=nb_interp+1
        else:
            nbfra=nb_interp
        for inter in range(nbfra):
            if inter%interp_step!=0:
                continue
            stop = time.time()
            print('time='+str(stop-start) +'  Building meshes '+str(day_i)+'_'+str(inter))
            actorVessels=build_vessels(day_i,inter,renderer,actorVessels,usePrecomputed)
            actorMoelle=build_moelle(day_i,inter,renderer,actorMoelle,usePrecomputed)
            actorCambium=build_cambium(day_i,inter,renderer,actorCambium,usePrecomputed)
            if(view_silhouette):
                actorSilhouette=build_silhouette(day_i,inter,renderer,actorSilhouette,usePrecomputed)
            if(view_mushroom):
                actorMushroom=build_mushroom(day_i,inter,nb_interp,renderer,actorMushroom)
            update_moving_legends(textActorMRI,textActorINTER,actP,day_i+inter/nb_interp,x_margin,space_between_texts,window_height,y_margin,x_plus,mobile_rendering)
            renWin.Render()
            imageFilter.Modified()
            movieWriter.Write()

            time.sleep(1)
            to_front_view(camera)
            renWin.Render()
            imageFilterFront.Modified()
            movieWriterFront.Write()
            from_front_view(camera)
            time.sleep(1)

            to_up_view(camera)
            set_lights_on_upper_mode(light_green,light_green2,light_green3)
            renWin.Render()
            imageFilterUp.Modified()
            movieWriterUp.Write()
            from_up_view(camera)
            set_lights_on_normal_mode(light_green,light_green2,light_green3)
            time.sleep(1)

            to_right_view(camera)
            renWin.Render()
            imageFilterRight.Modified()
            movieWriterRight.Write()
            from_right_view(camera)
            time.sleep(1)

            
    sequence_idle_and_right(100,timestep,renWin,imageFilter,movieWriter,imageFilterRight,movieWriterRight,camera)        
    movieWriter.End()
    movieWriterRight.End()
    movieWriterFront.End()
    movieWriterFront.End()

elif(type_interaction==1):
    renderer.ResetCamera()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(renderer)
    camera=renderer.GetActiveCamera()
    renWin.SetSize(window_width,window_height)
    create_lights_for_movie(renderer)
    setup_camera_initial_position(camera)
    setup_interaction(renWin,renderer)



else :
    renderer.ResetCamera()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(renderer)
    camera=renderer.GetActiveCamera()
    renWin.SetSize(window_width,window_height)
    create_lights_for_movie(renderer)
    setup_camera_initial_position(camera)
    renWin.Render()


