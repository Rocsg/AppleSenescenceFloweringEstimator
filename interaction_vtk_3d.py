#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 10:53:18 2019

@author: fernandr
"""
#from utils.add_data import *
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()
import vtk
x_end=512
y_end=512
z_end=512

#CREATION DU RENDERER
renderer = vtk.vtkRenderer()
renderer.SetBackground(0,0,0)


#AJOUT DES DONNEES
renderer = add_data_to_renderer_3d(renderer)


#CREATION RENDER WINDOW
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)


#PREMIER RENDER ET GESTION LUMIERES
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
iren.Render()
camera=renderer.GetActiveCamera()
renWin.SetSize(1500,800)
renderer=create_light(renderer)



# GESTION CAMERA
camera.SetPosition(x_end*1.5, y_end*1.5,z_end*1.5);
camera.SetFocalPoint(x_end/2,y_end/2, z_end/2);
camera.Azimuth(14)
camera.SetFocalPoint(x_end/2,y_end/2, z_end/2);
camera.Roll(-103)


#CREATION INTERACTOR
iren.Start()


