#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Jul 12 18:09:56 2019

@author: fernandr
"""

nb_interp=120
day_max=3

#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jul  2 10:53:18 2019
@author: fernandr
"""
from skimage import io
import vtk
from vtk.util.misc import vtkGetDataRoot
VTK_DATA_ROOT = vtkGetDataRoot()
from scene_3d_helper_functions import *


#CREATION DU RENDERER
renderer = vtk.vtkRenderer()
renderer.SetBackground(0,0,0)


#AJOUT DES DONNEES, GESTION CAMERA ET LUMIERE
source_rep='/home/fernandr/Bureau/Test/Visu2/Compute/'
x_end,y_end,z_end=512,512,512
y_last,z_last=260,260
size,window_width,window_height=511 ,1200, 896
z_begin_irm,z_end_irm=180,370
framerate,timestep=40,0.025
type=0  #test
#type=1  #movie building



def build_mesh_and_write_to_file(path_source,path_dest,isoVal,z_min,z_max,y_crop,z_crop,size):
    data_matrix = io.imread(path_source)
    x_end=data_matrix.shape[0]
    y_end=data_matrix.shape[1]
    z_end=data_matrix.shape[2]
    data_matrix[z_crop:size,y_crop:size,:]=0
    data_matrix[z_max:size+1,:,:]=0
    data_matrix[0:z_min,:,:]=0
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
    surface.SetValue( 0, isoVal )      #########################"
    writer=vtk.vtkPolyDataWriter()
    writer.SetFileName(path_dest)
    writer.SetInputData(surface.GetOutput());
    writer.Write();


#Build mesh
data_rep='/mnt/DD_COMMON/Data_VITIMAGE/Movie_maker_v2/img_interp/'
build_mesh_and_write_to_file(data_rep+"images/camb01_0.tif",data_rep+"mesh/camb01_0.vtp",57.5,z_begin_irm,z_end_irm,y_last,z_last,size)
build_mesh_and_write_to_file(data_rep+"images/moe01_0.tif",data_rep+"mesh/moe01_0.vtp",127.5,z_begin_irm,z_end_irm,y_last,z_last,size)
build_mesh_and_write_to_file(data_rep+"images/ves01_0.tif",data_rep+"mesh/ves01_0.vtp",197.5,z_begin_irm,z_end_irm,y_last,z_last,size)



    polydata=vtk.vtkPolyData()
    reader=vtk.vtkPolyDataReader()
    reader.SetFileName(filename.c_str());
  reader->Update();
  
  // Visualize
  vtkSmartPointer<vtkPolyDataMapper> mapper =
    vtkSmartPointer<vtkPolyDataMapper>::New();
  mapper->SetInputConnection(reader->GetOutputPort());



def load_mesh_from_file(path,r,g,b,opac,spec,diff,amb,isoVal,z_min,z_max,y_crop,z_crop,size):
    writer=vtk.vtkPolyDataWriter()
    surface.SetValue( 0, isoVal )      #########################"
    geoBoneMapper = vtk.vtkPolyDataMapper()
    geoBoneMapper.SetInputConnection(surface.GetOutputPort() )
    geoBoneMapper.ScalarVisibilityOff()
    actorCur = vtk.vtkLODActor()
    actorCur.SetMapper( geoBoneMapper )
    actorCur.GetProperty().SetColor( r, g, b)   ##############""
    actorCur.GetProperty().SetOpacity(opac )   ##############""
    actorCur.GetProperty().SetInterpolationToGouraud ()   ##############""
    actorCur.GetProperty().SetSpecular(spec)   ##############""
    actorCur.GetProperty().SetDiffuseColor( r, g, b )   ##############""
    actorCur.GetProperty().SetDiffuse(diff)   ##############""
    actorCur.GetProperty().SetAmbientColor( r, g, b )   ##############""
    actorCur.GetProperty().SetAmbient(amb)   ##############""
    return actorCur
