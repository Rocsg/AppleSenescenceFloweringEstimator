#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 16:14:54 2019

@author: fernandr
"""
import time
from skimage import io
import vtk
import numpy as np
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()


def sequence_turn_around_global(timestep,renWin,imageFilter,movieWriter,camera):
    #PAUSE
    sequence_idle(100,timestep,renWin,imageFilter,movieWriter,camera)
    
    #TURN LEFT
    sequence_turn_azimuth(192,-0.5,timestep,renWin,imageFilter,movieWriter,camera)
    sequence_stop_azimuth_slowly(10,5,-0.5,timestep,renWin,imageFilter,movieWriter,camera)
    sequence_idle(100,timestep,renWin,imageFilter,movieWriter,camera)
    
    #TURN RIGHT AND ELEVATE
    sequence_turn_azimuth_and_elevate(20,0.5,0.35,timestep,renWin,imageFilter,movieWriter,camera)
    sequence_turn_azimuth_and_stop_elevate_slowly(5,7,0.5,0.35,timestep,renWin,imageFilter,movieWriter,camera)
    sequence_turn_azimuth(36,0.5,timestep,renWin,imageFilter,movieWriter,camera)
    sequence_turn_azimuth_and_elevate(48,0.5,-0.35,timestep,renWin,imageFilter,movieWriter,camera)
    sequence_turn_azimuth_and_stop_elevate_slowly(5,7,0.5,-0.35,timestep,renWin,imageFilter,movieWriter,camera)
    sequence_stop_azimuth_slowly(10,5,0.5,timestep,renWin,imageFilter,movieWriter,camera)
    
    #PAUSE
    sequence_idle(50,timestep,renWin,imageFilter,movieWriter,camera)
    
    #ZOOM
    sequence_zoom(5,10,80,0.001,timestep,renWin,imageFilter,movieWriter,camera)
    
    #PAUSE
    sequence_idle(100,timestep,renWin,imageFilter,movieWriter,camera)
    
    
    
    









def sequence_idle(n_frames,timestep,renWin,imageFilter,moviewriter,camera):
    for i in range(n_frames):
        time.sleep(timestep)
        renWin.Render()
        imageFilter.Modified()
        moviewriter.Write()
        if (i%10==0):
            print('idle : '+str(i)+'/'+str(n_frames))


def sequence_turn_azimuth(n_frames,deltaAz,timestep,renWin,imageFilter,moviewriter,camera):
    for i in range(n_frames):
        time.sleep(timestep)
        camera.Azimuth(deltaAz)
        renWin.Render()
        imageFilter.Modified()
        moviewriter.Write()
        if (i%10==0):
            print('turn : '+str(i)+'/'+str(n_frames))



def sequence_turn_azimuth_and_elevate(n_frames,deltaAz,deltaEl,timestep,renWin,imageFilter,moviewriter,camera):
    for i in range(n_frames):
        time.sleep(timestep)
        camera.Azimuth(deltaAz)
        camera.Elevation(deltaEl)
        renWin.Render()
        imageFilter.Modified()
        moviewriter.Write()
        if (i%10==0):
            print('turn_and_elevate : '+str(i)+'/'+str(n_frames))



def sequence_turn_azimuth_and_stop_elevate_slowly(j_range,i_range,deltaAz,deltaEl,timestep,renWin,imageFilter,moviewriter,camera):
    for j in range (j_range):
        for i in range(i_range):
            time.sleep(timestep)
            camera.Azimuth(deltaAz)
            camera.Elevation(deltaEl/j_range*(j_range-j))
            renWin.Render()
            imageFilter.Modified()
            moviewriter.Write()
        print('turn and stop elevate : '+str(j)+'/'+str(j_range))



def sequence_stop_azimuth_slowly(j_range,i_range,deltaAz,timestep,renWin,imageFilter,moviewriter,camera):
    for j in range (j_range):
        for i in range(i_range):
            time.sleep(timestep)
            camera.Azimuth(1.0/j_range*(j_range-1-j)*deltaAz)
            renWin.Render()
            imageFilter.Modified()
            moviewriter.Write()
        print('turn and stop azimuth : '+str(j)+'/'+str(j_range))


def sequence_zoom(j_range,i_range,n_frames,zoom_factor,timestep,renWin,imageFilter,moviewriter,camera):
    for j in range (j_range):
        for i in range(i_range):
            time.sleep(timestep)
            camera.Zoom(1+j*zoom_factor)
            renWin.Render()
            imageFilter.Modified()
            moviewriter.Write()
        print('accelerate zoom : '+str(j)+'/'+str(j_range))
    
    for i in range(n_frames):
        time.sleep(timestep)
        camera.Zoom(1+j_range*zoom_factor)
        renWin.Render()
        imageFilter.Modified()
        moviewriter.Write()
        if (i%10==0):
            print('zoom : '+str(i)+'/'+str(n_frames))
    
    for j in range (j_range):
        for i in range(i_range):
            time.sleep(timestep)
            camera.Zoom(1+(j_range-j)*zoom_factor)
            renWin.Render()
            imageFilter.Modified()
            moviewriter.Write()
        print('zoom : '+str(j)+'/'+str(j_range))





def setup_camera_initial_position(camera):
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    camera.SetPosition(size_x*1.5, size_y*2.5,size_z*2.5);
    camera.SetFocalPoint(size_x/2,size_y/2, size_z/2);
    camera.Azimuth(14)
    camera.SetFocalPoint(size_x/2,size_y/2, size_z/2);
    camera.Roll(-103)
    camera.Roll(-25)
    camera.Elevation(10)
    camera.Azimuth(50)    
    camera.Zoom(1.2)
    camera.Roll(-10)
    camera.Elevation(-5)
    camera.Azimuth(35)    
    camera.Roll(-10)

def create_lights_for_movie(renderer):
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    # create a green light
    light_green = vtk.vtkLight()
    light_green.SetPositional(1)
    light_green.SetPosition(size_x*2, -size_y*2,size_z*2)
    light_green.SetColor(0.6, 0.6, 0.6)
    light_green.SetIntensity(0.7)
    renderer.AddLight(light_green)
    
    light_green2 = vtk.vtkLight()
    light_green2.SetPositional(1)
    light_green2.SetPosition(-size_x*2+1000, size_y*2,size_z*2)
    light_green2.SetColor(0.8, 0.8, 0.8)
    light_green2.SetIntensity(1.0)
    renderer.AddLight(light_green2)
    
    light_green3 = vtk.vtkLight()
    light_green3.SetPositional(1)
    light_green3.SetPosition(-size_x*2, size_y*2+1000,size_z*2+1000)
    light_green3.SetColor(0.8, 0.8, 0.8)
    light_green3.SetIntensity(1.4)
    renderer.AddLight(light_green3)



def setup_movie(framerate,path_to_movie,renWin):
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
    moviewriter.SetFileName(path_to_movie)
    moviewriter.Start()
    return imageFilter,moviewriter



def setup_interaction(renWin,renderer):
    iren = vtk.vtkRenderWindowInteractor()
    iren.SetRenderWindow(renWin)
    iren.Render()
    camera=renderer.GetActiveCamera()
    renWin.SetSize(1500,800)
    iren.Start()





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
#    data_matrix[:,:,:]=0   ,x_start_crop:size_x-1
#    print('retrait du cube : ')
#    print(str(0)+'-'+str(x_start_crop)+' X '+str(y_start_crop)+'-'+str(size_y)+' X '+str(z_start_crop)+'-'+str(size_z) ) 
#    print('sur shape= : '+str(data_matrix.shape[2])+' x '+str(data_matrix.shape[1])+' x '+str(data_matrix.shape[0]) )
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


def get_image_constants(crop_type=0):
    #Crop 0 : ne touche pas aux donnees
    #Crop 1 : enleve un quart de l'objet
    #Crop 2 : enleve un huitieme de l'objet
    y_start_crop,z_start_crop=150,210
    size_x,size_y,size_z=320,300,472
    if(crop_type==0):
        x_start_crop, y_start_crop,z_start_crop=0,size_y,size_z
    elif(crop_type==1) :
        x_start_crop, y_start_crop,z_start_crop=size_x,150,210
    else :
        x_start_crop, y_start_crop,z_start_crop=180,150,210
    z_begin_irm,z_end_irm=50,370
    return z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z


def build_moelle(day_i,inter,renderer,actor,usePrecomputed):
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
    actor=build_actor_from_image(source_rep+'/images/moe'+basenom+'_gauss.tif',r,g,b,opac,spec,diff,amb,isoVal,1)
    actor.SetVisibility(True)
    renderer.AddActor(actor)
    return actor

def build_cambium(day_i,inter,renderer,actor,usePrecomputed):
    day_i_plus=day_i+1
    basenom=str(day_i)+str(day_i_plus)+'_'+str(inter)
    source_rep=get_source_rep()
    r,g,b=0.712, 0.554,0.5
    opac,spec,diff,amb=1.0, 0.2, 0.4, 0.18
    isoVal=67.5
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    if(actor is None):
        a=1        
    else: 
        actor.SetVisibility(False)
        renderer.RemoveActor(actor)
    actor= build_actor_from_image(source_rep+'/images/camb'+basenom+'_gauss.tif',r,g,b,opac,spec,diff,amb,isoVal,1)
    actor.SetVisibility(True)
    renderer.AddActor(actor)
    return actor

def build_silhouette(day_i,inter,renderer,actor,usePrecomputed):
    day_i_plus=day_i+1
    basenom=str(day_i)+str(day_i_plus)+'_'+str(inter)
    source_rep=get_source_rep()
    r,g,b=0.812, 0.454,0.4
    opac,spec,diff,amb=0.15, 0.4, 0.4, 0.18
    isoVal=67.5
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    if(actor is None):
        a=1        
    else: 
        actor.SetVisibility(False)
        renderer.RemoveActor(actor)
    actor= build_actor_from_image(source_rep+'/images/camb'+basenom+'_gauss.tif',r,g,b,opac,spec,diff,amb,isoVal)
    actor.SetVisibility(True)
    actor.GetProperty().SetSpecularColor(0.9,0.7,0.7)
    renderer.AddActor(actor)
    return actor


def build_mushroom(day_i,inter,nb_interp,renderer,actor,usePrecomputed):
    day_i_plus=day_i+1
    basenom=str(day_i)+str(day_i_plus)+'_'+str(inter)
    source_rep=get_source_rep()
    r,g,b=0.9, 0.1,0.1
    opac,spec,diff,amb=0.25, 0.7, 0.4, 0.18
    isoVal=127.5
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    if(actor is None):
        a=1        
    else: 
        actor.SetVisibility(False)
        renderer.RemoveActor(actor)
    actor= build_actor_from_image(source_rep+'/mushroom/seg'+basenom+'.tif',r,g,b,opac,spec,diff,amb,isoVal,0,1,source_rep+'/images/camb'+basenom+'_gauss.tif')
    actor.SetVisibility(True)
    actor.GetProperty().SetSpecularColor(1.0,0.4,0.4)
    renderer.AddActor(actor)
    return actor


def build_vessels(day_i,inter,renderer,actor,usePrecomputed):
    day_i_plus=day_i+1
    basenom=str(day_i)+str(day_i_plus)+'_'+str(inter)
    source_rep=get_source_rep()
    r,g,b=0.576, 0.688,0.412
    opac,spec,diff,amb=1.0, 0.3, 0.3, 0.1
    isoVal=182.5
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants(1)
    if(actor is None):
        a=1        
    else:
        actor.SetVisibility(False)
        renderer.RemoveActor(actor)
    actor=build_actor_from_image(source_rep+'/images/ves'+basenom+'_gauss.tif',r,g,b,opac,spec,diff,amb,isoVal,1)
    actor.GetProperty().SetSpecularColor(0.8,0.9,0.7)
    actor.SetVisibility(True)
    renderer.AddActor(actor)
    return actor

def get_source_rep():
    return '/mnt/DD_COMMON/Data_VITIMAGE/Movie_maker_v2/img_interp'



def to_front_view(camera):
    camera.Azimuth(-55)
    camera.Elevation(-35)
    camera.Roll(2)
    camera.SetFocalPoint(160,150,206)
    camera.Zoom(2.3)

def from_front_view(camera):
    camera.Zoom(1/2.3)
    camera.SetFocalPoint(160,150,236)
    camera.Roll(-2)
    camera.Elevation(35)
    camera.Azimuth(55)
 

def from_up_view(camera):
    camera.Zoom(1/4.3)
    camera.Roll(83)
    camera.SetFocalPoint(160,150,236)
    camera.Elevation(-50)
    camera.Azimuth(60)

def to_up_view(camera):
    camera.Azimuth(-60)
    camera.Elevation(50)
    camera.SetFocalPoint(160,230,236)
    camera.Roll(-83)
    camera.Zoom(4.3)



def to_right_view(camera):
    camera.Azimuth(27)
    camera.Elevation(-30)
    camera.Zoom(3.4)
    camera.Yaw(4)
    camera.Roll(-1.2)

def from_right_view(camera):
    camera.Roll(1.2)
    camera.Yaw(-4)
    camera.Zoom(1/3.4)
    camera.Elevation(30)
    camera.Azimuth(-27)

def build_actor_from_mesh_file(path,r,g,b,opac,spec,diff,amb,isoVal):
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    print("reading mesh from file : "+str(path))
    reader=vtk.vtkPolyDataReader()
    reader.SetFileName(path);
    geoBoneMapper = vtk.vtkPolyDataMapper()
    geoBoneMapper.SetInputConnection(reader.GetOutputPort())
    geoBoneMapper.ScalarVisibilityOff()
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

