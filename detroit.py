from tkinter.font import names
import matplotlib.pyplot as plt 
import os
import pandas as pd 
import numpy as np
import csv

file_path = 'D://codefield//2022_homework//trip_distribution.csv'

colums = ['1', '2', '3', '4', 'total_origin', 'future_origin']
index = ['1', '2', '3', '4', 'total_destination', 'future_destination']
df = pd.read_csv(file_path,header = None,delimiter=',')
data = pd.DataFrame(df)

data.index = index
data.columns = colums

print(data)