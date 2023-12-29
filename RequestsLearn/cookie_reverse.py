# -*- coding: utf-8 -*-
import json
import requests

url = "https://stock.xueqiu.com/v5/stock/screener/quote/list.json?page=1&size=10&type=sha&order_by=percent&order=desc"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Referer": "https://movie.douban.com/explore",
    "Cookie": "xq_a_token=9eb4932f3197a06d242009fa2ee386ce66c8799f; xqat=9eb4932f3197a06d242009fa2ee386ce66c8799f; xq_r_token=d7a7d3c7d70d9e116b3f0277feb01c5b9543559b; xq_id_token=eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJ1aWQiOi0xLCJpc3MiOiJ1YyIsImV4cCI6MTcwNTg4NDA0OSwiY3RtIjoxNzAzMzIyODA1MzA3LCJjaWQiOiJkOWQwbjRBWnVwIn0.JQPbR_RvHkSZIztxJyDb2w_rTzIg-nL85IPb6Q0Q4P0bhiYFc18pK0sMkZDT1GJxM3YuzPXWedFNG4lJt0NoEfwmxvsH7Lv5NMJhTZBR605xbMwIhMaevban56iJDNCnEET466GoNPTJ1ghep5349fxAcxdqMvLW0M9QHg-Op-sY0FBecCXqsneOvLRfkqN7tYWwJktzSQdyRFGm3OSQQiHJ26d8_c3W62fGye8cXVojjKQLoY3qTb5fcM8obhO6L9f6gUAGG9V1DDeOQ3CKis5Ti-A6O8PILqeBeSRBBesbPXDDgsfoZP2oaIbH0LUlgNl1CgfC_xUkjVD0aJDJ3Q; cookiesu=421703322834816; u=421703322834816; device_id=f6eaaa028ca332f3d6cdcb3a1460a955; Hm_lvt_1db88642e346389874251b5a1eded6e3=1703322868; Hm_lpvt_1db88642e346389874251b5a1eded6e3=1703322976"
}

response = requests.get(url=url, headers=headers)
response.encoding = response.apparent_encoding  # 'utf-8'
res_text = response.text

# res_json = response.json()
res_json = json.loads(res_text)

datas = res_json["data"]["list"]
for data in datas:
    print(data["name"])

# 写文件
with open("./results/xueqiu.json", "w", encoding=response.encoding) as f:
    # f.write(res_text)
    json.dump(res_json, f)

f.close()
