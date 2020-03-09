
from sequences import *



############################### MAIN RUPTORS ############
spec_int=4
magic_RMN_modality='T1'
view_bois_sain=0
view_amadou,zmax_amadou,z_min_amadou=1, 450,50
view_necrose=0
view_bubbles=1
view_fibers,colormap_fibers=1,15
experiencesLocation=0 #0=chez Romain, 1= chez Cedric
if(experiencesLocation==0):
    chez_moi='/home/fernandr/Bureau/ML_CEP/RESULTS/EXP_6_ON_STACKS/'
    separ='/'
else:
    chez_moi='\C:\Thing\path_to_cedric_data\\'
    separ=''
#########################################################



specimens=["CEP011_AS1","CEP012_AS2","CEP013_AS3","CEP014_RES1","CEP015_RES2","CEP016_RES3","CEP017_S1","CEP018_S2","CEP019_S3","CEP020_APO1","CEP021_APO2","CEP022_APO3"]
zmax_distances=(2*(200+86)  , 2*(200+76)  , 2*(200+174)  ,          2*(200+65)  , 2*(200+97)  , 2*(200+108)  ,  
                2*(200+71)   ,2*(200+74)  , 2*(200+68)  ,           2*(200+59)  , 2*(200+42)   , 2*(200+118) )
zmax_distances=zmax_distances*2
spec_view=specimens[spec_int]
type_interaction=1  #0=fix sur modele, 1=interactionmode sur modele,  2=video
marge_aux_fraises=20


action_building=0
action_building_all_fibers_watermarks=0
action_building_all_fibers=0
action_building_one_fiber=0
action_building_all_cambium=0
action_building_one_cambium=0
action_building_all_bubbles=0
action_view=1 #1= view, 0= dont view






iso_cambium=40
fiber_viewed=3
use_sub='_sub' # '_sub' or ''
style=4
scenario=5 #4= normal   1 = fibers concrete with colours   2=cambium concrete with colours
           #3 = fibers VR with colours   4=cambium VR with colours   5 cambium VR with fibersin
amadou_based_colormap=0 #0=no shading   #1 = shading based on distance to amadou
#0 : bois sain =marron clair, ecorce=blanc, necrose =jaune, bois noir=transparent
#1 : bois sain =vert, ecorce=blanc, necrose =jaune , bois noir = transparent
#2 : bois sain =blanc cassé, ecorce=marron, necrose =jaune orange , bois noir = marron sombre
#3 : a documenter
#4 : bois sain =transpa, ecorce=transpa noir, necrose =rouge vif , bois noir = transpa
import sys


""" 
################################################################
#########  BUILDING MESH  ######################################
################################################################
 """

if(action_building==1):
    a=time.time()
    specimens=["CEP011_AS1","CEP012_AS2","CEP013_AS3","CEP014_RES1","CEP015_RES2","CEP016_RES3","CEP017_S1","CEP018_S2","CEP019_S3","CEP020_APO1","CEP021_APO2","CEP022_APO3"]
    for spec in specimens:
        rep=chez_moi+spec+separ
        print('Building meshes full for specimen '+spec)
        #build_mesh_and_save(rep+'segmentation_iso_AMAD.tif',rep+'mesh_amadou_sub.vtp',  0,      200.5,0,z_min_amadou,zmax_amadou)
        build_mesh_and_save(rep+'segmentation_iso.tif',rep+'mesh_glob_sub.vtp',           0.95,   0.5,crop_type=0,slice_min=-1,slice_max=-1)
        #build_mesh_and_save(rep+'segmentation_iso_NECROSE.tif',rep+'mesh_necrose_sub.vtp',0,      200.5,crop_type=0,slice_min=-1,slice_max=-1)
        #build_mesh_and_save(rep+'segmentation_iso_SAIN.tif',rep+'mesh_sain_sub.vtp'      ,0,   127.5,crop_type=0,slice_min=-1,slice_max=-1)
        print('Building meshes sub for specimen '+spec)
        b=time.time()-a
        print('')
        print('TIME='+str(int(b)))
        print('')


if(action_building_all_fibers_watermarks==1):
    a=time.time()
    specimens=["CEP011_AS1","CEP012_AS2","CEP013_AS3","CEP014_RES1","CEP015_RES2","CEP016_RES3","CEP017_S1","CEP018_S2","CEP019_S3","CEP020_APO1","CEP021_APO2","CEP022_APO3"]
    #specimens=["CEP011_AS1"]
    for spec in specimens:
        for num in range(1):
            fib_num=num+3
            rep=chez_moi+spec+separ
            print('Building meshes of fibers_level '+spec)
            
            build_mesh_and_save(rep+'fibers_level_'+str(fib_num)+'_watermarked.tif',rep+'mesh_fiber_level_'+str(fib_num)+'_watermarked.vtp',
                                0,   192.5,crop_type=0,slice_min=-1,slice_max=-1)
            b=time.time()-a
            print('')
            print('TIME='+str(int(b)))
            print('')


