#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan  6 21:30:43 2020

@author: fernandr
"""

import pandas as pd
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

