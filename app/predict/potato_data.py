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

# 최소 수확 기간과 최대 수확 기간을 변수로 받아 평균 수확 기간을 구함
least_harvest_time = 80
most_harvest_time = 120
avg_harvest_time = int((least_harvest_time + most_harvest_time) / 2)

# 오늘 날짜와 평균 수확 기간 전의 날짜를 구함
end_date = datetime.today().date()
start_date = end_date - timedelta(avg_harvest_time)
print(end_date)
print(start_date)

# kamis의 api url
kamis_cert_key = os.getenv('kamis_cert_key')
kamis_cert_id = os.getenv('kamis_cert_id')
parts = urlparse(f'http://www.kamis.or.kr/service/price/xml.do?action=periodProductList&p_productclscode=02&p_startday=2022-10-01&p_endday=2022-10-31&p_itemcategorycode=200&p_itemcode=246&p_kindcode=00&p_productrankcode=01&p_convert_kg_yn=N&p_cert_key={kamis_cert_key}&p_cert_id={kamis_cert_id}&p_returntype=json')
qs = dict(parse_qsl(parts.query))

# kamis의 api 날짜 값에 start_date와 end_date의 날짜 정보를 입력함
qs['p_startday'] = start_date
qs['p_endday'] = end_date
qs['p_itemcategorycode'] = '100'  # 식량작물
qs['p_itemcode'] = '152'          # 감자
qs['p_kindcode'] = '01'           # 수미

# 바꾼 api url을 new_url로 저장 후 리퀘스트 받음
parts = parts._replace(query=urlencode(qs))
new_url = urlunparse(parts)
response = requests.get(new_url)
contents = response.text

# json 형식의 데이터를 받아 data의 item 값들을 받아옴
json_ob = json.loads(contents)
body = json_ob['data']['item']

# 평균 값만 추출하고 데이터프레임으로 만듦
product_list = list(filter(lambda item : item['countyname'] == '평균', body))
product = pd.DataFrame.from_dict(product_list)

# 연도와 월일 컬럼을 하나로 합침
product['date'] = product['yyyy'] + "/" + product['regday']
print(product)

# 날짜와 가격 컬럼만을 추출해 result로 선언
result = product[['date', 'price']]
print(result)

# 날짜 데이터를 하이픈을 제거한 형태로 바꿈
end_date = end_date.strftime('%Y%m%d')
start_date = start_date.strftime('%Y%m%d')

# 기상청의 api url
weather_authkey = os.getenv('weather_authkey')
parts = urlparse(f'https://apihub.kma.go.kr/api/typ01/url/kma_sfcdd3.php?tm1=20090101&tm2=20191231&stn=212&authKey={weather_authkey}')
qs = dict(parse_qsl(parts.query))

# 기상청 api의 날짜 값에 start_date와 end_date의 날짜 정보를 입력함
qs['tm1'] = start_date
qs['tm2'] = end_date
qs['stn'] = '100'         # 대관령 지점번호

# 바꾼 api url을 new_url로 저장 후 리퀘스트 받음
parts = parts._replace(query=urlencode(qs))
new_url = urlunparse(parts)
response = requests.get(new_url)
contents = response.text

# 불필요한 정보들을 제거하기 위해 start_date의 값과 #7777END가 시작하는 인덱스를 추출하고 start와 end로 저장
start = contents.index(start_date)
end = contents.index('#7777END')

# 필요한 정보만을 추출해 weather 변수에 대입하고 split 해줌
weather = contents[start:end]
split = weather.split()

# 날씨 정보의 컬럼의 수가 56개이므로 56개마다 리스트를 split함
def list_chunk(lst, n):
    return [lst[i:i+n] for i in range(0, len(lst), n)]

list_chunked = list_chunk(split, 56)

# 데이터프레임으로 선언 후 각 열마다 컬럼명을 지정함
df = pd.DataFrame(list_chunked)
df.columns = ['관측일', '국내 지점번호', '일 평균 풍속', '일 풍정', '최대풍향', '최대풍속', '최대풍속 시각', '최대순간풍향', '최대순간풍속', '최대순간풍속 시각', '일 평균기온', '최고기온', '최고기온 시각', '최저기온', '최저기온 시각', '일 평균 이슬점온도', '일 평균 지면온도', '일 최저 초상온도', '일 평균 상대습도', '최저습도', '최저습도 시각', '일 평균 수증기압', '소형 증발량', '대형 증발량', '안개계속시간', '일 평균 현지기압', '일 평균 해면기압', '최고 해면기압', '최고 해면기압 시각', '최저 해면기압', '최저 해면기압 시각', '일 평균 전운량', '일조합', '가조시간', '캄벨 일조', '일사합', '최대 1시간일사', '최대 1시간일사 시각', '일 강수량', '9-9 강수량', '강수계속시간', '1시간 최다강수량', '1시간 최다강수량 시각', '10분간 최다강수량', '10분간 최다강수량 시각', '최대 강우강도', '최대 강우강도 시각', '최심 신적설', '최심 신적설 시각', '최심 적설', '최심 적설 시각', '0.5m 지중온도', '1.0m 지중온도', '1.5m 지중온도', '3.0m 지중온도', '5.0m 지중온도']

# 필요한 컬럼만을 weather 변수에 대입
weather_df = df[['관측일', '국내 지점번호', '일 평균기온', '최고기온', '최저기온', '일 평균 전운량', '일조합', '일 강수량']]
print(weather_df)

random_number = random.choices(range(1000,3000), k=14)
print(random_number)