# -*- coding:utf-8 -*- #
# I don't like the world. I just like you
# author : pyl owo,
# time : 2020/7/28
import json
import random
import re

import requests
from lxml import etree
from fake_useragent import UserAgent
from retrying import retry
from video_search_unit.Video_Infringement_Config import config_of_video as config
# 页码cur 从0开始
from video_search_unit.video_spider_tools import get_proxy, md5_use

movie_tvplay_api = "https://s.video.qq.com/load_poster_list_info?otype=json&cur={}&num=20&plat=2&pver=0&req_type=3&query={}&intention_id=3"

headers = {

    'authority': 's.video.qq.com',

    'user-agent': UserAgent().random,

    "Proxy-Tunnel": str(random.randint(1, 10000)),
    'sec-fetch-dest': 'script',
    'accept': '*/*',
    'sec-fetch-site': 'same-site',
    'sec-fetch-mode': 'no-cors',
    'referer': 'https://v.qq.com/x/search/',
    'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
  #'cookie': 'pgv_pvid=969648000; eas_sid=s4mukmzv9A5QS2SH6asWquje1b; tvfe_boss_uuid=b346701b91b6f761; video_guid=aaa9ba490c531ec5; video_platform=2; pgv_pvi=7859116032; RK=YvIdEmsGWe; ptcz=d495fa3fb79431c15d58a98c8233cd3a9f518a8964aa8f5863f267760f527d13; pgv_info=ssid=s6579512994'
}
#
# response = requests.request("GET", url, headers=headers, data = payload)
#
# print(response.text.encode('utf8'))

# 单一请求
@retry(stop_max_attempt_number=3, wait_fixed=10)
def get_response_single(url,proxy=None):
    return requests.get(url, headers=headers, proxies=proxy)

# 搜索视频响应解析
def parse_search_video(response, search_key='', yangben_dict=None) -> list:
    # print(response.text)
    try:
        response_json_str = re.match('QZOutputJson=(.*);',response.text).group(1)
        # print(response_json_str)
        response_data = json.loads(response_json_str, strict=False)
    except:
        return []
    else:
        # print(response_data)
        result_list = []
        video_list_data = response_data.get("PosterListMod", {}).get("posterList", [])
        # print(video_list_data)
        for v_i in video_list_data:
            # print(v_i)
            video_dict = dict()
            video_dict["video2_title"] = v_i.get('title', ' ').replace("\x05", '').replace("\x06", '')
            if not check_video_title(video_dict.get("video2_title"), search_key):
                continue
            video_dict["video2_url"] = v_i.get('url', '')
            # video_dict["video2_author"] = v_i.get('author', '')
            video_dict["video2_url_hash"] = md5_use(video_dict.get("video2_url"))
            video_dict["video2_platform"] = "腾讯视频"
            # 样本数据
            if yangben_dict and isinstance(yangben_dict, dict):
                video_dict["video_title"] = yangben_dict.get("video_title")
                video_dict["video_author"] = yangben_dict.get("video_author")
                video_dict["video_url"] = yangben_dict.get("video_url")
            # print(video_dict)
            result_list.append(video_dict)
        return result_list

def search_movie_tvplay_by_api(search_key: str, search_type_list=None,
                     start_page=config.get("tengxun_video_search_offset", {}).get("start", 1) - 1,
                     end_page=config.get("tengxun_video_search_offset", {}).get("end", 2) - 1,
                     yangben_dict=None, proxy=None):
    search_result_temp = []
    for i in range(start_page, end_page + 1):
        # print(movie_tvplay_api.format(i, search_key))
        search_response = get_response_single(url=movie_tvplay_api.format(i, search_key),proxy=proxy)
        search_result_temp.append(parse_search_video(search_response, search_key, yangben_dict))
    return [j for i in search_result_temp for j in i]
# 视频搜索结果通过标题模糊 %key% 筛除
def check_video_title(need_check_title: str, search_title_key=""):
    return True if str(need_check_title).find(str(search_title_key)) >= 0 else False


if __name__ == '__main__':
    print(search_movie_tvplay_by_api('西游记',proxy=get_proxy()))