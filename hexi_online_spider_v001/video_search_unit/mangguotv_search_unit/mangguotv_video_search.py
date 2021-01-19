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


class MangGuoVideo:

    def __init__(self, use_proxy=True):
        self.search_video_url = "https://mobileso.bz.mgtv.com/pc/search/v1?q={}&pn={}&pc=10&du={}"
        self.headers = {
            'user-agent': UserAgent().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
            'authority': 'mobileso.bz.mgtv.com',
            # 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'accept': '*/*',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'no-cors',
            'sec-fetch-dest': 'script',
            'referer': 'https://so.mgtv.com/',
            'accept-language': 'zh-CN,zh;q=0.9',
            # 'cookie': '_source_=C; __STKUUID=63ffb86c-7321-4b40-8311-7ac6643e902f; PLANB_FREQUENCY=X4uteELxPBIZZG1t; MQGUID=1317658985314304000; __MQGUID=1317658985314304000; mba_deviceid=b80d741c-fb5d-ceaf-3152-8ffd65e24818; mba_sessionid=8de2f3b6-3b1c-930c-40ed-70a97d5c498c; mba_cxid_expiration=1603036800000; mba_cxid=8kpqp21m4cm; sessionid=1602989433876_8kpqp21m4cm; beta_timer=1602989433960; pc_v6=v6; mba_last_action_time=1602989478697; lastActionTime=1602989478713; historylist=%u98CE%u72AC%u5C11%u5E74%u7684%u5929%u7A7A%24hjgs%24%u6211%u7231%u4F60%u4E2D%u56FD%24hjgs%241%24hjgs%24'
        }
        self.proxy = get_proxy() if use_proxy else None

    @retry(stop_max_attempt_number=3, wait_fixed=10)
    def search_songs(self, song_name = '', **kwargs) -> list:
        
        # 搜索页码search_page
        _start = config["mangguotv_video_search_offset"]["start_page"]
        if kwargs.get("page_num"):
            # print(1111)
            search_page = int(kwargs.get("page_num")) + _start - 1
        else:
            search_page = _start

        # 搜索类别 search_type
        _type = config['video_search_type_default'] if not kwargs.get("search_type") else kwargs.get("search_type")
        # print(_type)
        # serial 电视剧oi 4
        # movie  电影 3
        # program 综艺
        #
        # 搜索时长 search_duration
        _duration = config['video_search_duration_default'] if not kwargs.get("search_duration") else kwargs.get("search_duration")
        #
        search_result_temp = []
        if not song_name:
            return search_result_temp
        # print(self.search_video_url.format(song_name, search_page, _duration))
        search_url = self.search_video_url.format(song_name, search_page, _duration)
        search_response = self.get_response_single(search_url)
        search_result_temp.append(self.parse_search_video_song(search_response,_type))
        # print(search_url)
        return unit_result_clear_for_video([j for i in search_result_temp for j in i], **kwargs)

    # 单一请求
    @retry(stop_max_attempt_number=3, wait_fixed=600)
    def get_response_single(self, url):
        return requests.get(url, headers=self.headers, proxies=self.proxy)

    def get_mongo_video_info(self, video_data: dict):
        info_dict = dict()
        info_dict['video2_title'] = video_data.get('title', '').replace('<B>', '')
        info_dict['video2_url'] = self.url_add_http(video_data.get('url', ''))
        info_dict['video2_author'] = ''
        info_dict['video2_pubtime'] = video_data.get('desc', [])[0].get('text') if len(video_data.get('desc', [])) > 0 else ''
        info_dict["video2_url_hash"] = md5_use(info_dict.get("video2_url"))
        info_dict['video2_platform'] = "芒果tv"
        duration_str_temp = video_data.get('updateInfo', '')
        duration, duration_str = unify_duration_format(duration_str_temp)
        info_dict["video2_duration"] = duration  # 时长（秒数）
        info_dict["video2_duration_str"] = duration_str  # 时长（字符串）
        return info_dict

    def get_mongo_movie_info(self, video_data: dict):
        info_dict = dict()
        info_dict['video2_title'] = video_data.get('title', '').replace('<B>', '')
        try:
            url = video_data.get('sourceList', [])[0].get('url')
        except:
            return {}
        else:
            if not url.startswith('http'):
                url = "https:" + url
            else:
                url = url
        info_dict['video2_url'] = url
        info_dict['video2_author'] = ''
        info_dict['video2_pubtime'] = video_data.get('desc', [])[1].get('text') if len(video_data.get('desc', [])) > 1 else ''
        info_dict["video2_url_hash"] = md5_use(info_dict.get("video2_url"))
        info_dict['video2_platform'] = "芒果tv"
        duration_str_temp = video_data.get('updateInfo', '')
        duration, duration_str = unify_duration_format(duration_str_temp)
        info_dict["video2_duration"] = duration  # 时长（秒数）
        info_dict["video2_duration_str"] = duration_str  # 时长（字符串）
        return info_dict
    def url_add_http(self, url: str):
        if not url.startswith('http'):
            url = "https:" + url
        else:
            url = url
        return url
    def get_mongo_program_info(self, video_data: dict):
        info_dict = dict()
        # print(video_data)
        data_list = video_data.get('yearList', [])[0] if len(video_data.get('yearList', [])) > 0 else {}
        info_dict['video2_title'] = data_list.get('title', '').replace('<B>', '')
        info_dict['video2_url'] = self.url_add_http(data_list.get('sourceList', [])[0].get('url') if len(data_list.get('sourceList', [])) > 0 else '')
        info_dict['video2_author'] = ''
        info_dict['video2_pubtime'] = ''
        info_dict["video2_url_hash"] = md5_use(info_dict.get("video2_url"))
        info_dict['video2_platform'] = "芒果tv"
        duration_str_temp = video_data.get('updateInfo', '')
        duration, duration_str = unify_duration_format(duration_str_temp)
        info_dict["video2_duration"] = duration  # 时长（秒数）
        info_dict["video2_duration_str"] = duration_str  # 时长（字符串）
        return info_dict
    def get_mongo_serial_info(self, video_data: dict):
        info_dict = dict()
        # print(video_data)
        info_dict['video2_title'] = video_data.get('title', '').replace('<B>', '')
        info_dict['video2_url'] = self.url_add_http(video_data.get('sourceList', [])[0].get('url') if len(video_data.get('sourceList', [])) > 0 else '')
        info_dict['video2_author'] = video_data.get('desc', [])[1].get('text') if len(video_data.get('desc', [])) > 1 else ''
        info_dict['video2_pubtime'] = video_data.get('playTime', '')
        info_dict["video2_url_hash"] = md5_use(info_dict.get("video2_url"))
        info_dict['video2_platform'] = "芒果tv"
        duration_str_temp = video_data.get('updateInfo', '')
        duration, duration_str = unify_duration_format(duration_str_temp)
        info_dict["video2_duration"] = duration  # 时长（秒数）
        info_dict["video2_duration_str"] = duration_str  # 时长（字符串）
        return info_dict
    # 搜索视频响应解析
    def parse_search_video_song(self, response, search_type=0) -> list:
        # print(response.text)
        # print(response.url)
        try:
            tree = json.loads(response.text)
        except:
            return []
        else:
            result_list = []
            try:
                video_song_list_data = tree.get('data', {}).get('contents', [])
            except:
                video_song_list_data =[]
            for v_s in video_song_list_data:
                if v_s.get('type', '') == 'video':
                    if search_type == 0 or search_type== 2:  # 2,  # 视频
                        result_list.append(self.get_mongo_video_info(v_s.get('data', {})))
                elif v_s.get('type', '') == 'movie':
                    if search_type == 0 or search_type == 3:  # 3,  # 电影
                        result_list.append(self.get_mongo_movie_info(v_s.get('data', {})))
                elif v_s.get('type', '') == 'serial':
                    if search_type == 0 or search_type == 4:  # 4,  # 电视剧
                        result_list.append(self.get_mongo_serial_info(v_s.get('data', {})))
                elif v_s.get('type', '') == 'program':
                    if search_type == 0 or search_type == 6:  # 6,  # 综艺
                        result_list.append(self.get_mongo_program_info(v_s.get('data', {})))
                else:
                    pass
        return result_list

    # 视频搜索结果通过标题模糊 %key% 筛除
    def check_video_title(self, need_check_title: str, search_title_key=""):
        return True

search_songs = MangGuoVideo(use_proxy=True).search_songs
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
    res = MangGuoVideo().search_songs('班淑传奇', **kwags)
    # res = MangGuoVideo().search_songs('风犬少年', **{'video_url':'1111', 'page_num':1, 'search_duration': 2})
    print(res)
    print(len(res))
