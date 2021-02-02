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

class JinRICartoon:
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
            }
        self.api_qin_quan_search_key = ''
        self.search_base_url = "https://www.toutiao.com/api/search/content/?aid=24&app_name=web_search&offset={}&format=json&keyword={}&autoload=true&count=20&en_qc=1&cur_tab=1&from=search_tab&pd=synthesis"
        self.qin_quan_info_url_pre = "https://www.toutiao.com"

    # 搜索侵权
    def search_qin_quan(self, search_key: str, **kwargs):
        _page = int(kwargs.get("page_num",1)) + ENGINE_CONF["jinri_search_offset"]["start_page"] - 1 if int(kwargs.get("page_num",1)) else ENGINE_CONF["jinri_search_offset"]["start_page"]
        # print("xxxx",int(_page))
        # print("xxxx",int(_page)*20)
        return self.parse_search_qin_quan(unify_requests(url=self.search_base_url.format(int(_page)*20,quote(search_key)), headers=self.headers, proxies=self.proxy), **kwargs)

    # 侵权详情 *
    def qin_quan_info(self, qin_quan_url):
        return unify_requests(url=qin_quan_url, headers=self.headers, proxies=self.proxy)

    # 搜索视频响应解析
    def parse_search_qin_quan(self, response, **kwargs) -> list:
        # print(response.text)
        # print(response.url)
        result_list = []
        for q_l in response.json()["data"]:
            if "abstract" in q_l:
                # qin_quan_url_str = q_l.get("article_url","")  # 侵权链接 article_url
                qin_quan_url_str = "https://www.toutiao.com/a{}/".format(q_l.get("group_id",""))  # 侵权链接 article_url
                # qin_quan_author_str =  q_l.get("media_name", "") # 侵权作者
                qin_quan_title_str = q_l["title"].replace("</em>","").replace("<em>","") # 侵权标题
                qin_quan_abstract_str = q_l["abstract"].replace("</em>","").replace("<em>","")  # 侵权简介

                engine_dict = dict()
                engine_dict['qinquan_platform'] = '今日头条'  # 侵权平台
                engine_dict['qinquan_title'] = qin_quan_title_str  # 侵权标题
                engine_dict['qinquan_URL'] = qin_quan_url_str # 侵权链接
                engine_dict['qinquan_text'] = qin_quan_abstract_str # 侵权详情
                # if qin_quan_abstract_str:
                result_list.append(engine_dict)
        return result_list


# 统一的调用 search_qin_quans
search_engines = JinRICartoon().search_qin_quan
if __name__ == "__main__":
    yangben_dict = {
        'id': '10000',
        # 'yang_ben_author_str': '伊藤伸平神乐坂淳',
        'yang_ben_title_str': '枪爷异闻录',
        'yang_ben_url_str': 'https://t.shuqi.com/cover/6695029',
        'page_num': 1,

    }
    result = search_engines('19名“保护伞”获刑！孙小果案大量细节曝光 其母出镜忏悔：我这个母亲很失败', **yangben_dict)
    # shuqi = ShuQiNovel(use_proxy=True)
    # result = shuqi.search_qin_quan('爱', **yangben_dict)
    print(len(result))
    print(result)
