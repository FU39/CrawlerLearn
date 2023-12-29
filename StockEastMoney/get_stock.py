# -*- coding: utf-8 -*-

# http://quote.eastmoney.com/center/gridlist.html
# 爬取该页面股票信息

import requests
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import json
import csv


def get_html(url):
    r = requests.get(url, headers={
        'User-Agent': UserAgent().random,
    })
    r.encoding = r.apparent_encoding
    return r.text


# num为爬取多少条记录，可手动设置
num = 20
# 该地址为页面实际获取数据的接口地址
stock_url = 'http://99.push2.eastmoney.com/api/qt/clist/get?cb=jQuery112408733409809437476_1623137764048&pn=1&pz=20&po=1&np=1&ut=bd1d9ddb04089700cf9c27f6f7426281&fltt=2&invt=2&fid=f3&fs=m:0+t:80&fields=f1,f2,f3,f4,f5,f6,f7,f8,f9,f10,f12,f13,f14,f15,f16,f17,f18,f20,f21,f23,f24,f25,f22,f11,f62,f128,f136,f115,f152&_=1623137764167:formatted'
if __name__ == '__main__':
    res_text = get_html(stock_url)
    json_text = res_text.split("(")[1].split(")")[0]
    res_json = json.loads(json_text)
    datas = res_json["data"]["diff"]
    datalist = []
    for data in datas:
        # if (str().startswith('6') or str(data["f12"]).startswith('3') or str(data["f12"]).startswith('0')):
        row = [data["f12"], data["f14"]]
        datalist.append(row)
    print(datalist)

    with open('./results/stock.csv', 'w+', encoding='utf-8', newline="") as f:
        writer = csv.writer(f)
        writer.writerow(('代码', '名称'))
        for data in datalist:
            writer.writerow((data[0] + "\t", data[1] + "\t"))
    f.close()
