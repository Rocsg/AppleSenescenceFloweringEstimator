#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Oct  9 17:11:40 2019

@author: fernandr
"""
from papercep import *
rep='/home/fernandr/Bureau/EX_CEDRIC/V3/RESULTS/'



exps=('RESULTS_V3_1-32_NFEAT_14__NTREE_250__KIND_5_CL/NFEAT_14__NTREE_250__KIND_5_CL___TwoOnTesting',
      'RESULTS_V3__1-64_NFEAT_14__NTREE_250__KIND_5_CL/NFEAT_14__NTREE_250__KIND_5_CL___TwoOnTesting',
      'RESULTS_V3__2-64_NFEAT_14__NTREE_250__KIND_5_CL/2-64_NFEAT_14__NTREE_250__KIND_5_CL___TwoOnTesting',
      'RESULTS_V3__4-64_NFEAT_14__NTREE_250__KIND_5_CL/4-64_NFEAT_14__NTREE_250__KIND_5_CL___TwoOnTesting')

#Process data
#compute_red_tab()
#valsYellow=compute_yellow_tab()
valsBrown=compute_brown_tab()
#visualize data
config=0
min=40
max=100
#compute_spiders(99,valsYellow,min,max,4)
compute_decreasing_plot_with_resolution(valsBrown)
#compute_spiders(1,valsYellow,min,max,4)
#compute_spiders(2,valsYellow,min,max,4)
#config=0 -> monomod RX T1 T2 M0 Both
#config=1 -> missing one -RX -T1 -T2 -M0 Both
#config=2 -> missing one -RX alone - Irm alone - Both


#confusion=read_confusion_mat_from_full_text(exp,0,1)
#accuracy_class(confusion,4)

