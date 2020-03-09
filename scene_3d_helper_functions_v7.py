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

""" 
######################################################################################################################################
#########      CONSTANTES OBSERVATION          #######################################################################################
######################################################################################################################################
 """
 
 
def create_bw_lookup_table():
    return create_lookup_table(0,255,0,0, 0,0, 0,1)
 
def create_rainbow_lookup_table(saturation,contrast):
    return create_lookup_table(0,255,saturation,saturation, 0.6,-0.1, contrast,contrast)


def create_lookup_table(intensity_min,intensity_max,sat_min,sat_max,hue_min,hue_max,cont_min,cont_max):
     # Start by creating a black/white lookup table.
    bwLut = vtk.vtkLookupTable()
    bwLut.SetTableRange(intensity_min,intensity_max)
    bwLut.SetSaturationRange(sat_min,sat_max)
    bwLut.SetHueRange(hue_min, hue_max)
    bwLut.SetValueRange(cont_min, cont_max)
    bwLut.Build()  # effective built
 
def get_field_rep():
    return '/mnt/DD_COMMON/Data_VITIMAGE/Movie_maker_v2/champs/samples'
 
def get_source_rep():
    return '/mnt/DD_COMMON/Data_VITIMAGE/Movie_maker_v2/img_interp'

def get_mri_colour():
    return 1,215/255,0

def get_interpolation_colour():
    return 175/255, 238/255, 238/255

def get_cambium_colour():
    return 0.712, 0.554,0.5


def set_actor_color_to_cambium(actorCur):
    r,g,b=get_cambium_colour()
    opac,spec,diff,amb=1.0, 0.2, 0.4, 0.18
    actorCur.GetProperty().SetColor( r, g, b) 
    actorCur.GetProperty().SetOpacity(opac )  
    actorCur.GetProperty().SetInterpolationToGouraud ()
    actorCur.GetProperty().SetSpecular(spec)
    actorCur.GetProperty().SetDiffuseColor( r, g, b )  
    actorCur.GetProperty().SetDiffuse(diff)  
    actorCur.GetProperty().SetAmbientColor( r, g, b )   
    actorCur.GetProperty().SetAmbient(amb)  
    
def get_mushroom_colours():
    return    0.9, 0.1,0.1 ,      0.45, 0.7, 0.4, 0.18           ,1.0  ,0.2  ,0.2
    #            r,g,b,              opac,spec,diff,amb ,        spec_r,spec_g,spec_b

def get_silhouette_colours():
    return  0.8, 0.8,1.0 ,        0.11, 0.7 ,0.4,0.18           ,1.0 , 1.0  ,1.0 
    #          r,g,b,                opac,spec,diff,amb ,       spec_r,spec_g,spec_b


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


def window_size_config(day_max,mobile_rendering):
    police_1,police_2=36,24
    if(mobile_rendering==0):
        window_width,window_height=1200, 896
    if(mobile_rendering==1):
        window_width,window_height=1920, 1080
    if(mobile_rendering==2):
        window_width,window_height=3840,2160
        police_1,police_2=72,48
    if(mobile_rendering==3):
        window_width,window_height=1080,1920

    x_margin=window_width/12
    text_width=int(np.round(police_1*200/36))
    y_margin=int(round(window_height/18))
    text_height=int(np.round(police_1*50/36))
    x_plus=int(round(window_width*140/1200))
    space_between_texts=(window_width-2*x_margin-text_width)/(day_max)
    return window_width,window_height,x_margin,text_width,y_margin,text_height,police_1,police_2,x_plus,space_between_texts


""" 
######################################################################################################################################
#########       SEQUENCES AVEC CAMERA          #######################################################################################
######################################################################################################################################
 """
