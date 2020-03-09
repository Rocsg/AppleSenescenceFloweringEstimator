#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Nov 25 22:09:04 2019

@author: fernandr
"""

#Define the parameters area

exp='Second_one'
balance_amadou=1
prepare_folders_for_experiment(exp)
transform_weka_data_to_normalized_npy_data(exp,balance_amadou)
split_training_augmented_crossvalidation_test_sets(exp,0,0)

#./1574801760_config.npy Last
# Intervalle courant 1574802579    1574802815

exp='Second_one'
cross_mode=0
best_config=hyper_optimization(exp,cross_mode)


exp='Second_one'
cross_mode=2
first_ever=1574797181
last_ever=2574873339

first=1574873340 #step 8
first=1574891454 #step 9

import matplotlib.pyplot as plt
plt.close('all')
configurations_comparisons(exp,build_unique_index_list_for_exp(exp,first,last_ever),focus=2)

configurations_comparisons(exp,build_unique_index_list_for_exp(exp,first_ever,last_ever),focus=2)
