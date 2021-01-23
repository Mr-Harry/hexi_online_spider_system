# -*- coding:utf-8 -*-
# Chance favors the prepared mind.
# author : pyl owo,
# time : 2020/9/22

import json
import random

from fake_useragent import UserAgent
from lxml import etree

from audio_tool import get_proxy, unify_requests, md5_use, clear_text, str_similar, get_parms_value
from engine_search_unit.engine_spider_settings import ENGINE_CONF
from urllib.parse import quote

class BeiJinShiJian():
    def __init__(self, use_proxy=True):
        self.proxy = get_proxy() if use_proxy else None
        self.headers = {
            'User-Agent': UserAgent().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            'Cookie': '__guid=7bc8e28c-5d52-11eb-b263-6c92bf418e4a; z_api_request_time=0.036978006362915'
        }
        self.api_qin_quan_search_key = ''
        self.search_base_url = "https://pc.api.btime.com/search?callback=xyy&keyword={kw}&type=news&channel=search&device_id=3549c1f0ecad19e3c70f475ab1dc0b60&sort=score&recent=all&refresh=1&req_count=1&refresh_type=1&pid=3&from=&offset=0&page_refresh_id=&page={page}&_=1611390801058"
        self.qin_quan_info_url_pre = 'https://www.btime.com/', # 域名

    # 搜索侵权
    def search_qin_quan(self, search_key: str, **kwargs):
        _page = int(kwargs.get("page_num",1)) + ENGINE_CONF["beijinshijian_search_offset"]["start_page"] - 1 if int(kwargs.get("page_num",1)) else ENGINE_CONF["beijinshijian_search_offset"]["start_page"]
        # print(self.search_base_url.format(page=int(_page),kw=quote(search_key)))
        return self.parse_search_qin_quan(unify_requests(url=self.search_base_url.format(page=int(_page),kw=quote(search_key)), headers=self.headers, proxies=self.proxy), **kwargs)

    # 侵权详情 *
    def qin_quan_info(self, qin_quan_url):
        return unify_requests(url=qin_quan_url, headers=self.headers, proxies=self.proxy)

    # 搜索视频响应解析
    def parse_search_qin_quan(self, response, **kwargs) -> list:
        result_list = []

        try:
            info = response.text[4:-1]
            print(info)
            response_json = json.loads(info)
        except :
            return []
        if "data" in response_json:
            for each in response_json["data"]:
                qin_quan_title_str = each["data"]["title"].replace("</b>","").replace("<b>","")
                qin_quan_url_str = each["open_url"]
                qin_quan_abstract_str = ""
                engine_dict = dict()
                engine_dict['qinquan_platform'] = '北京时间'  # 侵权平台
                engine_dict['qinquan_title'] = qin_quan_title_str  # 侵权标题
                engine_dict['qinquan_URL'] = qin_quan_url_str # 侵权链接
                engine_dict['qinquan_text'] = qin_quan_abstract_str # 侵权详情
                # if qin_quan_abstract_str:
                result_list.append(engine_dict)
        return result_list

# 统一的调用 search_qin_quans
search_engines = BeiJinShiJian().search_qin_quan
if __name__ == "__main__":
    yangben_dict = {
        'id': '10000',
        # 'yang_ben_author_str': '伊藤伸平神乐坂淳',
        'yang_ben_title_str': '枪爷异闻录',
        'yang_ben_url_str': 'https://t.shuqi.com/cover/6695029',
        'page_num': 1,

    }
    result = search_engines('孙小果的“保护伞”判了！母亲20年，继父19年，还有17人获刑', **yangben_dict)
    # shuqi = ShuQiNovel(use_proxy=True)
    # result = shuqi.search_qin_quan('爱', **yangben_dict)
    print(len(result))
    print(result)