def sequence_turn_around_global(timestep,renWin,imageFilter,movieWriter,camera):
    sequence_turn_azimuth(192-5-15,-0.5,timestep,renWin,imageFilter,movieWriter,camera)
    sequence_stop_azimuth_slowly(10,5,-0.5,timestep,renWin,imageFilter,movieWriter,camera)
    sequence_idle(60,timestep,renWin,imageFilter,movieWriter,camera)
    
    #TURN RIGHT AND ELEVATE
    sequence_turn_azimuth_and_elevate(20,0.5,0.35,timestep,renWin,imageFilter,movieWriter,camera)
    sequence_turn_azimuth_and_stop_elevate_slowly(5,7,0.5,0.35,timestep,renWin,imageFilter,movieWriter,camera)
    sequence_turn_azimuth(74-5,0.5,timestep,renWin,imageFilter,movieWriter,camera)
    sequence_turn_azimuth_and_elevate(20,0.5,-0.35,timestep,renWin,imageFilter,movieWriter,camera)
    sequence_turn_azimuth_and_stop_elevate_slowly(5,7,0.5,-0.35,timestep,renWin,imageFilter,movieWriter,camera)
    sequence_stop_azimuth_slowly(10,5,0.5,timestep,renWin,imageFilter,movieWriter,camera)
    
def sequence_disappear_full(renderer,actorVesselsFull,actorMoelleFull,actorCambiumFull,actorVessels,actorMoelle,actorCambium,n_frames,timestep,renWin,imageFilter,movieWriter,camera): 
    actorVessels.GetProperty().SetOpacity(1)
    actorMoelle.GetProperty().SetOpacity(1)
    actorCambium.GetProperty().SetOpacity(1)
    for i in range(n_frames):
        actorVesselsFull.GetProperty().SetOpacity((n_frames-i)/n_frames)
        actorMoelleFull.GetProperty().SetOpacity((n_frames-i)/n_frames)
        actorCambiumFull.GetProperty().SetOpacity((n_frames-i)/n_frames)
        time.sleep(timestep)
        renWin.Render()
        imageFilter.Modified()
        movieWriter.Write()
        if (i%10==0):
            print('disappear : '+str(i)+'/'+str(n_frames))
   
    
def sequence_idle(n_frames,timestep,renWin,imageFilter,moviewriter,camera):
    for i in range(n_frames):
        time.sleep(timestep)
        renWin.Render()
        imageFilter.Modified()
        moviewriter.Write()
        if (i%10==0):
            print('idle : '+str(i)+'/'+str(n_frames))

    
def sequence_idle_and_right(n_frames,timestep,renWin,imageFilter,moviewriter,imageFilterRight,moviewriterRight,camera):
    for i in range(n_frames):
        time.sleep(timestep)
        renWin.Render()
        imageFilter.Modified()
        moviewriter.Write()
        if (i%10==0):
            print('idle oblique: '+str(i)+'/'+str(n_frames))
    to_right_view(camera)
    for i in range(n_frames):
        renWin.Render()
        imageFilterRight.Modified()
        moviewriterRight.Write()
        if (i%10==0):
            print('idle right: '+str(i)+'/'+str(n_frames))
    from_right_view(camera)
        

