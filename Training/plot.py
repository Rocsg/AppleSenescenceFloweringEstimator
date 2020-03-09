#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Jan  9 09:50:32 2020

@author: fernandr
"""
#cd /home/fernandr/Python_prog/Training/Medium-Data-Exploration/
import json
import pandas as pd
import numpy as np
%matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns
sns.set(
    font_scale=1.5,
    style="whitegrid",
    rc={'figure.figsize':(20,7)}
)

sales_team = pd.read_csv('./Medium-Data-Exploration/sales_team.csv')
order_leads = pd.read_csv('./Medium-Data-Exploration/order_leads.csv')
invoices = pd.read_csv('./Medium-Data-Exploration/invoices.csv')
