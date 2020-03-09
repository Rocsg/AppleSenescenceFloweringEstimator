#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 10:53:18 2019
@author: fernandr
"""
from skimage import io
import vtk
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()
from scene_3d_helper_functions import *


#CREATION DU RENDERER
renderer = vtk.vtkRenderer()
renderer.SetBackground(0,0,0)

#AJOUT DES DONNEES, GESTION CAMERA ET LUMIERE
source_rep='/home/fernandr/Bureau/Test/Visu2/Compute/'
path_to_movie=source_rep+"movie_V2.ogg"
x_end,y_end,z_end=512,512,512
y_last,z_last=260,260
size,window_width,window_height=511 ,1200, 896
z_begin_irm,z_end_irm=180,370
framerate,timestep=40,0.025
type=0  #test
#type=1  #movie building



data_D1 = io.imread(source_rep+'D1_mush_to_size.tif')
data_D1[z_end_irm:size+1,:,:]=0
data_D1[0:z_begin_irm,:,:]=0
dataImporter6 = vtk.vtkImageImport()


# ELEMENTS DU TISSU DANS L IMAGE INITIALE
print('Ajout de moelle...')
r,g,b=0.922, 0.804,0.72
opac,spec,diff,amb=1.0, 0.2, 0.3, 0.18
isoVal=127.5
actorMoelle=build_actor(source_rep+'D0_moelle_gauss.tif',r,g,b,opac,spec,diff,amb,isoVal,z_begin_irm,z_end_irm,y_last,z_last,size)
renderer.AddActor(actorMoelle)

print('Ajout de cambium...')
r,g,b=0.712, 0.554,0.5
opac,spec,diff,amb=1.0, 0.2, 0.4, 0.18
isoVal=57.5
actorCambium=build_actor(source_rep+'D0_camb_gauss4.tif',r,g,b,opac,spec,diff,amb,isoVal,z_begin_irm,z_end_irm,y_last,z_last,size)
renderer.AddActor(actorCambium)

print('Ajout de vaisseaux...')
r,g,b=0.576, 0.688,0.412
opac,spec,diff,amb=1.0, 0.3, 0.3, 0.1
isoVal=192.5
actorVessels=build_actor(source_rep+'D0_vaisseaux_gauss2.tif',r,g,b,opac,spec,diff,amb,isoVal,z_begin_irm,z_end_irm,y_last,z_last,size)
actorVessels.GetProperty().SetSpecularColor(0.8,0.9,0.7)
renderer.AddActor(actorVessels)




# ELEMENTS DU TISSU SEGMENTATION
print('Ajout de segD3...')
r,g,b=1.0, 0.1,0.1
opac,spec,diff,amb=0.35, 0.3, 0.4, 0.4
isoVal=117.5
actorSegD3=build_actor(source_rep+'D3_mush_to_size.tif',r,g,b,opac,spec,diff,amb,isoVal,z_begin_irm,z_end_irm,y_end,z_end,size)
renderer.AddActor(actorSegD3)

print('Ajout de segD2...')
r,g,b=1.0, 1.0,0.1
opac,spec,diff,amb=0.65, 0.3, 0.4, 0.18
isoVal=227.5
actorSegD2=build_actor(source_rep+'D2_mush_to_size.tif',r,g,b,opac,spec,diff,amb,isoVal,z_begin_irm,z_end_irm,y_end,z_end,size)
renderer.AddActor(actorSegD2)

print('Ajout de segD1...')
r,g,b=0.1, 1.0,0.1
opac,spec,diff,amb=0.7, 0.3, 0.3, 0.08
isoVal=237.5
actorSegD1=build_actor(source_rep+'D1_mush_to_size.tif',r,g,b,opac,spec,diff,amb,isoVal,z_begin_irm,z_end_irm,y_end,z_end,size)
renderer.AddActor(actorSegD1)

print('Ajout de segD0...')
r,g,b=0.2, 0.2,0.2
opac,spec,diff,amb=0.9, 0.005, 1.004, 1.018
isoVal=247.5
actorSegD0=build_actor(source_rep+'D0_mush_to_size.tif',r,g,b,opac,spec,diff,amb,isoVal,z_begin_irm,z_end_irm,y_end,z_end,size)
renderer.AddActor(actorSegD0)



   


#SETUP CAMERA, RENDER WINDOW, LIGHTS AND MOVIE BUILDER
renderer.ResetCamera()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)
renWin.Render()
camera=renderer.GetActiveCamera()
renWin.SetSize(window_width,window_height)
create_lights_for_movie(renderer)
imageFilter,movieWriter=setup_movie(framerate,path_to_movie,renWin)
camera_set_initial_position(camera)





#PAUSE
sequence_idle(100,timestep,renWin,imageFilter,movieWriter,camera)

#TURN LEFT
sequence_turn_azimuth(192,-0.5,timestep,renWin,imageFilter,movieWriter,camera)
sequence_stop_azimuth_slowly(10,5,-0.5,timestep,renWin,imageFilter,movieWriter,camera)
sequence_idle(100,timestep,renWin,imageFilter,movieWriter,camera)

#TURN RIGHT AND ELEVATE
sequence_turn_azimuth_and_elevate(20,0.5,0.35,timestep,renWin,imageFilter,movieWriter,camera)
sequence_turn_azimuth_and_stop_elevate_slowly(20,0.5,0.35,timestep,renWin,imageFilter,movieWriter,camera)
sequence_turn_azimuth(36,0.5,timestep,renWin,imageFilter,movieWriter,camera)
sequence_turn_azimuth_and_elevate(48,0.5,-0.35,timestep,renWin,imageFilter,movieWriter,camera)
sequence_turn_azimuth_and_stop_elevate_slowly(5,7,0.5,-0.35,timestep,renWin,imageFilter,movieWriter,camera)
sequence_stop_azimuth_slowly(10,5,0.5,timestep,renWin,imageFilter,movieWriter,camera)

#PAUSE
sequence_idle(50,timestep,renWin,imageFilter,movieWriter,camera)

#ZOOM
sequence_zoom(5,10,80,0.001,timestep,renWin,imageFilter,movieWriter,camera)

#PAUSE
sequence_idle(100,timestep,renWin,imageFilter,movieWriter,camera)





##### J0 ONLY
actorSegD3.SetVisibility(False)
actorSegD2.SetVisibility(False)
actorSegD1.SetVisibility(False)
actorSegD0.SetVisibility(True)
sequence_idle(100,timestep,renWin,imageFilter,movieWriter,camera)

##### J1 ONLY
actorSegD3.SetVisibility(False)
actorSegD2.SetVisibility(False)
actorSegD1.SetVisibility(True)
actorSegD0.SetVisibility(False)
sequence_idle(100,timestep,renWin,imageFilter,movieWriter,camera)

##### J2 ONLY
actorSegD3.SetVisibility(False)
actorSegD2.SetVisibility(True)
actorSegD1.SetVisibility(False)
actorSegD0.SetVisibility(False)
sequence_idle(100,timestep,renWin,imageFilter,movieWriter,camera)

##### J2 ONLY
actorSegD3.SetVisibility(True)
actorSegD2.SetVisibility(False)
actorSegD1.SetVisibility(False)
actorSegD0.SetVisibility(False)
actorSegD3.GetProperty().SetOpacity(0.7)
actorSegD3.GetProperty().SetAmbient(0.18)   ##############""
sequence_idle(100,timestep,renWin,imageFilter,movieWriter,camera)

#### BOTH
actorSegD3.SetVisibility(True)
actorSegD2.SetVisibility(True)
actorSegD1.SetVisibility(True)
actorSegD0.SetVisibility(True)
actorSegD3.GetProperty().SetOpacity(0.35)
sequence_idle(200,timestep,renWin,imageFilter,movieWriter,camera)



moviewriter.End()
    

