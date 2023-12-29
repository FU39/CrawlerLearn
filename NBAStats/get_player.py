# -*- coding: utf-8 -*-

import requests
from bs4 import BeautifulSoup
import re
import csv
import matplotlib.pyplot as plt
import pandas as pd

player = 'Lebron James'


def get_player_id(player='Kobe'):
    """
    获取球员在网址中的 ID
    :param player: 球员名
    :return: 球员 ID
    """
    url = "http://www.stat-nba.com/playerList.php"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Referer": "http://www.stat-nba.com/playerList.php?name=%E7%A7%91%E6%AF%94",
        "Cookie": "Hm_lvt_102e5c22af038a553a8610096bcc8bd4=1703349722,1703840266,1703841428,1703841536; Hm_lpvt_102e5c22af038a553a8610096bcc8bd4=1703848125"
    }
    params = {
        "name": player
    }

    response = requests.get(url=url, headers=headers, params=params)
    response.encoding = response.apparent_encoding  # utf-8
    res_text = response.text

    # 查找 player 对应的结果, 获取 player_id
    soup = BeautifulSoup(res_text, "html.parser")
    for player_list in soup.find_all(class_='playerList'):
        for div in player_list.find_all("div", class_="name"):
            for a in div.find_all("a"):
                name = a.get_text()
                res = re.search(player, name, re.I)
                if res is not None:
                    href = a.get("href")
                    player_id = href.split('/')[2].split('.')[0]
                    return player_id


def get_response(player_id='195', game_type='season'):
    """
    获取网页数据
    :param player_id: 球员 ID
    :param game_type: season(常规赛), playoff(季后赛), allstar(全明星)
    :return:
    """
    url = "http://www.stat-nba.com/player/stat_box/" + player_id + "_" + game_type + ".html"
    response = requests.get(url)
    response.encoding = response.apparent_encoding
    res_text = response.text
    return res_text


def get_datas(res_text, game_type):
    """
    获取球员历史数据
    :param res_text: 网页数据
    :param game_type: season(常规赛), playoff(季后赛), allstar(全明星)
    :return:
    """
    soup = BeautifulSoup(res_text, "html.parser")
    table = soup.find_all(id='stat_box_avg')

    # 数据
    datas = []
    # 表头
    header = []
    # test_header = []
    thead = table[0].find_all("thead")
    tr_head = thead[0].find_all("tr")
    for th in tr_head[0].find_all("th"):
        item = th.get_text()
        # print(type(item), item)
        if item != '':
            # test_header.append(item)
            header.append(item)
    # if game_type == "season":
    #     header = ["赛季", "球队", "出场", "首发", "时间", "投篮", "命中", "出手", "三分", "命中", "出手", "罚球", "命中",
    #               "出手", "篮板", "前场", "后场", "助攻", "抢断", "盖帽", "失误", "犯规", "得分", "胜", "负"]
    # elif game_type == "playoff":
    #     header = ["赛季", "球队", "出场", "时间", "投篮", "命中", "出手", "三分", "命中", "出手", "罚球", "命中", "出手",
    #               "篮板", "前场", "后场", "助攻", "抢断", "盖帽", "失误", "犯规", "得分", "胜", "负"]
    # elif game_type == "allstar":
    #     header = ["赛季", "球队", "首发", "时间", "投篮", "命中", "出手", "三分", "命中", "出手", "罚球", "命中", "出手",
    #               "篮板", "前场", "后场", "助攻", "抢断", "盖帽", "失误", "犯规", "得分"]
    datas.append(header)

    for tr in table[0].find_all("tr", class_="sort"):
        row = []
        for td in tr.find_all("td"):
            rank = td.get("rank")
            if rank is not None:
                row.append(td.get_text())
        datas.append(row)
    return datas


