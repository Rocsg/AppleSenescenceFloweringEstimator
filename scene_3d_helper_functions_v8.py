#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 16:14:54 2019

@author: fernandr
"""

""" 
######################################################################################################################################
#########  CONVERSION DONNEES VERS OBJETS 3D   #######################################################################################
######################################################################################################################################
 """
def build_mesh_and_write_to_file(path_source,path_dest,isoVal):
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    data_matrix = io.imread(path_source)
    data_matrix[z_last:size_z,y_last:size_y,:]=0
    data_matrix[z_end_irm:size_z+1,:,:]=0
    data_matrix[0:z_begin_irm,:,:]=0
    dataImporter = vtk.vtkImageImport()
    data_string = data_matrix.tostring()
    dataImporter.CopyImportVoidPointer(data_string, len(data_string))
    dataImporter.SetDataScalarTypeToUnsignedChar()
    dataImporter.SetNumberOfScalarComponents(1)
    dataImporter.SetDataExtent(0, size_x, 0, size_y, 0, size_z)
    dataImporter.SetWholeExtent(0, size_x, 0, size_y, 0, size_z)
    dataImporter.SetDataSpacing( 1,1,1 )
    surface = vtk.vtkContourFilter()
    surface.SetInputConnection( dataImporter.GetOutputPort() )
    surface.ComputeNormalsOn()
    surface.SetValue( 0, isoVal ) 
    surface.Update()
    writer=vtk.vtkPolyDataWriter()
    writer.SetFileName(path_dest)
    writer.SetInputData(surface.GetOutput());
    writer.Write();


def build_actor_from_image(path_source,r,g,b,opac,spec,diff,amb,isoVal,crop_type=0,reduced_data_type=0,path_alternative=None):
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants(crop_type)    
    if(reduced_data_type==1):
        data_matrix=io.imread(path_alternative)
        data_matrix[:,:,:]=0
        mush=io.imread(path_source)
        data_matrix[80:380, 200:265, 64:235]=mush
    else:
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
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants(crop_type)    
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



def build_planar_view_from_image(axis,path_source,opac,renderer,crop_type,colormap=0):
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants(crop_type)    
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
  
    lut=get_common_colormaps(colormap)

    colors = vtk.vtkImageMapToColors()
    colors.SetInputConnection(dataImporter.GetOutputPort())
    colors.SetLookupTable(Lut)
    colors.Update()
    plane = vtk.vtkImageActor()
    plane.GetMapper().SetInputConnection(colors.GetOutputPort())
    set_slice(plane,axis)

    # Actors are added to the renderer.
    renderer.AddActor(plane)
    return plane



def set_slice(plane,axis,slice=-1,crop_type=0):
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants(crop_type)    
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
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants(crop_type)    
    data_matrix = io.imread(path_source)     
    data_matrix[z_start_crop:size_z,y_start_crop:size_y,0:x_start_crop]=0
    data_matrix[z_end_irm:size_z,:,:]=0
    data_matrix[0:z_begin_irm,:,:]=0
    data_matrix[zmax:size_z,:,:]=0
    data_matrix[0:zmin,:,:]=0
    dataImporter = vtk.vtkImageImport()
    data_string = data_matrix.tostring()
    dataImporter.CopyImportVoidPointer(data_string, len(data_string))
    dataImporter.SetDataScalarTypeToUnsignedChar()
    dataImporter.SetNumberOfScalarComponents(1)
    dataImporter.SetDataExtent(0, size_x-1, 0, size_y-1, 0, size_z-1)
    dataImporter.SetWholeExtent(0, size_x-1, 0, size_y-1, 0, size_z-1)
    dataImporter.SetDataSpacing( 1,1,1 )
  
    
    
    volumeMapper = vtk.vtkSmartVolumeMapper()
    volumeMapper.SetBlendModeToComposite()
    volumeMapper.SetInputConnection(dataImporter.GetOutputPort());
    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.ShadeOn()
  
    compositeOpacity = vtk.vtkPiecewiseFunction()
    compositeOpacity.AddPoint(0.0,0.0);
    compositeOpacity.AddPoint(40.0,0.0);
    compositeOpacity.AddPoint(200.0,opac);
    compositeOpacity.AddPoint(255.0,opac);
    volumeProperty.SetScalarOpacity(compositeOpacity)
      
    color = vtk.vtkColorTransferFunction()
    color.AddRGBPoint(0.0  ,0.0,0.0,0.0)
    color.AddRGBPoint(40.0  ,0.0,0.0,0.0)
    color.AddRGBPoint(255.0,1.0,1.0,1.0)


    
    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)
    lut=get_common_colormaps(colormap)
    set_volume_colormap(volume,lut)
    renderer.AddViewProp(volume)
    
#    volumeMapper.SetRequestedRenderModeToRayCastAndTexture()
    volumeMapper.SetRequestedRenderModeToRayCast()
    return volume


def build_moelle(day_i,inter,renderer,actor,crop_type=1):
    day_i_plus=day_i+1
    basenom=str(day_i)+str(day_i_plus)+'_'+str(inter)
    source_rep=get_source_rep()
    r,g,b=0.922, 0.804,0.72
    opac,spec,diff,amb=1.0, 0.2, 0.3, 0.18
    isoVal=55.5
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    if(actor is None):
        a=1        
    else: 
        actor.SetVisibility(False)
        renderer.RemoveActor(actor)
    actor=build_actor_from_image(source_rep+'/images/moe'+basenom+'_gauss.tif',r,g,b,opac,spec,diff,amb,isoVal,crop_type)
    actor.SetVisibility(True)
    renderer.AddActor(actor)
    return actor

def build_cambium(day_i,inter,renderer,actor,crop_type=1):
    day_i_plus=day_i+1
    basenom=str(day_i)+str(day_i_plus)+'_'+str(inter)
    source_rep=get_source_rep()
    r,g,b=get_cambium_rgb()
    opac,spec,diff,amb=1.0, 0.2, 0.4, 0.18
    isoVal=67.5
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    if(actor is None):
        a=1        
    else: 
        actor.SetVisibility(False)
        renderer.RemoveActor(actor)
    actor= build_actor_from_image(source_rep+'/images/camb'+basenom+'_gauss.tif',r,g,b,opac,spec,diff,amb,isoVal,crop_type)
    actor.SetVisibility(True)
    renderer.AddActor(actor)
    return actor


def build_silhouette(day_i,inter,renderer,actor):
    day_i_plus=day_i+1
    basenom=str(day_i)+str(day_i_plus)+'_'+str(inter)
    source_rep=get_source_rep()
    r,g,b,   opac,spec,diff,amb ,  spec_r,spec_g,spec_b=get_silhouette_colours()

    isoVal=127.5
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    if(actor is None):
        a=1        
    else: 
        actor.SetVisibility(False)
        renderer.RemoveActor(actor)
    actor= build_actor_from_image(source_rep+'/images/sil'+basenom+'.tif',r,g,b,opac,spec,diff,amb,isoVal,0,0)
    actor.SetVisibility(True)
    actor.GetProperty().SetSpecularColor( spec_r,spec_g,spec_b)
    renderer.AddActor(actor)
    return actor


def build_mushroom(day_i,inter,nb_interp,renderer,actor):
    day_i_plus=day_i+1
    basenom=str(day_i)+str(day_i_plus)+'_'+str(inter)
    source_rep=get_source_rep()
    r,g,b,   opac,spec,diff,amb ,  spec_r,spec_g,spec_b=get_mushroom_colours()

    isoVal=127.5
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    if(actor is None):
        a=1        
    else: 
        actor.SetVisibility(False)
        renderer.RemoveActor(actor)
    actor= build_actor_from_image(source_rep+'/mushroom/seg'+basenom+'.tif',r,g,b,opac,spec,diff,amb,isoVal,0,1,source_rep+'/images/camb'+basenom+'_gauss.tif')
    actor.SetVisibility(True)
    actor.GetProperty().SetSpecularColor( spec_r,spec_g,spec_b)
    renderer.AddActor(actor)
    return actor


def build_vessels(day_i,inter,renderer,actor,crop_type=1):
    day_i_plus=day_i+1
    basenom=str(day_i)+str(day_i_plus)+'_'+str(inter)
    source_rep=get_source_rep()
    r,g,b=0.576, 0.688,0.412
    opac,spec,diff,amb=1.0, 0.3, 0.3, 0.1
    isoVal=182.5
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants(crop_type)
        
    if(actor is None):
        a=1        
    else:
        actor.SetVisibility(False)
        renderer.RemoveActor(actor)
    actor=build_actor_from_image(source_rep+'/images/ves'+basenom+'_gauss.tif',r,g,b,opac,spec,diff,amb,isoVal,crop_type)
    actor.GetProperty().SetSpecularColor(0.8,0.9,0.7)
    actor.SetVisibility(True)
    renderer.AddActor(actor)
    return actor



def build_vr(day_i,inter,nb_interp,renderer,volume,crop_type,zmin,zmax,colormap=0):
    day_i_plus=day_i+1
    basenom=str(day_i)+str(day_i_plus)+'_'+str(inter)
    source_rep=get_source_rep()
    opac=1
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants(crop_type)
        
    if(volume is None):
        a=1        
    else:
        renderer.RemoveViewProp(volume)
    if(zmin<0):
        zmin=0
    if(zmax>size_z):
        zmax=size_z
    if(zmin>zmax):
        zmin=zmax
    volume=build_volume_rendering_view_from_image(source_rep+'/images/full'+basenom+'.tif',opac,renderer,crop_type,zmin,zmax,colormap)
    print('volume built from file : '+source_rep+'/images/full'+basenom+'.tif')
    
    return volume






def build_mpr(day_i,inter,renderer,volume,crop_type,colormap):
    day_i_plus=day_i+1
    basenom=str(day_i)+str(day_i_plus)+'_'+str(inter)
    source_rep=get_source_rep()
    opac=1
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants(crop_type)
        
    if(volume is None):
        a=1        
    else:
        renderer.RemoveViewProp(volume)
    XY_plane,XZ_plane,YZ_plane=build_multi_planar_view_from_image(source_rep+'/images/full'+basenom+'.tif',opac,renderer,crop_type,colormap)
    return XY_plane,XZ_plane,YZ_plane



def build_planar(axis,day_i,inter,renderer,plane,crop_type=0,direction=0,colormap=0):
    day_i_plus=day_i+1
    basenom=str(day_i)+str(day_i_plus)+'_'+str(inter)
    source_rep=get_source_rep()
    opac=1
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants(crop_type)
        
    if(plane is None):
        a=1        
    else:
        plane.SetVisibility(False)
        renderer.RemoveActor(plane)
    if(direction==0):
        plane=build_planar_view_from_image(axis,source_rep+'/images/full'+basenom+'.tif',opac,renderer,crop_type,colormap)
    if(direction==1):
        basenom=str(day_i)+str(day_i_plus)+'_t'+str(inter)
        plane=build_planar_view_from_image(axis,source_rep+'/images/front_d_'+basenom+'_samples.tif',opac,renderer,crop_type,colormap)
    if(direction==2):
        basenom=str(day_i)+str(day_i_plus)+'_t'+str(inter)
        plane=build_planar_view_from_image(axis,source_rep+'/images/back_d_'+basenom+'_samples.tif',opac,renderer,crop_type,colormap)
    return plane