def sequence_idle_with_red_text(day_max, timestep,renWin,imageFilter,moviewriter,camera,renderer,actorVesselsFull,actorMoelleFull,actorCambiumFull,actorCambium,mobile_rendering=0):
    window_width,window_height,x_margin,text_width,y_margin,text_height,police_1,police_2,x_plus,space_between_texts=window_size_config(day_max,mobile_rendering)
    actorMushroom=build_mushroom(0,0,120,renderer,None)
    final_mush_opacity=actorMushroom.GetProperty().GetOpacity()
    initial_mush_opacity=1.0
 
    
    
    #FIRST EXPLANATION ######################################################"
    actorVesselsFull.GetProperty().SetOpacity(1)
    actorCambiumFull.GetProperty().SetOpacity(1)
    actorMoelleFull.GetProperty().SetOpacity(1)
    actorCambium.GetProperty().SetOpacity(0)
    set_actor_color_to_cambium(actorMushroom) 
    actorMushroom.GetProperty().SetInterpolationToGouraud ()
    textActor = vtk.vtkTextActor()
    text1=""
    text1=text1+"A squared piece of bark is taken off from the specimen.\n"
    text1=text1+"A squared piece of fungus inoculum is inserted below with agarose\n"
    textActor.SetInput ( text1 )
    textActor.SetPosition ( int(round(window_width*80/1200)), window_height-3.5*police_1-10)
    textActor.GetTextProperty().SetFontSize (police_1)
    textActor.GetTextProperty().SetOpacity ( 0 )
    textActor.GetTextProperty().SetFontFamilyToTimes()
    textActor.GetTextProperty().SetColor (1.0, 1.0, 1.0 )
    renderer.AddActor2D ( textActor )

    textActor2 = vtk.vtkTextActor()
    text2="fungus inoculum"
    textActor2.SetInput ( text2 )
    textActor2.SetPosition ( int(round(window_width*80/1200))+int(round(police_1*8.3)), window_height-2.42*police_1-10)
    textActor2.GetTextProperty().SetFontSize (police_1)
    textActor2.GetTextProperty().SetOpacity ( 0 )
    textActor2.GetTextProperty().SetFontFamilyToTimes()
    textActor2.GetTextProperty().SetColor ( 1.0, 0.1, 0.1  )
    renderer.AddActor2D ( textActor2 )


    #FIRST TEXT APPEARING
    for i in range(10):
        textActor.GetTextProperty().SetOpacity ( i/10 )
        time.sleep(timestep)
        renWin.Render()
        imageFilter.Modified()
        moviewriter.Write()
    textActor.GetTextProperty().SetOpacity ( 1 )

    #FIRST TEXT READING TIME
    for i in range(25):
        if (i==10):
            r,g,b,              opac,spec,diff,amb ,        spec_r,spec_g,spec_b=get_mushroom_colours()
            actorMushroom.GetProperty().SetColor( r, g, b) 
            actorMushroom.GetProperty().SetInterpolationToGouraud ()
            actorMushroom.GetProperty().SetSpecular(spec)
            actorMushroom.GetProperty().SetDiffuseColor( r, g, b )  
            actorMushroom.GetProperty().SetDiffuse(diff)  
            actorMushroom.GetProperty().SetAmbientColor( r, g, b )   
            actorMushroom.GetProperty().SetAmbient(amb)  
            textActor2.GetTextProperty().SetOpacity ( 1 )

        time.sleep(timestep)
        renWin.Render()
        imageFilter.Modified()
        moviewriter.Write()
   
    
    #FULL TISSUES DISAPPEARING
    actorCambium.GetProperty().SetOpacity(1)
    for i in range(10):
        time.sleep(timestep)
        renWin.Render()
        imageFilter.Modified()
        moviewriter.Write()
        actorVesselsFull.GetProperty().SetOpacity((9-i)/10)
        actorMoelleFull.GetProperty().SetOpacity((9-i)/10)
        actorCambiumFull.GetProperty().SetOpacity((9-i)/10)
        textActor.GetTextProperty().SetOpacity ((9-i)/10)
        textActor2.GetTextProperty().SetOpacity ((9-i)/10)
    renderer.RemoveActor(actorVesselsFull)
    renderer.RemoveActor(actorMoelleFull)
    renderer.RemoveActor(actorCambiumFull)
    renderer.RemoveActor(textActor)

    #PLAIN MUSHROOM VIEWING
    for i in range(30):
        time.sleep(timestep)
        renWin.Render()
        imageFilter.Modified()
        moviewriter.Write()





    #MUSHROOM CHANGING TO FINAL MUSHROOM COLOUR, SECOND TEXT APPEARING ######################################################"
    n_transition=10
    r,g,b,              opac,spec,diff,amb ,        spec_r,spec_g,spec_b=get_mushroom_colours()
    textActor = vtk.vtkTextActor()
    text1=""
    text1=text1+"Magnetic Resonance Imaging is used to observe water distribution\n"
    text1=text1+"in the tissues and keep track of active tissues over time.\n"
    text1=text1+""
    textActor.SetInput (text1)
    textActor.SetPosition ( int(round(window_width*80/1200)), window_height-3.3*police_1-10)
    textActor.GetTextProperty().SetFontSize ( police_1 )
    textActor.GetTextProperty().SetFontFamilyToTimes()
    textActor.GetTextProperty().SetColor ( 1.0, 1 , 1 )
    textActor.GetTextProperty().SetOpacity(1)
    renderer.AddActor2D ( textActor )

    #SECOND TEXT READING TIME
    for i in range(250):
        time.sleep(timestep)
        renWin.Render()
        imageFilter.Modified()
        moviewriter.Write()

 
    #SECOND TEXT VANISHING
    for i in range(10):
        textActor.GetTextProperty().SetOpacity ( (10-i)/10 )
        time.sleep(timestep)
        renWin.Render()
        imageFilter.Modified()
        moviewriter.Write()
    renderer.RemoveActor(textActor)
    return actorMushroom    


    #THIRD TEXT AND VIEW ON THREE MRI ######################################################"
    textActor = vtk.vtkTextActor()
    text1=""
    text1=text1+"The specimen is observed four times with MRI,\nwith 35 days between successive acquisitions.\n"
    textActor.SetInput (text1)
    textActor.SetPosition ( int(round(window_width*80/1200)), window_height-3.3*police_1-10)
    textActor.GetTextProperty().SetFontSize ( police_1 )
    textActor.GetTextProperty().SetFontFamilyToTimes()
    textActor.GetTextProperty().SetColor ( 1.0, 1 , 1 )
    textActor.GetTextProperty().SetOpacity(1)
    renderer.AddActor2D ( textActor )

    #SECOND TEXT READING TIME
    for i in range(300):
        if(i==150):
            #Hide all models
            a=1
            #Show MRI one in multiplanar

            #Show MRI two in multiplanar

            #Show MRI three in multiplanar

            #Show MRI four in multiplanar


        time.sleep(timestep)
        renWin.Render()
        imageFilter.Modified()
        moviewriter.Write()

 
    #THIRD TEXT VANISHING
    for i in range(10):
        textActor.GetTextProperty().SetOpacity ( (10-i)/10 )
        #MRI VANISHING
        time.sleep(timestep)
        renWin.Render()
        imageFilter.Modified()
        moviewriter.Write()
    renderer.RemoveActor(textActor)
 
    
    
    #FOURTH TEXT AND VIEW OF LIFE PASSING BY ON MRI ######################################################"
    textActor = vtk.vtkTextActor()
    text1=""
    text1=text1+""
    text1=text1+"The registration procedure align the four images and estimate the tissue deformation\n"
    text1=text1+"This deformation field is then interpolated to produce a time-lapse observation"
    textActor.SetInput (text1)
    textActor.SetPosition ( int(round(window_width*80/1200)), window_height-3.3*police_1-10)
    textActor.GetTextProperty().SetFontSize ( police_1 )
    textActor.GetTextProperty().SetFontFamilyToTimes()
    textActor.GetTextProperty().SetColor ( 1.0, 1 , 1 )
    textActor.GetTextProperty().SetOpacity(1)
    renderer.AddActor2D ( textActor )

    #FOURTH TEXT READING TIME
    for i in range(400):
        if(i==200):
            a=1
            # SHOWING EACH SUCCESSIVE MRI


        time.sleep(timestep)
        renWin.Render()
        imageFilter.Modified()
        moviewriter.Write()

 
    #FOURTH TEXT VANISHING
    for i in range(10):
        textActor.GetTextProperty().SetOpacity ( (10-i)/10 )
        # LAST MRI VANISHING
        time.sleep(timestep)
        renWin.Render()
        imageFilter.Modified()
        moviewriter.Write()
    renderer.RemoveActor(textActor)
 
    
    
    #FIFTH TEXT AND MODEL T0 APPEARING PROGRESSIVELY WITH MUSH IN FINAL ######################################################"
    textActor = vtk.vtkTextActor()
    text1=""
    text1=text1+"From each interpolated MR image, a 3D model is built for visualization purpose\nusing thresholding and isosurface extraction\n"
    text1=text1+"Tissues desactivating during experience are shown in red"
    textActor.SetInput (text1)
    textActor.SetPosition ( int(round(window_width*80/1200)), window_height-3.3*police_1-10)
    textActor.GetTextProperty().SetFontSize ( police_1 )
    textActor.GetTextProperty().SetFontFamilyToTimes()
    textActor.GetTextProperty().SetColor ( 1.0, 1 , 1 )
    textActor.GetTextProperty().SetOpacity(1)
    renderer.AddActor2D ( textActor )

    #FIFTH TEXT READING TIME
    for i in range(400):
        if(i==200):
            a=1
            # SHOWING EACH SUCCESSIVE MRI


        time.sleep(timestep)
        renWin.Render()
        imageFilter.Modified()
        moviewriter.Write()

 
    #FIFTH TEXT VANISHING
    for i in range(10):
        textActor.GetTextProperty().SetOpacity ( (10-i)/10 )
        # LAST MRI VANISHING
        time.sleep(timestep)
        renWin.Render()
        imageFilter.Modified()
        moviewriter.Write()
    renderer.RemoveActor(textActor)
   
    textActor.SetInput (text1)
    textActor.SetPosition ( int(round(window_width*80/1200)), window_height-3.3*police_1-10)
    textActor.GetTextProperty().SetFontSize ( police_1 )
    textActor.GetTextProperty().SetFontFamilyToTimes()
    textActor.GetTextProperty().SetColor ( 1.0, 1 , 1 )
    textActor.GetTextProperty().SetOpacity(1)
    renderer.AddActor2D ( textActor )

    #SECOND TEXT READING TIME
    for i in range(250):
        if(i==150):
            a=1
        time.sleep(timestep)
        renWin.Render()
        imageFilter.Modified()
        moviewriter.Write()

 
    #SECOND TEXT VANISHING
    for i in range(10):
        textActor.GetTextProperty().SetOpacity ( (10-i)/10 )
        time.sleep(timestep)
        renWin.Render()
        imageFilter.Modified()
        moviewriter.Write()
    renderer.RemoveActor(textActor)
    return actorMushroom    









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







