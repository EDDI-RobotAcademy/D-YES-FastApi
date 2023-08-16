import csv

import pandas as pd
import requests
import json
import pprint

url = 'https://apihub.kma.go.kr/api/typ01/url/kma_sfcdd3.php?tm1=20220101&tm2=20221231&stn=212&authKey=oT-QHdeESMi_kB3XhPjInw'
response = requests.get(url)
contents = response.text

print(contents)

f = open("홍천.txt", 'w')
f.write(contents)
f.close()

#txt = pd.read_csv(url)
#print(txt)

#txt = txt.loc[4:368]
#print(txt)

#txt = txt.iloc[:, 0:5]
#print(txt)

