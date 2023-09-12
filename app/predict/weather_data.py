# -*- coding: cp949 -*-

import pandas as pd
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, timedelta
from urllib.parse import urlparse, parse_qsl, urlencode, urlunparse


def get_weather_data(start_days, end_days, weather_column):
    load_dotenv()

    # 평균 기온 데이터 구간
    today = datetime.today().date()
    start_date = (today - timedelta(days=start_days)).strftime("%Y%m%d")
    end_date = (today - timedelta(days=end_days)).strftime("%Y%m%d")

    # 기상청의 api url
    weather_authkey = os.getenv('weather_authkey')
    parts = urlparse(
        f'https://apihub.kma.go.kr/api/typ01/url/kma_sfcdd3.php?tm1=20090101&tm2=20191231&stn=212&authKey={weather_authkey}')
    qs = dict(parse_qsl(parts.query))

    # 기상청 api의 날짜 값에 start_date와 end_date의 날짜 정보를 입력함
    qs['tm1'] = start_date
    qs['tm2'] = end_date
    qs['stn'] = '100'  # 대관령 지점번호

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
        return [lst[i:i + n] for i in range(0, len(lst), n)]

    list_chunked = list_chunk(split, 56)

    # 데이터프레임으로 선언 후 각 열마다 컬럼명을 지정함
    df = pd.DataFrame(list_chunked)
    df.columns = ['관측일', '국내 지점번호', '일 평균 풍속', '일 풍정', '최대풍향', '최대풍속', '최대풍속 시각', '최대순간풍향', '최대순간풍속', '최대순간풍속 시각',
                  '일 평균기온', '최고기온', '최고기온 시각', '최저기온', '최저기온 시각', '일 평균 이슬점온도', '일 평균 지면온도', '일 최저 초상온도', '일 평균 상대습도',
                  '최저습도', '최저습도 시각', '일 평균 수증기압', '소형 증발량', '대형 증발량', '안개계속시간', '일 평균 현지기압', '일 평균 해면기압', '최고 해면기압',
                  '최고 해면기압 시각', '최저 해면기압', '최저 해면기압 시각', '일 평균 전운량', '일조합', '가조시간', '캄벨 일조', '일사합', '최대 1시간일사',
                  '최대 1시간일사 시각', '일 강수량', '9-9 강수량', '강수계속시간', '1시간 최다강수량', '1시간 최다강수량 시각', '10분간 최다강수량',
                  '10분간 최다강수량 시각', '최대 강우강도', '최대 강우강도 시각', '최심 신적설', '최심 신적설 시각', '최심 적설', '최심 적설 시각', '0.5m 지중온도',
                  '1.0m 지중온도', '1.5m 지중온도', '3.0m 지중온도', '5.0m 지중온도']

    # 필요한 컬럼만을 weather 변수에 대입
    temp_weather_df = df[['관측일', weather_column]]

    return temp_weather_df
