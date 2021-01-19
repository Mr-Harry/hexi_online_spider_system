# -*- coding:utf-8 -*- #
# I don't like the world. I just like you
# author : pyl owo,
# time : 2020/7/14
import json
import random
from urllib.parse import urlencode

from fake_useragent import UserAgent
from lxml import etree
import requests
from pip._vendor.retrying import retry
from video_search_unit.Video_Infringement_Config import config_of_video as config
from audio_tool import get_proxy, md5_use, unit_result_clear_for_video, unify_duration_format

import requests


class MiGuVideo:

    def __init__(self, use_proxy=True):
        self.search_video_url = "https://jadeite.migu.cn/search/v3/open-search"
        self.headers = {
            'User-Agent': UserAgent().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'terminalId': 'WWW',
            'appId': 'miguvideo',
            # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'Content-Type': 'application/json',
            'Origin': 'https://www.miguvideo.com',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.miguvideo.com/',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        self.data = "{\"k\":\"%s\",\"pageIdx\":%s,\"contDisplayType\":\"\",\"pageSize\":10,\"packId\":\"1002581,1002601,1003861,1003862,1003863,1003864,1003865,1003866,1004041,1004121,1004261,1004262,1004281,1004321,1004262,1004281,1004322,1004261,1004421,1004422,1002781,1004301,1004641,1004761,1005061\",\"mediaSource\":\"9000001\",\"copyrightTerminal\":3,\"sid\":\"ICPU5QXGRN9M5JNULCC1N2MFR65UC946B3HAE2MC6SNVE9BF5QYGK04ACM84DLQD\",\"searchScene\":2,\"ct\":101}"

        self.proxy = get_proxy() if use_proxy else None

    @retry(stop_max_attempt_number=3, wait_fixed=10)
    def search_songs(self, song_name = '', **kwargs) -> list:
        
        # 搜索页码search_page
        _start = config["migu_video_search_offset"]["start_page"]
        if kwargs.get("page_num"):
            # print(1111)
            search_page = int(kwargs.get("page_num")) + _start - 1
        else:
            search_page = _start

        # 搜索类别 search_type
        _type = config['video_search_type_default']
        
        #
        # 搜索时长 search_duration
        #
        search_result_temp = []
        if not song_name:
            return search_result_temp
        search_url = self.search_video_url
        search_data = {'k': song_name, 'pageIdx': search_page, 'contDisplayType': '', 'pageSize': 10, 'packId': '1002581,1002601,1003861,1003862,1003863,1003864,1003865,1003866,1004041,1004121,1004261,1004262,1004281,1004321,1004262,1004281,1004322,1004261,1004421,1004422,1002781,1004301,1004641,1004761,1005061', 'mediaSource': '9000001', 'copyrightTerminal': 3, 'sid': 'ICPU5QXGRN9M5JNULCC1N2MFR65UC946B3HAE2MC6SNVE9BF5QYGK04ACM84DLQD', 'searchScene': 2, 'ct': 101}
        # print(search_data)
        search_response = self.get_response_single(search_url, data=json.dumps(search_data))
        search_result_temp.append(self.parse_search_video_song(search_response))
        # print(search_url)
        return unit_result_clear_for_video([j for i in search_result_temp for j in i])

    # 单一请求
    @retry(stop_max_attempt_number=3, wait_fixed=600)
    def get_response_single(self, url, data):
        return requests.post(url, headers=self.headers, data=data, proxies=self.proxy)

    # 搜索视频响应解析
    def parse_search_video_song(self, response) -> list:
        # print(response.text)
        # print(response.url)
        try:
            tree = json.loads(response.text)
            # print(tree)
            # exit(0)
        except:
            return []
        else:
            result_list = []
            try:
                # print(tree)
                video_song_list_data = tree.get('body', {}).get('shortMediaAssetList', [])
            except:
                video_song_list_data =[]
            for v_s in video_song_list_data:
                video_dict = dict()
                video_dict["video2_title"] = v_s.get("name", '')
                if not self.check_video_title(video_dict.get("video2_title")):
                    continue
                video_dict["video2_url"] = "https://www.miguvideo.com/mgs/website/prd/detail.html?cid=" + str(v_s.get("pID", ''))
                video_dict["video2_author"] = v_s.get("uploader", '')
                # video_dict["video_author_zone"] = "".join(v_s.xpath(".//a[@class='video-meta-user']/@href"))
                video_dict["video2_pubtime"] = v_s.get("publishTime", '')
                video_dict["video2_url_hash"] = md5_use(video_dict.get("video2_url"))
                video_dict["video2_platform"] = "咪咕视频"
                duration_str_temp = v_s.get('duration', '')
                duration, duration_str = unify_duration_format(duration_str_temp)
                video_dict["video2_duration"] = duration  # 时长（秒数）
                video_dict["video2_duration_str"] = duration_str  # 时长（字符串）
                result_list.append(video_dict)
                # print(video_dict)

        return result_list

    # 视频搜索结果通过标题模糊 %key% 筛除
    def check_video_title(self, need_check_title: str, search_title_key=""):
        return True

search_songs = MiGuVideo(use_proxy=True).search_songs
if __name__ == '__main__':
    print(MiGuVideo().search_songs('宝马5系舒服？那是你没把这车开透彻那是你没把这车开透彻', **{'video_url':'1111', 'page_num':2}))
