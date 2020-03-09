#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jul 18 13:22:39 2019

@author: fernandr
"""

    
from build_objects_V08 import *

def sequence_01_title(day_max,nb_interp,n_frames,timestep,renWin,imageFilter,moviewriter,camera,renderer,mobile_rendering=0):
    window_width,window_height,x_margin,text_width,y_margin,text_height,police_1,police_2,x_plus,space_between_texts=window_size_config(day_max,mobile_rendering)
    trans_object,trans_text,reading_time=get_transition_times()
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    rectangleActor=setup_rectangle(day_max,mobile_rendering,renderer,0.18,True,0,0,0)

    light=add_light_right_vr(renderer)
    sigma_level=6

    text1=""
    text1=text1+"     Vine infection by fungal inoculum\n"
    text1=text1+"observed through Magnetic Resonance Imaging"
    textActor=add_text(text1,window_width*0.13,window_height-3*police_1-10,5*police_1//4,0,day_max,mobile_rendering,renderer)
    actorInoc=build_mushroom(0,0,nb_interp,renderer,None,sigma_level)
    actorInoc.GetProperty().SetOpacity(1)



    camera.Elevation(-5)
    camera.Azimuth(30)
    camera.Zoom(1.5)
    actorPlane=build_planar(2,0,nb_interp,renderer,None,0,0,2)
    actorPlane.GetProperty().SetOpacity(1)
    slice=z_begin_irm+(z_end_irm-z_begin_irm)//2
    set_slice(actorPlane,2,slice)
    text_and_actors_appearing(trans_text,textActor,(actorPlane,actorInoc),None,renderer,timestep,renWin,imageFilter,moviewriter,(1.0,1.0,1.0,0.9))
    actorVolume=build_vr(0,0,nb_interp,renderer,None,4,130,285)
    n_total=day_max*nb_interp+1
    for da in range(day_max):
        for inte in range(nb_interp):
            print(str(da)+" "+str(inte))
            print()
            print('actor volume')
            actorVolume=build_vr(da,inte,nb_interp,renderer,actorVolume,4,130,285)
            print()
            print('actor plane')
            actorPlane=build_planar(2,da,inte,renderer,actorPlane,0,0,2)
            print()
            print('actor silhouette')
            #actorSilhouette=build_silhouette(0,0,renderer,actorSilhouette)
            #actorSilhouette=build_silhouette(da,inte,renderer,actorSilhouette)
            print('here='+str(sigma_level))
#            actorInoc=build_mushroom(da,inte,nb_interp,renderer,actorInoc,sigma_level)
            actorInoc=build_mushroom_continuous(da,inte,nb_interp,renderer,actorInoc)
            actorInoc.GetProperty().SetOpacity(1)
            index=da*nb_interp+inte
            set_actor_rgb(actorInoc,1,0.1+0.5*(1-index/n_total),0.1+0.5*(1-index/n_total))
            actorInoc.GetProperty().SetSpecularColor(1, 0.3, 0.3)      
            snapshot(timestep,renWin,imageFilter,moviewriter)
            
    text_and_actors_disappearing(trans_text,(textActor,),None,None,renderer,timestep,renWin,imageFilter,moviewriter,(1.0,1.0,1.0,0.9))
    renderer.RemoveViewProp(actorVolume)
    renderer.RemoveActor(actorPlane)
    renderer.RemoveActor(actorInoc)
    camera.Zoom(0.66667)
    camera.Azimuth(-30)
    camera.Elevation(5)
    renderer.RemoveActor(rectangleActor)
    light.SetIntensity(0)
    
    
    
    
    
    
    
    
    
    
    
def sequence_02_retrait_ecorce(day_max, timestep,renWin,imageFilter,moviewriter,camera,renderer,mobile_rendering=0):
    window_width,window_height,x_margin,text_width,y_margin,text_height,police_1,police_2,x_plus,space_between_texts=window_size_config(day_max,mobile_rendering)
    trans_object,trans_text,reading_time=get_transition_times()
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    rectangleActor=setup_rectangle(day_max,mobile_rendering,renderer,0.15,True,0,0,0)

    actorInoc=build_mushroom(0,0,120,renderer,None,4)
    actorVessels=build_vessels(0,0,renderer,None,0)
    actorMoelle=build_moelle(0,0,renderer,None,0)
    actorCambium=build_cambium(0,0,renderer,None,0)
    actorVessels.GetProperty().SetOpacity(0)
    actorCambium.GetProperty().SetOpacity(0)
    actorMoelle.GetProperty().SetOpacity(0)
    set_actor_color_to_cambium(actorInoc)    

    # OBJECT APPEARING WITH DRIVEN LEGEND
    text1="Experiments are conducted on one-year-old vine cutting."
    textActor=add_text(text1,window_width*150/1200,window_height-2*police_1-10,police_1,0,day_max,mobile_rendering,renderer)
    text_and_actors_appearing(trans_text,textActor,(actorVessels,actorCambium,actorMoelle,actorInoc),None,renderer,timestep,renWin,imageFilter,moviewriter)
    sequence_idle(reading_time*0.4,timestep,renWin,imageFilter,moviewriter,camera)

    text_and_actors_disappearing(trans_object,(textActor,),None,None,renderer,timestep,renWin,imageFilter,moviewriter)    
    sequence_idle(trans_text,timestep,renWin,imageFilter,moviewriter,camera)
    text1="   A square piece of bark is taken off."
    textActor=add_text(text1,window_width*150/1200,window_height-2*police_1-10,police_1,0,day_max,mobile_rendering,renderer)
    text_and_actors_appearing(trans_text,textActor,None,None,renderer,timestep,renWin,imageFilter,moviewriter)
    sequence_idle(reading_time*0.2,timestep,renWin,imageFilter,moviewriter,camera)
   
     # BARK PIECE GOING BLACK
    for i in range(trans_object):
        actor_going_black(actorInoc,trans_object,i+1)
        snapshot(timestep,renWin,imageFilter,moviewriter)   
    sequence_idle(trans_object,timestep,renWin,imageFilter,moviewriter,camera)

    # BARK PIECE GOING TRANSLUCENT
    text_and_actors_disappearing(trans_object,None,(actorInoc,),None,renderer,timestep,renWin,imageFilter,moviewriter)    
    sequence_idle(trans_object*2,timestep,renWin,imageFilter,moviewriter,camera)
     
    #TEXT VANISHING
    text_and_actors_disappearing(trans_object,(textActor,),None,None,renderer,timestep,renWin,imageFilter,moviewriter)    
    renderer.RemoveActor(textActor)
    sequence_idle(trans_object,timestep,renWin,imageFilter,moviewriter,camera)



    # FIRST TEXT APPEARING
    text1=" Fungal inoculum is inserted inside with agarose\n"
    textActor=add_text(text1,window_width*80/1200,window_height-3*police_1-10,police_1,0,day_max,mobile_rendering,renderer)
    text_and_actors_appearing(trans_text,textActor,None,None,renderer,timestep,renWin,imageFilter,moviewriter)
 
    # WAITING, AND SUDDENLY DISPLAYING RED INOCULUM
    textActor2=add_text("fungal inoculum",int(round(window_width*80/1200))+int(round(police_1*8.3)),window_height-1.92*police_1-10,police_1,0,day_max,mobile_rendering,renderer,1.0,0.1,0.1)
    sequence_idle(trans_object*15,timestep,renWin,imageFilter,moviewriter,camera)
    textActor2.GetTextProperty().SetOpacity ( 1 )
    set_actor_rgb(actorInoc,1,0.1,0.1)
    actorInoc.GetProperty().SetOpacity(1)
    sequence_idle(trans_object*5,timestep,renWin,imageFilter,moviewriter,camera)

     # EVERYTHING DISAPPEARING
    text_and_actors_disappearing(trans_text,(rectangleActor,textActor,textActor2),None,None,renderer,timestep,renWin,imageFilter,moviewriter)    
    text_actors_and_props_removed((rectangleActor,textActor,textActor2),(actorInoc,actorVessels,actorCambium,actorMoelle),None,renderer)















def sequence_03_mri_observations(day_max, timestep,nb_interp,renWin,imageFilter,moviewriter,camera,renderer,mobile_rendering=0):
    window_width,window_height,x_margin,text_width,y_margin,text_height,police_1,police_2,x_plus,space_between_texts=window_size_config(day_max,mobile_rendering)
    trans_object,trans_text,reading_time=get_transition_times()
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()

    actorVolume=None
    actorPlane=build_planar(2,0,0,renderer,None,0,0,2)
    actorPlane.GetProperty().SetOpacity(0)
    slice=z_begin_irm
    print("setting slice "+str(slice))
    set_slice(actorPlane,2,slice)

    rectangleActor=setup_rectangle(day_max,mobile_rendering,renderer,0.15,True,0,0,0)
    text1="     Vine is observed with Magnetic Resonance Imaging (MRI)"
    textActor=add_text(text1,window_width*140/1200,window_height-2.3*police_1-10,police_1,0,day_max,mobile_rendering,renderer)
    text_and_actors_appearing(trans_text,textActor,None,None,renderer,timestep,renWin,imageFilter,moviewriter)
    sequence_idle(reading_time*0.2,timestep,renWin,imageFilter,moviewriter,camera)
   
    # READING TIME
    timeMRI_idling=0
    timeMRI_starting=3*trans_object
    timeMRI_at_the_top=6*trans_object
    timeMRI_at_the_down=15*trans_object
    diff_frames=timeMRI_at_the_top-timeMRI_starting
    diff_z=z_end_irm-1-z_begin_irm
    for i in range(timeMRI_at_the_down):
        print('')
        print('i='+str(i))
        
        if(i==timeMRI_idling):
            #MRI planar appears at slice zMax
            actorPlane.GetProperty().SetOpacity(1)
            slice=z_end_irm-1
            set_slice(actorPlane,2,slice)

        if((i>=timeMRI_starting) & (i<timeMRI_at_the_top)):
            #MRI planar starts slicing
            diff_i=i-timeMRI_starting
            slice=int(round(z_end_irm-1-diff_i*(diff_z/diff_frames)))
            set_slice(actorPlane,2,slice)
            
        if(i>=timeMRI_at_the_top):
            #MRI planar slice down, appearing volume rendering
            diff_i=i-timeMRI_at_the_top
            slice=int(round(z_begin_irm+diff_i*(diff_z/diff_frames)))
            set_slice(actorPlane,2,slice)
            actorVolume=build_vr(0,0,nb_interp,renderer,actorVolume,0,z_begin_irm,slice)
        renderer.ResetCameraClippingRange()
        snapshot(timestep,renWin,imageFilter,moviewriter)

    #Second text
    text_and_actors_disappearing(trans_text,(textActor,),None,None,renderer,timestep,renWin,imageFilter,moviewriter)    
    sequence_idle(trans_text,timestep,renWin,imageFilter,moviewriter,camera)   
    text1="Acquisition parameters are set so as to detect\nthe presence of water to keep track of active tissues"
    textActor=add_text(text1,window_width*140/1200,window_height-2.3*police_1-10,police_1,0,day_max,mobile_rendering,renderer)
    text_and_actors_appearing(trans_text,textActor,None,None,renderer,timestep,renWin,imageFilter,moviewriter)
    sequence_idle(reading_time*0.6,timestep,renWin,imageFilter,moviewriter,camera)    

    #second text and object vanishing
    set_volume_opacity(actorVolume,0,40,255)
    text_and_actors_disappearing(trans_text,(textActor,),(actorPlane,),(actorVolume,),renderer,timestep,renWin,imageFilter,moviewriter)    

    text_actors_and_props_removed((textActor,rectangleActor),None,(actorPlane,actorVolume),renderer)
    sequence_idle(trans_object,timestep,renWin,imageFilter,moviewriter,camera)    
    













def sequence_04_successive_volumes(day_max,nb_interp, timestep,renWin,imageFilter,moviewriter,camera,renderer,mobile_rendering=0):
    window_width,window_height,x_margin,text_width,y_margin,text_height,police_1,police_2,x_plus,space_between_texts=window_size_config(day_max,mobile_rendering)
    trans_object,trans_text,reading_time=get_transition_times()
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()

    rectangleActor=setup_rectangle(day_max,mobile_rendering,renderer,0.15,True,0,0,0)
    actorVolume=None
    text1="The specimen is observed over a 105-day period,\nonce every 35 days"
    textActor=add_text(text1,window_width*80/1200,window_height-3*police_1-10,police_1,0,day_max,mobile_rendering,renderer)
    text_and_actors_appearing(trans_text,textActor,None,None,renderer,timestep,renWin,imageFilter,moviewriter)
    sequence_idle(reading_time*0.7,timestep,renWin,imageFilter,moviewriter,camera)


    #appearing IRM i and legend i
    for da in range(day_max+1):
        text1="Image stack I\nobservation at t = "+str(35*da)+" days"
        textActor2=add_text(text1,window_width*50/1200,window_height-18.3*police_1-10,police_1,0,day_max,mobile_rendering,renderer)
        text2=""+str(35*da)+""
        textActor3=add_text(text2,window_width*80/1200,window_height-18.3*police_1-10,police_1/2,0,day_max,mobile_rendering,renderer)
        textActor2.GetProperty().SetOpacity(1)
        textActor3.GetProperty().SetOpacity(1)

        timeMRI_at_the_top=0*trans_object
        timeMRI_at_the_down=2*trans_object
        diff_frames=timeMRI_at_the_down-timeMRI_at_the_top
        diff_z=z_end_irm-1-z_begin_irm
        if da==0:
            actorPlane=build_planar(2,da,0,renderer,None,0,0,2)
        else:
            actorPlane=build_planar(2,(da-1),nb_interp,renderer,None,0,0,2)
        for i in range(timeMRI_at_the_down):
            diff_i=i-timeMRI_at_the_top
            slice=int(round(z_begin_irm+diff_i*(diff_z/diff_frames)))
            set_slice(actorPlane,2,slice)
            if da==0:
                actorVolume=build_vr(da,0,nb_interp,renderer,actorVolume,0,z_begin_irm,slice)
            else:
                actorVolume=build_vr(da-1,nb_interp,nb_interp,renderer,actorVolume,0,z_begin_irm,slice)
            renderer.ResetCameraClippingRange()
            snapshot(timestep,renWin,imageFilter,moviewriter)

        sequence_idle(trans_object*4,timestep,renWin,imageFilter,moviewriter,camera)
     
        # volume and text disappearing
        set_volume_opacity(actorVolume,0,40,255)
        text_and_actors_disappearing(1,(textActor2,textActor3),(actorPlane,),None,renderer,timestep,renWin,imageFilter,moviewriter)        
        text_actors_and_props_removed((textActor2,),None,(actorPlane,actorVolume),renderer)
        sequence_idle(trans_object,timestep,renWin,imageFilter,moviewriter,camera)    
    
    #main text disappearing
    text_and_actors_disappearing(trans_text,(textActor,),None,None,renderer,timestep,renWin,imageFilter,moviewriter)        
    text_actors_and_props_removed((textActor,rectangleActor),None,None,renderer)

    sequence_idle(trans_object,timestep,renWin,imageFilter,moviewriter,camera)    
     

    


def sequence_05_registration(day_max, timestep,nb_interp,renWin,imageFilter,moviewriter,camera,renderer,mobile_rendering=0):
    window_width,window_height,x_margin,text_width,y_margin,text_height,police_1,police_2,x_plus,space_between_texts=window_size_config(day_max,mobile_rendering)
    trans_object,trans_text,reading_time=get_transition_times()
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
    slice=245
    distance_init=0
    actorPlane1=None
    actorPlane2=None
    to_up_centered_view(camera)
    y_offset=50
    x_offset=-210
    rectangleActorUp=setup_rectangle(day_max,mobile_rendering,renderer,0.15,True,0,0,0)
    rectangleActorDown=setup_rectangle(day_max,mobile_rendering,renderer,0.15,False,0,0,0)

    camera.Elevation(-180)
    camera.Zoom(0.7)
    incr=0
    t_app1=30
    t_app2=30
    t_waiting_rec=40
    t_during_rec_1_sin=100
    t_waiting_rec_2_dense=35
    t_during_rec=120
    t_waiting_forward=60    
    n_total_frames=776
    t_forward=n_total_frames-t_during_rec-t_waiting_rec-t_app2-t_app1
    plane=None
    actual_t2_time=35
    actual_t1_time=0
    actual_fusion_time=0


    #appearing T1
    for t in range (t_app1):
        plane=build_planar_slice(t,renderer,plane,x_offset,y_offset)        
        renderer.ResetCameraClippingRange()
        print(t)
        snapshot(timestep,renWin,imageFilter,moviewriter)
    text1="I"
    textActorT1=add_text(text1,window_width*(77/1200), 4*(police_2+police_1)//3,(police_2+police_1)//2,0,day_max,mobile_rendering,renderer,0.2,1,0.2)
    text2=""+str(0)+""
    textActorT12=add_text(text2,window_width*80/1200,4*(police_2+police_1)//3,(police_2+police_1)//4,0,day_max,mobile_rendering,renderer)
    textActorT1.GetProperty().SetOpacity(1)
    textActorT12.GetProperty().SetOpacity(1)
    incr=incr+t_app1
     #Preparing TX
    text3="Fused image\nat t="
    textActorTX=add_text(text3,window_width*(500)/1200,4*(police_2+police_1)//3,(police_2+police_1)//2,0,day_max,mobile_rendering,renderer)
   
    
    
    #appearing T2
    for t in range (t_app2):
        plane=build_planar_slice(t+incr,renderer,plane,x_offset,y_offset)        
        renderer.ResetCameraClippingRange()
        print(t)
        snapshot(timestep,renWin,imageFilter,moviewriter)
    text2="Original image at t=35 days"
    textActorT2=add_text(text2,window_width*(777/1200), 4*(police_2+police_1)//3,(police_2+police_1)//2,0,day_max,mobile_rendering,renderer,1.0,0,0)
    text_and_actors_appearing(trans_text,textActorT2,None,None,renderer,timestep,renWin,imageFilter,moviewriter)

    text1="I"
    textActorT2=add_text(text1,window_width*(777/1200), 4*(police_2+police_1)//3,(police_2+police_1)//2,0,day_max,mobile_rendering,renderer,1.0,0,0)
    text2=""+str(35)+""
    textActorT22=add_text(text2,window_width*777/1200,4*(police_2+police_1)//3,(police_2+police_1)//4,0,day_max,mobile_rendering,renderer)
    textActorT2.GetProperty().SetOpacity(1)
    textActorT22.GetProperty().SetOpacity(1)




    text1="The four successive image stacks I , I  , I  and I   \nare registered pairwise to link the successive observations"
    textActor=add_text(text1,window_width*160/1200, window_height-3*police_1-10,police_1,0,day_max,mobile_rendering,renderer,1.0,1.0,1.0)
    text2="  0   35   70   105"
    textActor2=add_text(text2,window_width*160/1200,window_height-3*police_1-10,police_1//2,0,day_max,mobile_rendering,renderer)
    textActor.GetProperty().SetOpacity(1)
    textActor2.GetProperty().SetOpacity(1)
    sequence_idle(reading_time*0.5,timestep,renWin,imageFilter,moviewriter,camera)    


    #Rapprochement en translation
    incr=incr+t_app2
    for t in range (t_waiting_rec+t_during_rec_1_sin):
        plane=build_planar_slice(t+incr,renderer,plane,x_offset,y_offset)        
        renderer.ResetCameraClippingRange()
        print(t)
        snapshot(timestep,renWin,imageFilter,moviewriter)


    #Zoom
    progressive_zoom(timestep,renWin,imageFilter,moviewriter,camera)

 
    #Recalage
    incr=incr+t_waiting_rec+t_during_rec_1_sin+t_waiting_rec_2_dense
    start_act=35
    posx,posy=textActorT2.GetPosition()
    textActorT2.SetPosition(posx,posy-(police_2+police_1)/2);
    for t in range (t_during_rec):
        actual_t2_time=int(round((start_act-0)*(t_during_rec-1-t)/t_during_rec))
        plane=build_planar_slice(t+incr,renderer,plane,x_offset,y_offset)
        textActorT2.SetInput("I  interpolated at t="+str(actual_t2_time)+" days")
        renderer.ResetCameraClippingRange()
        print(t)
        snapshot(timestep,renWin,imageFilter,moviewriter)
    text_and_actors_disappearing(trans_text,(textActor,),None,None,renderer,timestep,renWin,imageFilter,moviewriter)        
    text_actors_and_props_removed((textActor,),None,None,renderer)
    sequence_idle(trans_object,timestep,renWin,imageFilter,moviewriter,camera)    
    renderer.RemoveActor(rectangleActorUp)
    sequence_idle(2*trans_object,timestep,renWin,imageFilter,moviewriter,camera)    



    #New text and moving text T1
    rectangleActorUp=setup_rectangle(day_max,mobile_rendering,renderer,0.15,True,0,0,0)
    text="The deformations estimated during registration\nare used to interpolate images"
    textActor=add_text(text,window_width*160/1200, window_height-3*police_1-10,police_1,0,day_max,mobile_rendering,renderer)
    text_and_actors_appearing(trans_text,textActor,None,None,renderer,timestep,renWin,imageFilter,moviewriter)
    posx,posy=textActorT1.GetPosition()
    textActorT1.SetPosition(posx,posy-(police_2+police_1)/2);
    posx,posy=textActorTX.GetPosition()
    textActorTX.SetPosition(posx,posy-(police_2+police_1)/2);
    sequence_idle(reading_time*0.5,timestep,renWin,imageFilter,moviewriter,camera)    
    
    
    t_appear_white=245
    t_only_white=275
    incr=incr+t_during_rec
    opac_X=0
    n_fra,vect_time,vect_day,vect_fra=progressive_acceleration_in_time2(nb_interp,day_max,incr)
    print ('frames : '+str(n_fra))
    for t in range (n_fra):
        actual_t1_time=int(round(35*(vect_day[t]+vect_time[t]/120.0)))
        actual_t2_time=actual_t1_time
        if ( (t>=t_appear_white) & (t<t_only_white) ):
            opac_X= (t+1-t_appear_white)/(t_only_white-t_appear_white)
        textActorT1.SetInput("I  interpolated at t="+str(actual_t1_time)+" days")
        textActorT2.SetInput("I   interpolated at t="+str(actual_t2_time)+" days")
        textActorTX.SetInput("Fused image at t="+str(actual_t2_time)+" days")
        textActorT1.GetTextProperty().SetOpacity(1-opac_X)
        textActorT12.GetTextProperty().SetOpacity(1-opac_X)
        textActorT2.GetTextProperty().SetOpacity(1-opac_X)
        textActorT22.GetTextProperty().SetOpacity(1-opac_X)
        textActorTX.GetTextProperty().SetOpacity(opac_X)
        plane=build_planar_slice(int(round(vect_fra[t])),renderer,plane,x_offset,y_offset)
        renderer.ResetCameraClippingRange()
        print(t)
        snapshot(timestep,renWin,imageFilter,moviewriter)
 
    sequence_idle(trans_object,timestep,renWin,imageFilter,moviewriter,camera)    
    text_and_actors_disappearing(trans_text,(textActor,textActor2,textActorT1,textActorT2,textActorT12,textActorT22,textActorTX),None,None,renderer,timestep,renWin,imageFilter,moviewriter)        
    text_actors_and_props_removed((textActor,rectangleActorUp,rectangleActorDown,textActor2,textActorT1,textActorT2,textActorT12,textActorT22,textActorTX),None,None,renderer)
    renderer.RemoveViewProp(plane)



def sequence_07_interpolation_volume  (day_max, timestep,nb_interp,renWin,imageFilter,moviewriter,camera,renderer,mobile_rendering=0):
    window_width,window_height,x_margin,text_width,y_margin,text_height,police_1,police_2,x_plus,space_between_texts=window_size_config(day_max,mobile_rendering)
    trans_object,trans_text,reading_time=get_transition_times()
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()

    rectangleActor=setup_rectangle(day_max,mobile_rendering,renderer,0.15,True,0,0,0)
    light=new_light_for_front_view(renderer)  
    to_front_view(camera)



    # Text and volumes appearing
    text1="Interpolation over time helps building a \"time-lapse observation\"\nwith a very high temporal resolution (one computed image every 6 hours)\n"
    textActor=add_text(text1,window_width*80/1200,window_height-3.3*police_1-10,police_1,0,day_max,mobile_rendering,renderer)
    actorVolume=build_vr(0,0,nb_interp,renderer,None,0,z_begin_irm,z_end_irm,1)
    text_and_actors_appearing(trans_text,textActor,None,actorVolume,renderer,timestep,renWin,imageFilter,moviewriter)
    sequence_idle(2*reading_time//3,timestep,renWin,imageFilter,moviewriter,camera)



    # Slicing time over volume
    for da in range(day_max):
        if(da==day_max):
            n_int=nb_interp+1
        else:
            n_int=nb_interp
        for ti in range(n_int):
            print('ti='+str(ti)+'da='+str(da))
            actorVolume=build_vr(da,ti,nb_interp,renderer,actorVolume,0,z_begin_irm,z_end_irm,1)
            snapshot(timestep,renWin,imageFilter,moviewriter)

    renderer.RemoveActor(textActor)
    sequence_idle(trans_object,timestep,renWin,imageFilter,moviewriter,camera)    
    
    #Second text appearing, then everything disappear
    text1="Unactivated tissues appear as areas vanishing over time"
    textActor=add_text(text1,window_width*100/1200,window_height-2.3*police_1-10,police_1,0,day_max,mobile_rendering,renderer)
    text_and_actors_appearing(trans_text,textActor,None,None,renderer,timestep,renWin,imageFilter,moviewriter)
    sequence_idle(reading_time//2,timestep,renWin,imageFilter,moviewriter,camera)
    text_and_actors_disappearing(trans_text,(textActor,),None,None,renderer,timestep,renWin,imageFilter,moviewriter)        
    text_actors_and_props_removed((textActor,rectangleActor),None,(actorVolume,),renderer)
    snapshot(timestep,renWin,imageFilter,moviewriter)

    from_front_view(camera)
    light.SetIntensity(0)






def sequence_08_destruction_area(day_max, timestep,nb_interp,renWin,imageFilter,moviewriter,camera,renderer,mobile_rendering=0):
    window_width,window_height,x_margin,text_width,y_margin,text_height,police_1,police_2,x_plus,space_between_texts=window_size_config(day_max,mobile_rendering)
    trans_object,trans_text,reading_time=get_transition_times()
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()

    

    # Text and volumes appearing
    rectangleActor=setup_rectangle(day_max,mobile_rendering,renderer,0.15,True,0,0,0)
    text1="The unactivated tissues area around the inoculation point\nis detected and segmented in each original image."
    textActor=add_text(text1,window_width*80/1200,window_height-3.3*police_1-10,police_1,0,day_max,mobile_rendering,renderer)
    text_and_actors_appearing(trans_text,textActor,None,None,renderer,timestep,renWin,imageFilter,moviewriter)
    #sequence_idle(reading_time//2,timestep,renWin,imageFilter,moviewriter,camera)


    #APPEARING IRM_i AND LEGEND_i
    for i in range(day_max+1):
        #LEGEND AND VOLUME
        text1="t = "+str(35*i)+" days"
        textActorI=add_text(text1,window_width*80/1200,window_height-18.3*police_1-10,police_1,0,day_max,mobile_rendering,renderer)
        if(i==0):
            silhouette=build_silhouette(0,0,renderer,None)
            mushroom=build_mushroom(0,0,nb_interp,renderer,None,4)            
        else:
            silhouette=build_silhouette((i-1),120,renderer,None)
            mushroom=build_mushroom((i-1),120,nb_interp,renderer,None,4)
        text_and_actors_appearing(trans_text,textActor,(silhouette,mushroom),None,renderer,timestep,renWin,imageFilter,moviewriter,(0.15,1.0))
        sequence_idle(trans_object*5,timestep,renWin,imageFilter,moviewriter,camera)
        text_and_actors_disappearing(trans_text,(textActor,),(silhouette,mushroom),None,renderer,timestep,renWin,imageFilter,moviewriter,(0.15,1.0))
        text_actors_and_props_removed((textActorI,),(silhouette,mushroom),None,renderer)
        sequence_idle(trans_object*3,timestep,renWin,imageFilter,moviewriter,camera)

    renderer.RemoveActor(rectangleActor)        





def sequence_09_interpolation_volume  (day_max, timestep,nb_interp,renWin,imageFilter,moviewriter,camera,renderer,mobile_rendering=0):
    window_width,window_height,x_margin,text_width,y_margin,text_height,police_1,police_2,x_plus,space_between_texts=window_size_config(day_max,mobile_rendering)
    trans_object,trans_text,reading_time=get_transition_times()
    z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()

    to_front_view(camera)
    # Text and volumes appearing and idling
    rectangleActor=setup_rectangle(day_max,mobile_rendering,renderer,0.15,True,0,0,0)
    silhouette=build_silhouette(0,0,renderer,None)
    mushroom=build_mushroom(0,0,nb_interp,renderer,None,4)
    text1="The growth of this area is then interpolated over time\nusing an offset strategy"
    textActor=add_text(text1,window_width*80/1200,window_height-2.8*police_1-10,police_1,0,day_max,mobile_rendering,renderer)
    text_and_actors_appearing(trans_text,textActor,(silhouette,),None,renderer,timestep,renWin,imageFilter,moviewriter,(0.15,))
    sequence_idle(reading_time//2,timestep,renWin,imageFilter,moviewriter,camera)
 


    #Successive views of mushrooms
    for da in range(day_max):
        if(da==day_max):
            n_int=nb_interp+1
        else:
            n_int=nb_interp
        for ti in range(n_int):
            print('ti='+str(ti)+'da='+str(da))
            print(str(da)+" "+str(ti))
            silhouette=build_silhouette(da,ti,renderer,silhouette)
            mushroom=build_mushroom(da,ti,nb_interp,renderer,mushroom,4)
            snapshot(timestep,renWin,imageFilter,moviewriter)
    sequence_idle(4*trans_object,timestep,renWin,imageFilter,moviewriter,camera)
 
    
    
    #Disappearing
    text_and_actors_disappearing(trans_text,(textActor,),(silhouette,mushroom),None,renderer,timestep,renWin,imageFilter,moviewriter)
    text_actors_and_props_removed((textActor,rectangleActor),(silhouette,mushroom),None,renderer)
    from_front_view(camera)




def sequence_X_turn_around_global(timestep,renWin,imageFilter,movieWriter,camera):
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




