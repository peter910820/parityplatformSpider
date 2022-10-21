import requests
from bs4 import BeautifulSoup

res = requests.get('https://www.findprice.com.tw/')
soup = BeautifulSoup(res.text, 'lxml')

data = soup.select('div.goodsdiv')
for d in data:
    img = d.findAll('img')
    a = d.findAll('a')
    font = d.find('font')

    print(img[1]['src'])
    print('N' + d.text.replace(' ','').split('\xa0')[0].split('N')[1])
    print(font.text.replace('\xa0',''))
    print(a[-1].text)