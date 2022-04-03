# Description: Detroit方法（增长系数法预测城市居民出行分布）
# Author：21216492
# Date：2022/04/02

from calendar import EPOCH
from cmath import nan
import matplotlib.pyplot as plt 
import os
import pandas as pd 
import numpy as np
import csv

file_path = 'D://codefield//2022_homework//trip_distribution.csv'

colums = ['1', '2', '3', '4']
index = ['1', '2', '3', '4']

df = pd.read_csv(file_path,header = None,delimiter=',')

data = pd.DataFrame(df)
data.index = index
data.columns = colums

data['Total_generate'] = data.apply(lambda x: x.sum(), axis=1)
data.loc['Total_attract'] = data.apply(lambda x: x.sum(), axis=0)

# estimated future origins and estimated future destinations

Estimated_future_generation = [1200, 1050, 380, 770]
future_generation_dict = dict(zip(colums, Estimated_future_generation))
Estimated_future_attraction = [670, 730, 950, 1050]
future_attraction_dict = dict(zip(colums, Estimated_future_attraction))

SUM = sum(Estimated_future_attraction)

data['generation_growth'] = ''
data.loc['attract_growth'] = ''

# calculate the growth of the generate and attraction

for item in colums:
    i = colums.index(item)
    data.at[item, 'generation_growth'] = Estimated_future_generation[i] / data.iat[i, 4]
    data.at['attract_growth', item] = Estimated_future_attraction[i] / data.iat[4, i]

G = data.at['Total_attract', 'Total_generate'] / SUM

epoch = 1

for origin in colums:
    for dst in index:

        data.at[origin, dst] = data.at[origin, dst] * G * data.at[origin, 'generation_growth'] * data.at['attract_growth', dst]

# update the total_attract and total_generation
data['Total_generate'] = data.iloc[0:4, :].sum(axis=0)
data.loc['Total_attract'] = data.iloc[:, 0:5].sum(axis=0)  


for item in colums:
    i = colums.index(item)

    data.at[item, 'generation_growth'] = Estimated_future_generation[i] / data.at[item, 'Total_generate']
    data.at['attract_growth', item] = Estimated_future_attraction[i] / data.at['Total_attract', item]


print(data)
data.to_csv('epoch1.csv', sep='\t')