""" 
######################################################################################################################################
######### SETUP CAMERA, OBJETS ET LUMIERE      #######################################################################################
######################################################################################################################################
"""
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
    camera.Azimuth(35-5)  
    camera.Roll(-10)
    camera.Azimuth(-15)  

def start_lights(renderer): 
    light_green = vtk.vtkLight()
    renderer.AddLight(light_green)
    light_green2 = vtk.vtkLight()
    renderer.AddLight(light_green2)
    light_green3 = vtk.vtkLight()
    renderer.AddLight(light_green3)
    return light_green,light_green2,light_green3,

def set_lights_on_normal_mode(light_green,light_green2,light_green3):
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    light_green.SetPositional(1)
    light_green.SetPosition(size_x*2, -size_y*2,size_z*2)
    light_green.SetColor(0.6, 0.6, 0.6)
    light_green.SetIntensity(0.7)
    
    light_green2.SetPositional(1)
    light_green2.SetPosition(-size_x*2+1000, size_y*2,size_z*2)
    light_green2.SetColor(0.8, 0.8, 0.8)
    light_green2.SetIntensity(1.0)
    
    light_green3.SetPositional(1)
    light_green3.SetPosition(-size_x*2, size_y*2+1000,size_z*2+1000)
    light_green3.SetColor(0.8, 0.8, 0.8)
    light_green3.SetIntensity(1.4)

