from haversine import haversine
import pandas as pd
from datetime import datetime 


data_file = "week 11\data_standard.csv"

colums = ['isdn', 'date', 'timestamp','city','did','lng','lat']
df = pd.read_csv(data_file,delimiter=',', encoding='unicode_escape')

gps_data = pd.DataFrame(df)
gps_data.columns = colums

# print(gps_data)

person_1 = gps_data.query('isdn == 5264')
person_2 = gps_data.query('isdn == 8586')
person_3 = gps_data.query('isdn == 5264')
# person_1.to_csv('week 11\person_1', sep=',', index=False, header=colums)
# person_2.to_csv('week 11\person_2', sep=',', index=False, header=colums)
# person_3.to_csv('week 11\person_3', sep=',', index=False, header=colums)

did_list = []
did_during = []
did_pos = []
cur_did = person_1.at[0, 'did']
inital_time = datetime.strptime(person_1.at[0, 'timestamp'], '%Y/%m/%d %H:%M')

for i in range(1, len(person_1)):
    if person_1.at[i, 'did'] == cur_did:
        now_time = datetime.strptime(person_1.at[i, 'timestamp'], '%Y/%m/%d %H:%M')
        during_time = now_time - inital_time
    else: 
        did_list.append(cur_did)  
        did_pos.append((person_1.at[i, 'lng'], person_1.at[i, 'lat']))  
        did_during.append(during_time)
        cur_did = person_1.at[i, 'did']
        inital_time = datetime.strptime(person_1.at[i, 'timestamp'], '%Y/%m/%d %H:%M') 

print(did_during)
# a = gps_data.at[3, 'timestamp']
# b = gps_data.at[1, 'date']
# print(a)
# print(b)
# a = datetime.strptime(a, '%Y/%m/%d %H:%M')
# # b = datetime.strptime(b, '%Y-%m-%d')
# print(a)
# # print(b)

