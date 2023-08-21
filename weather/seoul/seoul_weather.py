import requests

url = 'https://apihub.kma.go.kr/api/typ01/url/kma_sfcdd3.php?tm1=20090101&tm2=20191231&stn=108&authKey=oT-QHdeESMi_kB3XhPjInw'
response = requests.get(url)
contents = response.text

print(contents)

f = open("서울.txt", 'w')
f.write(contents)
f.close()