if(action_building_all_fibers==1):
    a=time.time()
    specimens=["CEP011_AS1","CEP012_AS2","CEP013_AS3","CEP014_RES1","CEP015_RES2","CEP016_RES3","CEP017_S1","CEP018_S2","CEP019_S3","CEP020_APO1","CEP021_APO2","CEP022_APO3"]
    for spec in specimens:
        for num in range(8):
            fib_num=num-4
            rep=chez_moi+spec+separ
            print('Building meshes of fibers_level '+spec)
            
            build_mesh_and_save(rep+'fibers_level_'+str(fib_num)+'.tif',rep+'mesh_fiber_level_'+str(fib_num)+'.vtp',          0,   192.5,crop_type=0,slice_min=-1,slice_max=-1)
            b=time.time()-a
            print('')
            print('TIME='+str(int(b)))
            print('')

if(action_building_one_fiber==1):
    a=time.time()
    spec=specimens[spec_int]
    for num in range(8):
        fib_num=num-4
        rep=chez_moi+spec+separ
        print('Building meshes of fibers_level '+spec)
        
        build_mesh_and_save(rep+'fibers_level_'+str(fib_num)+'.tif',rep+'mesh_fiber_level_'+str(fib_num)+'.vtp',          0,   192.5,crop_type=0,slice_min=-1,slice_max=-1)
        b=time.time()-a
        print('')
        print('TIME='+str(int(b)))
        print('')


if(action_building_all_cambium==1):
    a=time.time()
    specimens=["CEP011_AS1","CEP012_AS2","CEP013_AS3","CEP014_RES1","CEP015_RES2","CEP016_RES3","CEP017_S1","CEP018_S2","CEP019_S3","CEP020_APO1","CEP021_APO2","CEP022_APO3"]
    #specimens=["CEP020_APO1"]
    for spec in specimens:
        rep=chez_moi+spec+separ
        print('Building meshes of fibers_level '+spec)
        
        build_mesh_and_save(rep+'cambium_T1.tif',rep+'mesh_cambium.vtp',          0,   iso_cambium,crop_type=0,slice_min=-1,slice_max=zmax_distances[spec_int]-marge_aux_fraises)
        b=time.time()-a
        print('')
        print('TIME='+str(int(b)))
        print('')

if(action_building_all_bubbles==1):
    a=time.time()
    specimens=["CEP011_AS1","CEP012_AS2","CEP013_AS3","CEP014_RES1","CEP015_RES2","CEP016_RES3","CEP017_S1","CEP018_S2","CEP019_S3","CEP020_APO1","CEP021_APO2","CEP022_APO3"]
    #specimens=["CEP011_AS1"]
    #specimens=["CEP020_APO1"]
    for spec in specimens:
        rep=chez_moi+spec+separ
        print('Building meshes of fibers_level '+spec)
        
        build_mesh_and_save(rep+'bubbles.tif',rep+'mesh_bubbles.vtp',          0,   iso_cambium,crop_type=0,slice_min=-1,slice_max=-1)
        b=time.time()-a
        print('')
        print('TIME='+str(int(b)))
        print('')


if(action_building_one_cambium==1):
    a=time.time()
    spec=specimens[spec_int]
    rep=chez_moi+spec+separ
    print('Building meshes of fibers_level '+spec)
    
    build_mesh_and_save(rep+'cambium_T2.tif',rep+'mesh_cambium.vtp',          0,   iso_cambium,crop_type=0,slice_min=-1,slice_max=-1)
    b=time.time()-a
    print('')
    print('TIME='+str(int(b)))
    print('')





""" 
################################################################
#########  SETUP GENERAL  ######################################
################################################################
 """

if(action_view==0):
    sys.exit(0)
    
renderer = vtk.vtkRenderer()
renderer.SetBackground(0.0,0.0,0.0)



#AJOUT DES DONNEES, GESTION CAMERA ET LUMIERE
rep=chez_moi+spec_view+separ


