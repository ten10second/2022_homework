# Description: Detroit方法（增长系数法预测城市居民出行分布）
# Author：21216492
# Date：2022/04/02



from tkinter.font import names
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

print(data)