# -*- coding:utf-8 -*- #
# I don't like the world. I just like you
# author : pyl owo,
# time : 2020/7/14
import random
from urllib.parse import urlencode

from fake_useragent import UserAgent
from lxml import etree
import requests
from pip._vendor.retrying import retry
from video_search_unit.Video_Infringement_Config import config_of_video as config
from audio_tool import get_proxy, md5_use, unify_duration_format, unit_result_clear_for_video, str_to_datetime, \
    re_datetime_str


class SoHuVideo:

    def __init__(self, use_proxy=True):
        self.search_video_url = "https://so.tv.sohu.com/mts?wd={}&c=0&v=0&length=0&limit=0&site=0&o=0&p={}&st=0&suged=&filter=0"
        self.headers = {
            'user-agent': UserAgent().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
            'authority': 'so.tv.sohu.com',
            'upgrade-insecure-requests': '1',
            # 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            # 'referer': 'https://so.tv.sohu.com/mts?wd=%E9%A3%8E%E7%8A%AC%E5%B0%91%E5%B9%B4&c=0&v=0&length=0&limit=0&site=0&o=0&p=2&st=0&suged=&filter=0',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': 'SUV=1601474004637bnjkbt; gidinf=x099980108ee1232af40c546f000fe8958a98e49b425; IPLOC=CN1101; Hm_lvt_082a80ccf2db99dbd7b5006fe0744b57=1602224414; newpuid=16022244144504801212; sokey=%5B%7B%22key%22%3A%22%E6%88%91%22%7D%5D; _muid_=1602558951457632; beans_freq=1; reqtype=pc; landingrefer=https%3A%2F%2Ffilm.sohu.com%2F; beans_dmp=%7B%2210191%22%3A1602224417%2C%22admaster%22%3A1602224416%2C%22shunfei%22%3A1602224416%2C%22reachmax%22%3A1602224416%2C%22lingji%22%3A1602224416%2C%22yoyi%22%3A1602224416%2C%22ipinyou%22%3A1602224416%2C%22ipinyou_admaster%22%3A1602224416%2C%22miaozhen%22%3A1602816444%2C%22diantong%22%3A1602224416%2C%22huayang%22%3A1602224416%2C%22precisionS%22%3A1602224417%7D; beans_dmp_done=1; iwt_uuid=68d78827-26e8-4b23-ac5a-b35ed553c078; t=1602816559524'
        }
        self.proxy = get_proxy() if use_proxy else None

    @retry(stop_max_attempt_number=3, wait_fixed=10)
    def search_songs(self, song_name = '', **kwargs) -> list:
        
        # 搜索页码search_page
        _start = config["souhu_video_search_offset"]["start_page"]
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
        search_url = self.search_video_url.format(song_name, search_page)
        search_response = self.get_response_single(search_url)
        search_result_temp.append(self.parse_search_video_song(search_response))
        # print(search_url)
        return unit_result_clear_for_video([j for i in search_result_temp for j in i], **kwargs)

    # 单一请求
    @retry(stop_max_attempt_number=3, wait_fixed=600)
    def get_response_single(self, url):
        return requests.get(url, headers=self.headers, proxies=self.proxy)

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
                video_song_list_data = tree.xpath("//ul[@class='list170 cfix']/li")
            except:
                video_song_list_data =[]
            for v_s in video_song_list_data:
                video_dict = dict()
                video_dict["video2_title"] = "".join(v_s.xpath("./strong/a//text()"))
                if not self.check_video_title(video_dict.get("video2_title")):
                    continue
                v2_url = "".join(v_s.xpath("./strong/a/@href"))
                video_dict["video2_url"] = v2_url if v2_url.startswith('https:') else "https:" + v2_url
                p_data = v_s.xpath("./p/a/text()")
                if not self.check_video_url(video_dict.get("video2_url")):
                    continue
                video_dict["video2_author"] = "".join(p_data[0]) if len(p_data) > 0 else ''
                # video_dict["video_author_zone"] = "".join(v_s.xpath(".//a[@class='video-meta-user']/@href"))
                video_dict["video2_pubtime"] = re_datetime_str(str_to_datetime("".join(p_data[1]) if len(p_data) > 1 else ''))
                video_dict["video2_pubtime2"] = "".join(p_data[1]) if len(p_data) > 1 else ''
                video_dict["video2_url_hash"] = md5_use(video_dict.get("video2_url"))
                video_dict["video2_platform"] = "搜狐视频"
                duration_str_temp = "".join(v_s.xpath(".//span[@class='maskTx']/text()"))
                duration, duration_str = unify_duration_format(duration_str_temp)
                video_dict["video2_duration"] = duration  # 时长（秒数）
                video_dict["video2_duration_str"] = duration_str  # 时长（字符串）
                result_list.append(video_dict)
                # print(video_dict)

        return result_list

    # 视频搜索结果通过标题模糊 %key% 筛除 tv.sohu.com/v/
    def check_video_title(self, need_check_title: str, search_title_key=""):
        return True
    def check_video_url(self, need_check_url: str):
        yao = ['tv.sohu.com/v/']
        for i in yao:
            if i in need_check_url:
                return True
            return False

search_songs = SoHuVideo(use_proxy=True).search_songs
if __name__ == '__main__':
    kwags = {
        "id": 574979,
        "video_title": "班淑传奇",
        "video_url": "https://v.youku.com/v_show/id_XMTM3MjQ5NjEzMg==.html?spm=a2h0c.8166622.PhoneSokuProgram_1.dselectbutton_1&showid=f2103904e95911e4b2ad#班淑传奇第38集",
        "video_author": "",
        "video_album": "",
        "video_platform": "优酷1030测试电视剧一部4_55_1",
        "video_check_platform": "2",
        "sub_table_name": "sub_4_55",
        "task_type": 1,
        "search_key_words": "班淑传奇",
        "confirm_key_words": "班淑传奇",
        "filter_key_words_list": "片花_穿帮_片头曲_片尾曲_预告_插曲_翻唱_翻唱_发布会_演唱_演奏_合唱_专访_合奏_打call_宣传_原唱_cover_原曲_片花_穿帮_音乐_主题歌_有声小说_片头_片尾",
    }
    x = SoHuVideo().search_songs('班淑传奇', **kwags)
    print(x)
    print(len(x))
