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
from audio_tool import get_proxy, md5_use, unify_duration_format, unit_result_clear_for_video


class QuanMinXiao_video_search_offset:

    def __init__(self, use_proxy=True):
        self.search_video_url = "https://quanmin.baidu.com/wise/growth/api/home/searchmorelist?rn=12&pn={1}&q={0}&type=search&_format=json"
        self.headers = {
            'user-agent': UserAgent().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
            'authority': 'quanmin.baidu.com',
            # 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://quanmin.baidu.com/query/%E6%88%91%E7%88%B1%E4%BD%A0',
            'accept-language': 'zh-CN,zh;q=0.9',
            # 'Cookie': 'BAIDUID=86BF4725C1255426485B0FC1C121091B:FG=1'
        }
        self.proxy = get_proxy() if use_proxy else None

    @retry(stop_max_attempt_number=3, wait_fixed=10)
    def search_songs(self, song_name = '', **kwargs) -> list:
        
        # 搜索页码search_page
        _start = config["quanminxiaoshipin_video_search_offset"]["start_page"]
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
            tree = json.loads(response.text)
        except:
            return []
        else:
            result_list = []
            try:
                video_song_list_data = tree.get('data', {}).get('list', {}).get('video_list', [])
            except:
                video_song_list_data =[]
            for v_s in video_song_list_data:
                video_dict = dict()
                video_dict["video2_title"] = v_s.get("title", '').replace('<i>', '').replace('</i>', '')
                if not self.check_video_title(video_dict.get("video2_title")):
                    continue
                video_dict["video2_url"] = v_s.get("url", '')
                video_dict["video2_author"] = v_s.get("author", {}).get('name', '')
                # video_dict["video_author_zone"] = "".join(v_s.xpath(".//a[@class='video-meta-user']/@href"))
                video_dict["video2_pubtime"] = ''
                video_dict["video2_url_hash"] = md5_use(video_dict.get("video2_url"))
                video_dict["video2_platform"] = "全民小视频"  # time_length
                duration_str_temp = v_s.get("time_length", '')
                duration, duration_str = unify_duration_format(duration_str_temp)
                video_dict["video2_duration"] = duration  # 时长（秒数）
                video_dict["video2_duration_str"] = duration_str  # 时长（字符串）
                result_list.append(video_dict)
                # print(video_dict)

        return result_list

    # 视频搜索结果通过标题模糊 %key% 筛除
    def check_video_title(self, need_check_title: str, search_title_key=""):
        return True

search_songs = QuanMinXiao_video_search_offset(use_proxy=True).search_songs
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
    print(QuanMinXiao_video_search_offset().search_songs('班淑传奇', **kwags))
