#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jul  3 00:15:26 2019

@author: fernandr
"""
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()
import vtk
from skimage import io

def add_data_to_renderer_3d(renderer) :
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
    r=0.922
    g=0.804
    b= 0.72
    data_matrix0 = io.imread(source_rep+'D0_moelle_gauss.tif')
    data_matrix0[z_last:size,y_last:size,:]=0
    data_matrix0[z_end_irm:size+1,:,:]=0
    data_matrix0[0:z_begin_irm,:,:]=0
    dataImporter0 = vtk.vtkImageImport()
    data_string0 = data_matrix0.tostring()
    dataImporter0.CopyImportVoidPointer(data_string0, len(data_string0))
    dataImporter0.SetDataScalarTypeToUnsignedChar()
    dataImporter0.SetNumberOfScalarComponents(1)
    dataImporter0.SetDataExtent(0, x_end-1, 0, y_end-1, 0, z_end-1)
    dataImporter0.SetWholeExtent(0,x_end-1, 0, y_end-1, 0, z_end-1)
    dataImporter0.SetDataSpacing( 1,1,1 )
    surface0 = vtk.vtkContourFilter()
    surface0.SetInputConnection( dataImporter0.GetOutputPort() )
    surface0.ComputeNormalsOn()
    surface0.SetValue( 0, 127.5 )      #########################"
    geoBoneMapper0 = vtk.vtkPolyDataMapper()
    geoBoneMapper0.SetInputConnection(surface0.GetOutputPort() )
    geoBoneMapper0.ScalarVisibilityOff()
    actorBoneImg0 = vtk.vtkLODActor()
    actorBoneImg0.SetMapper( geoBoneMapper0 )
    actorBoneImg0.GetProperty().SetColor( r, g, b)   ##############""
    actorBoneImg0.GetProperty().SetOpacity(1.0 )   ##############""
    actorBoneImg0.GetProperty().SetInterpolationToGouraud ()   ##############""
    #actorBoneImgMoelle.GetProperty().SetSpecularColor(0.9,0.9,0.9)   ##############""
    actorBoneImg0.GetProperty().SetSpecular(0.2)   ##############""
    actorBoneImg0.GetProperty().SetDiffuseColor( r, g, b )   ##############""
    actorBoneImg0.GetProperty().SetDiffuse(0.3)   ##############""
    actorBoneImg0.GetProperty().SetAmbientColor( r, g, b )   ##############""
    actorBoneImg0.GetProperty().SetAmbient(0.18)   ##############""
    renderer.AddActor(actorBoneImg0)
    
    
    
    
    
    print('Ajout de img...')
    data_matrix2 = io.imread(source_rep+'D0_camb_gauss4.tif')
    r=0.712
    g=0.554
    b= 0.5
    data_matrix2[z_last:size,y_last:size,:]=0
    data_matrix2[z_end_irm:size+1,:,:]=0
    data_matrix2[0:z_begin_irm,:,:]=0
    dataImporter2 = vtk.vtkImageImport()
    data_string2 = data_matrix2.tostring()
    dataImporter2.CopyImportVoidPointer(data_string2, len(data_string2))
    dataImporter2.SetDataScalarTypeToUnsignedChar()
    dataImporter2.SetNumberOfScalarComponents(1)
    dataImporter2.SetDataExtent(0, x_end-1, 0, y_end-1, 0, z_end-1)
    dataImporter2.SetWholeExtent(0,x_end-1, 0, y_end-1, 0, z_end-1)
    dataImporter2.SetDataSpacing( 1,1,1 )
    surface2 = vtk.vtkContourFilter()
    surface2.SetInputConnection( dataImporter2.GetOutputPort() )
    surface2.ComputeNormalsOn()
    surface2.SetValue( 0, 57.5 )      #########################"
    geoBoneMapper2 = vtk.vtkPolyDataMapper()
    geoBoneMapper2.SetInputConnection(surface2.GetOutputPort() )
    geoBoneMapper2.ScalarVisibilityOff()
    actorBoneImg2 = vtk.vtkActor()
    actorBoneImg2.SetMapper( geoBoneMapper2)
    actorBoneImg2.GetProperty().SetColor(r,g,b )   ##############""
    actorBoneImg2.GetProperty().SetOpacity(1.0 )   ##############""
    actorBoneImg2.GetProperty().SetInterpolationToGouraud ()   ##############""
    actorBoneImg2.GetProperty().SetSpecularColor(0.8,0.6,0.6)   ##############""
    actorBoneImg2.GetProperty().SetSpecular(0.2)   ##############""
    actorBoneImg2.GetProperty().SetDiffuseColor(r,g,b)   ##############""
    actorBoneImg2.GetProperty().SetDiffuse(0.4)   ##############""
    actorBoneImg2.GetProperty().SetAmbientColor(r,g,b)   ##############""
    actorBoneImg2.GetProperty().SetAmbient(0.18)   ##############""

    renderer.AddActor(actorBoneImg2)
    
    
    
    
    
    # VAISSEAUX
    
    print('Ajout de img...')
    r=0.576
    g=0.688
    b= 0.412
    data_matrix3 = io.imread(source_rep+'D0_vaisseaux_gauss2.tif')
    data_matrix3[z_last:size,y_last:size,:]=0
    data_matrix3[z_end_irm:size+1,:,:]=0
    data_matrix3[0:z_begin_irm,:,:]=0
    dataImporter3 = vtk.vtkImageImport()
    data_string3 = data_matrix3.tostring()
    dataImporter3.CopyImportVoidPointer(data_string3, len(data_string3))
    dataImporter3.SetDataScalarTypeToUnsignedChar()
    dataImporter3.SetNumberOfScalarComponents(1)
    dataImporter3.SetDataExtent(0, x_end-1, 0, y_end-1, 0, z_end-1)
    dataImporter3.SetWholeExtent(0,x_end-1, 0, y_end-1, 0, z_end-1)
    dataImporter3.SetDataSpacing( 1,1,1 )
    surface3 = vtk.vtkContourFilter()
    surface3.SetInputConnection( dataImporter3.GetOutputPort() )
    surface3.ComputeNormalsOn()
    surface3.SetValue( 0, 192.5 )      #########################"
    surface3.Update()
    geoBoneMapper3 = vtk.vtkPolyDataMapper()
    geoBoneMapper3.SetInputConnection(surface3.GetOutputPort() )
    geoBoneMapper3.ScalarVisibilityOff()
    actorBoneImg3 = vtk.vtkActor()
    actorBoneImg3.SetMapper( geoBoneMapper3 )
    actorBoneImg3.GetProperty().SetColor( r,g,b )  
    actorBoneImg3.GetProperty().SetOpacity(1.0 ) 
    actorBoneImg3.GetProperty().SetInterpolationToGouraud () 
    actorBoneImg3.GetProperty().SetSpecularColor(0.8,0.9,0.7)  
    actorBoneImg3.GetProperty().SetSpecular(0.3) 
    actorBoneImg3.GetProperty().SetDiffuseColor(r,g,b) 
    actorBoneImg3.GetProperty().SetDiffuse(0.3)  
    actorBoneImg3.GetProperty().SetAmbientColor(r,g,b)   
    actorBoneImg3.GetProperty().SetAmbient(0.1)  
    
    renderer.AddActor(actorBoneImg3)
    
    
    
    
    
    
    print('Ajout de D3...')
    r=1.0
    g=0.1
    b=0.1
    data_D3 = io.imread(source_rep+'D3_mush_to_size.tif')
    data_D3[z_end_irm:size+1,:,:]=0
    data_D3[0:z_begin_irm,:,:]=0
    dataImporter4 = vtk.vtkImageImport()
    data_string4 = data_D3.tostring()
    dataImporter4.CopyImportVoidPointer(data_string4, len(data_string4))
    dataImporter4.SetDataScalarTypeToUnsignedChar()
    dataImporter4.SetNumberOfScalarComponents(1)
    dataImporter4.SetDataExtent(0, x_end-1, 0, y_end-1, 0, z_end-1)
    dataImporter4.SetWholeExtent(0,x_end-1, 0, y_end-1, 0, z_end-1)
    dataImporter4.SetDataSpacing( 1,1,1 )
    surface4 = vtk.vtkMarchingCubes()
    surface4.SetInputConnection( dataImporter4.GetOutputPort() )
    surface4.ComputeNormalsOn()
    surface4.SetValue( 0, 117.5 )      #########################"
    geoBoneMapper4 = vtk.vtkPolyDataMapper()
    geoBoneMapper4.SetInputConnection(surface4.GetOutputPort() )
    geoBoneMapper4.ScalarVisibilityOff()
    actorBone4 = vtk.vtkActor()
    actorBone4.SetMapper( geoBoneMapper4 )
    actorBone4.GetProperty().SetColor(r,g,b )   ##############""
    actorBone4.GetProperty().SetOpacity(0.35 )   ##############""
    actorBone4.GetProperty().SetInterpolationToGouraud ()   ##############""
    #actorBone3.GetProperty().SetSpecularColor(0.9,1,0.9)   ##############""
    actorBone4.GetProperty().SetSpecular(0.3)   ##############""
    actorBone4.GetProperty().SetDiffuseColor(r,g,b)   ##############""
    actorBone4.GetProperty().SetDiffuse(0.4)   ##############""
    actorBone4.GetProperty().SetAmbientColor(r,g,b)   ##############""
    actorBone4.GetProperty().SetAmbient(0.4)   ##############""
    
    renderer.AddActor(actorBone4)
    
    
    
    
    
    
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
    return renderer



def create_light(renderer):
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
    return renderer

def create_light2(renderer):
    x_end=512
    y_end=512
    z_end=512
    # create a green light
    light_green = vtk.vtkLight()
    light_green.SetPositional(1)
    light_green.SetPosition(-x_end*2, y_end*2,z_end*2)
    light_green.SetColor(1.0, 1.0, 1.0)
    light_green.SetIntensity(1.0)
    renderer.AddLight(light_green)
    return renderer