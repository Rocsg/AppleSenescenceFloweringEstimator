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

def add_data_to_renderer(renderer) :
    source_rep='/mnt/DD_COMMON/Data_VITIMAGE/'
    x_end=512
    y_end=512
    z_end=512
    z_last=230
    y_last=260
    size=511
    z_end_irm=300
    
    print('Ajout de moelle...')
    r=0.922
    g=0.804
    b= 0.72
    data_matrix0 = io.imread(source_rep+'moelle_gauss.tif')
    data_matrix0[z_last:size,y_last:size,:]=0
    data_matrix0[z_end_irm:size,:,:]=0
    data_matrix0[0:100,:,:]=0
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
    surface0.SetValue( 0, 100.5 )      #########################"
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
    actorBoneImg0.GetProperty().SetDiffuse(0.4)   ##############""
    actorBoneImg0.GetProperty().SetAmbientColor( r, g, b )   ##############""
    actorBoneImg0.GetProperty().SetAmbient(0.18)   ##############""
    renderer.AddActor(actorBoneImg0)
    
    
    
    
    print('Ajout de img...')
    r=0.516
    g=0.992
    b= 0.528
    data_matrix1 = io.imread(source_rep+'cambium_only.tif')
    data_matrix1[z_last:size,y_last:size,:]=0
    data_matrix1[z_end_irm:size,:,:]=0
    data_matrix1[0:100,:,:]=0
    dataImporter1 = vtk.vtkImageImport()
    data_string1 = data_matrix1.tostring()
    dataImporter1.CopyImportVoidPointer(data_string1, len(data_string1))
    dataImporter1.SetDataScalarTypeToUnsignedChar()
    dataImporter1.SetNumberOfScalarComponents(1)
    dataImporter1.SetDataExtent(0, x_end-1, 0, y_end-1, 0, z_end-1)
    dataImporter1.SetWholeExtent(0,x_end-1, 0, y_end-1, 0, z_end-1)
    dataImporter1.SetDataSpacing( 1,1,1 )
    surface1 = vtk.vtkFlyingEdges3D()
    surface1.ComputeNormalsOn()
    surface1.ComputeGradientsOn()
    surface1.SetInputConnection( dataImporter1.GetOutputPort() )
    surface1.SetValue( 0, 80.5 )      #########################"
    geoBoneMapper1 = vtk.vtkPolyDataMapper()
    geoBoneMapper1.SetInputConnection(surface1.GetOutputPort() )
    geoBoneMapper1.ScalarVisibilityOff()
    actorBoneImg1 = vtk.vtkActor()
    actorBoneImg1.SetMapper( geoBoneMapper1 )
    actorBoneImg1.GetProperty().SetColor(r, g, b )   ##############""
    actorBoneImg1.GetProperty().SetOpacity(1.0 )   ##############""
    actorBoneImg1.GetProperty().SetInterpolationToGouraud ()   ##############""
    #actorBoneImgCambium.GetProperty().SetSpecularColor(0.9,0.9,0.9)   ##############""
    actorBoneImg1.GetProperty().SetSpecular(0.2)   ##############""
    actorBoneImg1.GetProperty().SetDiffuseColor(r, g, b)   ##############""
    actorBoneImg1.GetProperty().SetDiffuse(0.4)   ##############""
    actorBoneImg1.GetProperty().SetAmbientColor(r, g, b)   ##############""
    actorBoneImg1.GetProperty().SetAmbient(0.18)   ##############""
    renderer.AddActor(actorBoneImg1)
    
    
    print('Ajout de img...')
    data_matrix2 = io.imread(source_rep+'liber_only_sur_D1.tif')


    r=0.612
    g=0.404
    b= 0.3
    bmpReader = vtk.vtkBMPReader()
    bmpReader.SetFileName("/home/fernandr/Bureau/masonry.BMP")
    atext = vtk.vtkTexture()
    atext.SetInputConnection(bmpReader.GetOutputPort())
    atext.InterpolateOn()

    data_matrix2[z_last:size,y_last:size,:]=0
    data_matrix2[z_end_irm:size,:,:]=0
    data_matrix2[0:100,:,:]=0
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
    surface2.SetValue( 0, 100.5 )      #########################"
    geoBoneMapper2 = vtk.vtkPolyDataMapper()
    geoBoneMapper2.SetInputConnection(surface2.GetOutputPort() )
    geoBoneMapper2.ScalarVisibilityOff()

#    tmapper = vtk.vtkTextureMapToCylinder()
    #    tmapper.SetInputConnection(surface1.GetOutputPort())
#    tmapper.SetInputConnection(geoBoneMapper2.GetOutputPort())
#    tmapper.PreventSeamOn()
    
    
    # We scale the texture coordinate to get some repeat patterns.
#    xform = vtk.vtkTransformTextureCoords()
#    xform.SetInputConnection(tmapper.GetOutputPort())
#    xform.SetScale(4, 4, 1)
    
#    mapper = vtk.vtkDataSetMapper()
#    mapper.SetInputConnection(xform.GetOutputPort())
    
