# -*- coding:utf-8 -*-
# Chance favors the prepared mind.
# author : pyl owo,
# time : 2020/10/9

import json
import random
from urllib.parse import urlencode

import requests
from fake_useragent import UserAgent
from retrying import retry
from audio_tool import get_proxy, md5_use, unify_duration_format, unit_result_clear_for_video
from video_search_unit.Video_Infringement_Config import config_of_video as config


class BilibiliVideo:
    def __init__(self, use_proxy=True):
        self.proxy = get_proxy() if use_proxy else None
        self.headers = {
            'user-agent': UserAgent().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
            'authority': 'api.bilibili.com',
            'sec-fetch-dest': 'script',
            'accept': '*/*',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'no-cors',
            'referer': 'https://search.bilibili.com/video',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        }
        self.domain = "https://api.bilibili.com/"
        self.search_video_url = self.domain + "x/web-interface/search/type"
        self.yangben_dict = {}
        self.api_video_search_key = ""
        self.api_video_search_params = {}
        self.video_search_type_list = []

    def set_search_base_params(self):
        page_setting = config.get("bilibili_video_search_offset", {}).get("start", 1)
        self.api_video_search_params = {
            'keyword': "",  # 搜索关键字
            'search_type': "",  # video
            'page': page_setting,
            'highlight': 1,
            'duration':1, # 时长
            'tids': 3, # 音乐
            'single_column': 0,
            'changing': 'id',
            '__refresh__': 'true',
            '__reload__': 'false',
            'jsonp': 'jsonp',
        }

    def set_video_search_key(self, video_search_key: str):
        self.api_video_search_key = video_search_key
        self.api_video_search_params['keyword'] = video_search_key

    def set_search_params_page(self, page: int):
        self.api_video_search_params['page'] = page

    def set_search_params_start_page(self, start_page=config.get("bilibili_video_search_offset", {}).get("start", 1)):
        self.api_video_search_params['page'] = start_page

    def set_search_params_search_type(self, search_type: str):
        self.api_video_search_params['search_type'] = search_type

    def get_search_api_url(self):
        query_string = urlencode(self.api_video_search_params)
        return self.search_video_url + '?' + query_string

    # 单一请求
    @retry(stop_max_attempt_number=3, wait_fixed=10)
    def get_response_single(self, url):
        return requests.get(url, headers=self.headers, proxies=self.proxy)

    def get_bili_type_list(self, search_type):
        if not search_type:
            _bilibili_type_list = config['bilibili_search_parms_types'].values()
        elif search_type == 0:
            _bilibili_type_list = config['bilibili_search_parms_types'].values()
        elif search_type == 2:
            _bilibili_type_list = [config['bilibili_search_parms_types'].get(1)]
        # elif search_type == 3:
        #     _bilibili_type_list = [config['bilibili_search_parms_types'].get(2)]
        # elif search_type == 4:
        #     _bilibili_type_list = [config['bilibili_search_parms_types'].get(3)]
        else:
            _bilibili_type_list = config['bilibili_search_parms_types'].values()
        return _bilibili_type_list

    def search_video(self, search_key: str, **kwargs):
        if not search_key:
            return []
        # 搜索页码search_page
        _start = config["bilibili_video_search_offset"]["start_page"]
        if kwargs.get("page_num"):
            search_page = int(kwargs.get("page_num")) + _start - 1
        else:
            search_page = _start

        # 搜索类别 search_type
        _type = config['video_search_type_default']
        _bilibili_type_list = self.get_bili_type_list(kwargs.get("search_type"))

        #
        # 搜索时长 search_duration
        #

        search_result_temp = []
        if not search_key:
            return search_result_temp
        self.set_search_base_params()
        self.set_video_search_key(str(search_key))
        self.set_search_params_start_page(search_page)
        # #####
        # self.video_search_type_list = get_video_search_type_list("bilibili_video_search_type_list", video_search_type)
        # ####
        # page_setting = config.get("bilibili_video_search_offset")
        # start_page = page_setting.get("start", 1)
        # end_page = page_setting.get("end", 2)
        for b_t in _bilibili_type_list:
            self.set_search_params_search_type(b_t)
            search_url = self.get_search_api_url()
            # print(search_url)
            search_response = self.get_response_single(search_url)
            search_result_temp.append(self.parse_search_video(search_response))
        return unit_result_clear_for_video([j for i in search_result_temp for j in i], **kwargs)

    # 搜索视频响应解析
    def parse_search_video(self, response) -> list:
        try:
            response_dict = json.loads(response.text)
        except:
            return []
        else:
            result_list = []
            # print(response_dict.get('data', {}))
            video_list_data = response_dict.get('data', {}).get('result', []) if response_dict.get('data', {}) else []
            for v_i in video_list_data:
                video_dict = dict()
                video_dict["video2_title"] = v_i.get('title', ' ').replace('<em class="keyword">', '').replace('</em>',
                                                                                                               '').replace(
                    ' ', '')
                if not self.check_video_title(video_dict.get("video2_title")):
                    continue

                video_dict["video2_url"] = v_i.get('arcurl', '')
                if not video_dict["video2_url"]:
                    continue
                if 'bilibili.com' not in video_dict.get('video2_url'):
                    continue
                video_dict["video2_author"] = v_i.get('author', '')
                video_dict["video2_url_hash"] = md5_use(video_dict.get("video2_url"))
                video_dict["video2_platform"] = "哔哩哔哩"
                video_dict["video2_id"] = v_i.get('aid', '')
                duration_str_temp = v_i.get('duration', '')
                duration, duration_str = unify_duration_format(duration_str_temp)
                video_dict["video2_duration"] = duration  # 时长（秒数）
                video_dict["video2_duration_str"] = duration_str  # 时长（字符串）

                # 样本数据
                if self.yangben_dict and isinstance(self.yangben_dict, dict):
                    video_dict["video_title"] = self.yangben_dict.get("video_title")
                    video_dict["video_author"] = self.yangben_dict.get("video_author")
                    video_dict["video_url"] = self.yangben_dict.get("video_url")
                result_list.append(video_dict)
            return result_list

    # # 视频搜索结果通过标题模糊 %key% 筛除
    # def check_video_title(self, need_check_title: str, search_title_key=""):
    #     if not search_title_key:
    #         search_title_key = self.api_video_search_key
    #     return True if str(need_check_title).find(str(search_title_key)) >= 0 else False
    # 视频搜索结果通过标题模糊 %key% 筛除
    def check_video_title(self, need_check_title: str, search_title_key=""):
        return True


search_songs = BilibiliVideo(use_proxy=True).search_video

if __name__ == "__main__":
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
    bilibili = BilibiliVideo(use_proxy=True)
    result = bilibili.search_video('班淑传奇', **kwags)
    print(len(result))
    print(result)