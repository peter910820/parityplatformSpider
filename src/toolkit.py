import os,json,requests
from bs4 import BeautifulSoup

def parity(keyword):
    base_url = 'https://www.findprice.com.tw/'
    res = requests.get(f'{base_url}g/{keyword}')
    soup = BeautifulSoup(res.text, 'lxml')
    data = soup.select('div.divHotGoods')

    json_data = '{"type": "carousel","contents": ['
    judge = 0
    for i in data:
        if judge == 6: break
        j = i.select('div.GoodsImg')[0]

        json_data += '''{
                    "type": "bubble",
                    "header": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": [
                        {
                            "type": "text",
                            "text": "'''+i.select('div.GoodsGname')[0].text+'''"
                        }
                        ]
                    },
                    "hero": {
                        "type": "image",
                        "url": "'''+j.find('img')['src']+'''"
                    }, "body": {
                        "type": "box",
                        "layout": "vertical",
                        "contents": ['''
        k = i.select('div.divHotDetail')[0]
        s = k.find_all('a')
        for shop in s:
            try:
                json_data += '''{
                            "type": "box",
                            "layout": "horizontal",
                            "contents": [
                            {
                                "type": "image",
                                "url": "'''+shop.find('img')['src']+'''",
                                "size": "25px",
                                "position": "absolute",
                                "offsetTop": "lg"
                            },
                            {
                                "type": "text",
                                "text": "'''+shop.select('div.divHotDetailListTitle')[0].text+'''",
                                "offsetStart": "50px"
                            }
                            ],
                            "spacing": "none",
                            "margin": "none",
                            "paddingAll": "xl"
                        },
                        {
                            "type": "button",
                            "action": {
                            "type": "uri",
                            "label": "'''+shop.select('span.rec-price')[0].text+'''",
                            "uri": "'''+shop['href']+'''"
                            },
                            "style": "primary"
                        },'''
            except:
                break
        json_data = json_data[:-1]
        json_data += ''' ] } },'''
        judge += 1

    json_data = json_data[:-1]
    json_data +=  ']}'
    
    return json_data