def write_csv(datas, path):
    """
    写入 csv 文件
    :param datas: 数据
    :param path: 写入文件路径
    """
    with open(path, 'w', encoding='utf-8-sig', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(datas)

    f.close()


def show_data(player='Kobe', game_type='season', item='篮板', plot_name='line'):
    """
    显示篮板, 助攻, 得分等数据
    :param player: 球员
    :param game_type: season, playoff, allstar
    :param item: 篮板, 助攻, 得分, all
    :param plot_name: line(折线图), bar(条形图)
    :return:
    """
    file_name = './results/' + player + '_' + game_type + '.csv'
    datas = pd.read_csv(file_name)
    timeline = datas['赛季'].values.tolist()
    timeline.reverse()
    reb_data = datas['篮板'].values.tolist()  # 篮板数据
    ast_data = datas['助攻'].values.tolist()  # 助攻数据
    pts_data = datas['得分'].values.tolist()  # 得分数据
    reb_data.reverse()
    ast_data.reverse()
    pts_data.reverse()

    if plot_name == 'line':
        if item == 'all':
            plt.plot(timeline, reb_data, c='r', linestyle="-.")
            plt.plot(timeline, ast_data, c='g', linestyle="--")
            plt.plot(timeline, pts_data, c='b', linestyle="-")
            legend = ['篮板', '助攻', '得分']
        elif item == '篮板':
            plt.plot(timeline, reb_data, c='g', linestyle="-")
            legend = [item]
        elif item == '助攻':
            plt.plot(timeline, ast_data, c='g', linestyle="-")
            legend = [item]
        elif item == '得分':
            plt.plot(timeline, pts_data, c='g', linestyle="-")
            legend = [item]
        else:
            return
    elif plot_name == 'bar':
        # facecolor: 表面的颜色
        # edgecolor: 边框的颜色
        if item == 'all':
            fig = plt.figure(figsize=(15, 5))
            ax1 = plt.subplot(131)
            plt.bar(timeline, reb_data, facecolor='#9999ff', edgecolor='white')
            plt.legend(['篮板'])
            plt.title(player + '职业生涯数据分析：' + game_type)
            plt.xticks(rotation=60)
            plt.xlabel('赛季')
            plt.ylabel('篮板')

            ax2 = plt.subplot(132)
            plt.bar(timeline, ast_data, facecolor='#999900', edgecolor='white')
            plt.legend(['助攻'])
            plt.title(player + '职业生涯数据分析：' + game_type)
            plt.xticks(rotation=60)
            plt.xlabel('赛季')
            plt.ylabel('助攻')

            ax3 = plt.subplot(133)
            plt.bar(timeline, pts_data, facecolor='#9988ff', edgecolor='white')
            legend = ['得分']
        elif item == '篮板':
            plt.bar(timeline, reb_data, facecolor='#9900ff', edgecolor='white')
            legend = [item]
        elif item == '助攻':
            plt.bar(timeline, ast_data, facecolor='#9900ff', edgecolor='white')
            legend = [item]
        elif item == '得分':
            plt.bar(timeline, pts_data, facecolor='#9900ff', edgecolor='white')
            legend = [item]
        else:
            return
    else:
        return

    plt.legend(legend)
    plt.title(player + '职业生涯数据分析：' + game_type)
    plt.xticks(rotation=60)
    plt.xlabel('赛季')
    if item != 'all':
        plt.ylabel(item)
    else:
        plt.ylabel('数据')

    fig_name = './results/{}_{}_{}_{}.png'.format(player, game_type, item, plot_name)
    plt.savefig(fig_name)
    plt.show()


if __name__ == '__main__':
    # 设置显示中文
    plt.rcParams['font.sans-serif'] = ['simhei']  # 指定默认字体
    # plt.rcParams['font.sans-serif']=['Fangsong']  # 用来显示中文标签
    plt.rcParams['axes.unicode_minus'] = False  # 用来显示负号
    plt.rcParams['figure.dpi'] = 100  # 每英寸点数

    player_id = get_player_id(player=player)

    for game_type in ['season', 'playoff', 'allstar']:
        res_player = get_response(player_id=player_id, game_type=game_type)
        datas_player = get_datas(res_text=res_player, game_type=game_type)
        path_datas = './results/' + player + '_' + game_type + '.csv'
        write_csv(datas=datas_player, path=path_datas)
        print('{}.csv saved'.format(game_type))

        # 篮板、助攻、得分
        show_data(player=player, game_type=game_type, item='篮板', plot_name='bar')
        show_data(player=player, game_type=game_type, item='助攻', plot_name='bar')
        show_data(player=player, game_type=game_type, item='得分', plot_name='bar')
        show_data(player=player, game_type=game_type, item='all', plot_name='bar')
        show_data(player=player, game_type=game_type, item='篮板', plot_name='line')
        show_data(player=player, game_type=game_type, item='助攻', plot_name='line')
        show_data(player=player, game_type=game_type, item='得分', plot_name='line')
        show_data(player=player, game_type=game_type, item='all', plot_name='line')
