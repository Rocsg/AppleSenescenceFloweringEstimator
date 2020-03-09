#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 10:53:18 2019
@author: fernandr
"""
from scene_3d_helper_functions_v4 import *
#CREATION DU RENDERER
renderer = vtk.vtkRenderer()
renderer.SetBackground(0,0,0)

#AJOUT DES DONNEES, GESTION CAMERA ET LUMIERE
source_rep=get_source_rep()
path_to_movie="/mnt/DD_COMMON/Data_VITIMAGE/Movie_maker_v2/movie_V3_test_precompute.ogg"
tupa=get_image_constants()
print(tupa)
z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
window_width,window_height=1200, 896
framerate,timestep=25,0
nb_interp=120
day_max=3
version =3
interp_step=20
usePrecomputed=False
type_interaction=2  #0=fix, 1=interactionmode,  2=video
#type=1  #movie building


start = time.time()
print('time='+str(start))
day_i=0
day_i_plus=day_i+1
inter=0
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

print('')
print('Ajout de la silhouette...')
actorSilhouette= build_silhouette(day_i,inter,renderer,None,usePrecomputed)
stop = time.time()
print('time='+str(stop-start))




if(type_interaction==2):
    #SETUP CAMERA, RENDER WINDOW, LIGHTS AND MOVIE BUILDER
    renderer.ResetCamera()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(renderer)
    renWin.Render()
    camera=renderer.GetActiveCamera()
    renWin.SetSize(window_width,window_height)
    create_lights_for_movie(renderer)
    imageFilter,movieWriter=setup_movie(framerate,path_to_movie,renWin)
    setup_camera_initial_position(camera)
    sequence_idle(50,timestep,renWin,imageFilter,movieWriter,camera)        
    
    for day_i in range(day_max):
        day_i_plus=day_i+1
        for inter in range(nb_interp):
            if inter%interp_step!=0:
                continue
            stop = time.time()
            print('time='+str(stop-start))
            print('Building meshes for time '+str(day_i)+'_'+str(inter))
            actorVessels=build_vessels(day_i,inter,renderer,actorVessels,usePrecomputed)
            actorMoelle=build_moelle(day_i,inter,renderer,actorMoelle,usePrecomputed)
            actorCambium=build_cambium(day_i,inter,renderer,actorCambium,usePrecomputed)
            actorSilhouette=build_silhouette(day_i,inter,renderer,actorSilhouette,usePrecomputed)
            renWin.Render()
            imageFilter.Modified()
            movieWriter.Write()
            
    sequence_idle(100,timestep,renWin,imageFilter,movieWriter,camera)        
    movieWriter.End()
    

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


