#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 10:53:18 2019

@author: fernandr
"""


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
z_last=230
y_last=260
size=511
z_end_irm=300


renderer = vtk.vtkOpenGLRenderer()



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






print('Ajout de moelle...')
r=0.922
g=0.804
b= 0.72
data_matrix = io.imread('/home/fernandr/Bureau/Test/Visu/moelle_gauss.tif')
data_matrix[z_last:size,y_last:size,:]=0
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
surface = vtk.vtkContourFilter()
surface.SetInputConnection( dataImporter.GetOutputPort() )
surface.ComputeNormalsOn()
surface.SetValue( 0, 120.5 )      #########################"
geoBoneMapper = vtk.vtkOpenGLPolyDataMapper()
geoBoneMapper.SetInputConnection(surface.GetOutputPort() )
geoBoneMapper.ScalarVisibilityOff()
actorBoneImgMoelle = vtk.vtkLODActor()
actorBoneImgMoelle.SetMapper( geoBoneMapper )
actorBoneImgMoelle.GetProperty().SetColor( r, g, b)   ##############""
actorBoneImgMoelle.GetProperty().SetOpacity(1.0 )   ##############""
actorBoneImgMoelle.GetProperty().SetInterpolationToGouraud ()   ##############""
#actorBoneImgMoelle.GetProperty().SetSpecularColor(0.9,0.9,0.9)   ##############""
actorBoneImgMoelle.GetProperty().SetSpecular(0.2)   ##############""
actorBoneImgMoelle.GetProperty().SetDiffuseColor( r, g, b )   ##############""
actorBoneImgMoelle.GetProperty().SetDiffuse(0.4)   ##############""
actorBoneImgMoelle.GetProperty().SetAmbientColor( r, g, b )   ##############""
actorBoneImgMoelle.GetProperty().SetAmbient(0.18)   ##############""
renderer.AddActor(actorBoneImgMoelle)




print('Ajout de img...')
data_matrix = io.imread('/home/fernandr/Bureau/Test/Visu/cambium_only.tif')
r=0.516
g=0.992
b= 0.528
data_matrix[z_last:size,y_last:size,:]=0
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
surface = vtk.vtkContourFilter()
surface.SetInputConnection( dataImporter.GetOutputPort() )
surface.ComputeNormalsOn()
surface.SetValue( 0, 120.5 )      #########################"
geoBoneMapper = vtk.vtkOpenGLPolyDataMapper()
geoBoneMapper.SetInputConnection(surface.GetOutputPort() )
geoBoneMapper.ScalarVisibilityOff()
actorBoneImgCambium = vtk.vtkOpenGLActor()
actorBoneImgCambium.SetMapper( geoBoneMapper )
actorBoneImgCambium.GetProperty().SetColor(r, g, b )   ##############""
actorBoneImgCambium.GetProperty().SetOpacity(1.0 )   ##############""
actorBoneImgCambium.GetProperty().SetInterpolationToGouraud ()   ##############""
#actorBoneImgCambium.GetProperty().SetSpecularColor(0.9,0.9,0.9)   ##############""
actorBoneImgCambium.GetProperty().SetSpecular(0.2)   ##############""
actorBoneImgCambium.GetProperty().SetDiffuseColor(r, g, b)   ##############""
actorBoneImgCambium.GetProperty().SetDiffuse(0.4)   ##############""
actorBoneImgCambium.GetProperty().SetAmbientColor(r, g, b)   ##############""
actorBoneImgCambium.GetProperty().SetAmbient(0.18)   ##############""
renderer.AddActor(actorBoneImgCambium)



print('Ajout de img...')
data_matrix = io.imread('/home/fernandr/Bureau/Test/Visu/liber_only.tif')
r=0.612
g=0.404
b= 0.3
data_matrix[z_last:size,y_last:size,:]=0
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
surface = vtk.vtkContourFilter()
surface.SetInputConnection( dataImporter.GetOutputPort() )
surface.ComputeNormalsOn()
surface.SetValue( 0, 120.5 )      #########################"
geoBoneMapper = vtk.vtkOpenGLPolyDataMapper()
geoBoneMapper.SetInputConnection(surface.GetOutputPort() )
geoBoneMapper.ScalarVisibilityOff()
actorBoneImgLiber = vtk.vtkOpenGLActor()
actorBoneImgLiber.SetMapper( geoBoneMapper )
actorBoneImgLiber.GetProperty().SetColor(r,g,b )   ##############""
actorBoneImgLiber.GetProperty().SetOpacity(1.0 )   ##############""
actorBoneImgLiber.GetProperty().SetInterpolationToGouraud ()   ##############""
#actorBoneImgLiber.GetProperty().SetSpecularColor(0.9,0.9,0.9)   ##############""
actorBoneImgLiber.GetProperty().SetSpecular(0.2)   ##############""
actorBoneImgLiber.GetProperty().SetDiffuseColor(r,g,b)   ##############""
actorBoneImgLiber.GetProperty().SetDiffuse(0.4)   ##############""
actorBoneImgLiber.GetProperty().SetAmbientColor(r,g,b)   ##############""
actorBoneImgLiber.GetProperty().SetAmbient(0.18)   ##############""
renderer.AddActor(actorBoneImgLiber)





# VAISSEAUX

print('Ajout de img...')
r=0.576
g=0.688
b= 0.412
data_matrix = io.imread('/home/fernandr/Bureau/Test/Visu/vaisseaux.tif')
data_matrix[z_last:size,y_last:size,:]=0
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
surface = vtk.vtkContourFilter()
surface.SetInputConnection( dataImporter.GetOutputPort() )
surface.ComputeNormalsOn()
surface.SetValue( 0, 127.5 )      #########################"
geoBoneMapper = vtk.vtkOpenGLPolyDataMapper()
geoBoneMapper.SetInputConnection(surface.GetOutputPort() )
geoBoneMapper.ScalarVisibilityOff()
actorBoneImgVaisseaux = vtk.vtkOpenGLActor()
actorBoneImgVaisseaux.SetMapper( geoBoneMapper )
actorBoneImgVaisseaux.GetProperty().SetColor( r,g,b )   ##############""
actorBoneImgVaisseaux.GetProperty().SetOpacity(1.0 )   ##############""
actorBoneImgVaisseaux.GetProperty().SetInterpolationToGouraud ()   ##############""
actorBoneImgVaisseaux.GetProperty().SetSpecularColor(0.9,0.9,0.9)   ##############""
actorBoneImgVaisseaux.GetProperty().SetSpecular(0.3)   ##############""
actorBoneImgVaisseaux.GetProperty().SetDiffuseColor(r,g,b)   ##############""
actorBoneImgVaisseaux.GetProperty().SetDiffuse(0.3)   ##############""
actorBoneImgVaisseaux.GetProperty().SetAmbientColor(r,g,b)   ##############""
actorBoneImgVaisseaux.GetProperty().SetAmbient(0.1)   ##############""

renderer.AddActor(actorBoneImgVaisseaux)







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
geoBoneMapper = vtk.vtkOpenGLPolyDataMapper()
geoBoneMapper.SetInputConnection(surface.GetOutputPort() )
geoBoneMapper.ScalarVisibilityOff()
actorBone3 = vtk.vtkOpenGLActor()
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
geoBoneMapper = vtk.vtkOpenGLPolyDataMapper()
geoBoneMapper.SetInputConnection( surface.GetOutputPort() )
geoBoneMapper.ScalarVisibilityOff()
actorBone2 = vtk.vtkOpenGLActor()
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














camera =vtk.vtkCamera ();
renderer.SetActiveCamera(camera);
camera.SetPosition(x_end*1.5, y_end*1.5,z_end*1.5);
camera.SetFocalPoint(x_end/2,y_end/2, z_end/2);
camera.Azimuth(14)
camera.SetFocalPoint(x_end/2,y_end/2, z_end/2);
camera.Roll(-103)


renderer.SetBackground(0,0,0)
renWin = vtk.vtkXOpenGLRenderWindow()
renWin.AddRenderer(renderer)
renWin.SetSize(1500,800)
def CheckAbort(obj, event):
    if obj.GetEventPending() != 0:
        obj.SetAbortRender(1)
        obj.Finalize()
        ir= obj.GetInteractor()
        ir.TerminateApp();
        del renWin,ir
renWin.AddObserver("AbortCheckEvent", CheckAbort)



rendu='movie'
#rendu='movie1'
if rendu=='movie1':
    print('execution partie movie 1')
    import time

    #Setup filter
    imageFilter = vtk.vtkWindowToImageFilter()
    imageFilter.SetInput(renWin)
    imageFilter.SetInputBufferTypeToRGB()
    imageFilter.ReadFrontBufferOff()
    imageFilter.Update()
    
    #Setup movie writer
    moviewriter = vtk.vtkOggTheoraWriter() 
    moviewriter.SetInputConnection(imageFilter.GetOutputPort())
    moviewriter.SetFileName("/home/fernandr/Bureau/Test/Visu/test.ogg")
    moviewriter.Start()


    print('ok first part')
    for i in range(100):
        if(i%100==0):
            print(str(i))
        time.sleep(0.001)
#        camera.SetPosition(x_end*1.5, y_end*1.5,z_end*1.5);
    #    camera.SetFocalPoint(x_end/2,y_end/2, z_end/2);
        camera.Azimuth(1/30)
 #       camera.SetFocalPoint(x_end/2,y_end/2, z_end/2);
    #    camera.Roll(-103)
        
        renWin.Render()
        #Export a single frame
        imageFilter.Modified()
        moviewriter.Write()
    #Finish movie
    moviewriter.End()
    



if rendu=='movie2':
    print('execution partie movie 2')
    import time
    print('ok first part')
    for i in range(10000):
        if(i%100==0):
            print(str(i))
        time.sleep(0.001)
        camera.SetPosition(x_end*1.5, y_end*1.5,z_end*1.5);
    #    camera.SetFocalPoint(x_end/2,y_end/2, z_end/2);
        camera.Azimuth(i/30)
        camera.SetFocalPoint(x_end/2,y_end/2, z_end/2);
    #    camera.Roll(-103)
        
        renWin.Render()



print('GL ?'+str(renWin.SupportsOpenGL()))
print('Direct ?'+str(renWin.IsDirect()))

iren = vtk.vtkRenderWindowInteractor()
iren.SetRenderWindow(renWin)
renWin.Start()
iren.Initialize()
iren.Start()