def set_lights_on_upper_mode(light_green,light_green2,light_green3):
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    light_green.SetPositional(1)
    light_green.SetPosition(size_x*2, -size_y*2,size_z*2)
    light_green.SetColor(0.6, 0.6, 0.6)
    light_green.SetIntensity(0.7)
    
    light_green2.SetPositional(1)
    light_green2.SetPosition(-size_x*2+1000, size_y*2,size_z*2)
    light_green2.SetColor(0.8, 0.8, 0.8)
    light_green2.SetIntensity(1.0)
    
    light_green3.SetPositional(1)
    light_green3.SetPosition(size_x*2, size_y*2,size_z*2+1000)
    light_green3.SetColor(0.8, 0.8, 0.8)
    light_green3.SetIntensity(0.4)

def setup_movie(framerate,path_to_movie,renWin):
    imageFilter = vtk.vtkWindowToImageFilter()
    imageFilter.SetInput(renWin)
    imageFilter.SetInputBufferTypeToRGB()
    imageFilter.ReadFrontBufferOff()
    imageFilter.Update()
    moviewriter = vtk.vtkOggTheoraWriter() 
    moviewriter.SetRate(framerate) 
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





def build_volume_rendering_view_from_image(path_source,opac,renderer,crop_type):
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
  
    
    volumeMapper = vtk.vtkSmartVolumeMapper()
    volumeMapper.SetBlendModeToComposite()
    volumeMapper.SetInputConnection(dataImporter.GetOutputPort());
