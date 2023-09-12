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

    # ���� ������ ����
    today = datetime.today().date()
    start_date = today - timedelta(days=days)
    end_date = today

    # kamis�� api url
    kamis_cert_key = os.getenv('kamis_cert_key')
    kamis_cert_id = os.getenv('kamis_cert_id')
    parts = urlparse(
        f'http://www.kamis.or.kr/service/price/xml.do?action=periodProductList&p_productclscode=02&p_startday=2022-10-01&p_endday=2022-10-31&p_itemcategorycode=200&p_itemcode=246&p_kindcode=00&p_productrankcode=01&p_convert_kg_yn=N&p_cert_key={kamis_cert_key}&p_cert_id={kamis_cert_id}&p_returntype=json')
    qs = dict(parse_qsl(parts.query))

    # kamis�� api ��¥ ���� start_date�� end_date�� ��¥ ������ �Է���
    qs['p_startday'] = start_date.strftime("%Y-%m-%d")  # ���ڿ��� ��ȯ
    qs['p_endday'] = end_date.strftime("%Y-%m-%d")  # ���ڿ��� ��ȯ
    qs['p_itemcategorycode'] = p_itemcategorycode
    qs['p_itemcode'] = p_itemcode
    qs['p_kindcode'] = p_kindcode

    # �ٲ� api url�� new_url�� ���� �� ������Ʈ ����
    parts = parts._replace(query=urlencode(qs))
    new_url = urlunparse(parts)
    response = requests.get(new_url)
    contents = response.text

    # json ������ �����͸� �޾� data�� item ������ �޾ƿ�
    json_ob = json.loads(contents)
    body = json_ob['data']['item']

    # ��� ���� �����ϰ� ���������������� ����
    product_list = list(filter(lambda item: item['countyname'] == '���', body))
    product = pd.DataFrame.from_dict(product_list)

    # ������ ���� �÷��� �ϳ��� ��ħ
    product['date'] = product['yyyy'] + "/" + product['regday']

    # ��¥�� ���� �÷����� ������ result�� ����
    result = product[['date', 'price']]

    return result
