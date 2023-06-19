import pywasm
import time
import requests

# 忽略请求不安全的警告
import urllib3
from urllib3.exceptions import InsecureRequestWarning

urllib3.disable_warnings(InsecureRequestWarning)

base_url = 'https://spa14.scrape.center'
page = 10
runtime = pywasm.load('./Wasm.wasm')

for i in range(page):
    offset = i * 10
    sign = runtime.exec('encrypt', [offset, int(time.time())])
    url = f'{base_url}/api/movie/?limit=10&offset={offset}&sign={sign}'
    resp = requests.get(url, verify=False)

    print(resp.json())
