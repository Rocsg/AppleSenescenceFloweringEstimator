#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 10:53:18 2019

@author: fernandr
"""


import time
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()
import vtk
from vtk import *
import matplotlib.pyplot as plt
from skimage import io
import numpy as np
x_end=512
y_end=512
z_end=512







#CREATION DU RENDERER
renderer = vtk.vtkRenderer()
renderer.SetBackground(0,0,0)

#AJOUT DES DONNEES, GESTION CAMERA ET LUMIERE
renderer = add_data_to_renderer_3d(renderer)


#CREATION RENDER WINDOW
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)

#START INTERACTION
renWin.Render()
camera=renderer.GetActiveCamera()
renWin.SetSize(1500,800)
renderer=create_light(renderer)


print('execution partie movie 1')
print('GL ?'+str(renWin.SupportsOpenGL()))
print('Direct ?'+str(renWin.IsDirect()))
imageFilter = vtk.vtkWindowToImageFilter()
imageFilter.SetInput(renWin)
imageFilter.SetInputBufferTypeToRGB()
imageFilter.ReadFrontBufferOff()
imageFilter.Update()
moviewriter = vtk.vtkOggTheoraWriter() 
moviewriter.SetInputConnection(imageFilter.GetOutputPort())
moviewriter.SetFileName("/home/fernandr/Bureau/Test/Visu2/movie.ogg")
moviewriter.Start()
camera.SetPosition(x_end*1.5, y_end*1.5,z_end*1.5);
camera.SetFocalPoint(x_end/2,y_end/2, z_end/2);
camera.Azimuth(14)
camera.SetFocalPoint(x_end/2,y_end/2, z_end/2);
camera.Roll(-103)
for i in range(500):
    if(i%10==0):
        print(str(i))
    time.sleep(0.001)
    camera.Azimuth(1)
    renWin.Render()
    imageFilter.Modified()
    moviewriter.Write()
moviewriter.End()
    
print('GL ?'+str(renWin.SupportsOpenGL()))
print('Direct ?'+str(renWin.IsDirect()))

