# -*- coding:utf-8 -*-
# Chance favors the prepared mind.
# author : pyl owo,
# time : 2020/10/10


import json
import random
import re
from urllib import parse
from urllib.parse import urlencode

from fake_useragent import UserAgent
from lxml import etree

from audio_tool import unify_requests, get_proxy

from engine_search_unit.engine_spider_settings import ENGINE_CONF
from engine_search_unit.engine_spider_tools import qinquan_list_url_clear


class So360Engine:
    def __init__(self, use_proxy=True):
        self.proxy = get_proxy() if use_proxy else None
        self.headers = {
            'User-Agent': UserAgent().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'none',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            # 'Cookie': 'QiHooGUID=DECE32A2BDEF81F483AB805FBE654979.1602293543548; __guid=15484592.4355912534156993000.1602293543796.0598; webp=1; dpr=1; gtHuid=1; so_huid=11vY7wdOOVA1Ex5yDQdbhydMbtOL59LWUASCMV4uFbkgk%3D; __huid=11vY7wdOOVA1Ex5yDQdbhydMbtOL59LWUASCMV4uFbkgk%3D; erules=p1-17%7Cecr-2%7Cp2-16%7Cp4-8%7Cecl-1%7Cp3-2; _S=2vrvnug24ajflvrmpftt8gmi41; count=11'
        }

    # 搜索引擎搜索
    def search_engine(self, search_key: str, **kwargs):
        search_base_url = 'https://www.so.com/s?q={}&pn={}'
        search_result = []
        if not search_key:
            return search_result
        _start = ENGINE_CONF["so360_engine_offset"]["start_page"]
        if kwargs.get("page_num"):
            page = int(kwargs.get("page_num")) + ENGINE_CONF["so360_engine_offset"]["start_page"] - 1
        else:
            page = _start
        # print(search_base_url.format(search_key, page))
        respose_search = unify_requests(url=search_base_url.format(search_key, page), headers=self.headers,
                                        proxies=self.proxy)
        # print(respose_search.text)
        for each in self.parse_search_engine(respose_search, **kwargs):
            search_result.append(each)
        return search_result

    # 请求搜索出来的加密链接，从响应体中正则提取真实链接
    def parse_murl(self, url):
        if url and 'so.com/link' in url:
            try:
                r = unify_requests(url=url, proxies=get_proxy())
                href = re.search('<script>window.location.replace\("(.*?)"\)</script>', r.text, re.M | re.S).group(1)
            except Exception as e:
                try:
                    r = unify_requests(url=url, proxies=get_proxy())
                    href = re.search('<script>window.location.replace\("(.*?)"\)</script>', r.text, re.M | re.S).group(1)
                except Exception as e:
                    href = ''
        else:
            href = url
        return href
    # 搜索视频响应解析
    def parse_search_engine(self, response, **kwargs) -> list:
        try:
            # response.encoding = 'gb18030'
            response_data = etree.HTML(response.text)
            # print(response_dict)
        except:
            return []
        else:
            result_list = []
            engine_list_data = response_data.xpath('//ul[@class="result"]/li')
            # print(len(engine_list_data))
            for n_l in engine_list_data:
                qinquan_URL = "".join(n_l.xpath('./h3[@class="res-title"]/a/@href'))  # 侵权链接

                engine_dict = dict()
                engine_dict['qinquan_title'] = "".join(n_l.xpath('.//h3[@class="res-title"]/a//text()'))  # 侵权标题
                engine_dict['qinquan_URL'] = self.parse_murl(qinquan_URL)  # 侵权链接
                engine_dict['qinquan_text'] = "".join(n_l.xpath('./p[@class="res-desc"]//text()'))  # 侵权详情
                engine_dict['qinquan_platform'] = '360搜索'
                if engine_dict['qinquan_URL']:
                    result_list.append(engine_dict)
            # return result_list
            return qinquan_list_url_clear(result_list)


# 统一的调用 search_engines
search_engines = So360Engine(use_proxy=True).search_engine
if __name__ == "__main__":
    yangben_dict = {
        'id': '10000',
        'yang_ben_author_str': '夏末蔷薇',
        'yang_ben_title_str': '爱',
        'yang_ben_url_str': 'https://t.shuqi.com/cover/6695029',
        'page_num': 2,

    }
    result = search_engines('我', **yangben_dict)
    # shuqi = ShuQiNovel(use_proxy=True)
    # result = shuqi.search_engine('爱', **yangben_dict)
    print(len(result))
    print(result)
