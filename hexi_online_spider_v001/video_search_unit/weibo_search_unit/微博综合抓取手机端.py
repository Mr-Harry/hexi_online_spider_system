# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/12/7

import requests

headers = {
    'Accept': 'application/json, text/plain, */*',
    'Referer': 'https://m.weibo.cn/search?containerid=100103type%3D1%26q%3D%E5%81%87%E5%A6%82%E7%88%B1%E6%9C%89%E5%A4%A9%E6%84%8F',
    'MWeibo-Pwa': '1',
    'X-XSRF-TOKEN': 'c1f863',
    'X-Requested-With': 'XMLHttpRequest',
    'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Mobile Safari/537.36',
}

params = (
    ('containerid', '100103type=1&q=\u5047\u5982\u7231\u6709\u5929\u610F'),
    ('page_type', 'searchall'),
    ('page', '2'),
)

response = requests.get('https://m.weibo.cn/api/container/getIndex', headers=headers, params=params)

