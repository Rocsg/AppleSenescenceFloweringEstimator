#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 17:11:40 2019

@author: fernandr
"""
from utils import *
computeSpiders=1
computeResolutions=0

#compute_red_tab()


if(computeSpiders==1):
    valsYellow=compute_yellow_tab()
    #compute_spiders(config,valsYellow,min,max,4)
    #compute_spiders(1,valsYellow,min,max,4)
    compute_spiders(2,valsYellow,min,max,4)
    #config=0 -> monomod RX T1 T2 M0 Both
    #config=1 -> missing one -RX -T1 -T2 -M0 Both
    #config=2 ->  -RX alone - Irm alone - Both

if(computeResolutions==1):
    valsPurple=compute_purple_tab('EXP_2_TWO_FOLD/')   
    valsBrownConsensus=compute_brown_tab(1)
    valsBrown=compute_brown_tab(0)
    compute_decreasing_plot_with_resolution(valsBrown,valsPurple)
    compute_decreasing_plot_with_resolution(valsBrownConsensus,valsPurple)


