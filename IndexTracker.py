#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jun 27 09:30:27 2019
https://matplotlib.org/2.1.2/gallery/animation/image_slices_viewer.html
@author: fernandr
"""

from __future__ import print_function

import numpy as np
import matplotlib.pyplot as plt
from skimage import io

class Slicer_3d(object):
    def __init__(self,X):
        fig,self.ax = plt.subplots(2, 2)
        self.ax[0,0].set_title('Scroll and click to navigate')

        self.X = X
        self.zMax=X.shape[0]
        self.yMax=X.shape[1]
        self.xMax=X.shape[2]
        self.slices, self.rows, self.cols  = X.shape
        self.indZ = self.slices//2
        self.indX = self.cols//2
        self.indY = self.rows//2

        self.imZ = self.ax[0,0].imshow(self.X[self.indZ,:, :])
        self.imX = self.ax[0,1].imshow(self.X[:,:,self.indX])
        self.imY = self.ax[1,0].imshow(self.X[:,self.indY,:])
        self.update()
        fig.canvas.mpl_connect('scroll_event', self.onscroll)
        fig.canvas.mpl_connect('button_press_event', self.onclick)
        plt.show()

    def onscroll(self, event):
#        print("%s %s" % (event.button, event.step))
        if event.button == 'up':
            self.indZ = (self.indZ + 1) % self.slices
        else:
            self.indZ = (self.indZ - 1) % self.slices
        self.update()

    def onclick(self, event):
#        print('click')
#        print('%s click: button=%d, x=%d, y=%d, xdata=%f, ydata=%f' %
#              ('double' if event.dblclick else 'single', event.button,
#               event.x, event.y, event.xdata, event.ydata))
        self.indX=int(event.xdata)
        self.indY=int(event.ydata)
        self.update()



    def update(self):
        self.imZ.set_data(self.X[self.indZ, :, :])
        self.ax[0,0].set_ylabel('slice %s' % self.indZ)
        self.imZ.axes.figure.canvas.draw()
 
        self.imX.set_data(np.transpose(self.X[:,:,self.indX,]))
        self.ax[0,1].set_ylabel('X= %s' % self.indX)
        self.imX.axes.figure.canvas.draw()
        
        self.imY.set_data(self.X[:, self.indY, :])
        self.ax[1,0].set_ylabel('Y= %s' % self.indY)
        self.imY.axes.figure.canvas.draw()



def slicer_test(img):
    fig, ax = plt.subplots(2, 2)
    tracker = IndexTracker(img)
    fig.canvas.mpl_connect('scroll_event', tracker.onscroll)
    fig.canvas.mpl_connect('button_press_event', tracker.onclick)
    plt.show()




#irm_data = io.imread('/home/fernandr/Bureau/Test/Test_NN/python_data/source/IRM_small.tif')
#tracker = Slicer_3d(irm_data)
