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


class SouGouEngine:
    def __init__(self, use_proxy=True):
        self.proxy = get_proxy() if use_proxy else None
        self.headers = {
            'User-Agent': UserAgent().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            # 'Referer': 'https://www.sogou.com/web?query=%E9%A3%8E%E7%8A%AC%E5%B0%91%E5%B9%B4&_ast=1602551614&_asf=www.sogou.com&w=01029901&p=40040100&dp=1&cid=&s_from=result_up&sut=10391&sst0=1602552055240&lkt=15%2C1602552046520%2C1602552047782&sugsuv=1602551603046857&sugtime=1602552055240',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            # 'Cookie': 'ABTEST=0|1602552710|v17; SNUID=B957A9A8D3D16550B5C6DFE7D4E4C6FA; IPLOC=CN1100; SUID=6D837A7B5E1CA00A000000005F850386; ld=Ykllllllll2KP5DClllllVMVxxtlllllWT$RbyllllYlllllRylll5@@@@@@@@@@'
            }

    # 搜索引擎搜索
    def search_engine(self, search_key: str, **kwargs):
        search_base_url = 'https://www.sogou.com/web?query={}&page={}'
        search_result = []
        if not search_key:
            return search_result
        _start = ENGINE_CONF["sougou_engine_offset"]["start_page"]
        if kwargs.get("page_num"):
            page = int(kwargs.get("page_num")) + ENGINE_CONF["sougou_engine_offset"]["start_page"] - 1
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
        if url and 'sogou.com/link' in url:
            try:
                r = unify_requests(url=url, proxies=get_proxy())
                href = re.search('window.location.replace\("(.*?)"\)</script>', r.text, re.M | re.S).group(1)
            except Exception as e:
                try:
                    r = unify_requests(url=url, proxies=get_proxy())
                    href = re.search('window.location.replace\("(.*?)"\)</script>', r.text, re.M | re.S).group(
                        1)
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
            try:
                engine_list_data = response_data.xpath('//div[@class="results"]')[0]
            except:
                return result_list
            # 带图片或多个行段的特殊行
            especial_list_data = engine_list_data.xpath('./div[@class="vrwrap"]')
            # 普通的行
            comon_list_data = engine_list_data.xpath('./div[@class="rb"]')
            # print(len(especial_list_data))
            # print(len(comon_list_data))
            for n_l in especial_list_data:
                qinquan_URL = "".join(n_l.xpath('./h3/a/@href'))  # 侵权链接
                if "sogou.com" not in qinquan_URL:
                    qinquan_URL = "https://www.sogou.com" + qinquan_URL
                engine_dict = dict()
                engine_dict['qinquan_title'] = "".join(n_l.xpath('./h3/a//text()')).replace('\r', '').replace('\n', '').replace(' ', '')  # 侵权标题
                engine_dict['qinquan_URL'] = self.parse_murl(qinquan_URL)  # 侵权链接
                if not engine_dict['qinquan_URL']:
                    continue
                engine_dict['qinquan_text'] = "".join(n_l.xpath('.//p[@class="str_info"]//text()')).replace('\r', '').replace('\n', '').replace(' ', '')  # 侵权详情
                engine_dict['qinquan_platform'] = '搜狗搜索'
                if engine_dict['qinquan_title'] and engine_dict['qinquan_URL'] != "https://www.sogou.com" and engine_dict['qinquan_URL'] != "https://www.sogou.comjavascript:void(0);":
                    result_list.append(engine_dict)
            for n_l in comon_list_data:
                qinquan_URL = "".join(n_l.xpath('./h3/a/@href'))  # 侵权链接
                if "sogou.com" not in qinquan_URL:
                    qinquan_URL = "https://www.sogou.com" + qinquan_URL

                engine_dict = dict()
                engine_dict['qinquan_title'] = "".join(n_l.xpath('./h3/a//text()')).replace('\r', '').replace('\n', '').replace(' ', '')  # 侵权标题
                engine_dict['qinquan_URL'] = self.parse_murl(qinquan_URL)  # 侵权链接
                engine_dict['qinquan_text'] = "".join(n_l.xpath('.//div[@class="ft"]//text()')).replace('\r', '').replace('\n', '').replace(' ', '')  # 侵权详情
                engine_dict['qinquan_platform'] = '搜狗搜索'
                if 'sogou.com/link?url' in engine_dict['qinquan_URL']:
                    continue
                if engine_dict['qinquan_title'] and engine_dict['qinquan_URL'] != "https://www.sogou.com" and engine_dict['qinquan_URL'] != "https://www.sogou.comjavascript:void(0);":
                    result_list.append(engine_dict)
            # return result_list
            return qinquan_list_url_clear(result_list)


# 统一的调用 search_engines
search_engines = SouGouEngine(use_proxy=True).search_engine
if __name__ == "__main__":
    yangben_dict = {
        'id': '10000',
        'yang_ben_author_str': '夏末蔷薇',
        'yang_ben_title_str': '爱',
        'yang_ben_url_str': 'https://t.shuqi.com/cover/6695029',
        'page_num': 1,
    }
    result = search_engines('爱', **yangben_dict)
    # shuqi = ShuQiNovel(use_proxy=True)
    # result = shuqi.search_engine('爱', **yangben_dict)
    print(len(result))
    print(result)
