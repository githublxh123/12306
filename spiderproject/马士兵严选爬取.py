import requests
import pymysql


def get_requests(page):
    url = f'https://you-gateway.mashibing.com/mall/product/app/product/page?pageIndex={page}&length=20'
    resp = requests.get(url)
    return resp.json()


def parse(resp_data):
    lst = []
    records = resp_data.get('data').get('records')
    for item in records:
        lst.append([item.get('id'), item.get('name'), item.get('startingPrice')])
    return lst


def insert_data(sql, lst):
    db = pymysql.connect(host='127.0.0.1', user='root', password='lxh', database='msbyx')
    try:
        cursor = db.cursor()
        return cursor.executemany(sql, lst)
    except Exception as ex:
        print(ex)
    finally:
        db.commit()
        db.close()


if __name__ == '__main__':
    resp_data = get_requests(1)
    lst = parse(resp_data)
    # print(lst)
    # 数据的存储
    sql = 'insert into yanxuan values(%s,%s,%s)'
    # 调用存储数据的函数
    insert_data(sql, lst)
    print('程序结束，存储完毕!!!')
