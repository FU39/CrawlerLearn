# -*- coding: utf-8 -*-

import csv
import urllib.request as r
import threading

# 设置信号量，控制线程并发数
sem = threading.Semaphore(1)

url_start = 'http://quotes.money.163.com/service/chddata.html?code='
url_end = '&end=20210221&fields=TCLOSE;HIGH;LOW;TOPEN;LCLOSE;CHG;PCHG;VOTURNOVER;VATURNOVER'


def get_stock_list():
    """
    读取之前获取的个股 csv 丢入到一个列表中
    """
    stock_list = []
    with open('./results/stock.csv', 'r', encoding='utf-8') as f:
        f.seek(0)
        reader = csv.reader(f)
        for item in reader:
            stock_list.append(item)
    f.close()
    return stock_list


def download_file(url, file_path):
    # print(file_path)
    try:
        r.urlretrieve(url, file_path)
    except Exception as e:
        print(e)
    print(file_path, "is downloaded")
    pass


def download_file_sem(url, file_path):
    with sem:
        download_file(url, file_path)


if __name__ == '__main__':
    stockList = get_stock_list()
    stockList.pop(0)
    print(stockList)
    for s in stockList:
        scode = str(s[0].split("\t")[0])
        # 0：沪市；1：深市
        url = url_start + ("0" if scode.startswith('6') else "1") + scode + url_end
        print(url)
        file_path = "./results/" + (str(s[1].split("\t")[0]) + "_" + scode) + ".csv"
        threading.Thread(target=download_file_sem, args=(url, file_path)).start()
