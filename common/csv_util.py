# encoding: utf-8
# @Time : 2023/10/27 18:34
# @Auther : ISLEY
# @File : csv_util.py
# @DESC : csv文件工具

import pandas as pd

"""
    把数据写入csv文件
    @csv_url .csv文件名
    @csv_columns 文件列标题 列表
    @csv_data_list 文件数据 列表
"""


def write_to_csv(csv_url, csv_columns, csv_data_list):
    df = pd.DataFrame(csv_data_list, columns=csv_columns)
    try:
        print(f"写入csv文件 路径{csv_url}")
        df.to_csv(csv_url, index=False, sep=',')
        print("写入csv文件 结束")
    except Exception as e:
        print(f"写入csv文件发生异常 {e}")
