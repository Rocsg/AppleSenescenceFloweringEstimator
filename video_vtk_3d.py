#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 10:53:18 2019

@author: fernandr
"""

import time
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
x_end=512
y_end=512
z_end=512
z_last=260
y_last=260
size=511
z_end_irm=370
z_begin_irm=180

print('Ajout de moelle...')
r,g,b=0.922, 0.804,0.72
opac,spec,diff,amb=1.0, 0.2, 0.3, 0.18
isoVal=127.5
actorMoelle=build_actor(source_rep+'D0_moelle_gauss.tif',r,g,b,opac,spec,diff,isoVal)
renderer.AddActor(actorMoelle)


print('Ajout de cambium...')
r,g,b=0.712, 0.554,0.5
opac,spec,diff,amb=1.0, 0.2, 0.4, 0.18
isoVal=57.5
actorCambium=build_actor(source_rep+'D0_camb_gauss4.tif',r,g,b,opac,spec,diff,isoVal)
renderer.AddActor(actorCambium)

print('Ajout de vaisseaux...')
r,g,b=0.576, 0.688,0.412
opac,spec,diff,amb=1.0, 0.3, 0.3, 0.1
isoVal=192.5
actorVessels=build_actor(source_rep+'D0_vaisseaux_gauss2.tif',r,g,b,opac,spec,diff,isoVal)
actorVessels.GetProperty().SetSpecularColor(0.8,0.9,0.7)
renderer.AddActor(actorVessels)



print('Ajout de segD3...')
r,g,b=1.0, 0.1,0.1
opac,spec,diff,amb=0.35, 0.3, 0.4, 0.4
isoVal=117.5
actorSegD3=build_actor(source_rep+'D3_mush_to_size',r,g,b,opac,spec,diff,isoVal)
renderer.AddActor(actorSegD3)



print('Ajout de D2...')
r=1
g=1
b=0.1
data_D2 = io.imread(source_rep+'D2_mush_to_size.tif')
data_D2[z_end_irm:size+1,:,:]=0
data_D2[0:z_begin_irm,:,:]=0
dataImporter5 = vtk.vtkImageImport()
data_string5 = data_D2.tostring()
dataImporter5.CopyImportVoidPointer(data_string5, len(data_string5))
dataImporter5.SetDataScalarTypeToUnsignedChar()
dataImporter5.SetNumberOfScalarComponents(1)
dataImporter5.SetDataExtent(0, x_end-1, 0, y_end-1, 0, z_end-1)
dataImporter5.SetWholeExtent(0,x_end-1, 0, y_end-1, 0, z_end-1)
dataImporter5.SetDataSpacing( 1,1,1 )
surface5 = vtk.vtkMarchingCubes()
surface5.SetInputConnection( dataImporter5.GetOutputPort() )
surface5.ComputeNormalsOn()
surface5.SetValue( 0, 227.5 )      #########################"
geoBoneMapper5 = vtk.vtkPolyDataMapper()
geoBoneMapper5.SetInputConnection(surface5.GetOutputPort() )
geoBoneMapper5.ScalarVisibilityOff()
actorBone5 = vtk.vtkActor()
actorBone5.SetMapper( geoBoneMapper5 )
actorBone5.GetProperty().SetColor( r,g,b )   ##############""
actorBone5.GetProperty().SetOpacity( 0.65 )   ##############""
actorBone5.GetProperty().SetInterpolationToGouraud ()   ##############""
#actorBone2.GetProperty().SetSpecularColor(0.9,0.1,0.1)   ##############""
actorBone5.GetProperty().SetSpecular(0.3)   ##############""
actorBone5.GetProperty().SetDiffuseColor(r,g,b)   ##############""
actorBone5.GetProperty().SetDiffuse(0.4)   ##############""
actorBone5.GetProperty().SetAmbientColor(r,g,b)   ##############""
actorBone5.GetProperty().SetAmbient(0.18)   ##############""

renderer.AddActor(actorBone5)






print('Ajout de D1...')
r=0.1
g=1
b=0.1
data_D1 = io.imread(source_rep+'D1_mush_to_size.tif')
data_D1[z_end_irm:size+1,:,:]=0
data_D1[0:z_begin_irm,:,:]=0
dataImporter6 = vtk.vtkImageImport()
data_string6 = data_D1.tostring()
dataImporter6.CopyImportVoidPointer(data_string6, len(data_string6))
dataImporter6.SetDataScalarTypeToUnsignedChar()
dataImporter6.SetNumberOfScalarComponents(1)
dataImporter6.SetDataExtent(0, x_end-1, 0, y_end-1, 0, z_end-1)
dataImporter6.SetWholeExtent(0,x_end-1, 0, y_end-1, 0, z_end-1)
dataImporter6.SetDataSpacing( 1,1,1 )
surface6 = vtk.vtkMarchingCubes()
surface6.SetInputConnection( dataImporter6.GetOutputPort() )
surface6.ComputeNormalsOn()
surface6.SetValue( 0, 237.5 )      #########################"
geoBoneMapper6 = vtk.vtkPolyDataMapper()
geoBoneMapper6.SetInputConnection(surface6.GetOutputPort() )
geoBoneMapper6.ScalarVisibilityOff()
actorBone6 = vtk.vtkActor()
actorBone6.SetMapper( geoBoneMapper6 )
actorBone6.GetProperty().SetColor( r,g,b )   ##############""
actorBone6.GetProperty().SetOpacity( 0.7 )   ##############""
actorBone6.GetProperty().SetInterpolationToGouraud ()   ##############""
#actorBone2.GetProperty().SetSpecularColor(0.9,0.1,0.1)   ##############""
actorBone6.GetProperty().SetSpecular(0.3)   ##############""
actorBone6.GetProperty().SetDiffuseColor(r,g,b)   ##############""
actorBone6.GetProperty().SetDiffuse(0.3)   ##############""
actorBone6.GetProperty().SetAmbientColor(r,g,b)   ##############""
actorBone6.GetProperty().SetAmbient(0.08)   ##############""

renderer.AddActor(actorBone6)



print('Ajout de D0...')
r=0.2
g=0.2
b=0.2
data_D0 = io.imread(source_rep+'D0_mush_to_size.tif')
data_D0[z_end_irm:size+1,:,:]=0
data_D0[0:z_begin_irm,:,:]=0
dataImporter7 = vtk.vtkImageImport()
data_string7 = data_D0.tostring()
dataImporter7.CopyImportVoidPointer(data_string7, len(data_string7))
dataImporter7.SetDataScalarTypeToUnsignedChar()
dataImporter7.SetNumberOfScalarComponents(1)
dataImporter7.SetDataExtent(0, x_end-1, 0, y_end-1, 0, z_end-1)
dataImporter7.SetWholeExtent(0,x_end-1, 0, y_end-1, 0, z_end-1)
dataImporter7.SetDataSpacing( 1,1,1 )
surface7 = vtk.vtkMarchingCubes()
surface7.SetInputConnection( dataImporter7.GetOutputPort() )
surface7.ComputeNormalsOn()
surface7.SetValue( 0, 247.5 )      #########################"
geoBoneMapper7 = vtk.vtkPolyDataMapper()
geoBoneMapper7.SetInputConnection(surface7.GetOutputPort() )
geoBoneMapper7.ScalarVisibilityOff()
actorBone7 = vtk.vtkActor()
actorBone7.SetMapper( geoBoneMapper7 )
actorBone7.GetProperty().SetColor( r,g,b )   ##############""
actorBone7.GetProperty().SetOpacity( 0.9 )   ##############""
actorBone7.GetProperty().SetInterpolationToGouraud ()   ##############""
#actorBone2.GetProperty().SetSpecularColor(0.9,0.1,0.1)   ##############""
actorBone7.GetProperty().SetSpecular(0.005)   ##############""
actorBone7.GetProperty().SetDiffuseColor(r,g,b)   ##############""
actorBone7.GetProperty().SetDiffuse(1.004)   ##############""
actorBone7.GetProperty().SetAmbientColor(r,g,b)   ##############""
actorBone7.GetProperty().SetAmbient(1.018)   ##############""

renderer.AddActor(actorBone7)


   

renderer.ResetCamera()

#CREATION RENDER WINDOW
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)

#START INTERACTION
renWin.Render()
camera=renderer.GetActiveCamera()
renWin.SetSize(1280,896)
x_end=512
y_end=512
z_end=512
# create a green light
light_green = vtk.vtkLight()
light_green.SetPositional(1)
light_green.SetPosition(+x_end*2, -y_end*2,z_end*2)
light_green.SetColor(0.6, 0.6, 0.6)
light_green.SetIntensity(0.7)
renderer.AddLight(light_green)

light_green2 = vtk.vtkLight()
light_green2.SetPositional(1)
light_green2.SetPosition(-x_end*2+1000, y_end*2,z_end*2)
light_green2.SetColor(0.8, 0.8, 0.8)
light_green2.SetIntensity(1.0)
renderer.AddLight(light_green2)

light_green3 = vtk.vtkLight()
light_green3.SetPositional(1)
light_green3.SetPosition(-x_end*2, y_end*2+1000,z_end*2+1000)
light_green3.SetColor(0.8, 0.8, 0.8)
light_green3.SetIntensity(1.4)
renderer.AddLight(light_green3)


print('execution partie movie 1')
print('GL ?'+str(renWin.SupportsOpenGL()))
print('Direct ?'+str(renWin.IsDirect()))
imageFilter = vtk.vtkWindowToImageFilter()
imageFilter.SetInput(renWin)
imageFilter.SetInputBufferTypeToRGB()
imageFilter.ReadFrontBufferOff()
imageFilter.Update()
moviewriter = vtk.vtkOggTheoraWriter() 
moviewriter.SetRate(40) 
timestep=0
moviewriter.SetQuality(2) 	
moviewriter.SetInputConnection(imageFilter.GetOutputPort())
moviewriter.SetFileName("/home/fernandr/Bureau/Test/Visu2/movie.ogg")
moviewriter.Start()

camera_set_initial_position()

#STARTTTTTTTTTT
for i in range(100):
    time.sleep(timestep)
    renWin.Render()
    imageFilter.Modified()
    moviewriter.Write()


#########TO THE LEFT
for i in range(96*2):
    time.sleep(timestep)
    camera.Azimuth(-1*0.5)
    renWin.Render()
    imageFilter.Modified()
    moviewriter.Write()

for j in range (10):
    for i in range(5):
        time.sleep(timestep)
        camera.Azimuth(-0.1*(9-j)*0.5)
        renWin.Render()
        imageFilter.Modified()
        moviewriter.Write()



#STOP
for i in range(75):
    time.sleep(timestep)
    renWin.Render()
    imageFilter.Modified()
    moviewriter.Write()





#########TO THE RIGHT
for i in range(20):
    time.sleep(timestep)
    camera.Azimuth(1*0.5)
    camera.Elevation(0.5*0.7)
    renWin.Render()
    imageFilter.Modified()
    moviewriter.Write()


for j in range (5):
    for i in range(7):
        time.sleep(timestep)
        camera.Azimuth(1*0.5)
        camera.Elevation(0.1*0.7*(5-j))
        renWin.Render()
        imageFilter.Modified()
        moviewriter.Write()

for i in range(36):
    time.sleep(timestep)
    camera.Azimuth(1*0.5)
    renWin.Render()
    imageFilter.Modified()
    moviewriter.Write()

for i in range(48):
    time.sleep(timestep)
    camera.Azimuth(1*0.5)
    camera.Elevation(-0.5*0.7)
    renWin.Render()
    imageFilter.Modified()
    moviewriter.Write()

for j in range (5):
    for i in range(7):
        time.sleep(timestep)
        camera.Azimuth(1*0.5)
        camera.Elevation(-0.1*0.7*(5-j))
        renWin.Render()
        imageFilter.Modified()
        moviewriter.Write()



for j in range (10):
    for i in range(5):
        time.sleep(timestep)
        camera.Azimuth(0.1*(9-j)*0.5)
        renWin.Render()
        imageFilter.Modified()
        moviewriter.Write()



##### STOP
for i in range(50):
    time.sleep(timestep)
    renWin.Render()
    imageFilter.Modified()
    moviewriter.Write()


###FOCUS ON MUSHROOM
#for i in range(40):
#    time.sleep(timestep)
#    camera.Yaw(0.025)
#    renWin.Render()

#for j in range (5):
#    for i in range(5):
#        time.sleep(timestep)
#        camera.Azimuth(0.005*(5-j))
#        renWin.Render()


#### ZOOM
for j in range (5):
    for i in range(10):
        time.sleep(timestep)
        camera.Zoom(1+j*0.001)
        renWin.Render()
        imageFilter.Modified()
        moviewriter.Write()

for i in range(80):
    time.sleep(timestep)
    camera.Zoom(1.005)
    renWin.Render()
    imageFilter.Modified()
    moviewriter.Write()

for j in range (5):
    for i in range(10):
        time.sleep(timestep)
        camera.Zoom(1+(5-j)*0.001)
        renWin.Render()
        imageFilter.Modified()
        moviewriter.Write()


##### STOP
for i in range(100):
    time.sleep(timestep)
    renWin.Render()
    imageFilter.Modified()
    moviewriter.Write()


##### J0 ONLY
actorBone5.SetVisibility(False)
actorBone4.SetVisibility(False)
for i in range(100):
    time.sleep(timestep)
    renWin.Render()
    imageFilter.Modified()
    moviewriter.Write()

actorBone5.SetVisibility(True)
actorBone4.SetVisibility(False)
actorBone6.SetVisibility(False)
for i in range(100):
    time.sleep(timestep)
    renWin.Render()
    imageFilter.Modified()
    moviewriter.Write()

actorBone4.SetVisibility(True)
actorBone4.GetProperty().SetOpacity(0.7)
actorBone4.GetProperty().SetAmbient(0.18)   ##############""
actorBone5.SetVisibility(False)
actorBone6.SetVisibility(False)
for i in range(100):
    time.sleep(timestep)
    renWin.Render()
    imageFilter.Modified()
    moviewriter.Write()

actorBone4.SetVisibility(True)
actorBone4.GetProperty().SetOpacity(0.35)
actorBone5.SetVisibility(True)
actorBone6.SetVisibility(True)
for i in range(200):
    time.sleep(timestep)
    renWin.Render()
    imageFilter.Modified()
    moviewriter.Write()


moviewriter.End()
    

