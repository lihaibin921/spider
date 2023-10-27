# encoding: utf-8
# @Time : 2023/10/26 18:02
# @Auther : ISLEY
# @File : weibo_hot_spider.py
# @DESC : 微博热搜榜单爬虫
import bs4.element
import requests
from bs4 import BeautifulSoup
import pandas as pd
import time

weibo_hot_url = r'https://s.weibo.com/top/summary?cate=realtimehot'
weibo_hot_test_html = r"test/weibo/weibo_hot_test1.html"
weibo_hot_data_url = r"data/weibo/weibo_hot_data"
headers = {
    "Cookie": "SUB=_2AkMSZtbvf8NxqwJRmP0VymniaoV1yg_EieKkOic0JRMxHRl-yj9vqkZetRB6Oeb4AKIvpXFwtbJHOZuLYmBm2u_ea89N; SUBP=0033WrSXqPxfM72-Ws9jqgMF55529P9D9WWdfgqP2.vGGrYhQN.Fmr2.; _s_tentry=passport.weibo.com; Apache=1288904485164.4993.1698322905442; SINAGLOBAL=1288904485164.4993.1698322905442; ULV=1698322905444:1:1:1:1288904485164.4993.1698322905442:",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}

"""
    从本地读微博html文件 用于测试
    @return 返回html文本
"""


def get_data_from_local():
    try:
        with  open(weibo_hot_test_html, mode='r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError as ex:
        print(f"文件为找到 {ex}")
    except IOError as ex:
        print(f"IO异常 {ex}")
    except Exception as e:
        print(f"读文件发生未知异常 {e}")

    return None


"""
    发送请求 获取数据 返回文本(html)
    @return 文本
"""


def get_data_from_url():
    try:
        response = requests.get(weibo_hot_url, headers=headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"请求失败 错误代码 {response.status_code}")
    except Exception as e:
        print(f"请求发生异常 : {e}")
    return None


"""
    从html中解析微博热搜数据
    @content html文本
    @return 数据列表
"""


def get_data_from_html(content):
    if content is None:
        return None

    # 封装热搜数据列表
    hot_list = []
    valid_counter = 0
    soup = BeautifulSoup(content, 'lxml')
    tbody = soup.find("tbody")
    tr_list = tbody.contents

    # 循环遍历热数据
    for tr in tr_list:
        if not isinstance(tr, bs4.element.Tag):
            continue

        td1 = tr.find(class_='td-01')
        td2 = tr.find(class_='td-02')
        td3 = tr.find(class_='td-03')

        # 序列
        hot_index = td1.text.strip()

        # 链接
        hot_url = (r"https://s.weibo.com" + td2.a["href"]).strip()
        if 'href_to' in td2.a.attrs:
            hot_url = (r"https://s.weibo.com" + td2.a["href_to"]).strip()

        # 热度
        hot_num = ''
        if td2.span:
            hot_num = td2.span.text.strip()

        # 内容
        hot_text = td2.a.text.strip()

        # 标签
        hot_lab = td3.text.strip()
        hot_data = [hot_index, hot_url, hot_text, hot_num, hot_lab]

        # 记录
        valid_counter += 1
        print(f"获取第 {valid_counter} 条数据 : {hot_data}")

        hot_list.append(hot_data)

    return hot_list


"""
    将列表信息写进csv
    @list get_data_from_html 返回的列表
"""


def write_data_to_csv(data_list):
    columns = ['序号', '内容', '链接', '热度', '标签']
    df = pd.DataFrame(data_list, columns=columns)
    try:
        csv_url = weibo_hot_data_url + time.strftime("%Y-%m-%d %H-%M", time.localtime()) + '.csv'
        df.to_csv(csv_url, index=False, sep=',')
    except Exception as e:
        print(f"写入csv发生异常 {e}")


def weibo_hot_spider_main():
    # html_data = get_data_from_local()
    html_data = get_data_from_url()
    if html_data:
        print(f"爬虫开始")
        data_list = get_data_from_html(html_data)
        write_data_to_csv(data_list)
        print(f"爬虫结束")
    else:
        print(f"未从链接中获取到信息")