##    triangulation = vtk.vtkActor()
#    triangulation.SetMapper(mapper)
#    triangulation.SetTexture(atext)

    actorBoneImg2 = vtk.vtkActor()
    actorBoneImg2.SetMapper( geoBoneMapper2 )
 
    actorBoneImg2.GetProperty().SetColor(r,g,b )   ##############""
    actorBoneImg2.GetProperty().SetOpacity(0.8 )   ##############""
    actorBoneImg2.GetProperty().SetInterpolationToGouraud ()   ##############""
    #actorBoneImgLiber.GetProperty().SetSpecularColor(0.9,0.9,0.9)   ##############""
    actorBoneImg2.GetProperty().SetSpecular(0.2)   ##############""
    actorBoneImg2.GetProperty().SetDiffuseColor(r,g,b)   ##############""
    actorBoneImg2.GetProperty().SetDiffuse(0.4)   ##############""
    actorBoneImg2.GetProperty().SetAmbientColor(r,g,b)   ##############""
    actorBoneImg2.GetProperty().SetAmbient(0.18)   ##############""
    actorBoneImg2.SetTexture( atext )

    renderer.AddActor(actorBoneImg2)
    
    
    
    
    
    # VAISSEAUX
    
    print('Ajout de img...')
    r=0.576
    g=0.688
    b= 0.412
    data_matrix3 = io.imread(source_rep+'vaisseaux.tif')
    data_matrix3[z_last:size,y_last:size,:]=0
    data_matrix3[z_end_irm:size,:,:]=0
    data_matrix3[0:100,:,:]=0
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
    surface3.SetValue( 0, 127.5 )      #########################"
    surface3.Update()
    geoBoneMapper3 = vtk.vtkPolyDataMapper()
    geoBoneMapper3.SetInputConnection(surface3.GetOutputPort() )
    geoBoneMapper3.ScalarVisibilityOff()
    actorBoneImg3 = vtk.vtkActor()
    actorBoneImg3.SetMapper( geoBoneMapper3 )
    actorBoneImg3.GetProperty().SetColor( r,g,b )  
    actorBoneImg3.GetProperty().SetOpacity(1.0 ) 
    actorBoneImg3.GetProperty().SetInterpolationToGouraud () 
    actorBoneImg3.GetProperty().SetSpecularColor(0.9,0.9,0.9)  
    actorBoneImg3.GetProperty().SetSpecular(0.3) 
    actorBoneImg3.GetProperty().SetDiffuseColor(r,g,b) 
    actorBoneImg3.GetProperty().SetDiffuse(0.3)  
    actorBoneImg3.GetProperty().SetAmbientColor(r,g,b)   
    actorBoneImg3.GetProperty().SetAmbient(0.1)  
    
    renderer.AddActor(actorBoneImg3)
    
    
    
    
    
    
    
    print('Ajout de D3...')
    data_D3 = io.imread(source_rep+'segD3.tif')
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
    surface4.SetValue( 0, 127.5 )      #########################"
    geoBoneMapper4 = vtk.vtkPolyDataMapper()
    geoBoneMapper4.SetInputConnection(surface4.GetOutputPort() )
    geoBoneMapper4.ScalarVisibilityOff()
    actorBone4 = vtk.vtkActor()
    actorBone4.SetMapper( geoBoneMapper4 )
    actorBone4.GetProperty().SetColor( 0.93, 0.1, 0.1 )   ##############""
    actorBone4.GetProperty().SetOpacity(0.65 )   ##############""
    actorBone4.GetProperty().SetInterpolationToGouraud ()   ##############""
    #actorBone3.GetProperty().SetSpecularColor(0.9,1,0.9)   ##############""
    actorBone4.GetProperty().SetSpecular(0.5)   ##############""
    actorBone4.GetProperty().SetDiffuseColor(0.95,0.1,0.1)   ##############""
    actorBone4.GetProperty().SetDiffuse(0.4)   ##############""
    actorBone4.GetProperty().SetAmbientColor(1.0,0.1,0.1)   ##############""
    actorBone4.GetProperty().SetAmbient(0.4)   ##############""
    
    renderer.AddActor(actorBone4)
    
    
    
    
    
    print('Ajout de D2...')
    data_D2 = io.imread(source_rep+'segD2.tif')
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
    surface5.SetValue( 0, 128.5 )      #########################"
    geoBoneMapper5 = vtk.vtkPolyDataMapper()
    geoBoneMapper5.SetInputConnection( surface5.GetOutputPort() )
    geoBoneMapper5.ScalarVisibilityOff()
    actorBone5 = vtk.vtkActor()
    actorBone5.SetMapper( geoBoneMapper5 )
    actorBone5.GetProperty().SetColor( 1.0, 1.0, 0.1 )   ##############""
    actorBone5.GetProperty().SetOpacity( 0.85 )   ##############""
    actorBone5.GetProperty().SetInterpolationToGouraud ()   ##############""
    #actorBone2.GetProperty().SetSpecularColor(0.9,0.1,0.1)   ##############""
    actorBone5.GetProperty().SetSpecular(0.4)   ##############""
    actorBone5.GetProperty().SetDiffuseColor(1.0,1.0,0.1)   ##############""
    actorBone5.GetProperty().SetDiffuse(0.4)   ##############""
    actorBone5.GetProperty().SetAmbientColor(1.0,1.0,0.1)   ##############""
    actorBone5.GetProperty().SetAmbient(0.18)   ##############""
    renderer.AddActor(actorBone5)

    renderer.ResetCamera()


    return renderer



def create_light(renderer):
    x_end=512
    y_end=512
    z_end=512
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