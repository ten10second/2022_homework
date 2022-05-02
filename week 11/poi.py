from haversine import haversine
import pandas as pd
from datetime import datetime 
import numpy as np


def split_condecutibe_num(data):
    res = []
    for i in range(len(data)):
        if not res:
            res.append([data[i]])
        elif data[i-1] + 1 == data[i]:
            res[-1].append(data[i])
        else: 
            res.append([data[i]])

    return res


data_file = "week 11\data_standard.csv"

colums = ['isdn', 'date', 'timestamp','city','did','lng','lat']
df = pd.read_csv(data_file,delimiter=',', encoding='unicode_escape')

gps_data = pd.DataFrame(df)
gps_data.columns = colums

# print(gps_data)

person_1 = gps_data.query('isdn == 5264')
person_1 = person_1.reset_index(drop=True)
person_2 = gps_data.query('isdn == 8586')
person_2 = person_2.reset_index(drop=True)
person_3 = gps_data.query('isdn == 5264')
person_3 = person_3.reset_index(drop=True)
# dataframe.to_csv('week 11\dataframe', sep=',', index=False, header=colums)
# person_2.to_csv('week 11\person_2', sep=',', index=False, header=colums)
# person_3.to_csv('week 11\person_3', sep=',', index=False, header=colums)

def define_poi(dataframe):

    did_list = []
    did_during = []
    did_pos = []
    cur_did = dataframe.at[0, 'did']
    inital_time = datetime.strptime(dataframe.at[0, 'timestamp'], '%Y/%m/%d %H:%M')

    for i in range(1, len(dataframe)):
        if dataframe.at[i, 'did'] == cur_did:
            now_time = datetime.strptime(dataframe.at[i, 'timestamp'], '%Y/%m/%d %H:%M')
            during_time = now_time - inital_time
            during_time = during_time.seconds / 60

        else: 
            did_list.append(cur_did)  
            did_pos.append((dataframe.at[i, 'lng'], dataframe.at[i, 'lat']))  
            did_during.append(during_time)
            cur_did = dataframe.at[i, 'did']
            inital_time = datetime.strptime(dataframe.at[i, 'timestamp'], '%Y/%m/%d %H:%M') 
    # 时间判断依据: 
    # 
    # 先筛选大于30min的时段 直接判断为poi
    # 小于15min的时段 直接判断为 move point


    dataframe.insert(loc = len(colums), column='poi_point', value=0)

    for i in range(len(did_during)):
        if did_during[i] > 30:
            mark = did_list[i]
            mask = dataframe['did'] == mark
            time_index = np.flatnonzero(mask)
            time_index = time_index.tolist()

            split_res = split_condecutibe_num(time_index)

            for j in split_res:

                start_time = datetime.strptime(dataframe.at[j[0], 'timestamp'], '%Y/%m/%d %H:%M')
                end_time = datetime.strptime(dataframe.at[j[-1], 'timestamp'], '%Y/%m/%d %H:%M')
                if (end_time - start_time).seconds / 60 > 30:
                    for k in j:
                        dataframe.at[k, 'poi_point'] = 1

    return dataframe

poi2 = define_poi(person_2)
poi2.to_csv('week 11\person2_poi', sep=',', index = False)

poi3 = define_poi(person_3)
poi2.to_csv('week 11\person3_poi', sep=',', index = False)