#else
#  volumeMapper->SetInputData(imageData);
    volumeProperty = vtk.vtkVolumeProperty()
    volumeProperty.ShadeOn()
#    volumeProperty.SetInterpolationType(VTK_LINEAR_INTERPOLATION);
  
    compositeOpacity = vtk.vtkPiecewiseFunction()
    compositeOpacity.AddPoint(0.0,0.0);
    compositeOpacity.AddPoint(100.0,0.0);
    compositeOpacity.AddPoint(255.0,opac);
    volumeProperty.SetScalarOpacity(compositeOpacity)
      
    color = vtk.vtkColorTransferFunction()
    color.AddRGBPoint(0.0  ,0.0,0.0,0.0)
    color.AddRGBPoint(100.0  ,0.0,0.0,0.0)
#    color.AddRGBPoint(40.0  ,1.0,0.0,0.0)
    color.AddRGBPoint(255.0,1.0,1.0,1.0)
    volumeProperty.SetColor(color)
    
    volume = vtk.vtkVolume()
    volume.SetMapper(volumeMapper)
    volume.SetProperty(volumeProperty)
    renderer.AddViewProp(volume)
  
#    volumeMapper.SetRequestedRenderModeToRayCastAndTexture()
    volumeMapper.SetRequestedRenderModeToRayCast()
    return volume


def build_moelle(day_i,inter,renderer,actor,usePrecomputed,crop_type=1):
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

def build_cambium(day_i,inter,renderer,actor,usePrecomputed,crop_type=1):
    day_i_plus=day_i+1
    basenom=str(day_i)+str(day_i_plus)+'_'+str(inter)
    source_rep=get_source_rep()
    r,g,b=get_cambium_colour()
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


def build_silhouette(day_i,inter,renderer,actor,usePrecomputed):
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


def build_vessels(day_i,inter,renderer,actor,usePrecomputed,crop_type=1):
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



def build_vr(day_i,inter,renderer,volume,usePrecomputed,crop_type=0):
    day_i_plus=day_i+1
    basenom=str(day_i)+str(day_i_plus)+'_'+str(inter)
    source_rep=get_source_rep()
    opac=1
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants(crop_type)
        
    if(volume is None):
        a=1        
    else:
        volume.SetVisibility(False)
        renderer.RemoveViewProp(volume)
    volume=build_volume_rendering_view_from_image(source_rep+'/images/full'+basenom+'.tif',opac,renderer,crop_type)
    volume.SetVisibility(True)
    return volume






def build_mpr(day_i,inter,renderer,volume,usePrecomputed,crop_type=0):
    day_i_plus=day_i+1
    basenom=str(day_i)+str(day_i_plus)+'_'+str(inter)
    source_rep=get_source_rep()
    opac=1
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants(crop_type)
        
    if(volume is None):
        a=1        
    else:
        volume.SetVisibility(False)
        renderer.RemoveViewProp(volume)
    XY_plane,XZ_plane,YZ_plane=build_multi_planar_view_from_image(source_rep+'/images/full'+basenom+'.tif',opac,renderer,crop_type)
    return XY_plane,XZ_plane,YZ_plane







""" 
######################################################################################################################################
#########  CHANGEMENTS DE VUE ET RETOUR VUE    #######################################################################################
######################################################################################################################################
 """
def to_front_view(camera):
    camera.Azimuth(-55+5)
    camera.Elevation(-35)
    camera.Roll(2)
    camera.SetFocalPoint(160,150,206)
    camera.Zoom(2.3)

def from_front_view(camera):
    camera.Zoom(1/2.3)
    camera.SetFocalPoint(160,150,236)
    camera.Roll(-2)
    camera.Elevation(35)
    camera.Azimuth(55-5)
 

