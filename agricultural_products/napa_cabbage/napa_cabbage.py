import pandas as pd

df = pd.read_csv('배추(전체) 거래정보-평균가격.csv')
print(df)

df1 = df[['일자', '서울가락도매\n평균가격 (원/kg)']]
print(df1)

df1 = df1.fillna(0)
print(df1)

df1.to_csv('napa_cabbage.csv')