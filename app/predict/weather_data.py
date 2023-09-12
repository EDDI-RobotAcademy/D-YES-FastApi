# -*- coding: cp949 -*-

import pandas as pd
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse


def get_weather_data(start_days, end_days, weather_column):
    load_dotenv()

    # ��� ��� ������ ����
    today = datetime.today().date()
    start_date = (today - timedelta(days=start_days)).strftime("%Y%m%d")
    end_date = (today - timedelta(days=end_days)).strftime("%Y%m%d")

    # ���û�� api url
    weather_authkey = os.getenv('weather_authkey')
    parts = urlparse(
        f'https://apihub.kma.go.kr/api/typ01/url/kma_sfcdd3.php?tm1=20090101&tm2=20191231&stn=212&authKey={weather_authkey}')
    qs = dict(parse_qsl(parts.query))

    # ���û api�� ��¥ ���� start_date�� end_date�� ��¥ ������ �Է���
    qs['tm1'] = start_date
    qs['tm2'] = end_date
    qs['stn'] = '100'  # ����� ������ȣ

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
        return [lst[i:i + n] for i in range(0, len(lst), n)]

    list_chunked = list_chunk(split, 56)

    # ���������������� ���� �� �� ������ �÷����� ������
    df = pd.DataFrame(list_chunked)
    df.columns = ['������', '���� ������ȣ', '�� ��� ǳ��', '�� ǳ��', '�ִ�ǳ��', '�ִ�ǳ��', '�ִ�ǳ�� �ð�', '�ִ����ǳ��', '�ִ����ǳ��', '�ִ����ǳ�� �ð�',
                  '�� ��ձ��', '�ְ���', '�ְ��� �ð�', '�������', '������� �ð�', '�� ��� �̽����µ�', '�� ��� ����µ�', '�� ���� �ʻ�µ�', '�� ��� ������',
                  '��������', '�������� �ð�', '�� ��� �������', '���� ���߷�', '���� ���߷�', '�Ȱ���ӽð�', '�� ��� �������', '�� ��� �ظ���', '�ְ� �ظ���',
                  '�ְ� �ظ��� �ð�', '���� �ظ���', '���� �ظ��� �ð�', '�� ��� ���', '������', '�����ð�', 'į�� ����', '�ϻ���', '�ִ� 1�ð��ϻ�',
                  '�ִ� 1�ð��ϻ� �ð�', '�� ������', '9-9 ������', '������ӽð�', '1�ð� �ִٰ�����', '1�ð� �ִٰ����� �ð�', '10�а� �ִٰ�����',
                  '10�а� �ִٰ����� �ð�', '�ִ� ���찭��', '�ִ� ���찭�� �ð�', '�ֽ� ������', '�ֽ� ������ �ð�', '�ֽ� ����', '�ֽ� ���� �ð�', '0.5m ���߿µ�',
                  '1.0m ���߿µ�', '1.5m ���߿µ�', '3.0m ���߿µ�', '5.0m ���߿µ�']

    # �ʿ��� �÷����� weather ������ ����
    temp_weather_df = df[['������', weather_column]]

    return temp_weather_df
