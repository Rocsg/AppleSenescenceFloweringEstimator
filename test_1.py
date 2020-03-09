#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Jun 25 20:53:49 2019
    
@author: fernandr
"""

import numpy as np
import pandas as pd
from keras.models import Sequential
from keras.layers import Dense
np.random.seed(8)
#load hrdataset

#Find and import data from a kaggle set
import os
cwd = os.getcwd()
print(cwd)
hr_data = pd.read_csv('/home/fernandr/Python_prog/data/HR.csv', header=0)


# split into input (X) and output (Y) variables
data_trnsf = pd.get_dummies(hr_data, columns =['salary', 'sales'])
data_trnsf.columns
X = data_trnsf.drop('left', axis=1)
X.columns
 

from sklearn.model_selection import train_test_split
X_train, X_test, Y_train, Y_test = train_test_split(X,
data_trnsf.left, test_size=0.3, random_state=42)

# create model
model = Sequential()
model.add(Dense(12, input_dim=20, activation='relu'))
model.add(Dense(10, activation='relu'))
model.add(Dense(1, activation='sigmoid'))

# Compile model
model.compile(loss='binary_crossentropy', optimizer='adam',
 metrics=['accuracy'])

# Fit the model
X_train = np.array(X_train)
model.fit(X_train, Y_train, epochs=100, batch_size=10)

# evaluate the model
scores = model.evaluate(X_train, Y_train)
print("%s: %.4f%%" % (model.metrics_names[1], scores[1]*100))
X_test = np.array(X_test)
scores = model.evaluate(X_test, Y_test)
print("%s: %.4f%%" % (model.metrics_names[1], scores[1]*100))