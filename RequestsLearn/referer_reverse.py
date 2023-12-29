# -*- coding: utf-8 -*-

import requests

url = "https://m.douban.com/rexxar/api/v2/movie/recommend?refresh=0&start=0&count=20&selected_categories=%7B%7D&uncollect=false&tags="
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Referer": "https://movie.douban.com/explore"
}

response = requests.get(url=url, headers=headers)
response.encoding = response.apparent_encoding  # ascii
res_text = response.text

# 写文件
with open("./results/douban.json", "w", encoding=response.encoding) as f:
    f.write(res_text)

f.close()
