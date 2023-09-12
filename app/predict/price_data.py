# -*- coding: cp949 -*-

import pandas as pd
import requests
import os
from dotenv import load_dotenv
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse
from datetime import datetime, timedelta
import json


def get_kamis_price_data(days, p_itemcategorycode, p_itemcode, p_kindcode):
    load_dotenv()

    # 가격 데이터 구간
    today = datetime.today().date()
    start_date = today - timedelta(days=days)
    end_date = today

    # kamis의 api url
    kamis_cert_key = os.getenv('kamis_cert_key')
    kamis_cert_id = os.getenv('kamis_cert_id')
    parts = urlparse(
        f'http://www.kamis.or.kr/service/price/xml.do?action=periodProductList&p_productclscode=02&p_startday=2022-10-01&p_endday=2022-10-31&p_itemcategorycode=200&p_itemcode=246&p_kindcode=00&p_productrankcode=01&p_convert_kg_yn=N&p_cert_key={kamis_cert_key}&p_cert_id={kamis_cert_id}&p_returntype=json')
    qs = dict(parse_qsl(parts.query))

    # kamis의 api 날짜 값에 start_date와 end_date의 날짜 정보를 입력함
    qs['p_startday'] = start_date.strftime("%Y-%m-%d")  # 문자열로 변환
    qs['p_endday'] = end_date.strftime("%Y-%m-%d")  # 문자열로 변환
    qs['p_itemcategorycode'] = p_itemcategorycode
    qs['p_itemcode'] = p_itemcode
    qs['p_kindcode'] = p_kindcode

    # 바꾼 api url을 new_url로 저장 후 리퀘스트 받음
    parts = parts._replace(query=urlencode(qs))
    new_url = urlunparse(parts)
    response = requests.get(new_url)
    contents = response.text

    # json 형식의 데이터를 받아 data의 item 값들을 받아옴
    json_ob = json.loads(contents)
    body = json_ob['data']['item']

    # 평균 값만 추출하고 데이터프레임으로 만듦
    product_list = list(filter(lambda item: item['countyname'] == '평균', body))
    product = pd.DataFrame.from_dict(product_list)

    # 연도와 월일 컬럼을 하나로 합침
    product['date'] = product['yyyy'] + "/" + product['regday']

    # 날짜와 가격 컬럼만을 추출해 result로 선언
    result = product[['date', 'price']]

    return result
