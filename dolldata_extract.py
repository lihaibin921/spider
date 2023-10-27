"""
    提取dolldata
"""

from bs4 import BeautifulSoup
import pandas as pd
import requests

dolldata_url = r"https://www.gfwiki.org/w/%E6%88%98%E6%9C%AF%E4%BA%BA%E5%BD%A2%E5%9B%BE%E9%89%B4"
file_name = r"D:\develop\resources\dolldata.txt"
csv_url = r"D:\develop\resources\dolldata.csv"
excel_url = r"D:\develop\resources\dolldata.xlsx"
column_name = ['id', '名称', '类型', '影响格1', '影响格2', '获取方式', '制造时间']
counter = 0
request_headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36"
}

'''
    按路径读取文件 返回字符串
    @file_name 文件路径
    @return 文件文本
'''


def read_txt(file_name):
    try:
        with open(file_name, mode='r', encoding='utf-8') as file:
            content = file.read()

            return content
    except FileNotFoundError:
        print("文件未找到, 请检查文件路径")
    except IOError as e:
        print("发生IO异常", e)
    except Exception as e:
        print("发生未知异常", e)


'''
    @数据列表
'''


def write_to_csv(list):
    try:
        df = pd.DataFrame(data=list, columns=column_name)
        df.to_csv(csv_url, index=False, encoding='utf-8', sep=',')
    except Exception as e:
        print('写入csv文件发生异常', e)


'''
    @数据列表
'''


def write_to_excel(list):
    try:
        df = pd.DataFrame(data=list, columns=column_name)
        df.to_excel(excel_url, index=False)
    except Exception as e:
        print('写入excel文件发生异常', e)


'''
    @content html文本
'''


def extract_html(content):
    soup = BeautifulSoup(content, 'lxml')
    dolldata_list = soup.find_all(class_='dolldata')
    dolldata_csv_values = []
    for doll in dolldata_list:
        # print(doll.prettify())
        global counter
        counter += 1

        doll_id = int(doll.attrs['data-id'])
        doll_name = doll.attrs['data-name-ingame']
        doll_type = doll.attrs['data-type']
        doll_effect1 = doll.attrs['data-tile-effect1']
        doll_effect2 = doll.attrs['data-tile-effect2']
        doll_obtain = doll.attrs['data-obtain-method']
        doll_time = doll.attrs['data-production-time']
        print(doll_id, doll_name, doll_type, doll_effect1, doll_effect2, doll_obtain, doll_time)

        dolldata_row = [doll_id, doll_name, doll_type, doll_effect1, doll_effect2, doll_obtain, doll_time]
        dolldata_csv_values.append(dolldata_row)

    write_to_csv(dolldata_csv_values)
    # write_to_excel(dolldata_csv_values)


'''
    
'''


def spider():
    try:
        response = requests.get(dolldata_url, headers=request_headers)

        if response.status_code == 200:
            print(response.text)
        else:
            print(f"请求失败，状态码：{response.status_code}")

    except requests.exceptions as ex:
        print(f"请求发生异常 {ex}")
    except Exception as e:
        print(f"请求发生其他异常 {e}")


# 定义主函数
def main():
    spider()
    # content = read_txt(file_name)
    ##print(content)
    # extract_html(content)
    # print("总计 %d" % counter)


# 执行主函数
if __name__ == '__main__':
    main()
