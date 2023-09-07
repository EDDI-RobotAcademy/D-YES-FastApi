# -*- coding: cp949 -*-

import pandas as pd
import requests
import json
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
import random

load_dotenv()

# �ּ� ��Ȯ �Ⱓ�� �ִ� ��Ȯ �Ⱓ�� ������ �޾� ��� ��Ȯ �Ⱓ�� ����
least_harvest_time = 80
most_harvest_time = 120
avg_harvest_time = int((least_harvest_time + most_harvest_time) / 2)

# ���� ��¥�� ��� ��Ȯ �Ⱓ ���� ��¥�� ����
end_date = datetime.today().date()
start_date = end_date - timedelta(avg_harvest_time)
print(end_date)
print(start_date)

# kamis�� api url
kamis_cert_key = os.getenv('kamis_cert_key')
kamis_cert_id = os.getenv('kamis_cert_id')
parts = urlparse(f'http://www.kamis.or.kr/service/price/xml.do?action=periodProductList&p_productclscode=02&p_startday=2022-10-01&p_endday=2022-10-31&p_itemcategorycode=200&p_itemcode=246&p_kindcode=00&p_productrankcode=01&p_convert_kg_yn=N&p_cert_key={kamis_cert_key}&p_cert_id={kamis_cert_id}&p_returntype=json')
qs = dict(parse_qsl(parts.query))

# kamis�� api ��¥ ���� start_date�� end_date�� ��¥ ������ �Է���
qs['p_startday'] = start_date
qs['p_endday'] = end_date
qs['p_itemcategorycode'] = '100'  # �ķ��۹�
qs['p_itemcode'] = '152'          # ����
qs['p_kindcode'] = '01'           # ����

# �ٲ� api url�� new_url�� ���� �� ������Ʈ ����
parts = parts._replace(query=urlencode(qs))
new_url = urlunparse(parts)
response = requests.get(new_url)
contents = response.text

# json ������ �����͸� �޾� data�� item ������ �޾ƿ�
json_ob = json.loads(contents)
body = json_ob['data']['item']

# ��� ���� �����ϰ� ���������������� ����
product_list = list(filter(lambda item : item['countyname'] == '���', body))
product = pd.DataFrame.from_dict(product_list)

# ������ ���� �÷��� �ϳ��� ��ħ
product['date'] = product['yyyy'] + "/" + product['regday']
print(product)

# ��¥�� ���� �÷����� ������ result�� ����
result = product[['date', 'price']]
print(result)

# ��¥ �����͸� �������� ������ ���·� �ٲ�
end_date = end_date.strftime('%Y%m%d')
start_date = start_date.strftime('%Y%m%d')

# ���û�� api url
weather_authkey = os.getenv('weather_authkey')
parts = urlparse(f'https://apihub.kma.go.kr/api/typ01/url/kma_sfcdd3.php?tm1=20090101&tm2=20191231&stn=212&authKey={weather_authkey}')
qs = dict(parse_qsl(parts.query))

# ���û api�� ��¥ ���� start_date�� end_date�� ��¥ ������ �Է���
qs['tm1'] = start_date
qs['tm2'] = end_date
qs['stn'] = '100'         # ����� ������ȣ

# �ٲ� api url�� new_url�� ���� �� ������Ʈ ����
parts = parts._replace(query=urlencode(qs))
new_url = urlunparse(parts)
response = requests.get(new_url)
contents = response.text

# ���ʿ��� �������� �����ϱ� ���� start_date�� ���� #7777END�� �����ϴ� �ε����� �����ϰ� start�� end�� ����
start = contents.index(start_date)
end = contents.index('#7777END')

# �ʿ��� �������� ������ weather ������ �����ϰ� split ����
weather = contents[start:end]
split = weather.split()

# ���� ������ �÷��� ���� 56���̹Ƿ� 56������ ����Ʈ�� split��
def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

list_chunked = list_chunk(split, 56)

# ���������������� ���� �� �� ������ �÷����� ������
df = pd.DataFrame(list_chunked)
df.columns = ['������', '���� ������ȣ', '�� ��� ǳ��', '�� ǳ��', '�ִ�ǳ��', '�ִ�ǳ��', '�ִ�ǳ�� �ð�', '�ִ����ǳ��', '�ִ����ǳ��', '�ִ����ǳ�� �ð�', '�� ��ձ��', '�ְ���', '�ְ��� �ð�', '�������', '������� �ð�', '�� ��� �̽����µ�', '�� ��� ����µ�', '�� ���� �ʻ�µ�', '�� ��� ������', '��������', '�������� �ð�', '�� ��� �������', '���� ���߷�', '���� ���߷�', '�Ȱ���ӽð�', '�� ��� �������', '�� ��� �ظ���', '�ְ� �ظ���', '�ְ� �ظ��� �ð�', '���� �ظ���', '���� �ظ��� �ð�', '�� ��� ���', '������', '�����ð�', 'į�� ����', '�ϻ���', '�ִ� 1�ð��ϻ�', '�ִ� 1�ð��ϻ� �ð�', '�� ������', '9-9 ������', '������ӽð�', '1�ð� �ִٰ�����', '1�ð� �ִٰ����� �ð�', '10�а� �ִٰ�����', '10�а� �ִٰ����� �ð�', '�ִ� ���찭��', '�ִ� ���찭�� �ð�', '�ֽ� ������', '�ֽ� ������ �ð�', '�ֽ� ����', '�ֽ� ���� �ð�', '0.5m ���߿µ�', '1.0m ���߿µ�', '1.5m ���߿µ�', '3.0m ���߿µ�', '5.0m ���߿µ�']

# �ʿ��� �÷����� weather ������ ����
weather_df = df[['������', '���� ������ȣ', '�� ��ձ��', '�ְ���', '�������', '�� ��� ���', '������', '�� ������']]
print(weather_df)

random_number = random.choices(range(1000,3000), k=14)
print(random_number)