from selenium import webdriver
from selenium.webdriver.common.by import By
import pymysql


class PC_Auto:
    driver = webdriver.Chrome()
    sales_url = ' https://price.pcauto.com.cn/top/sales/s1-t{0}-y{1}-m{2}.html'
    sales_car_top_lst = []

    def sales_car(self, num, year, month, type):  # type指的是轿车，SUV 还是MPV
        top_lst = []  # 存储排名
        brand_lst = []  # 存储车系
        price_lst = []  # 存储官方价
        rel_brand_lst = []  # 存储从属品牌
        sales_num_lst = []  # 存储月份销量
        sales_sum_lst = []  # 存储总销量
        self.driver.get(self.sales_url.format(num, year, month))
        # 定位排名
        top_num = self.driver.find_elements(by=By.CLASS_NAME, value='col1')
        for item in top_num:
            top_lst.append(item.text)

        # 定位车系
        brand_ele = self.driver.find_elements(by=By.CLASS_NAME, value='col2')
        for item in brand_ele:
            brand_lst.append(item.text)

        # 定位官方价
        price_ele = self.driver.find_elements(by=By.CLASS_NAME, value='col3')
        for item in price_ele:
            price_lst.append(item.text)

        # 定位从属品牌
        rel_brand_ele = self.driver.find_elements(by=By.CLASS_NAME, value='col4')
        for item in rel_brand_ele:
            rel_brand_lst.append(item.text)

        # 定位月份销量]
        sales_num_ele = self.driver.find_elements(by=By.CLASS_NAME, value='col5')
        for item in sales_num_ele:
            sales_num_lst.append(item.text)
        # 定位总销量
        sales_sum_ele = self.driver.find_elements(by=By.CLASS_NAME, value='col6')
        for item in sales_sum_ele:
            sales_sum_lst.append(item.text)

        # 使用zip函数进行打包
        for t, b, p, r, n, sn in zip(top_lst, brand_lst, price_lst, rel_brand_lst, sales_num_lst, sales_sum_lst):
            self.sales_car_top_lst.append([t, b, p, r, n, sn, type])

    def insert_data(self, sql, lst):
        db = pymysql.connect(host='127.0.0.1', user='root', password='root', database='pcauto')
        try:
            cursor = db.cursor()
            return cursor.executemany(sql, lst)
        except Exception as e:
            print(e)
        finally:
            db.commit()  # 提交
            db.close()

    def save(self, sql, lst):
        self.insert_data(sql, lst)

    def close(self):
        self.driver.quit()


if __name__ == '__main__':
    auto = PC_Auto()
    # 轿车
    auto.sales_car(1, 2022, 9, '轿车')
    #
    sql = 'insert into sales_car(top_id,brand,price,rel_brand,sales_num,sales_sum,type) values (%s,%s,%s,%s,%s,%s,%s)'
    auto.save(sql, auto.sales_car_top_lst)

    # SUV
    auto.sales_car(2, 2022, 9, 'SUV')
    sql = 'insert into sales_car(top_id,brand,price,rel_brand,sales_num,sales_sum,type) values (%s,%s,%s,%s,%s,%s,%s)'
    auto.save(sql, auto.sales_car_top_lst)

    # MPV
    auto.sales_car(3, 2022, 9, 'MPV')
    sql = 'insert into sales_car(top_id,brand,price,rel_brand,sales_num,sales_sum,type) values (%s,%s,%s,%s,%s,%s,%s)'
    auto.save(sql, auto.sales_car_top_lst)

    auto.close()
