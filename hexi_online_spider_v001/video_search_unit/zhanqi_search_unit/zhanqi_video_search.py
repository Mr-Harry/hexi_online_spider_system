# -*- coding:utf-8 -*- #
# I don't like the world. I just like you
# author : pyl owo,
# time : 2020/8/6
import json
import random

import requests
from fake_useragent import UserAgent
from retrying import retry

from audio_tool import get_proxy, unit_result_clear_for_video, md5_use, unify_duration_format
from video_search_unit.Video_Infringement_Config import config_of_video as config


class ZhanQiVideo:
    def __init__(self, use_proxy=True):
        self.proxy = get_proxy() if use_proxy else None
        self.headers =  {
            'authority': 'www.zhanqi.tv',
            'accept': 'application/json, text/javascript, */*; q=0.01',
            'user-agent': UserAgent().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
            # 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            # 'referer': 'https://www.zhanqi.tv/search?q=%E7%88%B1',
            'accept-language': 'zh-CN,zh;q=0.9',
            # 'cookie': 'PHPSESSID=6je84splkkbnps9rij1sil7dq3; gid=1828677448; cookie_ip=%2C2071626502; Hm_lvt_299cfc89fdba155674e083d478408f29=1605492516,1605509262; Hm_lpvt_299cfc89fdba155674e083d478408f29=1605509431'
}
        self.api_video_search_key = ''
        self.yangben_dict = {}
        self.search_video_url = "https://www.zhanqi.tv/api/zsearch/video?q={}&page={}&os=0&num=20"  # 页码page从0开始

    def search_video(self, search_key: str, **kwargs):
        search_result = []
        if not search_key:
            return search_result
        self.api_video_search_key = str(search_key)
        # 搜索页码search_page
        _start = config["leshi_video_search_offset"]["start_page"]
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
        # print(self.search_video_url)
        search_response = self.get_response_single(search_url)
        search_result_temp.append(self.parse_search_video(search_response))
        # print(search_url)
        return unit_result_clear_for_video([j for i in search_result_temp for j in i], **kwargs)

    # 搜索视频响应解析
    def parse_search_video(self, response) -> list:
        try:
            response_dict = json.loads(response.text)
            # print(response_dict)
        except:
            return []
        else:
            result_list = []
            video_list_data = response_dict.get('data', {}).get('videos', []) if response_dict.get('data',
                                                                                                  {}) else []
            for v_i in video_list_data:
                video_dict = dict()
                video_dict["video2_title"] = v_i.get('title', '').replace('<em>', '').replace('</em>', '')
                video_dict["video2_url"] = "https://www.zhanqi.tv" + str(v_i.get('videoUrl', ''))
                video_dict["video2_author"] = v_i.get('nickName', '')
                video_dict["video2_url_hash"] = md5_use(video_dict.get("video2_url"))
                video_dict["video2_platform"] = "战旗直播"
                duration_str_temp = v_i.get('duration', '')
                duration, duration_str = unify_duration_format(duration_str_temp)
                video_dict["video2_duration"] = duration  # 时长（秒数）
                video_dict["video2_duration_str"] = duration_str  # 时长（字符串）
                result_list.append(video_dict)
            return result_list
    # 单一请求
    @retry(stop_max_attempt_number=3, wait_fixed=10)
    def get_response_single(self, url):
        return requests.get(url, headers=self.headers, proxies=self.proxy)

search_songs = ZhanQiVideo(use_proxy=True).search_video
if __name__ == "__main__":
    mifan = ZhanQiVideo(use_proxy=True)
    result = mifan.search_video('好在 翻唱')
    print(len(result))
    print(result)
