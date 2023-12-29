# -*- coding: utf-8 -*-

import requests

url = "https://www.baidu.com/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
}

response = requests.get(url=url, headers=headers)
response.encoding = response.apparent_encoding  # utf-8
res_text = response.text
# res_text = response.content.decode("utf-8", "ignore")

# 写文件
with open("./results/baidu.html", "w", encoding=response.encoding) as f:
    f.write(res_text)

f.close()
