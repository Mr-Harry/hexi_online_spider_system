# -*- coding:utf-8 -*- #
# I don't like the world. I just like you
# author : pyl owo,
# time : 2020/7/14
import random
from urllib.parse import urlencode

from lxml import etree
import requests
from pip._vendor.retrying import retry
from Audio_Infringement_Config import config_of_video as config
from video_spider_tools import get_proxy, md5_use

class HuYaVideo:
    # 域名
    domain = "https://v.huya.com"
    api_video_search = "/index.php"
    api_video_search_key = ""
    api_video_search_params = {
        'r': "search/index",
        'w': "",  # 搜索关键字
        'type': "video",
        'p': 1,
    }

    def __init__(self, use_proxy=True):

        self.headers = {
            'user-agent': "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/83.0.4103.116 Safari/537.36",
            "Proxy-Tunnel": str(random.randint(1, 10000)),
        }
        self.yangben_dict = {}
        self.proxy = get_proxy() if use_proxy else None

    def set_video_search_key(self, video_search_key: str):
        self.api_video_search_key = video_search_key
        self.api_video_search_params['w'] = video_search_key

    def get_search_api_url(self, video_search_key="", page=1):
        if not video_search_key:
            video_search_key = self.api_video_search_key
        if not video_search_key:
            return
        self.api_video_search_params["p"] = page
        query_string = urlencode(self.api_video_search_params)
        return self.domain + self.api_video_search + '?' + query_string

    @retry(stop_max_attempt_number=3, wait_fixed=10)
    def search_songs(self, song_name=api_video_search_key, yangben_dict=None) -> list:
        self.yangben_dict = yangben_dict
        search_result_temp = []
        if not song_name:
            return search_result_temp
        self.set_video_search_key(str(song_name))
        page_setting = config.get("huya_video_search_offset")
        start_page = page_setting.get("start")
        end_page = page_setting.get("end")
        for i in range(start_page, end_page+1):
            search_url = self.get_search_api_url()
            # print(search_url)
            search_response = self.get_response_single(search_url, self.api_video_search_params)
            search_result_temp.append(self.parse_search_video_song(search_response))
        # print(search_url)
        return [j for i in search_result_temp for j in i]

    # 单一请求
    @retry(stop_max_attempt_number=3, wait_fixed=600)
    def get_response_single(self, url, params=None):
        if params is None:
            params = self.api_video_search_params
        return requests.get(url, headers=self.headers, params=params, proxies=self.proxy)

    # 搜索视频响应解析
    def parse_search_video_song(self, response) -> list:
        # print(response.text)
        # print(response.url)
        try:
            tree = etree.HTML(response.text)
        except:
            return []
        else:
            result_list = []
            try:
                video_song_list_data = tree.xpath("//ul[contains(@class,'vhy-video-list') and contains(@class,'w224') and "
                                              "contains(@class,'vhy-video-search-list')]")[0]
            except:
                video_song_list_data =[]
            for v_s in video_song_list_data:
                video_dict = dict()
                video_dict["video2_title"] = "".join(v_s.xpath(".//a[@class='video-wrap statpid']/@title"))
                if not self.check_video_title(video_dict.get("video2_title")):
                    continue
                video_dict["video2_url"] = "".join(v_s.xpath("./a/@href"))
                video_dict["video2_author"] = "".join(v_s.xpath(".//a[@class='video-meta-user']/@title"))
                # video_dict["video_author_zone"] = "".join(v_s.xpath(".//a[@class='video-meta-user']/@href"))
                video_dict["video2_pubtime"] = "".join(v_s.xpath(".//span[@class='video-meta-time']/text()"))
                video_dict["video2_url_hash"] = md5_use(video_dict.get("video2_url"))
                # 样本数据
                if self.yangben_dict and isinstance(self.yangben_dict, dict):
                    video_dict["video_title"] = self.yangben_dict.get("video_title")
                    video_dict["video_author"] = self.yangben_dict.get("video_author")
                    video_dict["video_url"] = self.yangben_dict.get("video_url")
                result_list.append(video_dict)
                # print(video_dict)

        return result_list

    # 视频搜索结果通过标题模糊 %key% 筛除
    def check_video_title(self, need_check_title: str, search_title_key=""):
        if not search_title_key:
            search_title_key = self.api_video_search_key
        return True if str(need_check_title).find(str(search_title_key)) >= 0 else False

search_songs = HuYaVideo(use_proxy=True).search_songs
if __name__ == '__main__':
    print(HuYaVideo().search_songs('老倒霉蛋了',yangben_dict={'video_url':'1111'}))
