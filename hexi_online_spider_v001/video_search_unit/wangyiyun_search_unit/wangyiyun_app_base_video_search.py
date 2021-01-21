# -*- coding:utf-8 -*-
# Chance favors the prepared mind.
# author : pyllowo,
# time : 2021/1/21

import json
from video_search_unit.Video_Infringement_Config import config_of_video as config
from audio_tool import md5_use, unify_duration_format, unit_result_clear_for_video, get_proxy
from video_search_unit.wangyiyun_search_unit.wangyiyun_app_base_all import mp4_search


class WangYiYun():
    def __init__(self):
        self.base_url = 'https://st.music.163.com/mlog/mlog.html?id={}'

    # 对搜索结果进行解析的函数
    def parms_search_songs(self, info, **kwargs):
        result_list = []
        data = info.get("data", {}).get("resources", [])

        if data:
            for each in data:
                dic_ = {}
                base_info = each.get('baseInfo', {}).get('resource', {})
                dic_["video2_title"] = base_info.get('mlogBaseData', {}).get('text', '')
                dic_["video2_author"] = base_info.get('userProfile', {}).get('nickname', '') if base_info.get(
                    'userProfile', {}) else ''
                dic_["video2_url"] = self.base_url.format(each.get('baseInfo', {}).get('id')) if base_info.get('status', '') == 1 else self.base_url.format(each.get('baseInfo', {}).get('id')) + '#|lpy|'
                dic_["video2_pubtime"] = base_info.get('mlogBaseData', {}).get('pubTime', '')
                dic_["video2_url_hash"] = md5_use((str(kwargs.get('id')) + "|" + dic_.get("video2_url")))
                dic_["video2_platform"] = "网易云音乐app视频"
                duration_str_temp = base_info.get('mlogBaseData', {}).get('duration') // 1000
                duration, duration_str = unify_duration_format(duration_str_temp)
                dic_["video2_duration"] = duration  # 时长（秒数）
                dic_["video2_duration_str"] = duration_str  # 时长（字符串）
                result_list.append(dic_)
        return result_list

    # 搜索歌曲接口
    def search_songs(self, song_name="", **kwargs):
        page_ = kwargs.get("page_num") if kwargs.get("page_num") else 1
        return unit_result_clear_for_video(
            self.parms_search_songs(mp4_search(song_name, page_)), **kwargs)


search_songs = WangYiYun().search_songs
if __name__ == '__main__':
    wy = WangYiYun()
    kwags = json.loads('''
    {"id": 1, "video_title": "\\u71d5\\u65e0\\u6b47", "video_url": "https://hexi.music/0120/1", "video_author": "\\u848b\\u96ea\\u513f", "video_album": "", "video_platform": "QQ\\u97f3\\u4e500120\\u97f3\\u4e50\\u5e73\\u53f0\\u5341\\u4e94\\u6d4b\\u8bd51_110_1", "video_check_platform": "4444", "task_type": 1, "page_num": 1, "search_key_words": "\\u71d5\\u65e0\\u6b47", "sub_table_name": "sub_1_110"}

    ''')
    # print(wy.search_songs(song_name="丑八怪",proxy=proxies))
    res = wy.search_songs('七里香', **kwags)
    print(res)
    print(len(res))