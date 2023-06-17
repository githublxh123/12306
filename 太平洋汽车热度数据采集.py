from selenium import webdriver
from selenium.webdriver.common.by import By
import pymysql


class PC_Auto:
    driver = webdriver.Chrome()
    url = 'https://price.pcauto.com.cn/top/k{0}-p{1}.html'
    top_lst = []

    def top(self, num, page, type):
        self.driver.get(self.url.format(num, page))
        top_sub_lst = []  # 存储排行榜的序号
        sname_lst = []  # 存储名称
        red_price_lst = []  # 存储的是官方价
        top_mark_lst = []  # 存储热度
        brand_lst = []  # 存储品牌
        level_lst = []  # 存储级别
        displacement_lst = []  # 存储排量
        transmission_case = []  # 存储变速箱
        # 定位序号
        index = self.driver.find_elements(by=By.CLASS_NAME, value='index')
        for item in index:
            top_sub_lst.append(item.text)
        # 定位sname
        sname_ele = self.driver.find_elements(by=By.CLASS_NAME, value='sname')
        for item in sname_ele:
            sname_lst.append(item.text)
        # 定位其它元素
        col_ele = self.driver.find_elements(by=By.CLASS_NAME, value='col')
        for i in range(len(col_ele)):
            if i % 6 == 0:
                # 官方价
                red_price_lst.append(col_ele[i].text[4:])  # 官方价：9.98-17.49万  将官方价： 从字符串中切掉
            elif i % 6 == 1:  # 热度
                top_mark_lst.append(col_ele[i].text[:-2])  # 142608热度  将热度 从字符串中切掉
            elif i % 6 == 2:  # 品牌
                brand_lst.append(col_ele[i].text[3:])  # 品牌：日产  将品牌: 从字符串切掉
            elif i % 6 == 3:  # 级别
                level_lst.append(col_ele[i].text[3:])  # 级别：紧凑型车  把级别：从字符串切掉
            elif i % 6 == 4:  # 排量
                displacement_lst.append(col_ele[i].text[3:])  # 排量：1.2L 1.6L 1.8L 2.0L 把排量： 从字符串中切掉
            elif i % 6 == 5:  # 变速箱
                transmission_case.append(col_ele[i].text[4:])  # 变速箱：手动 自动 无级变速 固定齿比 将变速箱： 从字符串中切掉
        # 使用zip函数 进行打包
        # 序号，名称，价格，热度，品牌，级别，排量，变速箱
        for n, s, p, h, b, l, d, t in zip(top_sub_lst, sname_lst, red_price_lst, top_mark_lst, brand_lst, level_lst,
                                          displacement_lst, transmission_case):
            self.top_lst.append([n, s, p, h, b, l, d, t, type])

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
    for i in range(1, 3):
        auto.top(0, i, '轿车')  # 0表示的是轿车
    sql = 'insert into top_mark (index_id,sname,price,top_mark,brand,levels,displacement,transmission_case,type) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    auto.save(sql, auto.top_lst)

    # 爬取SUV 前2页数据
    for i in range(1, 3):
        auto.top(75, i, 'SUV')
    sql = 'insert into top_mark (index_id,sname,price,top_mark,brand,levels,displacement,transmission_case,type) values (%s,%s,%s,%s,%s,%s,%s,%s,%s)'
    auto.save(sql, auto.top_lst)

    auto.close()
