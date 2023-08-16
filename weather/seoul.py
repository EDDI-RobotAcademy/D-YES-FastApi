import csv

import pandas as pd
import requests
import json
import pprint

file = open('서울.txt', 'r')
read = file.read()
split = read.split()
#print(split)

def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

list_chunked = list_chunk(split, 56)
print(list_chunked)

df = pd.DataFrame(list_chunked)
print(df)

df.columns = ['관측일', '국내 지점번호', '일 평균 풍속', '일 풍정', '최대풍향', '최대풍속', '최대풍속 시각', '최대순간풍향', '최대순간풍속', '최대순간풍속 시각', '일 평균기온', '최고기온', '최고기온 시각', '최저기온', '최저기온 시각', '일 평균 이슬점온도', '일 평균 지면온도', '일 최저 초상온도']

#df1 = df[['0', '1', '10', '11', '13', '31', '32', '38']]
print(df)

#df.to_csv('서울.csv')

file.close()
#data = file.read().splitlines()
#print(*data, sep='\n')