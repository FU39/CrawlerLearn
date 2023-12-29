# -*- coding: utf-8 -*-

import requests

category = '"悬疑"'

# get 提交的数据会放在 url 之后, 以 ? 分割 url 和传输数据, 参数之间以 & 相连
url = "https://m.douban.com/rexxar/api/v2/movie/recommend"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Referer": "https://movie.douban.com/explore"
}
params = {
    "start": "0",
    "count": "20",
    "selected_categories": f'{{"类型":{category}}}',
    "tags": category,
}
# print(f'{{"类型":{category}}}')
response = requests.get(url=url, headers=headers, params=params)
print("data:", response.json(), sep='\n')
response.encoding = response.apparent_encoding  # ascii
res_text = response.text

# 写文件
with open("./results/douban.json", "w", encoding=response.encoding) as f:
    f.write(res_text)

f.close()
