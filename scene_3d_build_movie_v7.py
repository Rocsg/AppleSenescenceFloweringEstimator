#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 10:53:18 2019
@author: fernandr
"""
from scene_3d_helper_functions_v7 import *


""" 
################################################################
#########  SETUP GENERAL  ######################################
################################################################
 """


renderer = vtk.vtkRenderer()
renderer.SetBackground(0,0,0)

#AJOUT DES DONNEES, GESTION CAMERA ET LUMIERE
source_rep=get_source_rep()
path_to_movie="/mnt/DD_COMMON/Data_VITIMAGE/Movie_maker_v2/Movie_export/Movie_V7"
version =3
day_max=3
usePrecomputed=False
view_silhouette=False
view_mushroom=True


z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
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








""" 
################################################################
#########  MISE EN PLACE OBJETS   ##############################
################################################################
 """
start = time.time()
print('Start. Time='+str(start))

# ELEMENTS DU TISSU DANS L IMAGE INITIALEa
print('')
print('Ajout de moelle...')
actorMoelleFull= build_moelle(day_i,inter,renderer,None,usePrecomputed,0)

print('')
print('Ajout de cambium...')
actorCambiumFull= build_cambium(day_i,inter,renderer,None,usePrecomputed,0)

print('')
print('Ajout de vaisseaux...')
actorVesselsFull= build_vessels(day_i,inter,renderer,None,usePrecomputed,0)

print('')
print('Ajout de silhouette...')
actorSilhouette= build_silhouette(day_i,inter,renderer,None,usePrecomputed)

if(view_mushroom):
    print('')
    print('Ajout du champignon...')
    if(type_interaction !=2):
        actorMushroom= build_mushroom(day_i,inter,nb_interp,renderer,None)

stop = time.time()
print('Object loaded. Time='+str(stop-start))











""" 
################################################################
#########  SCENARIO VIDEO   ##############################
################################################################
 """
if(type_interaction==2):
    day_i=0
    day_i_plus=1
    inter=0

    ###### TEST
    actorVesselsFull.GetProperty().SetOpacity(0)
    actorMoelleFull.GetProperty().SetOpacity(0)
    actorCambiumFull.GetProperty().SetOpacity(0)
#    actorVessels=build_vessels(day_i,inter,renderer,None,usePrecomputed)
 #   actorMoelle=build_moelle(day_i,inter,renderer,None,usePrecomputed)
 #   actorCambium=build_cambium(day_i,inter,renderer,None,usePrecomputed)
 #   actorVessels.GetProperty().SetOpacity(0)
 #   actorMoelle.GetProperty().SetOpacity(0)
 #   actorCambium.GetProperty().SetOpacity(0)
    actorImg0=build_mpr(day_i,inter,renderer,None,usePrecomputed)
    ###### TEST


    #SETUP CAMERA, RENDER WINDOW, LIGHTS AND MOVIE BUILDER
    renderer.ResetCamera()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(renderer)
    print("Is GPU capable :")
    print(renWin.ReportCapabilities());

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
       
    
    ###### TEST
    sequence_idle(20,timestep,renWin,imageFilter,movieWriter,camera)        
    actorImg0.GetProperty().GetScalarOpacity().AddPoint(255.0,0);
    renderer.RemoveViewProp(actorImg0)
    sequence_idle(10,timestep,renWin,imageFilter,movieWriter,camera)        
    actorImg0=build_mpr(day_i,inter,renderer,None,usePrecomputed)
    ###### TEST
    
    #OBJET SEUL, PUIS DISPARITION DU QUART DE L OBJET, QUI LAISSE APPARAITRE L INTERIEUR
    #sequence_idle(50,timestep,renWin,imageFilter,movieWriter,camera)        
    sequence_disappear_full(renderer,actorVesselsFull,actorMoelleFull,actorCambiumFull,actorVessels,actorMoelle,actorCambium,30,timestep,renWin,imageFilter,movieWriter,camera)            
#   sequence_idle(100,timestep,renWin,imageFilter,movieWriter,camera)        

    #SEQUENCE ROTATIVE POUR SE FAIRE UN APERCU GLOBAL DE L OBJET
    #sequence_turn_around_global(timestep,renWin,imageFilter,movieWriter,camera)
    #sequence_idle(20,timestep,renWin,imageFilter,movieWriter,camera) 

    #SEQUENCE EXPLICATIVE SUR L EXPERIENCE QUI SE DEROULE, AVEC APPARITION DU POINT D INOCULATION
    actorMushroom=sequence_idle_with_red_text(day_max,timestep,renWin,imageFilter,movieWriter,camera,renderer,actorVesselsFull,actorMoelleFull,actorCambiumFull,actorCambium,mobile_rendering) 



    #AFFICHAGE DE LA LEGENDE
    setup_rectangles(day_max,mobile_rendering,renderer)
    textActorMRI,textActorINTER,actP = setup_text_and_progress_bar(day_max,renderer,mobile_rendering)   
    sequence_idle(50,timestep,renWin,imageFilter,movieWriter,camera) 
    


    #BOUCLE D AFFICHAGE DE L OBJET
    for day_i in range(day_max):
        day_i_plus=day_i+1
        if day_i==day_max-1:
            nbfra=nb_interp+1
        else:
            nbfra=nb_interp
        for inter in range(nbfra):
            if inter%interp_step!=0:
                continue
            #ACTUALISATION MAILLAGES ET LEGENDE
            stop = time.time()
            print('time='+str(stop-start) +'  Building meshes '+str(day_i)+'_'+str(inter))
            actorVessels=build_vessels(day_i,inter,renderer,actorVessels,usePrecomputed)
            actorMoelle=build_moelle(day_i,inter,renderer,actorMoelle,usePrecomputed)
            actorCambium=build_cambium(day_i,inter,renderer,actorCambium,usePrecomputed)
            actorSilhouette= build_silhouette(day_i,inter,renderer,None,usePrecomputed)
            if(view_mushroom):
                actorMushroom=build_mushroom(day_i,inter,nb_interp,renderer,actorMushroom)
            update_moving_legends(textActorMRI,textActorINTERP,actP,x_time,mobile_rendering)

            #ENREGISTREMENT VUE OBLIQUE
            renWin.Render()
            imageFilter.Modified()
            movieWriter.Write()

            #ENREGISTREMENT VUE DE FACE
            to_front_view(camera)
            renWin.Render()
            imageFilterFront.Modified()
            movieWriterFront.Write()
            from_front_view(camera)

            #ENREGISTREMENT VUE DE DESSUS
            to_up_view(camera)
            set_lights_on_upper_mode(light_green,light_green2,light_green3)
            renWin.Render()
            imageFilterUp.Modified()
            movieWriterUp.Write()
            from_up_view(camera)
            set_lights_on_normal_mode(light_green,light_green2,light_green3)

            #ENREGISTREMENT VUE DE DROITE
            to_right_view(camera)
            renWin.Render()
            imageFilterRight.Modified()
            movieWriterRight.Write()
            from_right_view(camera)

            
    #ENREGISTREMENT VUE DE DROITE
    sequence_idle_and_right(100,timestep,renWin,imageFilter,movieWriter,imageFilterRight,movieWriterRight,camera)        
    movieWriter.End()
    movieWriterRight.End()
    movieWriterFront.End()
    movieWriterUp.End()





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


