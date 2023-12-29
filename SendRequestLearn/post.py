# -*- coding: utf-8 -*-

import requests

while 1:
    wd = input("请输入翻译内容：")

    res = requests.post("https://aidemo.youdao.com/trans?", params={}, headers={},
                        data={
                            "q": wd,
                            "from": "Auto",
                            "to": "Auto"
                        })

    print(res.json().get("translation")[0])
