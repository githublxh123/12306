import hashlib
import time
import base64
import requests

INDEX_URL = "https://spa6.scrape.center/api/movie/?limit={}&offset={}&token={}"
LIMIT = 10
OFFSET = 0


def get_token(args):
    # * 在列表中加入当前的时间戳；
    timestamp = str(int(time.time()))
    args.append(timestamp)
    # * 将列表内容用逗号拼接；
    # * 将拼接的结果进行SHA1编码；
    sign = hashlib.sha1(",".join(args).encode("utf-8")).hexdigest()
    # * 将编码的结果和时间戳再次拼接；
    # * 将拼接后的结果进行Base64编码。
    return base64.b64encode(",".join([sign, timestamp]).encode("utf-8")).decode("utf-8")


if __name__ == '__main__':
    # * 将/api/movie放到一个列表里；
    args = ['/api/movie']
    token = get_token(args)
    for i in range(10):
        index_url = INDEX_URL.format(LIMIT, OFFSET + (i * 10), token)
        # print(index_url)
        response = requests.get(index_url)
        print(response.json())
