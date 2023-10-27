# encoding: utf-8
# @Time : 2023/10/27 20:03
# @Auther : ISLEY
# @File : time_util.py
# @DESC : 时间相关工具

import time

__no_seconds_time_format = "%Y-%m-%d %H-%M"

"""
    返回时间字符串 只到分钟级别
"""


def get_now_no_seconds():
    return time.strftime(__no_seconds_time_format, time.localtime())
