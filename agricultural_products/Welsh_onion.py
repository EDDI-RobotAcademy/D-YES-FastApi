import csv

import pandas as pd
import requests
import json
import pprint

url = 'http://www.kamis.or.kr/service/price/xml.do?action=periodProductList&p_productclscode=02&p_startday=2022-10-01&p_endday=2022-10-31&p_itemcategorycode=200&p_itemcode=246&p_kindcode=00&p_productrankcode=01&p_countrycode=2401&p_convert_kg_yn=Y&p_cert_key=b7b28aa9-93af-410a-a88d-a8f192e02298&p_cert_id=3536&p_returntype=json'
response = requests.get(url)
contents = response.text

pp = pprint.PrettyPrinter(indent=4)
print(pp.pprint(contents))

json_ob = json.loads(contents)
print(json_ob)
print(type(json_ob))

body = json_ob['data']['item']
print(body)
print(body[38])
print(body[56])

print(body[38:57])

welsh = body[38:57]
print(welsh)

df = pd.DataFrame.from_dict(welsh)
print(df)

df.to_csv('welsh_onion.csv')