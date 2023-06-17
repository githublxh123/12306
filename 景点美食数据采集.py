import requests
# 使用XPath解析数据
from lxml import etree

import pymysql

url = 'https://www.mafengwo.cn/cy/{0}/0-0-{1}-0-0-1.html'
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'}


def get_request(city, food_type):
    resp = requests.get(url.format(city, food_type), headers=headers)
    return resp.text


lst = []


# 解析数据
def parse(html):
    # 获取HTML元素对象
    html = etree.HTML(html)
    # 使用XPath提取元素
    # 名称
    names = html.xpath('//ul[@class="poi-list"]/li/div[@class="title"]/h3/a/text()')
    # 最新点评
    rev_info = html.xpath('//ul[@class="poi-list"]/li/div[@class="rev-info"]/div[@class="rev-txt"]/p/text()')
    # 用户评分
    grade = html.xpath('//ul[@class="poi-list"]/li/div[@class="grade"]/em/text()')

    # 用户评论条数
    rev_num = html.xpath('//ul[@class="poi-list"]/li/div[@class="grade"]/p[@class="rev-num"]/em/text()')
    # 数据打包
    for n, r, g, num in zip(names, rev_info, grade, rev_num):
        lst.append([n, r, g, num])


def insert_data(sql, lst):
    db = pymysql.connect(host='127.0.0.1', user='root', password='lxh', database='mafengwo')
    try:
        cursor = db.cursor()
        return cursor.executemany(sql, lst)
    except Exception as e:
        print(e)
    finally:
        db.commit()  # 提交
        db.close()


if __name__ == '__main__':
    result = get_request(10099, 35279)  # 上海，本帮菜
    parse(result)  # 解析
    # print(lst)
    sql = 'insert into delicious_food(shop_name,rev_info,grade,rev_num) values(%s,%s,%s,%s)'
    insert_data(sql, lst)
