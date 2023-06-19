from selenium import webdriver
from selenium.webdriver.common.by import By
import time
import pymysql


def travel(city, page):
    url = 'https://www.mafengwo.cn/search/q.php?q={0}&p={1}&t=sales&kt=1'
    driver = webdriver.Chrome()
    driver.get(url.format(city, page))
    # 数据解析
    title_lst = []  # 标题
    desc_lst = []  # 描述
    sold_lst = []  # 已售
    price_lst = []  # 价格
    lst = []  # 存储总的数据
    # 提取场馆
    title_ele_lst = driver.find_elements(by=By.TAG_NAME, value='h3')
    for item in title_ele_lst:
        title_lst.append(item.text)
    # 提取描述
    desc_ele_lst = driver.find_elements(by=By.CLASS_NAME, value='seg-desc')
    for item in desc_ele_lst:
        desc_lst.append(item.text)
    # 提取已售和票价
    info_ele_lst = driver.find_elements(by=By.CLASS_NAME, value='seg-info-list')
    for item in info_ele_lst:
        temp = item.text.split('\n')
        if len(temp) == 2:
            sold_lst.append(temp[0])  # 索引为0的为已售
            price_lst.append(temp[1])  # 索引为1的为价格
        else:
            price_lst.append(temp[0])

    # 使用zip进行打包
    for t, d, s, p in zip(title_lst, desc_lst, sold_lst, price_lst):
        lst.append([t, d, s, p])
    return lst


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
    for i in range(1, 3):
        lst = travel('上海', i)
        sql = 'insert into travel(title,desc_info,sold,price) values(%s,%s,%s,%s)'
        insert_data(sql, lst)
        time.sleep(2)