def from_up_view(camera):
    camera.Zoom(1/4.3)
    camera.Roll(83)
    camera.SetFocalPoint(160,150,236)
    camera.Elevation(-50)
    camera.Azimuth(60-5)

def to_up_view(camera):
    camera.Azimuth(-60+5)
    camera.Elevation(50)
    camera.SetFocalPoint(160,230,236)
    camera.Roll(-83)
    camera.Zoom(4.3)



def to_right_view(camera):
    camera.Azimuth(21+5)
    camera.Elevation(-30)
    camera.Zoom(2.8)
    camera.Yaw(4)
    camera.Roll(-1.2)

def from_right_view(camera):
    camera.Roll(1.2)
    camera.Yaw(-4)
    camera.Zoom(1/2.8)
    camera.Elevation(30)
    camera.Azimuth(-21-5)




""" 
######################################################################################################################################
#########  SETUP ET MODIF AFFICHAGE LEGENDE    #######################################################################################
######################################################################################################################################
 """
def setup_rectangles(day_max,mobile_rendering,renderer):
    window_width,window_height,x_margin,text_width,y_margin,text_height,police_1,police_2,x_plus,space_between_texts=window_size_config(day_max,mobile_rendering)
    rinterp,ginterp,binterp=get_interpolation_colour()
    #FOND NOIR
    for i in range(int((window_width-x_margin+202)/3)):
        for j in range(int(21+2*y_margin/3)):
            actT=vtk.vtkTextActor()
            actT.SetInput ( "-" )
            actT.SetPosition ( x_margin/2+i*3-112, window_height-7-40-j*3+6 )
            actT.GetTextProperty().SetFontSize ( police_1*6 )
            actT.GetTextProperty().SetFontFamilyToTimes()
            actT.GetTextProperty().SetColor (rinterp,ginterp)
            actT.GetTextProperty().SetOpacity(0.02)
            renderer.AddActor2D ( actT )

    #FOND INTERPOLATION
    for d in range(day_max):
        for i in range(int(((window_width-2*x_margin)/day_max)/3)):
            for j in range(int(y_margin/4)):
                actT=vtk.vtkTextActor()
                actT.SetInput ( "-" )
                actT.SetPosition (space_between_texts*d+ x_margin/2+i*3, window_height-7-40-j*3+6 )
                actT.GetTextProperty().SetFontSize ( police_1*6 )
                actT.GetTextProperty().SetFontFamilyToTimes()
                actT.GetTextProperty().SetColor ( rinterp,ginterp)
                actT.GetTextProperty().SetOpacity(0.02)
                renderer.AddActor2D ( actT )