z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z=get_image_constants()
print('Starting rendering. Constants defined=z_begin_irm,z_end_irm,x_start_crop,y_start_crop,z_start_crop,size_x,size_y,size_z :'+str(z_begin_irm)+', '+str(z_end_irm)+', '+str(size_x)+', '+str(size_y)+', '+str(size_z))
mobile_rendering=0 # 0 = normal on personal computer, 1=1080p, 2= 4K TV, 3= mobile_phone
window_width,window_height,x_margin,text_width,y_margin,text_height,police_1,police_2,x_plus,space_between_texts=window_size_config(mobile_rendering)


framerate,timestep=25,0
type_view=0  # 0 = oblique 1=front, 2=right, 3 =up





""" 
################################################################
#########  MISE EN PLACE SILHOUETTE ET VUE   ##############################
################################################################
 """
start = time.time()
print('Start.')

#SETUP CAMERA, RENDER WINDOW, LIGHTS AND MOVIE BUILDER

#WARNING : THESE TWO LINES HELPS BUILDING THE SETUP
print('effectivement')
actorSilhouette=build_silhouette(rep+'mesh_glob'+use_sub+'.vtp',renderer,None,0,style) 
print('effectivement')

#WARNING : THESE TWO LINES HELPS BUILDING THE SETUP
print('')
print('Building bois sain')
if(view_bois_sain==1):
    actorBoisSain=build_bois_sain(rep+'mesh_sain'+use_sub+'.vtp',renderer,None,0,style) 
#actorBoisSain.GetProperty().SetOpacity(1.0)

print('')
print('Building amadou')
if(view_amadou==1):
    actorAmadou=build_amadou(rep+'mesh_amadou'+use_sub+'.vtp',renderer,None,0,style) 

print('')
print('Building bois noir')
if(view_necrose==1):
    actorNecrose=build_necrose(rep+'mesh_necrose'+use_sub+'.vtp',renderer,None,0,style) 
#actorAmadou.GetProperty().SetOpacity(1.0)

print('')
print('Building bubbles')
if(view_bubbles==1):
    actorBubbles=build_bubbles(rep+'mesh_bubbles.vtp',renderer,None,0,style) 
#actorAmadou.GetProperty().SetOpacity(1.0)

print('')
print('Building fibers')
if(view_fibers==1):
    if(scenario==1):
        actorFibers=build_fibers(rep+'mesh_fiber_level_'+str(fiber_viewed)+'.vtp',renderer,None,0,style) 
    elif(scenario==2):
        actorFibers=build_fibers(rep+'mesh_cambium.vtp',renderer,None,0,style)
    elif(scenario==3):
        actorFibers=build_volume_rendering_view_from_image(rep+'fibers_level_'+str(fiber_viewed)+'.tif',1,renderer,0,-1,-1,colormap=10)
    elif(scenario==4):
        actorFibers=build_volume_rendering_view_from_image(rep+'cambium_T1.tif',1,renderer,0,-1,-1,colormap=10)
    elif(scenario==5):
        actorFibers2=build_fibers(rep+'mesh_fiber_level_'+str(fiber_viewed)+'_watermarked.vtp',renderer,None,0,style) 
        actorFibers=build_volume_rendering_view_from_image(rep+'cambium_'+magic_RMN_modality+'.tif',1,renderer,0,-1,zmax_distances[spec_int]-marge_aux_fraises,colormap_fibers)
    elif(scenario==6):
        actorFibers2=build_fibers(rep+'mesh_fiber_level_'+str(fiber_viewed)+'_watermarked.vtp',renderer,None,0,style) 
        actorFibers=build_bois_sain(rep+'mesh_cambium.vtp',renderer,None,0,style)
 


if(type_interaction==0):
    renderer.ResetCamera()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(renderer)
    renWin.Render()
    camera=renderer.GetActiveCamera()
    renWin.SetSize(window_width,window_height)
    setup_title(spec_view,renderer,window_width,window_height)
    lights=start_lights(renderer,8)
    set_lights_on_normal_mode(lights)
    setup_camera_initial_position(camera)
    print('fixed render start')

elif(type_interaction==1):
    renderer.ResetCamera()
    renWin = vtk.vtkRenderWindow()
    renWin.AddRenderer(renderer)
    camera=renderer.GetActiveCamera()
    print('Setting size '+str(window_width)+' '+str(window_height))
    renWin.SetSize(window_width,window_height)
    setup_title(spec_view,renderer,window_width,window_height)
    lights=start_lights(renderer,8)
    set_lights_on_normal_mode(lights)
    setup_camera_initial_position(camera)
    print('interaction render start')
    setup_interaction(renWin,renderer)


