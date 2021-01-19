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
# import requests
#
# url = "https://m.sm.cn/s?q={}&from=smor&safe=1&snum=6&by=next&layout=html&page={}"
#
# payload = {}
# headers = {
# 'User-Agent': UserAgent().random,
# "Proxy-Tunnel": str(random.randint(1, 10000)),
#   'authority': 'm.sm.cn',
#   'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
#   'x-requested-with': 'XMLHttpRequest',
#   'accept': '*/*',
#   'sec-fetch-site': 'same-origin',
#   'sec-fetch-mode': 'cors',
#   'sec-fetch-dest': 'empty',
#   'accept-language': 'zh-CN,zh;q=0.9',
#   'Cookie': 'sm_uuid=2656ccc1555849503ebb0f066f442569%7C%7C%7C1602471831; sm_diu=2656ccc1555849503ebb0f066f442569%7C%7C12ede2604d91d58512%7C1602471831; sm_sid=e2a706a2e8bda7e2e2788052886dfd52'
# }
#
# response = requests.request("GET", url, headers=headers, data = payload)
#
# print(response.text.encode('utf8'))
from engine_search_unit.engine_spider_tools import clear_admin_url, qinquan_list_url_clear
from engine_search_unit.shenma_engine_unit.shenma_tools import true_url, redirect_url


class ShenMaEngine:
    def __init__(self, use_proxy=True):
        self.proxy = get_proxy() if use_proxy else None
        self.headers = {
            'user-agent': UserAgent().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
            'authority': 'm.sm.cn',
            # 'user-agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 13_2_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/13.0.3 Mobile/15E148 Safari/604.1',
            'x-requested-with': 'XMLHttpRequest',
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'accept-language': 'zh-CN,zh;q=0.9',
            # 'Cookie': 'sm_uuid=2656ccc1555849503ebb0f066f442569%7C%7C%7C1602471831; sm_diu=2656ccc1555849503ebb0f066f442569%7C%7C12ede2604d91d58512%7C1602471831; sm_sid=e2a706a2e8bda7e2e2788052886dfd52'
            }

    # 搜索引擎搜索
    def search_engine(self, search_key: str, **kwargs):
        search_base_url = 'https://m.sm.cn/s?q={}&from=smor&safe=1&snum=6&by=next&layout=html&page={}'
        search_result = []
        if not search_key:
            return search_result
        _start = ENGINE_CONF["shenma_engine_offset"]["start_page"]
        if kwargs.get("page_num"):
            page = int(kwargs.get("page_num")) + ENGINE_CONF["shenma_engine_offset"]["start_page"] - 1
        else:
            page = _start
        # print(search_base_url.format(search_key, page))
        respose_search = unify_requests(url=search_base_url.format(search_key, page), headers=self.headers,
                                        proxies=self.proxy)
        # print(respose_search.text)
        for each in self.parse_search_engine(respose_search, **kwargs):
            search_result.append(each)
        return search_result


    # 搜索视频响应解析
    def parse_search_engine(self, response, **kwargs) -> list:
        try:
            # response.encoding = 'gb18030'
            response_data = etree.HTML(response.text)
            # print(response.text)
        except:
            return []
        else:
            result_list = []
            # engine_list_data = response_data.xpath('//div[@class="sc c-container"]')
            engine_list_data = response_data.xpath("//div[contains(@class,'sc') and contains(@class,'c-container')]")
            # print(len(engine_list_data))
            for n_l in engine_list_data:
                # title
                try:
                    title_data = n_l.xpath('./div[@class="c-header--v1_0_0 c-title c-flex"]')[0].xpath('./a/@href')
                except:
                    continue
                # print(etree.tostring(title_data[0]))
                if not len(title_data):
                    continue
                engine_dict = dict()
                engine_dict['qinquan_title'] = "".join(n_l.xpath('./div[@class="c-header--v1_0_0 c-title c-flex"]/a//span[@c-bind="data.text"]//text()')).replace('\u200b', '')  # 侵权标题
                engine_dict['qinquan_URL'] = "".join(title_data)  # 侵权链接
                engine_dict['qinquan_text'] = "".join(n_l.xpath('.//span[@class="js-c-paragraph-text"]//text()')).replace('\u200b', '')  # 侵权详情
                engine_dict['qinquan_platform'] = '神马搜索'
                if engine_dict['qinquan_URL']:
                    if 'zm.sm-tc.cn/?src=' in engine_dict['qinquan_URL']:
                        shenma_true_url = true_url(redirect_url(engine_dict['qinquan_URL']))
                        if 'zm.sm-tc.cn/back?src=' in shenma_true_url or (not shenma_true_url):
                            continue
                        else:
                            engine_dict['qinquan_URL'] = shenma_true_url
                            if not engine_dict['qinquan_URL']:
                                continue
                    result_list.append(engine_dict)
            return qinquan_list_url_clear(result_list)
            # return result_list


# 统一的调用 search_engines
search_engines = ShenMaEngine(use_proxy=True).search_engine
if __name__ == "__main__":
    # yangben_dict = {1
    #     'id': '10000',
    #     'yang_ben_author_str': '夏末蔷薇',
    #     'yang_ben_title_str': '爱',
    #     'yang_ben_url_str': 'https://t.shuqi.com/cover/6695029',
    #     'page_num': 2,
    #
    # }
    yangben_dict = {'id': 560002, 'engine_title': '风犬少年的天空',
                    'engine_url': 'https://www.bilibili.com/bangumi/play/ep340226',
                    'engine_author': '', 'engine_platform': '搜索引擎风犬少年1014测试3_45_5',
                    'engine_check_platform': '2', 'sub_table_name': 'sub_3_45', 'task_type': 5,
                    'page_num': 4, 'search_key_words': '风犬少年的天空'}
    result = search_engines('“雪龙2”号释放首个探空气球', **yangben_dict)
    # shuqi = ShuQiNovel(use_proxy=True)
    # result = shuqi.search_engine('爱', **yangben_dict)
    print(len(result))
    print(result)
