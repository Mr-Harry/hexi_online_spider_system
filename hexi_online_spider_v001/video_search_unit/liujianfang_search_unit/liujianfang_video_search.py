# -*- coding:utf-8 -*- #
# I don't like the world. I just like you
# author : pyl owo,
# time : 2020/8/6
import json
import random

import requests
from fake_useragent import UserAgent
from lxml import etree
from retrying import retry

from audio_tool import get_proxy, unit_result_clear_for_video, md5_use, unify_duration_format
from video_search_unit.Video_Infringement_Config import config_of_video as config


class LiuJianFang:
    def __init__(self, use_proxy=True):
        self.proxy = get_proxy() if use_proxy else None
        self.headers =  {
            'user-agent': UserAgent().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
            'authority': 'v.6.cn',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            # 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'referer': 'https://v.6.cn/search.php?type=video&key=%E7%88%B1%E4%BD%A0&order=v&p=3',
            'accept-language': 'zh-CN,zh;q=0.9',
            # 'cookie': 'shrek_uuid=B5160550921008422; firVist=1605509211; _LiveGuestUser=1009988096%7C%E6%B8%B8%E5%AE%A23omi16; shrek_reft=0%7C160550925567092; shrek=B5160550921008422%7C160550925567092%7C0; _tracing=%2Fsearch.php-noname%7C%7C',
            'if-modified-since': 'Mon, 16 Nov 2020 07:17:46 GMT'
        }
        self.api_video_search_key = ''
        self.yangben_dict = {}
        self.search_video_url = "https://v.6.cn/search.php?type=video&key={}&order=v&p={}"  # 页码page从0开始

    def search_video(self, search_key: str, **kwargs):
        search_result = []
        if not search_key:
            return search_result
        self.api_video_search_key = str(search_key)
        # 搜索页码search_page
        _start = config["liujianfang_video_search_offset"]["start_page"]
        if kwargs.get("page_num"):
            # print(1111)
            search_page = int(kwargs.get("page_num")) + _start - 1
        else:
            search_page = _start

        # 搜索类别 search_type
        _type = config['video_search_type_default']
        search_result_temp = []
        if not search_key:
            return search_result_temp
        search_url = self.search_video_url.format(search_key, search_page)
        # print(search_url)
        search_response = self.get_response_single(search_url)
        search_result_temp.append(self.parse_search_video(search_response, **kwargs))
        # print(search_url)
        return unit_result_clear_for_video([j for i in search_result_temp for j in i], **kwargs)

    # 搜索视频响应解析
    def parse_search_video(self, response, **kwargs) -> list:
        try:
            response_dict = etree.HTML(response.text)
            # print(response_dict)
        except:
            return []
        else:
            result_list = []
            video_list_data = response_dict.xpath('//ul[@class="mmlist fix"]/li')
            for v_i in video_list_data:
                video_dict = dict()
                video_dict["video2_title"] = ''.join(v_i.xpath('./a/div[@class="info-box"]/p[@class="title"]/text()'))
                video_dict["video2_url"] = "https://v.6.cn/" + ''.join(v_i.xpath('./a/@href'))
                video_dict["video2_author"] = ''.join(v_i.xpath('./a/div[@class="info-box"]/p[@class="anchor"]/span[@class="alias"]/text()'))
                video_dict["video2_url_hash"] = md5_use(video_dict.get("video2_url"))
                video_dict["video2_platform"] = "六间房"
                duration_str_temp = ''.join(v_i.xpath('./a/i[@class="icon-time"]/text()'))
                # print(duration_str_temp)
                duration, duration_str = unify_duration_format(duration_str_temp)
                video_dict["video2_duration"] = duration  # 时长（秒数）
                video_dict["video2_duration_str"] = duration_str  # 时长（字符串）
                result_list.append(video_dict)
            return unit_result_clear_for_video(result_list, **kwargs)
    # 单一请求
    @retry(stop_max_attempt_number=3, wait_fixed=10)
    def get_response_single(self, url):
        return requests.get(url, headers=self.headers, proxies=self.proxy)

search_songs = LiuJianFang(use_proxy=True).search_video
if __name__ == "__main__":
    mifan = LiuJianFang(use_proxy=True)
    result = mifan.search_video('爱你')
    print(len(result))
    print(result)
