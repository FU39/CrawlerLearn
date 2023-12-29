# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re

player = "Lebron James"

url = "http://www.stat-nba.com/playerList.php"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
    "Referer": "http://www.stat-nba.com/playerList.php?name=%E7%A7%91%E6%AF%94",
    "Cookie": "Hm_lvt_102e5c22af038a553a8610096bcc8bd4=1703349722,1703840266,1703841428,1703841536; Hm_lpvt_102e5c22af038a553a8610096bcc8bd4=1703848125"
}
params = {
    "name": player
}

if __name__ == '__main__':
    response = requests.get(url=url, headers=headers, params=params)
    response.encoding = response.apparent_encoding  # utf-8
    res_text = response.text

    # 写文件
    with open("res.html", "w", encoding=response.encoding) as f:
        f.write(res_text)

    f.close()

    soup = BeautifulSoup(res_text, "html.parser")
    for player_list in soup.find_all(class_='playerList'):
        for div in player_list.find_all("div", class_="name"):
            for a in div.find_all("a"):
                name = a.get_text()
                res = re.search(player, name, re.I)
                if res is not None:
                    href = a.get("href")
                    player_id = href.split('/')[2].split('.')[0]
