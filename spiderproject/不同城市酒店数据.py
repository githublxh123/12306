from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait  # 显示等待
from selenium.webdriver.support import expected_conditions as EC  # 等待条件
import time
import pymysql

lst = []  # 存储最终的数据
url = 'https://www.mafengwo.cn/hotel/{0}/#avl=0&distance=10000&price=-&feature=0&fav=0&sort=comment-DESC&page={1}'


def hotel_info(city, page):
    driver = webdriver.Chrome()
    title_ch = []  # 酒店中文名称
    title_eng = []  # 酒店英文名称
    address_lst = []  # 地址
    driver.get(url.format(city, page))

    # 显示等待
    WebDriverWait(driver, 1000).until(
        EC.presence_of_element_located((By.CLASS_NAME, 'dialog-container'))
    )
    time.sleep(10)
    driver.find_element(by=By.CLASS_NAME, value='dialog-confirm-btn').click()
    time.sleep(3)
    div_ele_lst = driver.find_elements(by=By.CLASS_NAME, value='title')
    for item in div_ele_lst:
        temp = item.text.split('\n')
        title_ch.append(temp[0])  # 索引为0的是中文
        title_eng.append(temp[1])  # 索引为1的是英文
    # 提取地址
    address_ele_lst = driver.find_elements(by=By.CLASS_NAME, value='location')
    for item in address_ele_lst:
        address_lst.append(item.text)

    # 使用zip函数进行打包
    for tc, te, add in zip(title_ch, title_eng, address_lst):
        lst.append([tc, te, add])


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
        hotel_info(10065, i)  # 北京
        time.sleep(2)
        hotel_info(10099, i)  # 上海

    sql = 'insert into hotel(name_ch,name_eng,address) values(%s,%s,%s)'
    insert_data(sql, lst)
