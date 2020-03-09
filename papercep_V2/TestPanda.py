#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 21:30:43 2020

@author: fernandr
"""

import pandas as pd
import numpy as np
data=pd.read_csv('you-datascientist/happiness_with_continent.csv')
data.head(4)
data.shape
data.columns
data.index
data.info()
data.describe()
data.sort_values(by='Year', ascending=True)
data[['Year']] #Double bracket to get a dataframe
data[['Year','Country name']]
data.iloc[10]

data.set_index('Country name',inplace=True)
data.loc['United States','Life Ladder']
data.sample(5)

condition=data['Life Ladder']>4
data.loc[condition]
cond_year=data['Year'].apply(lambda x:x%3==0)
cond_america=data['Continent'].apply(lambda x: 'America' in x)
data[cond_year & condition & cond_america]

data.iloc[:,:-1].idxmin()

def above_1000_below_10(x):
    try:
        pd.to_numeric(x)
    except:
        return 'no number column'
    
    if x>1000:
        return 'above_1000'
    elif x<10:
        return below_10
    else:
        return 'mid'
    
data['Year'].apply(above_1000_below_10)


data['Continent'].apply(lambda x: x.split(' ')[-1])

data['Year'] + data['Life Ladder']
data['Year'].astype(str) + '_'+data['Life Ladder'].astype(str)


data.groupby(['Country name'])['Life Ladder'].max()
data.groupby(['Year'])['Life Ladder'].idxmax()

data.groupby(['Year','Continent'])['Life Ladder'].idxmax()



def get_random_country(group):
    return np.random.choice(group.index.values)# Named function
data.groupby(['Year','Continent']).apply(get_random_country)# Unnamed function
data.groupby(['Year','Continent']).apply(
  lambda group: np.random.choice(group.index.values)
)

data['Life Ladder']-data.groupby(['Country name'])['Life Ladder'].transform(np.median)