def setup_text_and_progress_bar(day_max,renderer,mobile_rendering):
    window_width,window_height,x_margin,text_width,y_margin,text_height,police_1,police_2,x_plus,space_between_texts=window_size_config(day_max,mobile_rendering)
    rmri,gmri,bmri=get_mri_colour()
    rinterp,ginterp,binterp=get_interpolation_colour()

    #AFFICHER LES TEXTES t=..  et les textes MRI acquisition et les textes Interpolation    
    for ind_texte in range(day_max+1):
        textActor = vtk.vtkTextActor()
        textActor.SetInput ( "t = "+str((ind_texte)*35)+" days" )
        textActor.SetPosition ( x_margin+space_between_texts*ind_texte +x_plus, window_height-y_margin)
        textActor.GetTextProperty().SetFontSize ( police_2 )
        textActor.GetTextProperty().SetFontFamilyToTimes()
        textActor.GetTextProperty().SetColor ( rmri,gmri,bmri )
        renderer.AddActor2D ( textActor )

        textActor = vtk.vtkTextActor()
        textActor.SetInput ( "MRI acquisition" )
        textActor.SetPosition ( x_margin+space_between_texts*ind_texte +x_plus, window_height-2*y_margin)
        textActor.GetTextProperty().SetFontSize ( (police_2*2)/3 )
        textActor.GetTextProperty().SetFontFamilyToTimes()
        textActor.GetTextProperty().SetColor ( rmri,gmri,bmri )
        renderer.AddActor2D ( textActor )

        if(ind_texte>0):
            textActor = vtk.vtkTextActor()
            textActor.SetInput ( "Interpolation" )
            textActor.SetPosition ( x_margin+space_between_texts*(ind_texte-0.5) +x_plus, window_height-2*y_margin)
            textActor.GetTextProperty().SetFontSize ( (police_2*2)/3 )
            textActor.GetTextProperty().SetFontFamilyToTimes()
            textActor.GetTextProperty().SetColor ( rinterp,ginterp,binterp )
            renderer.AddActor2D ( textActor )

    #AFFICHER LA TIMELINE
    for i in range(182):
        actT=vtk.vtkTextActor()
        actT.SetInput ( "-" )
        actT.SetPosition ( x_margin/2+56+i*5 +x_plus, window_height-y_margin-27-20 )
        actT.GetTextProperty().SetFontSize ( police_1+6 )
        actT.GetTextProperty().SetFontFamilyToTimes()
        actT.GetTextProperty().SetColor ( 1.0, 1.0, 1.0)
        actT.GetTextProperty().SetOpacity(1)
        renderer.AddActor2D ( actT )

    #AFFICHER LES POINTS IRM SUR LA TIMELINE
    for i in range(day_max+1):
        actT=vtk.vtkTextActor()
        actT.SetInput ( "|" )
        actT.SetPosition ( x_margin+i*5+38+space_between_texts*i +x_plus, window_height-y_margin-28-20 )
        actT.GetTextProperty().SetFontSize ( (police_1*4)/3 )
        actT.GetTextProperty().SetFontFamilyToTimes()
        actT.GetTextProperty().SetColor (  rmri,gmri,bmri )
        actT.GetTextProperty().SetOpacity(1)
        renderer.AddActor2D ( actT )
        actT=vtk.vtkTextActor()
        actT.SetInput ( "-" )
        actT.SetPosition ( x_margin+i*5+43+space_between_texts*i +x_plus, window_height-y_margin-27-20 )
        actT.GetTextProperty().SetFontSize ( police_1+6 )
        actT.GetTextProperty().SetFontFamilyToTimes()
        actT.GetTextProperty().SetColor ( 1.0, 1.0, 1.0) 
        actT.GetTextProperty().SetOpacity(1)
        renderer.AddActor2D ( actT )
        actT=vtk.vtkTextActor()

    actT=vtk.vtkTextActor()
    actT.SetInput ( ">" )
    actT.SetPosition ( x_margin/2-149+220*5 +x_plus, window_height-y_margin-25-20 )
    actT.GetTextProperty().SetFontSize ( police_1 )
    actT.GetTextProperty().SetFontFamilyToTimes()
    actT.GetTextProperty().SetColor ( 1.0, 1.0, 1.0 )
    actT.GetTextProperty().SetOpacity(1)
    renderer.AddActor2D ( actT )


    actP=vtk.vtkTextActor()
    actP.SetInput ( "." )
    actP.SetPosition ( compute_x_screen_from_time_value(0,x_margin,space_between_texts,x_plus,False), window_height-y_margin-58-20  +x_plus)
    actP.GetTextProperty().SetFontSize ( police_1*5 )
    actP.GetTextProperty().SetFontFamilyToTimes()
    actP.GetTextProperty().SetColor ( 1.0, 1.0, 1.0 )
    actP.GetTextProperty().SetOpacity(1)
    renderer.AddActor2D ( actP )
      
    return textActorMRI,textActorINTER,actP

def compute_x_screen_from_time_value(x_time,day_max,mobile_rendering=0):
    window_width,window_height,x_margin,text_width,y_margin,text_height,police_1,police_2,x_plus,space_between_texts=window_size_config(day_max,mobile_rendering)
    return x_margin+25+(5+space_between_texts)*x_time +x_plus

def update_moving_legends(textActorMRI,textActorINTERP,actP,x_time,mobile_rendering=0):
    window_width,window_height,x_margin,text_width,y_margin,text_height,police_1,police_2,x_plus,space_between_texts=window_size_config(day_max,mobile_rendering)
    actP.SetPosition ( compute_x_screen_from_time_value(x_time,x_margin,space_between_texts,x_plus,False), window_height-y_margin-58-20 )
