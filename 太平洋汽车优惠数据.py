from selenium import webdriver
from selenium.webdriver.common.by import By
import pymysql


class PC_Auto:
    driver = webdriver.Chrome()
    url = 'https://price.pcauto.com.cn/market/r{0}/nb{1}/p{2}.html'  # 字符串格式化中的占位符
    lst = []  # 存储爬取的数据

    def price_info(self, num, brand, page):  # num表示是城市 brand车的品牌  page表示的是页码
        # 打开北京奔驰购车优惠 的网址
        self.driver.get(self.url.format(num, brand, page))
        # 定义列表
        title_lst = []  # 存储标题(品牌和型号)
        day_lst = []  # 存储剩余天数
        pro_lst = []  # 存储4S店的名称
        tel_lst = []  # 存储4S店的电话号码
        price_lst = []  # 存储售价

        # 定位标题
        txt_lst = self.driver.find_elements(by=By.CLASS_NAME, value='txt')
        for item in txt_lst:
            title_lst.append(item.text[0:len(item.text) - 5])  # 奔驰GLC 轿跑SUV(进口) 2023款 GLC 260 4MATIC 剩余7天 把剩余7天 切掉
            day_lst.append(item.text[-4:])  # 只要剩余的天数
        # 定位4S店的名称
        pro = self.driver.find_elements(by=By.CLASS_NAME, value='pro')
        for item in pro:
            pro_lst.append(item.text.split(' ')[1])
        # 定位tel电话
        tel = self.driver.find_elements(by=By.CLASS_NAME, value='tel')
        for item in tel:
            tel_lst.append(item.text.split(' ')[0])  # 400-819-8727 24H 售多市 进行劈分，结果是列表,索引为0的为电话号码
        # 定位的是售价
        price = self.driver.find_elements(by=By.CLASS_NAME, value='price-p')
        for item in price:
            price_lst.append(item.text)

        # 使用zip函数进行打包
        for t, d, p, tl, pri in zip(title_lst, day_lst, pro_lst, tel_lst, price_lst):
            self.lst.append([t, d, p, tl, pri])

    def insert_data(self, sql, lst):
        db = pymysql.connect(host='127.0.0.1', user='root', password='lxh', database='pcauto')
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
        auto.price_info(2, 4, i)
    sql = 'insert into pcautoprice(title,day,pro,phone,price) values(%s,%s,%s,%s,%s)'
    auto.save(sql, auto.lst)
    auto.close()
