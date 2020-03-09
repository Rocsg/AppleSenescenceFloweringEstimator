#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 13:29:55 2019

@author: fernandr
"""

""" 
######################################################################################################################################
#########  CONVERSION DONNEES VERS OBJETS 3D   #######################################################################################
######################################################################################################################################
 """
 
 
from view_camera_window_V08 import *



def build_actor_from_image(path_source,r,g,b,opac,spec,diff,amb,isoVal,crop_type=0,reduced_data_type=0,path_alternative=None,slice_min=-1,slice_max=-1):
    print('construction de l objet : '+str(path_source))
    print('caractéristiques (r , g, b, opac) : '+str(r)+' '+str(g)+' '+str(b)+' '+str(opac))
    print('croptype='+str(crop_type))
    
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    if(reduced_data_type==1):
        data_matrix=io.imread(path_alternative)
        data_matrix[:,:,:]=0
        mush=io.imread(path_source)
        data_matrix[80:380, 200:265, 64:235]=mush
    else:
        data_matrix = io.imread(path_source)
    data_matrix[z_start_crop:size_z,y_start_crop:size_y,0:x_start_crop]=0
#    if(slice_max+slice_min>0):
#        print('gestion slice min et max : '+str(slice_min)+' '+str(slice_max))
#        data_matrix[slice_max:size_z,:,:]=0
#        data_matrix[0:slice_min,:,:]=0
#    else :
#        print('pas de gestion de slice min et max')
    data_matrix[z_end_irm:size_z,:,:]=0
    data_matrix[0:z_begin_irm,:,:]=0
    print('avant importation, mean='+str(np.mean(data_matrix)))
    dataImporter = vtk.vtkImageImport()
    data_string = data_matrix.tostring()
    dataImporter.CopyImportVoidPointer(data_string, len(data_string))
    dataImporter.SetDataScalarTypeToUnsignedChar()
    dataImporter.SetNumberOfScalarComponents(1)
    dataImporter.SetDataExtent(0, size_x-1, 0, size_y-1, 0, size_z-1)
    dataImporter.SetWholeExtent(0, size_x-1, 0, size_y-1, 0, size_z-1)
    dataImporter.SetDataSpacing( 1,1,1 )
    surface = vtk.vtkMarchingCubes()
    surface.SetInputConnection( dataImporter.GetOutputPort() )
    surface.ComputeNormalsOn()
    surface.SetValue( 0, isoVal ) 
    geoBoneMapper = vtk.vtkPolyDataMapper()
    geoBoneMapper.SetInputConnection(surface.GetOutputPort())
    geoBoneMapper.ScalarVisibilityOff()
    geoBoneMapper.Update()
    actorCur = vtk.vtkLODActor()
    actorCur.SetMapper( geoBoneMapper )
    actorCur.GetProperty().SetColor( r, g, b) 
    actorCur.GetProperty().SetOpacity(opac )  
    actorCur.GetProperty().SetInterpolationToGouraud ()
    actorCur.GetProperty().SetSpecular(spec)
    actorCur.GetProperty().SetDiffuseColor( r, g, b )  
    actorCur.GetProperty().SetDiffuse(diff)  
    actorCur.GetProperty().SetAmbientColor( r, g, b )   
    actorCur.GetProperty().SetAmbient(amb)  
    return actorCur















def build_multi_planar_view_from_image(path_source,opac,renderer,crop_type):
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    data_matrix = io.imread(path_source)
    data_matrix[z_start_crop:size_z,y_start_crop:size_y,0:x_start_crop]=0
    data_matrix[z_end_irm:size_z,:,:]=0
    data_matrix[0:z_begin_irm,:,:]=0
    dataImporter = vtk.vtkImageImport()
    data_string = data_matrix.tostring()
    dataImporter.CopyImportVoidPointer(data_string, len(data_string))
    dataImporter.SetDataScalarTypeToUnsignedChar()
    dataImporter.SetNumberOfScalarComponents(1)
    dataImporter.SetDataExtent(0, size_x-1, 0, size_y-1, 0, size_z-1)
    dataImporter.SetWholeExtent(0, size_x-1, 0, size_y-1, 0, size_z-1)
    dataImporter.SetDataSpacing( 1,1,1 )
  
    bwLut=create_bw_lookup_table()
    YZ_colors = vtk.vtkImageMapToColors()
    YZ_colors.SetInputConnection(dataImporter.GetOutputPort())
    YZ_colors.SetLookupTable(bwLut)
    YZ_colors.Update()
    YZ_plane = vtk.vtkImageActor()
    YZ_plane.GetMapper().SetInputConnection(YZ_colors.GetOutputPort())
    YZ_plane.SetDisplayExtent(int(round(size_x/2)),int(round( size_x/2)), 0, size_y-1, 0, size_z-1)

    XY_colors = vtk.vtkImageMapToColors()
    XY_colors.SetInputConnection(dataImporter.GetOutputPort())
    XY_colors.SetLookupTable(bwLut)
    XY_colors.Update()
    XY_plane = vtk.vtkImageActor()
    XY_plane.GetMapper().SetInputConnection(XY_colors.GetOutputPort())
    XY_plane.SetDisplayExtent(0, size_x-1, 0, size_y-1, int(round(size_z/2)), int(round(size_z/2)))

    XZ_colors = vtk.vtkImageMapToColors()
    XZ_colors.SetInputConnection(dataImporter.GetOutputPort())
    XZ_colors.SetLookupTable(bwLut)
    XZ_colors.Update()
    XZ_plane = vtk.vtkImageActor()
    XZ_plane.GetMapper().SetInputConnection(XZ_colors.GetOutputPort())
    XZ_plane.SetDisplayExtent(0, size_x-1, int(round(size_y/2)), int(round(size_y/2)), 0, size_z-1)

    # Actors are added to the renderer.
    renderer.AddActor(XY_plane)
    renderer.AddActor(XZ_plane)
    renderer.AddActor(YZ_plane)

    # Note that when camera movement occurs (as it does in the Dolly()
    # method), the clipping planes often need adjusting. Clipping planes
    # consist of two planes: near and far along the view direction. The
    # near plane clips out objects in front of the plane; the far plane
    # clips out objects behind the plane. This way only what is drawn
    # between the planes is actually rendered.
#    aRenderer.ResetCameraClippingRange()
    return XY_plane,XZ_plane,YZ_plane



def build_planar_slice_from_RGBimage2(axis,path_source,opac,renderer):
    reader=vtk.vtkTIFFReader()
    reader.SetFileName(path_source)
    
    plane = vtk.vtkImageActor()
    plane.GetMapper().SetInputConnection(reader.GetOutputPort())
 
    # Actors are added to the renderer.
    renderer.AddActor(plane)
 
    return plane




def build_planar_slice_from_RGBimage(axis,path_source,opac,renderer):
    print("toto1")
    data_matrix = io.imread(path_source)
    
    dataImporter = vtk.vtkImageImport()
    data_string = data_matrix.tostring()
    print("toto2")
    dataImporter.CopyImportVoidPointer(data_string, len(data_string))
    dataImporter.SetDataScalarTypeToUnsignedChar()
    print("toto3")
    dataImporter.SetNumberOfScalarComponents(4)
    dataImporter.SetDataExtent(0, 720-1, 0, 300-1, 0, 0)
    print("toto4")
    dataImporter.SetWholeExtent(0, 720-1, 0, 300-1, 0, 0)
    dataImporter.SetDataSpacing( 1,1,1 )
    print("toto5")

    
    scalColors=vtk.vtkScalarsToColors()
    scalColors.SetVectorModeToRGBColors() 	
    print("toto6")
    scalColors.SetInputConnection(dataImporter.GetOutputPort())
    scalColors.Update()
    print("toto7")
    plane = vtk.vtkImageActor()
    plane.GetMapper().SetInputConnection(scalColors.GetOutputPort())
    print("toto8")

    # Actors are added to the renderer.
    renderer.AddActor(plane)
    print("toto9")

    return plane



def build_planar_view_from_image(axis,path_source,opac,renderer,crop_type,colormap=0):
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    data_matrix = io.imread(path_source)
    #data_matrix[z_start_crop:size_z,y_start_crop:size_y,0:x_start_crop]=0
    #data_matrix[z_end_irm:size_z,:,:]=0
    #data_matrix[0:z_begin_irm,:,:]=0
    print('avant importation, mean='+str(np.mean(data_matrix)))
    dataImporter = vtk.vtkImageImport()
    data_string = data_matrix.tostring()
    dataImporter.CopyImportVoidPointer(data_string, len(data_string))
    dataImporter.SetDataScalarTypeToUnsignedChar()
    dataImporter.SetNumberOfScalarComponents(1)
    dataImporter.SetDataExtent(0, size_x-1, 0, size_y-1, 0, size_z-1)
    dataImporter.SetWholeExtent(0, size_x-1, 0, size_y-1, 0, size_z-1)
    dataImporter.SetDataSpacing( 1,1,1 )
  
    lut=get_common_colormaps(colormap)

    colors = vtk.vtkImageMapToColors()
    colors.SetInputConnection(dataImporter.GetOutputPort())
    colors.SetLookupTable(lut)
    colors.Update()
    plane = vtk.vtkImageActor()
    plane.GetMapper().SetInputConnection(colors.GetOutputPort())
    set_slice(plane,axis)

    # Actors are added to the renderer.
    renderer.AddActor(plane)
    return plane



def set_slice(plane,axis,slice=-1,crop_type=0):
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    if(slice==-1):
        if(axis==0):
            slice=int(round(size_z/2))
        if(axis==1):
            slice=int(round(size_y/2))
        if(axis==2):
            slice=int(round(size_x/2))

    if(axis==0): #XY plane
        plane.SetDisplayExtent(slice,slice, 0, size_y-1,  z_begin_irm, z_end_irm)
    if(axis==1): #XZ plane
        plane.SetDisplayExtent(0,size_x-1, slice,slice, z_begin_irm, z_end_irm)
    if(axis==2): #YZ plane
        plane.SetDisplayExtent(0,size_x-1, 0, size_y-1, slice,slice)
    plane.GetMapper().Update()
    


def build_volume_rendering_view_from_image(path_source,opac,renderer,crop_type,zmin,zmax,colormap=0):
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    print('VR, construction de l objet : '+str(path_source))
    print('caractéristiques : (opac, zmin, zmax, colormap) '+str(opac)+' '+str(zmin)+' '+str(zmax)+' '+str(colormap))
    print('croptype='+str(crop_type))
    data_matrix = io.imread(path_source)
 #   data_matrix[z_start_crop:size_z,y_start_crop:size_y,0:x_start_crop]=0
 #   data_matrix[z_end_irm:size_z,:,:]=0
 #   data_matrix[0:z_begin_irm,:,:]=0
 #   data_matrix[zmax:size_z,:,:]=0
 #   data_matrix[0:zmin,:,:]=0
    print('avant importation, mean='+str(np.mean(data_matrix)))
    dataImporter = vtk.vtkImageImport()
    data_string = data_matrix.tostring()
    dataImporter.CopyImportVoidPointer(data_string, len(data_string))
    dataImporter.SetDataScalarTypeToUnsignedChar()
    dataImporter.SetNumberOfScalarComponents(1)
    dataImporter.SetDataExtent(0, size_x-1, 0, size_y-1, 0, size_z-1)
    dataImporter.SetWholeExtent(0, size_x-1, 0, size_y-1, 0, size_z-1)
    dataImporter.SetDataSpacing( 1,1,1 )
    print('apres importation, mean='+str(np.mean(data_matrix)))
  
    
    
    volumeMapper = vtk.vtkSmartVolumeMapper()
    volumeMapper.SetBlendModeToComposite()
    volumeMapper.SetInputConnection(dataImporter.GetOutputPort());
    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.ShadeOn()
  
    funcOpacityGradient = vtk.vtkPiecewiseFunction()
    funcOpacityGradient.AddPoint(1,   0.2)
    funcOpacityGradient.AddPoint(5,   0.4)
    funcOpacityGradient.AddPoint(100,   1.2)
    volumeProperty.SetGradientOpacity(funcOpacityGradient)
    
    compositeOpacity = vtk.vtkPiecewiseFunction()
    compositeOpacity.AddPoint(0.0,0.0);
    compositeOpacity.AddPoint(40.0,0.0);
    compositeOpacity.AddPoint(200.0,opac);
    compositeOpacity.AddPoint(255.0,opac);
    volumeProperty.SetScalarOpacity(compositeOpacity)
    volumeProperty.SetSpecular(0.3)
    volumeProperty.SetSpecularPower(100) 
    
    color = vtk.vtkColorTransferFunction()
    color.AddRGBPoint(0.0  ,0.0,0.0,0.0)
    color.AddRGBPoint(40.0  ,0.0,0.0,0.0)
    color.AddRGBPoint(255.0,1.0,1.0,1.0)

    volumeProperty.SetInterpolationTypeToLinear()    
    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)
    print('lut=')
    lut=get_common_colormaps(colormap)
    for i in range(256):
        print('BW lut i='+str(i)+'  ('+str(lut.GetTableValue(i)[0])+', '+str(lut.GetTableValue(i)[1])+', '+str(lut.GetTableValue(i)[2])+' ) ')
    set_volume_colormap(volume,lut)
    renderer.AddViewProp(volume)
    
#    volumeMapper.SetRequestedRenderModeToRayCastAndTexture()
    volumeMapper.SetRequestedRenderModeToRayCast()
    return volume

def text_actors_and_props_removed(texts,actors,props,renderer):
        if(texts != None):
            for textActor in texts:
                renderer.RemoveActor(textActor)        
        if(actors != None):
            for actor in actors:
                renderer.RemoveActor(actor)   
        if(props != None):
            for prop in props:
                renderer.RemoveViewProp(prop)   


    

def text_and_actors_disappearing(n_fra,text,actors,volumes,renderer,timestep,renWin,imageFilter,moviewriter,opacity_tuple=None):
    for i in range(n_fra):
        if(text != None):
            for textActor in text:
                textActor.GetTextProperty().SetOpacity ( (n_fra-1-i)/n_fra )        
        if(actors != None):
            for a in range(len(actors)):
                if(opacity_tuple != None):
                    actors[a].GetProperty().SetOpacity ( opacity_tuple[a]*(n_fra-1-i)/n_fra )
                else:
                    actors[a].GetProperty().SetOpacity ( 1*(n_fra-1-i)/n_fra )
        if(volumes != None):
            for volume in volumes:
                a=1                
        snapshot(timestep,renWin,imageFilter,moviewriter)


def add_text(text,x0,y0,police,opacity,day_max,mobile_rendering,renderer,r=1,g=1,b=1):
    textActor = vtk.vtkTextActor()
    textActor.SetInput (text)
    textActor.SetPosition (int(round(x0)),int(round(y0)))
    textActor.GetTextProperty().SetFontSize (police )
    textActor.GetTextProperty().SetFontFamilyToTimes()
    textActor.GetTextProperty().SetColor ( r,g,b )
    textActor.GetTextProperty().SetOpacity(opacity)
    renderer.AddActor2D ( textActor )   
    return textActor



def text_and_actors_appearing(n_fra,text,actors,a,renderer,timestep,renWin,imageFilter,moviewriter,opacity_tuple=None):
    for i in range(n_fra):
        if(text != None):
            text.GetTextProperty().SetOpacity ( (i+1)/n_fra )        
        if(actors != None):
            for a in range(len(actors)):
                if(opacity_tuple != None):
                    actors[a].GetProperty().SetOpacity ( opacity_tuple[a]*(i+1)/n_fra )
                else:
                    actors[a].GetProperty().SetOpacity ( 1*(i+1)/n_fra )

        snapshot(timestep,renWin,imageFilter,moviewriter)







































def build_volume_rendering_view_from_image2(path_source,opac,renderer,crop_type,zmin,zmax,colormap=0):
    z_begin_irm,z_end_irm,  x0,y0,z0,  xf,yf,zf,  size_x,size_y,size_z=get_image_constants_2(crop_type)
    print('VR, construction de l objet : '+str(path_source))
    print('caractéristiques : (opac, zmin, zmax, colormap) '+str(opac)+' '+str(zmin)+' '+str(zmax)+' '+str(colormap))
    print('croptype='+str(crop_type))
    data_matrix = io.imread(path_source)
    data_matrix[z0:zf,y0:yf,x0:xf]=0
    data_matrix[z_end_irm:size_z,:,:]=0
    data_matrix[0:z_begin_irm,:,:]=0
    data_matrix[zmax:size_z,:,:]=0
    data_matrix[0:zmin,:,:]=0
    print('avant importation, mean='+str(np.mean(data_matrix)))
    dataImporter = vtk.vtkImageImport()
    data_string = data_matrix.tostring()
    dataImporter.CopyImportVoidPointer(data_string, len(data_string))
    dataImporter.SetDataScalarTypeToUnsignedChar()
    dataImporter.SetNumberOfScalarComponents(1)
    dataImporter.SetDataExtent(0, size_x-1, 0, size_y-1, 0, size_z-1)
    dataImporter.SetWholeExtent(0, size_x-1, 0, size_y-1, 0, size_z-1)
    dataImporter.SetDataSpacing( 1,1,1 )
    print('apres importation, mean='+str(np.mean(data_matrix)))
  
    
    
    volumeMapper = vtk.vtkSmartVolumeMapper()
    volumeMapper.SetBlendModeToComposite()
    volumeMapper.SetInputConnection(dataImporter.GetOutputPort());
    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.ShadeOn()
  
    funcOpacityGradient = vtk.vtkPiecewiseFunction()
    funcOpacityGradient.AddPoint(1,   0.2)
    funcOpacityGradient.AddPoint(5,   0.4)
    funcOpacityGradient.AddPoint(100,   1.2)
    volumeProperty.SetGradientOpacity(funcOpacityGradient)
    
    compositeOpacity = vtk.vtkPiecewiseFunction()
    compositeOpacity.AddPoint(0.0,0.0);
    compositeOpacity.AddPoint(40.0,0.0);
    compositeOpacity.AddPoint(200.0,opac);
    compositeOpacity.AddPoint(255.0,opac);
    volumeProperty.SetScalarOpacity(compositeOpacity)
    volumeProperty.SetSpecular(0.3)
    volumeProperty.SetSpecularPower(100) 
    
    color = vtk.vtkColorTransferFunction()
    color.AddRGBPoint(0.0  ,0.0,0.0,0.0)
    color.AddRGBPoint(40.0  ,0.0,0.0,0.0)
    color.AddRGBPoint(255.0,1.0,1.0,1.0)

    volumeProperty.SetInterpolationTypeToLinear()    
    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)
    print('lut=')
    lut=get_common_colormaps(colormap)
    for i in range(256):
        print('BW lut i='+str(i)+'  ('+str(lut.GetTableValue(i)[0])+', '+str(lut.GetTableValue(i)[1])+', '+str(lut.GetTableValue(i)[2])+' ) ')
    set_volume_colormap(volume,lut)
    renderer.AddViewProp(volume)
    
#    volumeMapper.SetRequestedRenderModeToRayCastAndTexture()
    volumeMapper.SetRequestedRenderModeToRayCast()
    return volume
















def build_multi_planar_view_from_image2(path_source,opac,renderer,crop_type):
    z_begin_irm,z_end_irm,  x0,y0,z0,  xf,yf,zf,  size_x,size_y,size_z=get_image_constants_2(crop_type)
    data_matrix = io.imread(path_source)
    data_matrix[z0:zf,y0:yf,x0:xf]=0
    data_matrix[z_end_irm:size_z,:,:]=0
    data_matrix[0:z_begin_irm,:,:]=0
    dataImporter = vtk.vtkImageImport()
    data_string = data_matrix.tostring()
    dataImporter.CopyImportVoidPointer(data_string, len(data_string))
    dataImporter.SetDataScalarTypeToUnsignedChar()
    dataImporter.SetNumberOfScalarComponents(1)
    dataImporter.SetDataExtent(0, size_x-1, 0, size_y-1, 0, size_z-1)
    dataImporter.SetWholeExtent(0, size_x-1, 0, size_y-1, 0, size_z-1)
    dataImporter.SetDataSpacing( 1,1,1 )
  
    bwLut=create_bw_lookup_table()
    YZ_colors = vtk.vtkImageMapToColors()
    YZ_colors.SetInputConnection(dataImporter.GetOutputPort())
    YZ_colors.SetLookupTable(bwLut)
    YZ_colors.Update()
    YZ_plane = vtk.vtkImageActor()
    YZ_plane.GetMapper().SetInputConnection(YZ_colors.GetOutputPort())
    YZ_plane.SetDisplayExtent(int(round(size_x/2)),int(round( size_x/2)), 0, size_y-1, 0, size_z-1)

    XY_colors = vtk.vtkImageMapToColors()
    XY_colors.SetInputConnection(dataImporter.GetOutputPort())
    XY_colors.SetLookupTable(bwLut)
    XY_colors.Update()
    XY_plane = vtk.vtkImageActor()
    XY_plane.GetMapper().SetInputConnection(XY_colors.GetOutputPort())
    XY_plane.SetDisplayExtent(0, size_x-1, 0, size_y-1, int(round(size_z/2)), int(round(size_z/2)))

    XZ_colors = vtk.vtkImageMapToColors()
    XZ_colors.SetInputConnection(dataImporter.GetOutputPort())
    XZ_colors.SetLookupTable(bwLut)
    XZ_colors.Update()
    XZ_plane = vtk.vtkImageActor()
    XZ_plane.GetMapper().SetInputConnection(XZ_colors.GetOutputPort())
    XZ_plane.SetDisplayExtent(0, size_x-1, int(round(size_y/2)), int(round(size_y/2)), 0, size_z-1)

    # Actors are added to the renderer.
    renderer.AddActor(XY_plane)
    renderer.AddActor(XZ_plane)
    renderer.AddActor(YZ_plane)

    # Note that when camera movement occurs (as it does in the Dolly()
    # method), the clipping planes often need adjusting. Clipping planes
    # consist of two planes: near and far along the view direction. The
    # near plane clips out objects in front of the plane; the far plane
    # clips out objects behind the plane. This way only what is drawn
    # between the planes is actually rendered.
#    aRenderer.ResetCameraClippingRange()
    return XY_plane,XZ_plane,YZ_plane









def build_planar_view_from_image2(axis,path_source,opac,renderer,crop_type,colormap=0):
    z_begin_irm,z_end_irm,  x0,y0,z0,  xf,yf,zf,  size_x,size_y,size_z=get_image_constants_2(crop_type)
    data_matrix = io.imread(path_source)
    data_matrix[z0:zf,y0:yf,x0:xf]=0
    data_matrix[z_end_irm:size_z,:,:]=0
    data_matrix[0:z_begin_irm,:,:]=0
    print('avant importation, mean='+str(np.mean(data_matrix)))
    dataImporter = vtk.vtkImageImport()
    data_string = data_matrix.tostring()
    dataImporter.CopyImportVoidPointer(data_string, len(data_string))
    dataImporter.SetDataScalarTypeToUnsignedChar()
    dataImporter.SetNumberOfScalarComponents(1)
    dataImporter.SetDataExtent(0, size_x-1, 0, size_y-1, 0, size_z-1)
    dataImporter.SetWholeExtent(0, size_x-1, 0, size_y-1, 0, size_z-1)
    dataImporter.SetDataSpacing( 1,1,1 )
  
    lut=get_common_colormaps(colormap)

    colors = vtk.vtkImageMapToColors()
    colors.SetInputConnection(dataImporter.GetOutputPort())
    colors.SetLookupTable(lut)
    colors.Update()
    plane = vtk.vtkImageActor()
    plane.GetMapper().SetInputConnection(colors.GetOutputPort())
    set_slice(plane,axis)

    # Actors are added to the renderer.
    renderer.AddActor(plane)
    return plane








def build_actor_from_image2continuous(path_source,r,g,b,opac,spec,diff,amb,isoVal,crop_type=0,reduced_data_type=0,path_alternative=None,slice_min=-1,slice_max=-1):
    print('construction de l objet : '+str(path_source))
    print('caractéristiques (r , g, b, opac) : '+str(r)+' '+str(g)+' '+str(b)+' '+str(opac))
    print('croptype='+str(crop_type))
    
    z_begin_irm,z_end_irm,  x0,y0,z0,  xf,yf,zf,  size_x,size_y,size_z=get_image_constants_2(crop_type)
    data_matrix=io.imread(path_alternative)
    data_matrix[:,:,:]=2000
    mush0=io.imread(path_source+'0.tif')
    mush1=io.imread(path_source+'1.tif')
    mush2=io.imread(path_source+'2.tif')
    mush3=io.imread(path_source+'3.tif')
    mushn=mush0*256+mush1+mush2/256+mush3/(256*256)
    data_matrix[80:380, 200:265, 64:235]=mushn

    data_matrix[z0:zf,y0:yf,x0:xf]=0
    data_matrix[z_end_irm:size_z,:,:]=0
    data_matrix[0:z_begin_irm,:,:]=0
    print('avant importation, mean='+str(np.mean(data_matrix)))
    dataImporter = vtk.vtkImageImport()
    data_string = data_matrix.tostring()
    dataImporter.CopyImportVoidPointer(data_string, len(data_string))
    dataImporter.SetDataScalarTypeToDouble()
    dataImporter.SetNumberOfScalarComponents(1)
    dataImporter.SetDataExtent(0, size_x-1, 0, size_y-1, 0, size_z-1)
    dataImporter.SetWholeExtent(0, size_x-1, 0, size_y-1, 0, size_z-1)
    dataImporter.SetDataSpacing( 1,1,1 )
    surface = vtk.vtkMarchingCubes()
    surface.SetInputConnection( dataImporter.GetOutputPort() )
    surface.ComputeNormalsOn()
    surface.SetValue( 0, isoVal ) 
    geoBoneMapper = vtk.vtkPolyDataMapper()
    geoBoneMapper.SetInputConnection(surface.GetOutputPort())
    geoBoneMapper.ScalarVisibilityOff()
    geoBoneMapper.Update()
    actorCur = vtk.vtkLODActor()
    actorCur.SetMapper( geoBoneMapper )
    actorCur.GetProperty().SetColor( r, g, b) 
    actorCur.GetProperty().SetOpacity(opac )  
    actorCur.GetProperty().SetInterpolationToGouraud ()
    actorCur.GetProperty().SetSpecular(spec)
    actorCur.GetProperty().SetDiffuseColor( r, g, b )  
    actorCur.GetProperty().SetDiffuse(diff)  
    actorCur.GetProperty().SetAmbientColor( r, g, b )   
    actorCur.GetProperty().SetAmbient(amb)  
    return actorCur






def build_actor_from_image2(path_source,r,g,b,opac,spec,diff,amb,isoVal,crop_type=0,reduced_data_type=0,path_alternative=None,slice_min=-1,slice_max=-1):
    print('construction de l objet : '+str(path_source))
    print('caractéristiques (r , g, b, opac) : '+str(r)+' '+str(g)+' '+str(b)+' '+str(opac))
    print('croptype='+str(crop_type))
    
    z_begin_irm,z_end_irm,  x0,y0,z0,  xf,yf,zf,  size_x,size_y,size_z=get_image_constants_2(crop_type)
    if(reduced_data_type==1):
        data_matrix=io.imread(path_alternative)
        data_matrix[:,:,:]=0
        mush=io.imread(path_source)
        data_matrix[80:380, 200:265, 64:235]=mush
    else:
        data_matrix = io.imread(path_source)
    data_matrix[z0:zf,y0:yf,x0:xf]=0
    if(slice_max+slice_min>0):
        print('gestion slice min et max : '+str(slice_min)+' '+str(slice_max))
        data_matrix[slice_max:size_z,:,:]=0
        data_matrix[0:slice_min,:,:]=0
    else :
        print('pas de gestion de slice min et max')
    data_matrix[z_end_irm:size_z,:,:]=0
    data_matrix[0:z_begin_irm,:,:]=0
    print('avant importation, mean='+str(np.mean(data_matrix)))
    dataImporter = vtk.vtkImageImport()
    data_string = data_matrix.tostring()
    dataImporter.CopyImportVoidPointer(data_string, len(data_string))
    dataImporter.SetDataScalarTypeToUnsignedChar()
    dataImporter.SetNumberOfScalarComponents(1)
    dataImporter.SetDataExtent(0, size_x-1, 0, size_y-1, 0, size_z-1)
    dataImporter.SetWholeExtent(0, size_x-1, 0, size_y-1, 0, size_z-1)
    dataImporter.SetDataSpacing( 1,1,1 )
    surface = vtk.vtkMarchingCubes()
    surface.SetInputConnection( dataImporter.GetOutputPort() )
    surface.ComputeNormalsOn()
    surface.SetValue( 0, isoVal ) 
    geoBoneMapper = vtk.vtkPolyDataMapper()
    geoBoneMapper.SetInputConnection(surface.GetOutputPort())
    geoBoneMapper.ScalarVisibilityOff()
    geoBoneMapper.Update()
    actorCur = vtk.vtkLODActor()
    actorCur.SetMapper( geoBoneMapper )
    actorCur.GetProperty().SetColor( r, g, b) 
    actorCur.GetProperty().SetOpacity(opac )  
    actorCur.GetProperty().SetInterpolationToGouraud ()
    actorCur.GetProperty().SetSpecular(spec)
    actorCur.GetProperty().SetDiffuseColor( r, g, b )  
    actorCur.GetProperty().SetDiffuse(diff)  
    actorCur.GetProperty().SetAmbientColor( r, g, b )   
    actorCur.GetProperty().SetAmbient(amb)  
    return actorCur


def build_multi_planar_view_from_image2(path_source,opac,renderer,crop_type):
    z_begin_irm,z_end_irm,  x0,y0,z0,  xf,yf,zf,  size_x,size_y,size_z=get_image_constants_2(crop_type)
    data_matrix = io.imread(path_source)
    data_matrix[z0:zf,y0:yf,x0:xf]=0
    data_matrix[z_end_irm:size_z,:,:]=0
    data_matrix[0:z_begin_irm,:,:]=0
    dataImporter = vtk.vtkImageImport()
    data_string = data_matrix.tostring()
    dataImporter.CopyImportVoidPointer(data_string, len(data_string))
    dataImporter.SetDataScalarTypeToUnsignedChar()
    dataImporter.SetNumberOfScalarComponents(1)
    dataImporter.SetDataExtent(0, size_x-1, 0, size_y-1, 0, size_z-1)
    dataImporter.SetWholeExtent(0, size_x-1, 0, size_y-1, 0, size_z-1)
    dataImporter.SetDataSpacing( 1,1,1 )
  
    bwLut=create_bw_lookup_table()
    YZ_colors = vtk.vtkImageMapToColors()
    YZ_colors.SetInputConnection(dataImporter.GetOutputPort())
    YZ_colors.SetLookupTable(bwLut)
    YZ_colors.Update()
    YZ_plane = vtk.vtkImageActor()
    YZ_plane.GetMapper().SetInputConnection(YZ_colors.GetOutputPort())
    YZ_plane.SetDisplayExtent(int(round(size_x/2)),int(round( size_x/2)), 0, size_y-1, 0, size_z-1)

    XY_colors = vtk.vtkImageMapToColors()
    XY_colors.SetInputConnection(dataImporter.GetOutputPort())
    XY_colors.SetLookupTable(bwLut)
    XY_colors.Update()
    XY_plane = vtk.vtkImageActor()
    XY_plane.GetMapper().SetInputConnection(XY_colors.GetOutputPort())
    XY_plane.SetDisplayExtent(0, size_x-1, 0, size_y-1, int(round(size_z/2)), int(round(size_z/2)))

    XZ_colors = vtk.vtkImageMapToColors()
    XZ_colors.SetInputConnection(dataImporter.GetOutputPort())
    XZ_colors.SetLookupTable(bwLut)
    XZ_colors.Update()
    XZ_plane = vtk.vtkImageActor()
    XZ_plane.GetMapper().SetInputConnection(XZ_colors.GetOutputPort())
    XZ_plane.SetDisplayExtent(0, size_x-1, int(round(size_y/2)), int(round(size_y/2)), 0, size_z-1)

    # Actors are added to the renderer.
    renderer.AddActor(XY_plane)
    renderer.AddActor(XZ_plane)
    renderer.AddActor(YZ_plane)

    # Note that when camera movement occurs (as it does in the Dolly()
    # method), the clipping planes often need adjusting. Clipping planes
    # consist of two planes: near and far along the view direction. The
    # near plane clips out objects in front of the plane; the far plane
    # clips out objects behind the plane. This way only what is drawn
    # between the planes is actually rendered.
#    aRenderer.ResetCameraClippingRange()
    return XY_plane,XZ_plane,YZ_plane
