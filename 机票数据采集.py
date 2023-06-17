from selenium import webdriver
from selenium.webdriver.common.by import By

import pymysql


def get_plane_ticket(depart_city, depart_code, dest_city, dest_code, depart_date):
    url = 'https://www.mafengwo.cn/flight/#/list?departCity={0}&departCode={1}&destCity={2}&destCode={3}&type=oneWay&status=0&departDate={4}&destDate=&withChild=0'
    driver = webdriver.Chrome()
    driver.get(url.format(depart_city, depart_code, dest_city, dest_code, depart_date))
    # 数据解析
    # 航空公司和机型
    name_lst = []  # 航空公司
    info_lst = []  # 机型
    start_time = []  # 起飞起时
    from_airport = []  # 起飞机场
    end_time = []  # 抵达时间
    to_airport = []  # 抵达机场
    price_lst = []  # 机票的价格
    result_lst = []  # 存储最终结果
    lst = driver.find_elements(by=By.CLASS_NAME, value='v-list-item-name')
    for item in lst:
        info = item.text.split('\n')
        name_lst.append(info[0])  # 航空公司
        info_lst.append(info[1])  # 机型
    # 定位起飞时间，起飞机场，抵达时间，抵达机场
    time_ele_lst = driver.find_elements(by=By.CLASS_NAME, value='v-list-item-time')
    for i in range(0, len(time_ele_lst)):
        if i % 2 == 0:
            temp = time_ele_lst[i].text.split('\n')
            start_time.append(temp[0])  # 起飞时间
            from_airport.append(temp[1])  # 起飞机场
        else:
            temp = time_ele_lst[i].text.split('\n')
            end_time.append(temp[0])  # 抵达时间
            to_airport.append(temp[1])  # 抵达机场
    # 价格
    price_ele_lst = driver.find_elements(by=By.CLASS_NAME, value='v-list-item-price-desc')
    for item in price_ele_lst:
        price_lst.append(item.text)

    # 使用zip函数进行打包
    for name, info, s_t, f_a, e_t, t_a, p in zip(name_lst, info_lst, start_time, from_airport, end_time, to_airport,
                                                 price_lst):
        result_lst.append([name, info, s_t, f_a, e_t, t_a, p])

    return result_lst


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
    lst = get_plane_ticket('天津', 'TSN', '上海', 'SHA', '2022-11-11')
    sql = 'insert into plane_ticket(company,airplane_type,start_time,from_airport,end_time,to_airport,price) values (%s,%s,%s,%s,%s,%s,%s)'

    insert_data(sql, lst)
