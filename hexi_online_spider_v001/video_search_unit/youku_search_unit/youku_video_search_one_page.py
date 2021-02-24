# -*- coding:utf-8 -*- #
# I don't like the world. I just like you
# author : pyl owo,
# time : 2020/7/30
import json
import re

import requests
from retrying import retry

from audio_tool import get_proxy, md5_use, unify_duration_format, unit_result_clear_for_video, str_to_datetime, \
    re_datetime_str
from video_search_unit.Video_Infringement_Config import config_of_video as config

class YouKu:
    def __init__(self, use_proxy=True):
        self.proxy = get_proxy() if use_proxy else None
        self.headers = {
            'authority': 'so.youku.com',
            'upgrade-insecure-requests': '1',
            'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36',
            'sec-fetch-dest': 'document',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'referer': 'https://so.youku.com/search_video/q_%E6%B5%B7%E8%B4%BC%E7%8E%8B',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            'cookie': '__wpkreporterwid_=21867722-2348-45f0-059e-c480a035bdc6; firstExpireTime=1596094577461; firstTimes=1; __ysuid=1574263464605Nue; cna=OSv+FsVwkWgCAbfG90GL3fXb; UM_distinctid=1738eb58f42791-0aea2fc11ea88a-317a055e-1fa400-1738eb58f43603; __aysid=15958271312197rU; modalFrequency={"UUID":"4","times":1,"firstTimeExpire":1596157990201}; youku_history_word=[%22%25E6%25B5%25B7%25E8%25B4%25BC%25E7%258E%258B%22%2C%22%25E9%2587%258D%25E5%2590%25AF%25E4%25B9%258B%25E6%259E%2581%25E6%25B5%25B7%25E5%2590%25AC%25E9%259B%25B7%2520%25E7%25AC%25AC%25E4%25B8%2580%25E5%25AD%25A3%22%2C%22%25E8%25A5%25BF%25E6%25B8%25B8%25E8%25AE%25B0%22%2C%22%25E8%25BF%2599%25EF%25BC%2581%25E5%25B0%25B1%25E6%2598%25AF%25E8%25A1%2597%25E8%2588%259E%2520%25E7%25AC%25AC%25E4%25B8%2589%25E5%25AD%25A3%22]; __ayft=1596087351741; __ayscnt=1; _m_h5_tk=bb1d7fd5b35e61fddee1909ad22cbc45_1596091313762; _m_h5_tk_enc=d719be51ad038e229759f09a8632d369; P_ck_ctl=77EB52F5046A0219C947951C97C334A7; ctoken=F-x_dbwId0Xx6V_GSdiY0Wh8; __arpvid=1596087399790YonC7C-1596087399873; __arycid=dh-1-00; __arcms=dh-1-00; __aypstp=3; __ayspstp=28; isg=BJeXu4a2hMxpiAB8ukl8NRMhJgLh3Gs-8xv66OnWNmb_GLxa867ljMdwergG90O2; _m_h5_tk=7eb62d6b9587397bf6168aa5cb44e931_1596016099938; _m_h5_tk_enc=0a4b5d949319841213f181a84a3691cb'
        }
        self.search_base_url = "https://so.youku.com/search_video/{}"
    def set_video_search_key(self, video_search_key: str):
        self.api_video_search_key = video_search_key
    # 单一请求
    @retry(stop_max_attempt_number=3, wait_fixed=10)
    def get_response_single(self, url):
        return requests.get(url, headers=self.headers, proxies=self.proxy)

    def search_video(self, search_key: str, **kwargs):
        search_result_temp = []
        if not search_key:
            return search_result_temp
        self.set_video_search_key(str(search_key))
        # 搜索页码search_page
        _start = config["youku_video_search_offset"]["start_page"]
        if kwargs.get("page_num"):
            search_page = int(kwargs.get("page_num")) + _start - 1
        else:
            search_page = _start

        # 搜索类别 search_type
        _type = config['video_search_type_default']
        video_search_type_list = [kwargs.get("search_type") if kwargs.get("search_type") else _type]

        #
        # 搜索时长 search_duration
        #

        search_url = self.search_base_url.format(search_key)
        # print(search_url)
        search_response = self.get_response_single(search_url)
        # print(video_search_type_list)
        return unit_result_clear_for_video(self.parse_search_video(search_response, video_search_type_list), **kwargs)

    # 搜索视频响应解析
    def parse_search_video(self, response,search_type_list=None) -> list:
        # print(search_type_list)
        try:
            html_json = re.search('window.__INITIAL_DATA__ =(.*)(});', response.text)
            json_data = html_json.group(1) + html_json.group(2)
            # print(json_data)
            response_dict = json.loads(json_data)
        except:
            return []
        else:
            result_list = []

            try:
                video_list_data = response_dict.get('data', {}).get('nodes', [])
                # print(json.dumps(video_list_data))
            except:
                video_list_data = []
            # for v_i in video_list_data[1:]:
            for j, v_i in enumerate(video_list_data):
                # print(v_i)
                #ju
                # data action  report trackInfo object_title/object_url
                # nodes []  nodes[]  data action report object_title /object_url
                if j == 0:
                    try:
                        video_info_dict_temp_list = v_i.get('nodes', [])[2].get('nodes', [])
                    except:
                        continue
                else:
                    try:
                        video_info_dict_temp_list = [v_i.get('nodes', [])[0].get('nodes', [])[0],]
                    except:
                        continue
                for video_info_dict_temp in video_info_dict_temp_list:
                    video_youku_type_int = video_info_dict_temp.get('type')
                    # print(video_youku_type_int)
                    video_info_dict = video_info_dict_temp.get('data', [])
                    # print(search_type_list)
                    if 0 in search_type_list:
                        pass
                    else:
                        if 1 in search_type_list:
                            if video_youku_type_int == 1005:
                                pass
                        else:
                            if video_youku_type_int == 1005:
                                continue
                        if 2 in search_type_list:
                            if video_youku_type_int == 1027 or video_youku_type_int == 1004:
                                pass
                        else:
                            if video_youku_type_int == 1027:
                                continue
                    video_dict = self.get_video_dict_by_json_info(video_info_dict, video_youku_type_int)
                    if not video_dict.get("video2_title"):
                        continue
                    if video_dict:
                        result_list.append(video_dict)
            return result_list

    def get_video_dict_by_json_info(self, video_info_dict, video_youku_type_int) -> dict:
        video_dict = dict()
        print(video_info_dict)
        video_base_url_id = video_info_dict.get('videoId', '')
        # print(video_base_url_id)
        video_base_url_id = video_info_dict.get('action', {}).get('report', {}).get('trackInfo', {}).get(
            'group_id') if not video_base_url_id else video_base_url_id
        if video_youku_type_int == 1005:
            video_dict["video2_url"] = "https://v.youku.com/v_show/id_" + str(video_base_url_id) + ".html"
        elif video_youku_type_int == 1027:
            video_dict["video2_url"] = "https://v.youku.com/v_nextstage/id_" + str(video_base_url_id) + ".html"
        elif video_youku_type_int == 1008:
            video_base_url_id = video_info_dict.get('action', {}).get('report', {}).get('trackInfo', {}).get(
                'tuid')
            video_dict["video2_url"] = "http://i.youku.com/u/" + str(video_base_url_id)
        else:
            video_dict["video2_url"] = "https://v.youku.com/v_show/id_" + str(video_base_url_id) + ".html"
        video_dict["video2_title"] = video_info_dict.get('action', {}).get('report', {}).get('trackInfo', {}).get(
            'object_title')
        video_dict["video2_author"] = video_info_dict.get('userName', '')
        if not self.check_video_title(video_dict.get("video2_title")):
            return {}

        video_dict["video2_url_hash"] = md5_use(video_dict.get("video2_url"))
        video_dict["video2_platform"] = "优酷"
        video_dict["video2_pubtime"] = re_datetime_str(str_to_datetime(video_info_dict.get('publishTime', '')))
        duration_str_temp = video_info_dict.get('screenShotDTO', {}).get('rightBottomText', '')
        duration, duration_str = unify_duration_format(duration_str_temp)
        video_dict["video2_duration"] = duration  # 时长（秒数）
        video_dict["video2_duration_str"] = duration_str  # 时长（字符串）

        return video_dict

    # 视频搜索结果通过标题模糊 %key% 筛除
    def check_video_title(self, need_check_title: str, search_title_key=""):
        return True
search_songs = YouKu().search_video
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
        "task_type": 6,
        "search_key_words": "班淑传奇",
        "confirm_key_words": "班淑传奇",
        "tvplay_task_list": [574942, 574945, 574948, 574951, 574954],
        "filter_key_words_list": "片花_穿帮_片头曲_片尾曲_预告_插曲_翻唱_翻唱_发布会_演唱_演奏_合唱_专访_合奏_打call_宣传_原唱_cover_原曲_片花_穿帮_音乐_主题歌_有声小说_片头_片尾",
    }
    youku = YouKu()
    import pprint
    result = youku.search_video("班淑传奇", **kwags)  # ,"3_4"
    pprint.pprint(result)
    print(len(result))