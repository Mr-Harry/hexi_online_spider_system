# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/11/29

import requests
import random

# 要访问的目标页面
targetUrl = "http://httpbin.org/get"

# 218.73.128.34&port=21001
proxy = "http://%(host)s:%(port)s" % {
    "host": "121.233.9.7",
    "port": "20067",
    # "user": Config_of_audio_infringement["proxyUser"],
    # "pass": Config_of_audio_infringement["proxyPass"],
}
proxies = {
    "http": proxy,
    "https": proxy,
}

#  设置IP切换头
tunnel = random.randint(1,10000)
headers = {
    "Proxy-Tunnel": str(tunnel), # MTZDR1ZKWEs6NDc2NzIw
    # "Proxy-Authorization": "Basic MTZDR1ZKWEs6NDc2NzIw",
           }



resp = requests.get(targetUrl, proxies=proxies, headers=headers)

print(resp.status_code)
print(resp.text)