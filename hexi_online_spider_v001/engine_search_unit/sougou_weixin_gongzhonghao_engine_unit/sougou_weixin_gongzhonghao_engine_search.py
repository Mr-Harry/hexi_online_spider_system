# -*- coding:utf-8 -*-
# Chance favors the prepared mind.
# author : pyl owo,
# time : 2020/10/23


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


class SouGouWeiXinEngine:
    def __init__(self, use_proxy=True):
        self.proxy = get_proxy() if use_proxy else None
        self.headers = {
            'User-Agent': UserAgent().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            # 'Referer': 'https://weixin.sogou.com/weixin?query=woaini&s_from=input&type=2&page=2&ie=utf8',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            # 'Cookie': 'IPLOC=CN1100; SUID=6D837A7B5E1CA00A000000005F850386; ld=kyllllllll2KP5DClllllVMVV8UlllllWT$RbylllltlllllRylll5@@@@@@@@@@; ABTEST=7|1603446573|v1; SNUID=360AF1F08C8E3ED8F3E449AA8CA04A94'
}

    # 搜索引擎搜索
    def search_engine(self, search_key: str, **kwargs):
        search_base_url = 'https://weixin.sogou.com/weixin?query={}&s_from=input&type=2&page={}&ie=utf8'
        search_result = []
        if not search_key:
            return search_result
        _start = ENGINE_CONF["sougou_weixin_gongzhonghao_engine_offset"]["start_page"]
        if kwargs.get("page_num"):
            page = int(kwargs.get("page_num")) + ENGINE_CONF["sougou_weixin_gongzhonghao_engine_offset"]["start_page"] - 1
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
    # def parse_murl(self, url):
    #     if url and 'weixin.sogou.com' in url:
    #         try:
    #             r = unify_requests(url=url, proxies=get_proxy())
    #             href = r.url
    #         except Exception as e:
    #             print(e)
    #             try:
    #                 r = unify_requests(url=url, proxies=get_proxy())
    #                 href = r.url
    #             except Exception as e:
    #                 print(e)
    #                 href = url
    #     else:
    #         href = url
    #     return href

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
            try:
                engine_list_data = response_data.xpath('//ul[@class="news-list"]/li')
                # print(len(engine_list_data))
            except:
                return result_list
            for n_l in engine_list_data:
                qinquan_URL = "https://weixin.sogou.com" + "".join(n_l.xpath('./div[@class="txt-box"]/h3/a/@href'))  # 侵权链接
                engine_dict = dict()
                engine_dict['qinquan_title'] = "".join(n_l.xpath('./div[@class="txt-box"]/h3/a//text()')).replace('\r', '').replace('\n', '').replace(' ', '')  # 侵权标题
                engine_dict['qinquan_author'] = "".join(n_l.xpath(".//div[contains(@class,'s-p')]/a/text()"))  # 侵权标题
                engine_dict['qinquan_URL'] = qinquan_URL  # 侵权链接
                # engine_dict['qinquan_URL'] = self.parse_murl(qinquan_URL)  # 侵权链接
                engine_dict['qinquan_text'] = "".join(n_l.xpath('.//p[@class="txt-info"]//text()')).replace('\r', '').replace('\n', '').replace(' ', '')  # 侵权详情
                engine_dict['qinquan_platform'] = '搜狗微信搜索'
                result_list.append(engine_dict)
            # return result_list
            return qinquan_list_url_clear(result_list)


# 统一的调用 search_engines
search_engines = SouGouWeiXinEngine(use_proxy=True).search_engine
if __name__ == "__main__":
    yangben_dict = {
        'id': '10000',
        'yang_ben_author_str': '夏末蔷薇',
        'yang_ben_title_str': '爱',
        'yang_ben_url_str': 'https://t.shuqi.com/cover/6695029',
        'page_num': 1,
    }
    result = search_engines('woaini', **yangben_dict)
    # shuqi = ShuQiNovel(use_proxy=True)
    # result = shuqi.search_engine('爱', **yangben_dict)
    print(len(result))
    print(result)
