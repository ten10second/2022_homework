# Description: Attraction Trip-End Balancing Method Gravity Model calculation
# Author：21216492 zhimiao_shi
# Date：2022/04/09

import os
from turtle import distance
import pandas as pd 
import numpy as np
import csv
import argparse
import math

parser = argparse.ArgumentParser()
parser.add_argument("--epoch", default=100, help="输入迭代的次数")
args = parser.parse_args()


# calculate the f_cij
def resistent(distance):
    return format(math.exp(-0.01*distance), '.2f')


distance_matrix = np.array([
    [10, 15, 20],
    [15, 8, 17],
    [20, 17, 8]
], dtype=float)

zones = 3
B = [1.0, 1.0, 1.0]

resistent_matrix = np.zeros([zones, zones])

for i in range(distance_matrix.shape[0]):
    for j in range(distance_matrix.shape[1]):
        resistent_matrix[i][j] = resistent(distance_matrix[i][j])

# print(resistent_matrix)

file_path = 'demo2.csv'

colums = ['1', '2', '3']
index = ['1', '2', '3']

df = pd.read_csv(file_path,header = None,delimiter=',')

curr_data = pd.DataFrame(df)
curr_data.index = index
curr_data.columns = colums

curr_data['O_i'] = curr_data.apply(lambda x: x.sum(), axis=1)
curr_data.loc['D_j'] = curr_data.apply(lambda x: x.sum(), axis=0)

# print(curr_data)  # 当前OD矩阵

# the second matrix: B * D * resistence

epoch = 1
epoch_nums= args.epoch

while epoch < int(epoch_nums):


    BD_matrix = np.zeros([3, 3])
    for i in range(zones):
        BD_matrix[i] = np.multiply(resistent_matrix[i], curr_data.loc['D_j'][:3])
        BD_matrix[i] = np.multiply(BD_matrix[i], np.array(B))

    BD_dataframe = pd.DataFrame(BD_matrix, index=index, columns=colums)
    BD_dataframe['bd_sum'] = BD_dataframe.apply(lambda x: x.sum(), axis=1)
    # print(BD_dataframe)


    T_matrix = np.zeros([zones, zones])
    T_dataframe = pd.DataFrame(T_matrix, index=index, columns=colums)

    for i in index:
        for j in colums:
            T_dataframe.at[i,j] = curr_data.at[i, 'O_i'] * (BD_dataframe.at[i, j]/ BD_dataframe.at[i, 'bd_sum'])
    T_dataframe.loc['t_sum'] = T_dataframe.apply(lambda x: x.sum(), axis=0)

    for zone in colums:
        i = colums.index(zone)
        if T_dataframe.at['t_sum', zone] == 0 and curr_data.at['D_j', zone] == 0:
            B[i] = 1.0
        else:
            B[i] = curr_data.at['D_j', zone] / T_dataframe.at['t_sum', zone]

    T_dataframe.loc['B'] = B
    if all(0.97 <= _ <= 1.03 for _ in B):
        print('the min epoch is {}'.format(epoch))
        print(T_dataframe)
        break
    else:
        epoch += 1

# print('After {} epoches, the results are not satisfied the constrains'.format(int(epoch_nums)))
# print(T_dataframe)