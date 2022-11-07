import requests
from bs4 import BeautifulSoup

base_url = 'https://www.findprice.com.tw/'
res = requests.get(f'{base_url}g/iphone')
soup = BeautifulSoup(res.text, 'lxml')
data = soup.select('div.divHotGoods')

for i in data:
    # print(i.select('div.GoodsGname')[0].text) #title

    j = i.select('div.GoodsImg')[0]
    # print(j.find('img')['src']) #img

    k = i.select('div.divHotDetail')[0]
    s = k.find_all('a')
    for shop in s:
        try:
            # print(shop.find('img')['src'],sep=',') #img
            # print(shop.select('div.divHotDetailListTitle')[0].text,sep=',')
            # print(shop.select('span.rec-price')[0].text)
            print(shop['href'])
        except:
            break