# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/7/3
import random

from urllib import parse
import json
from Audio_Infringement_Config import Config_of_audio_infringement as config
from audio_tool import md5_use
from audio_tool import get_proxy
from audio_tool import unit_result_clear_for_audio
import requests, pprint
from fake_useragent import UserAgent
from retrying import retry
from lxml import etree
from audio_tool import clear_text
"song-item clearfix "
class QianQian:
    ua = UserAgent()
    DOMAIN = "http://music.taihe.com"

    # 各个API接口地址
    # 搜索音乐接口
    APISearch = "/search"

    def __init__(self, use_proxy=True):
        self.proxy = get_proxy() if use_proxy else None
        self.headers = {
            "user-agent": self.ua.random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
            'authority': 'music.taihe.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        }

    def _get_api_url(self, api):
        return self.DOMAIN + api

    # 对搜索结果进行解析的函数
    def parms_search_songs(self,info):
        result_list =[]
        select = etree.HTML(info.text)
        if select is not None:  # 如果有数据
            # print(etree.tostring(select).decode())
            search_div = select.xpath(
                "//li[@class='pr t clearfix']")
            # print(len(search_div))
            if search_div:
                for each in search_div:
                    dic_ = {}
                    dic_["audio2_songName"] = "".join(each.xpath("./div[@class='song ellipsis clearfix']/div/a/text()"))
                    dic_["audio2_artistName"] = "".join(each.xpath("./div[@class='artist ellipsis']/a/text()"))
                    dic_["audio2_albumName"] = "".join(each.xpath("./div[@class='album ellipsis']/a/text()"))
                    # print(dic_["audio2_songName"])
                    # dic_["audio2_songId"] = "".join(each.xpath("./div/span[@class='song-title']/a/@href")).replace(
                    #     '/song/',
                    #     '')
                    dic_["audio2_songId"] = "".join(each.xpath("./div[@class='song ellipsis clearfix']/div/a/@href")).replace('/song/', '')  # 字符形式的ID
                    dic_["audio2_platform"] = "千千音乐"
                    dic_["audio2_songStringId"] = "".join(each.xpath("./div[@class='song ellipsis clearfix']/div/a/@href")).replace('/song/', '')  # 字符形式的ID
                    dic_["audio2_url"] = "{}{}".format(self.DOMAIN, "".join(each.xpath("./div[@class='song ellipsis clearfix']/div/a/@href")))
                    dic_["audio2_url_hash"] = md5_use(text=dic_["audio2_url"])
                    result_list.append(dic_)
        else:
            print("没有数据 div")
            return []
        # print(result_list)
        return result_list

        # 单一请求
    @retry(stop_max_attempt_number=3, wait_fixed=10)
    def get_response_single(self, url):
        return requests.get(url, headers=self.headers, proxies=self.proxy)

    # @retry(stop_max_attempt_number=3,wait_fixed=600)
    # def get_response_single(self, url):
    #     return requests.get(url, headers=self.headers, proxies=self.proxy)

    # @retry(stop_max_attempt_number=3, wait_fixed=10)
    # def get_response_single(self, url):
    #     return requests.get(url, headers=self.headers, proxies=self.proxy)
    # 获取千千搜索结果
    @retry(stop_max_attempt_number=3,wait_fixed=600)
    def search_songs(self, song_name='在希望的田野上', **kwargs):
        if song_name:
            search_url = self._get_api_url(self.APISearch) + "?word=" + song_name
            # print(search_url)
        else:
            return []
        # if kwargs.get("page_num"):
        #     if config["qianqian_search_offset"]["start_page"]==0:
        #         _start = kwargs.get("page_num")-1
        #         _end = kwargs.get("page_num")
        #     elif config["qianqian_search_offset"]["start_page"]==1:
        #         _start = kwargs.get("page_num")
        #         _end = kwargs.get("page_num") + 1
        result = self.get_response_single(url=search_url)
        result_list = self.parms_search_songs(result)
        return unit_result_clear_for_audio(result_list=result_list,**kwargs)


search_songs = QianQian().search_songs
if __name__ == '__main__':
    proxy = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": config["proxyHost"],
        "port": config["proxyPort"],
        "user": config["proxyUser"],
        "pass": config["proxyPass"],
    }
    proxies = {
        "http": proxy,
        "https": proxy,
    }

    # qq = QianQian()
    # print(qq.search_songs(song_name="你好"))
    each = {
        "id": 165806,
        "audio_title": "丑八怪",
        "audio_url": "https://y.qq.com/n/yqq/song/001yus1q2xXSf0.html",
        "audio_author": "伦桑",
        "audio_album": "",
        "audio_platform": "8000任务新增九千",
        "audio_check_platform": "1_2_3",
        "sub_table_name": "sub_1_17",
        "task_type": 2,
        "page_num": 1,
        "search_key_words": "爱",
        # "confirm_key_words": "Live",
        # "filter_key_words_list": "片花_穿帮_片头曲_片尾曲_预告_插曲_翻唱_翻唱_发布会_演唱_演奏_合唱_专访_合奏_打call_宣传_原唱_cover_原曲_片花_穿帮_音乐_主题歌_有声小说_片头_片尾",
        # "filter_key_words_list": "演员",

    }

    # print(wy.search_songs(song_name="丑八怪",proxy=proxies))
    info = search_songs(song_name=each["search_key_words"],proxy=proxies, **each)
    print(len(info))
    print(info)

