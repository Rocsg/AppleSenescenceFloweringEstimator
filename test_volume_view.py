#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import vtk
from vtk import *
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()
import matplotlib.pyplot as plt
from skimage import io
import numpy as np
# Create the standard renderer, render window and interactor
camera =vtk.vtkCamera ();
camera.SetPosition(200, 200,200);
camera.SetFocalPoint(100, 100, 100);


















renderer = vtk.vtkRenderer()
renderer.SetActiveCamera(camera);
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)



x_end=512
y_end=512
z_end=512

z_last=210
y_last=310

size=511
z_end_irm=400

















print('Ajout de img...')
data_matrix = io.imread('/home/fernandr/Bureau/Test/Visu/cambium.tif')
data_matrix[z_last:size,y_last:size,:]=data_matrix[z_last:size,y_last:size,:]/3
data_matrix[z_end_irm:size,:,:]=0
data_matrix[0:100,:,:]=0
dataImporter = vtk.vtkImageImport()
data_string = data_matrix.tostring()
dataImporter.CopyImportVoidPointer(data_string, len(data_string))
dataImporter.SetDataScalarTypeToUnsignedChar()
dataImporter.SetNumberOfScalarComponents(1)
dataImporter.SetDataExtent(0, x_end-1, 0, y_end-1, 0, z_end-1)
dataImporter.SetWholeExtent(0,x_end-1, 0, y_end-1, 0, z_end-1)
dataImporter.SetDataSpacing( 1,1,1 )
surface = vtk.vtkMarchingCubes()
surface.SetInputConnection( dataImporter.GetOutputPort() )
surface.ComputeNormalsOn()
surface.SetValue( 0, 80.5 )      #########################"
geoBoneMapper = vtk.vtkPolyDataMapper()
geoBoneMapper.SetInputConnection(surface.GetOutputPort() )
geoBoneMapper.ScalarVisibilityOff()
actorBoneImgCambium = vtk.vtkLODActor()
actorBoneImgCambium.SetNumberOfCloudPoints( 100000 )
actorBoneImgCambium.SetMapper( geoBoneMapper )
actorBoneImgCambium.GetProperty().SetColor( 0.5, 0.5, 0.5 )   ##############""
actorBoneImgCambium.GetProperty().SetOpacity(1.0 )   ##############""
actorBoneImgCambium.GetProperty().SetInterpolationToGouraud ()   ##############""
#actorBoneImgCambium.GetProperty().SetSpecularColor(0.9,1,0.9)   ##############""
actorBoneImgCambium.GetProperty().SetSpecular(0.2)   ##############""
actorBoneImgCambium.GetProperty().SetDiffuseColor(0.5,0.5,0.5)   ##############""
actorBoneImgCambium.GetProperty().SetDiffuse(0.4)   ##############""
actorBoneImgCambium.GetProperty().SetAmbientColor(0.5,0.5,0.5)   ##############""
actorBoneImgCambium.GetProperty().SetAmbient(0.18)   ##############""
renderer.AddActor(actorBoneImgCambium)













print('Ok.')
print('GPU rendering : start')

renderer.SetBackground(0,0,0)
renWin.SetSize(1500,800)

#def CheckAbort(obj, event):
#    if obj.GetEventPending() != 0:
#        obj.SetAbortRender(1)

#renWin.AddObserver("AbortCheckEvent", CheckAbort)

iren.Initialize()
renWin.Render()
iren.Start()

