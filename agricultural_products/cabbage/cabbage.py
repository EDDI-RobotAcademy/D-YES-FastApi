import pandas as pd

df = pd.read_csv('양배추_09~19_가격.csv')
print(df)

#df = df.add_prefix('09/')
#print(df)

#df1 = df[['일자', '서울가락도매\n평균가격 (원/kg)']]
#print(df1)

#df1 = df1.fillna(0)
#print(df1)