#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jul 22 17:17:45 2019

@author: fernandr
"""


sphere = vtk.vtkSphereSource()
  12 colorIt = vtk.vtkElevationFilter()
  13 colorIt.SetInputConnection(sphere.GetOutputPort())
  16 butterfly = vtk.vtkButterflySubdivisionFilter()
  17 butterfly.SetInputConnection(colorIt.GetOutputPort())
  18 butterfly.SetNumberOfSubdivisions(3)
  22 mapper = vtk.vtkPolyDataMapper()
  23 mapper.SetInputConnection(butterfly.GetOutputPort())
  25 actor = vtk.vtkActor()
  26 actor.SetMapper(mapper)
  27 linear = vtk.vtkLinearSubdivisionFilter()
  28 linear.SetInputConnection(colorIt.GetOutputPort())
  29 linear.SetNumberOfSubdivisions(3)
  30 mapper2 = vtk.vtkPolyDataMapper()
  31 mapper2.SetInputConnection(linear.GetOutputPort())
  33 actor2 = vtk.vtkActor()
  34 actor2.SetMapper(mapper2)







