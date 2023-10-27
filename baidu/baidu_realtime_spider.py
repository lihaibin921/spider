# encoding: utf-8
# @Time : 2023/10/27 14:43
# @Auther : ISLEY
# @File : baidu_realtime_spider.py
# @DESC : 百度热搜爬虫

import requests
from lxml import etree
from common import file_util, time_util, csv_util

__baidu_realtime_url = r"https://top.baidu.com/board?tab=realtime"
__baidu_realtime_local = r"test/baidu/baidu_realtime_test1.html"
__baidu_realtime_csv_url = r"data/baidu/baidu_realtime_data"
__headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}

"""
    发送请求, 获取html数据
    @return html文本
"""


def get_html_from_url():
    try:
        response = requests.get(__baidu_realtime_url, headers=__headers)
        if response.status_code == 200:
            return response.text
        else:
            print(f"请求失败 错误代码{response.status_code}")
    except Exception as e:
        print(f"请求异常 {e}")

    return None


"""
    解析html文件 返回数据列表
    @content html文本
    @return list
"""


def get_data_from_html(content):
    if content is None:
        return None

    # 使用lxml解析html文本
    realtime_html = etree.HTML(content)  # type: etree._Element
    # 获取链接列表
    hrefs = realtime_html.xpath('//*[@id="sanRoot"]/main/div[2]/div/div[2]/div/a[1]/@href')
    # 获取标题列表
    titles = realtime_html.xpath('//*[@id="sanRoot"]/main/div[2]/div/div[2]/div/div[2]/a[1]/div[1]/text()')
    # 获取热度指数
    hot_indexs = realtime_html.xpath('//*[@id="sanRoot"]/main/div[2]/div/div[2]/div/div[1]/div[2]/text()')

    # 将多组数据组合起来
    data_list = list(zip(hrefs, titles, hot_indexs))

    for href, title, index in data_list:
        print(href + "," + title + "," + index)

    return data_list


'''
    百度热搜爬虫
'''


def baidu_realtime_spider_main():
    # 获取html
    # content = file_util.read_file(__baidu_realtime_local)
    content = get_html_from_url()
    # 提取数据列表
    data_list = get_data_from_html(content)
    # 写入csv
    columns = ['链接', '标题', '热度']
    csv_url = __baidu_realtime_csv_url + time_util.get_now_no_seconds() + '.csv'
    csv_util.write_to_csv(csv_url, columns, data_list)
