# encoding: utf-8
# @Time : 2023/10/27 18:28
# @Auther : ISLEY
# @File : file_util.py
# @DESC : 通用文件工具

"""
    默认只读文件
    @file_url 文件路径
    @return 文本 默认None
"""


def read_file(file_url):
    try:
        with open(file_url, mode='r', encoding='utf-8') as file:
            content = file.read()
            return content
    except FileNotFoundError as ex:
        print(f"文件为找到 {ex}")
    except IOError as ex:
        print(f"IO异常 {ex}")
    except Exception as e:
        print(f"读文件发生未知异常 {e}")

    return None
