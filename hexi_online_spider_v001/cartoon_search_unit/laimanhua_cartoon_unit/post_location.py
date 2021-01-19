# Chance favors the prepared mind.
# author : pyl owo,
# time : 2020/12/16
# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/12/15

import requests
from urllib.parse import  unquote,quote
# 获得返回的location
def get_location(key_words:str):
    """
    :param
        key_words: 查询的关键词
    :return
        -1 错误的情况
        XXXXXXXX 正确返回字符
    """
    assert key_words!="", "key_words 不能为空！！！"
    headers = {
        'authority': 'www.laimanhua.com',
        'cache-control': 'max-age=0',
        'sec-ch-ua': '"Google Chrome";v="87", "\\"Not;A\\\\Brand";v="99", "Chromium";v="87"',
        'sec-ch-ua-mobile': '?0',
        'upgrade-insecure-requests': '1',
        'origin': 'https://www.laimanhua.com',
        'content-type': 'application/x-www-form-urlencoded',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.67 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.laimanhua.com/e/search/result/?searchid=294BDD90E1DDCB1C3796B4746F7B7BDA',
        'accept-language': 'zh-CN,zh;q=0.9',
        # 'cookie': 'UM_distinctid=17665396eae307-06a40582fe0968-18366153-1fa400-17665396eaf960; CNZZDATA1276171765=1680196636-1608012889-%7C1608022891; ASPSESSIONIDAGTARDTD=OCLEGPLDIDGIDEEHIMIIBJPF',
    }

    data = {
        # 'key': '{}'.format(quote(key_words.encode("gbk"))),
        'key': key_words.encode("gbk"),
        # 'button': '%CB%D1%CB%F7\uFFFD%FE%BB%AD'
        'button': '%CB%D1%CB%F7%C2%FE%BB%AD'
    }
    response = requests.post('https://www.laimanhua.com/e/search/', headers=headers, data=data, allow_redirects=False)
    # print(response.headers["Location"])
    if "Location" in response.headers and response.status_code==302 and "searchid" in response.headers["Location"]:
        return response.headers["Location"].split("searchid=")[-1]
    else:
        print("请检查get_location 状态码以及是否含有 Location")
        return -1
if __name__ == '__main__':
    info = get_location(key_words="我")
    print(info)