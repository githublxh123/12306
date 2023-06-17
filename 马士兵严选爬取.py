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


def save():
    pass


if __name__ == '__main__':
    resp_data = get_requests(1)
    lst = parse(resp_data)
    print(lst)
