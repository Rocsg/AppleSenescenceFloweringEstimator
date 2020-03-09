#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 10:53:18 2019

@author: fernandr
"""


import vtk
from vtk import*
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()
import matplotlib.pyplot as plt
from skimage import io
import numpy as np
x_end=512
y_end=512
z_end=512
z_last=230
y_last=260
size=511
z_end_irm=300


renderer = vtk.vtkRenderer()
renWin = vtk.vtkRenderWindow()
renWin.AddRenderer(renderer)
iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)


# create a green light
light_green = vtk.vtkLight()
light_green.SetPositional(1)
light_green.SetPosition(-x_end*2, y_end*2,z_end*2)
light_green.SetColor(0.3, 1.0, 0.3)
light_green.SetIntensity(1.0)
#renderer.AddLight(light_green)

light_green2 = vtk.vtkLight()
light_green2.SetPositional(1)
light_green2.SetPosition(-x_end*2+1000, y_end*2,z_end*2)
light_green2.SetColor(0.8, 0.8, 0.8)
light_green2.SetIntensity(1.4)
renderer.AddLight(light_green2)

light_green3 = vtk.vtkLight()
light_green3.SetPositional(1)
light_green3.SetPosition(-x_end*2, y_end*2+1000,z_end*2+1000)
light_green3.SetColor(0.8, 0.8, 0.8)
light_green3.SetIntensity(1.7)
renderer.AddLight(light_green3)






print('Ajout de img...')
data_matrix = io.imread('/home/fernandr/Bureau/Test/Visu/D0_bit_hr.tif')
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
surface.SetValue( 0, 117.5 )      #########################"
geoBoneMapper = vtk.vtkPolyDataMapper()
geoBoneMapper.SetInputConnection(surface.GetOutputPort() )
geoBoneMapper.ScalarVisibilityOff()
actorBoneImg = vtk.vtkLODActor()
actorBoneImg.SetNumberOfCloudPoints( 100000 )
actorBoneImg.SetMapper( geoBoneMapper )
actorBoneImg.GetProperty().SetColor( 0.5, 0.5, 0.5 )   ##############""
actorBoneImg.GetProperty().SetOpacity(1.0 )   ##############""
actorBoneImg.GetProperty().SetInterpolationToGouraud ()   ##############""
#actorBoneImg.GetProperty().SetSpecularColor(0.9,1,0.9)   ##############""
actorBoneImg.GetProperty().SetSpecular(0.2)   ##############""
actorBoneImg.GetProperty().SetDiffuseColor(0.5,0.5,0.5)   ##############""
actorBoneImg.GetProperty().SetDiffuse(0.4)   ##############""
actorBoneImg.GetProperty().SetAmbientColor(0.5,0.5,0.5)   ##############""
actorBoneImg.GetProperty().SetAmbient(0.18)   ##############""

renderer.AddActor(actorBoneImg)




print('Ajout de img...')
data_matrix = io.imread('/home/fernandr/Bureau/Test/Visu/D0_bit_hr.tif')
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
surface.SetValue( 0, 117.5 )      #########################"
geoBoneMapper = vtk.vtkPolyDataMapper()
geoBoneMapper.SetInputConnection(surface.GetOutputPort() )
geoBoneMapper.ScalarVisibilityOff()
actorBoneImg = vtk.vtkLODActor()
actorBoneImg.SetNumberOfCloudPoints( 100000 )
actorBoneImg.SetMapper( geoBoneMapper )
actorBoneImg.GetProperty().SetColor( 0.5, 0.5, 0.5 )   ##############""
actorBoneImg.GetProperty().SetOpacity(1.0 )   ##############""
actorBoneImg.GetProperty().SetInterpolationToGouraud ()   ##############""
#actorBoneImg.GetProperty().SetSpecularColor(0.9,1,0.9)   ##############""
actorBoneImg.GetProperty().SetSpecular(0.2)   ##############""
actorBoneImg.GetProperty().SetDiffuseColor(0.5,0.5,0.5)   ##############""
actorBoneImg.GetProperty().SetDiffuse(0.4)   ##############""
actorBoneImg.GetProperty().SetAmbientColor(0.5,0.5,0.5)   ##############""
actorBoneImg.GetProperty().SetAmbient(0.18)   ##############""

renderer.AddActor(actorBoneImg)





print('Ajout de img...')
data_matrix = io.imread('/home/fernandr/Bureau/Test/Visu/D0_bit_hr.tif')
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
surface.SetValue( 0, 117.5 )      #########################"
geoBoneMapper = vtk.vtkPolyDataMapper()
geoBoneMapper.SetInputConnection(surface.GetOutputPort() )
geoBoneMapper.ScalarVisibilityOff()
actorBoneImg = vtk.vtkLODActor()
actorBoneImg.SetNumberOfCloudPoints( 100000 )
actorBoneImg.SetMapper( geoBoneMapper )
actorBoneImg.GetProperty().SetColor( 0.5, 0.5, 0.5 )   ##############""
actorBoneImg.GetProperty().SetOpacity(1.0 )   ##############""
actorBoneImg.GetProperty().SetInterpolationToGouraud ()   ##############""
#actorBoneImg.GetProperty().SetSpecularColor(0.9,1,0.9)   ##############""
actorBoneImg.GetProperty().SetSpecular(0.2)   ##############""
actorBoneImg.GetProperty().SetDiffuseColor(0.5,0.5,0.5)   ##############""
actorBoneImg.GetProperty().SetDiffuse(0.4)   ##############""
actorBoneImg.GetProperty().SetAmbientColor(0.5,0.5,0.5)   ##############""
actorBoneImg.GetProperty().SetAmbient(0.18)   ##############""

renderer.AddActor(actorBoneImg)







print('Ajout de D3...')
data_D3 = io.imread('/home/fernandr/Bureau/Test/Visu/segD3.tif')
dataImporter = vtk.vtkImageImport()
data_string = data_D3.tostring()
dataImporter.CopyImportVoidPointer(data_string, len(data_string))
dataImporter.SetDataScalarTypeToUnsignedChar()
dataImporter.SetNumberOfScalarComponents(1)
dataImporter.SetDataExtent(0, x_end-1, 0, y_end-1, 0, z_end-1)
dataImporter.SetWholeExtent(0,x_end-1, 0, y_end-1, 0, z_end-1)
dataImporter.SetDataSpacing( 1,1,1 )
surface = vtk.vtkMarchingCubes()
surface.SetInputConnection( dataImporter.GetOutputPort() )
surface.ComputeNormalsOn()
surface.SetValue( 0, 127.5 )      #########################"
decimate = vtk.vtkDecimatePro();
decimate.SetInputConnection(surface.GetOutputPort());
#decimate.SetFeatureAngle(60.0);
#decimate.SetMaximumError(1);
decimate.SetTargetReduction(0.5);
geoBoneMapper = vtk.vtkPolyDataMapper()
geoBoneMapper.SetInputConnection(decimate.GetOutputPort() )
geoBoneMapper.ScalarVisibilityOff()
actorBone3 = vtk.vtkLODActor()
actorBone3.SetNumberOfCloudPoints( 100000 )
actorBone3.SetMapper( geoBoneMapper )
actorBone3.GetProperty().SetColor( 0.93, 0.1, 0.1 )   ##############""
actorBone3.GetProperty().SetOpacity(0.45 )   ##############""
actorBone3.GetProperty().SetInterpolationToGouraud ()   ##############""
#actorBone3.GetProperty().SetSpecularColor(0.9,1,0.9)   ##############""
actorBone3.GetProperty().SetSpecular(0.5)   ##############""
actorBone3.GetProperty().SetDiffuseColor(0.95,0.1,0.1)   ##############""
actorBone3.GetProperty().SetDiffuse(0.4)   ##############""
actorBone3.GetProperty().SetAmbientColor(1.0,0.1,0.1)   ##############""
actorBone3.GetProperty().SetAmbient(0.4)   ##############""

renderer.AddActor(actorBone3)





print('Ajout de D2...')
data_D2 = io.imread('/home/fernandr/Bureau/Test/Visu/segD2.tif')
dataImporter = vtk.vtkImageImport()
data_string = data_D2.tostring()
dataImporter.CopyImportVoidPointer(data_string, len(data_string))
dataImporter.SetDataScalarTypeToUnsignedChar()
dataImporter.SetNumberOfScalarComponents(1)
dataImporter.SetDataExtent(0, x_end-1, 0, y_end-1, 0, z_end-1)
dataImporter.SetWholeExtent(0,x_end-1, 0, y_end-1, 0, z_end-1)
dataImporter.SetDataSpacing( 1,1,1 )
surface = vtk.vtkMarchingCubes()
surface.SetInputConnection( dataImporter.GetOutputPort() )
surface.ComputeNormalsOn()
surface.SetValue( 0, 128.5 )      #########################"
geoBoneMapper = vtk.vtkPolyDataMapper()
geoBoneMapper.SetInputConnection( surface.GetOutputPort() )
geoBoneMapper.ScalarVisibilityOff()
actorBone2 = vtk.vtkLODActor()
actorBone2.SetNumberOfCloudPoints( 100000 )
actorBone2.SetMapper( geoBoneMapper )
actorBone2.GetProperty().SetColor( 1.0, 1.0, 0.1 )   ##############""
actorBone2.GetProperty().SetOpacity( 0.55 )   ##############""
actorBone2.GetProperty().SetInterpolationToGouraud ()   ##############""
#actorBone2.GetProperty().SetSpecularColor(0.9,0.1,0.1)   ##############""
actorBone2.GetProperty().SetSpecular(0.4)   ##############""
actorBone2.GetProperty().SetDiffuseColor(1.0,1.0,0.1)   ##############""
actorBone2.GetProperty().SetDiffuse(0.4)   ##############""
actorBone2.GetProperty().SetAmbientColor(1.0,1.0,0.1)   ##############""
actorBone2.GetProperty().SetAmbient(0.18)   ##############""
renderer.AddActor(actorBone2)


print('Ajout de D0...')
data_D0 = io.imread('/home/fernandr/Bureau/Test/Visu/segD0.tif')
dataImporter = vtk.vtkImageImport()
data_string = data_D0.tostring()
dataImporter.CopyImportVoidPointer(data_string, len(data_string))
dataImporter.SetDataScalarTypeToUnsignedChar()
dataImporter.SetNumberOfScalarComponents(1)
dataImporter.SetDataExtent(0, x_end-1, 0, y_end-1, 0, z_end-1)
dataImporter.SetWholeExtent(0,x_end-1, 0, y_end-1, 0, z_end-1)
dataImporter.SetDataSpacing( 1,1,1 )
surface = vtk.vtkMarchingCubes()
surface.SetInputConnection( dataImporter.GetOutputPort() )
surface.ComputeNormalsOn()
surface.SetValue( 0, 179.5 )      #########################"
geoBoneMapper = vtk.vtkPolyDataMapper()
geoBoneMapper.SetInputConnection( surface.GetOutputPort() )
geoBoneMapper.ScalarVisibilityOff()
actorBone0 = vtk.vtkLODActor()
actorBone0.SetNumberOfCloudPoints( 100000 )
actorBone0.SetMapper( geoBoneMapper )
actorBone0.GetProperty().SetColor( 0.9, 0.9, 0.9 )   ##############""
actorBone0.GetProperty().SetOpacity( 0.7 )   ##############""
actorBone0.GetProperty().SetInterpolationToGouraud ()   ##############""
#actorBone0.GetProperty().SetSpecularColor(0.9,2,0.9)   ##############""
actorBone0.GetProperty().SetSpecular(0.4)   ##############""
actorBone0.GetProperty().SetDiffuseColor(0.9, 0.9, 0.9)   ##############""
actorBone0.GetProperty().SetDiffuse(0.5)   ##############""
actorBone0.GetProperty().SetAmbientColor(0.9, 0.9, 0.9)   ##############""
actorBone0.GetProperty().SetAmbient(0.18)   ##############""
renderer.AddActor(actorBone0)












camera =vtk.vtkCamera ();
camera.SetPosition(x_end*1.5, y_end*1.5,z_end*1.5);
camera.SetFocalPoint(x_end/2,y_end/2, z_end/2);
camera.Azimuth(4)
camera.SetFocalPoint(x_end/2,y_end/2, z_end/2);
camera.Roll(-103)
renderer.SetActiveCamera(camera);


renderer.SetBackground(0,0,0)
renWin.SetSize(1500,800)

def CheckAbort(obj, event):
    if obj.GetEventPending() != 0:
        obj.SetAbortRender(1)

renWin.AddObserver("AbortCheckEvent", CheckAbort)

iren.Initialize()
renWin.Render()
iren.Start()

