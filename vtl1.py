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
renWin = vtk.vtkXOpenGLRenderWindow()
renWin.AddRenderer(renderer)
renWin.Start()
print('GL ?'+str(renWin.SupportsOpenGL()))
print('Direct ?'+str(renWin.IsDirect()))

import time
time.sleep(2)




#def CheckAbort(obj, event):
#    print('GL ?'+str(obj.SupportsOpenGL()))
 #   print('Direct ?'+str(obj.IsDirect()))
 #   if obj.GetEventPending() != 0:
 #       #obj.SetAbortRender(1)
 ##       obj.Finalize()
 #       ir= obj.GetInteractor()
 #       obj.CloseDisplay()
 #       obj.DestroyWindow()
 #       ir.TerminateApp()
#        del obj,ir
#renWin.AddObserver("AbortCheckEvent", CheckAbort)

