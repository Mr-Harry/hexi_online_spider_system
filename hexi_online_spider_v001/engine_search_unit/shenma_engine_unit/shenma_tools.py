# -*- coding:utf-8 -*-
# Chance favors the prepared mind.
# author : pyl owo,
# time : 2021/1/9

import requests

from audio_tool import get_proxy

url = "https://zm.sm-tc.cn/back?src=l4uLj8XQ0JLRnIaQk9GckJLQnJCRi5qRi9DNz83P0s%2FO0M7O0JyQkYuakYugzsfMzc7GzMigzNGXi5I%3D&uid=64dfc0b72779d36a21b49093924d02a7&restype=1&from=derive&depth=2&link_type=60&wap=false&force=true&bu=ss_doc&v=1"
def true_url(url, if_proxy=True):
    proxy = get_proxy() if if_proxy else {}
    payload={}
    headers = {
      'authority': 'zm.sm-tc.cn',
      'upgrade-insecure-requests': '1',
      'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
      'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
      'sec-fetch-site': 'same-origin',
      'sec-fetch-mode': 'navigate',
      'sec-fetch-user': '?1',
      'sec-fetch-dest': 'document',
      'referer': 'https://zm.sm-tc.cn/?src=l4uLj8XQ0JLRnIaQk9GckJLQnJCRi5qRi9DNz83P0s%2FO0M7O0JyQkYuakYugzsfMzc7GzMigzNGXi5I%3D&uid=64dfc0b72779d36a21b49093924d02a7&hid=64dfc0b72779d36a21b49093924d02a7&pos=3&cid=9&time=1610179871636&from=click&restype=1&pagetype=0020800003008402&bu=ss_doc&query=%E2%80%9C%E9%9B%AA%E9%BE%992%E2%80%9D%E5%8F%B7%E9%87%8A%E6%94%BE%E9%A6%96%E4%B8%AA%E6%8E%A2%E7%A9%BA%E6%B0%94%E7%90%83&mode=&v=1&force=true&wap=false&province=%E6%B9%96%E5%8C%97%E7%9C%81&city=%E6%AD%A6%E6%B1%89%E5%B8%82&uc_param_str=dnntnwvepffrgibijbprsvdsdichei',
      'accept-language': 'en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
      'cookie': 'cna=bFrvFwgutSkCAXt6ge4H1U4Q; xlly_s=1; isg=BAIC-IYq6SSNfvX4JZKFMC9BUwFk0wbtho7g1UwbX3Ugn6EZNGdR_cCdT5Pjz36F'
    }
    try:
        response = requests.request("GET", url, headers=headers, data=payload, proxies=proxy)
    except:
        return ''
    else:
        return response.url


def redirect_url(url):
    return url.replace('zm.sm-tc.cn/?', 'zm.sm-tc.cn/back?')