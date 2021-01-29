# -*- coding:utf-8 -*-
# Chance favors the prepared mind.
# author : pyllowo,
# time : 2021/1/21


import json

from audio_search_unit.wangyiyun_search_unit.wangyiyun_app_base_all import song_search
from audio_tool import md5_use, get_proxy
from audio_tool import unit_result_clear_for_audio


class WangYiYunNew(object):
    def __init__(self):
        self.base_url = "https://y.music.163.com/m/song?id={}"

    # 解析搜索的结果的函数
    def parms_search_songs(self, result, **kwargs):
        result_list = []
        # print(result)
        data = result.get('result', {}).get('songs',[])
        if data:
            for each in data:
                dic_ = {}
                dic_["audio2_albumName"] = ""
                dic_["audio2_artistName"] = "|".join([i.get('name', '') for i in each.get('ar', [])]) if each.get('ar', []) else ''
                dic_["audio2_songName"] = each.get('name')
                dic_["audio2_songId"] = each.get('id')
                dic_["audio2_songtime"] = ""  # 时间
                dic_["audio2_platform"] = "网易云音乐App"
                dic_["audio2_albumid"] = ""
                if each.get('privilege', {}).get('st') != 0:
                    continue
                url = self.base_url.format(each.get('id', ''))
                dic_["audio2_url"] = url
                dic_["audio2_url_hash"] = md5_use(str(kwargs.get('id')) + "|" +dic_["audio2_url"])
                result_list.append(dic_)
        return result_list

    # 查找歌曲
    def search_songs(self, song_name='在希望的田野上', **kwargs):
        page_ = kwargs.get("page_num") if kwargs.get("page_num") else 1
        return unit_result_clear_for_audio(result_list=self.parms_search_songs(song_search(song_name, page_)), **kwargs)


search_songs = WangYiYunNew().search_songs
if __name__ == '__main__':
    new_wangyi = WangYiYunNew()
    each = json.loads('{"id": 8, "audio_title": "\\u542c\\u6211\\u8bf4\\u8c22\\u8c22\\u4f60", "audio_url": "https://hexi.music/0120/8", "audio_author": "\\u674e\\u6615\\u878d", "audio_album": "", "audio_platform": "QQ\\u97f3\\u4e500120\\u97f3\\u4e50\\u5e73\\u53f0\\u5341\\u4e94\\u6d4b\\u8bd51_109_2", "audio_check_platform": "4444", "task_type": 2, "page_num": 1, "search_key_words": "\\u542c\\u6211\\u8bf4\\u8c22\\u8c22\\u4f60", "sub_table_name": "sub_1_109"}')

    # print(wy.search_songs(song_name="丑八怪",proxy=proxies))
    info = search_songs(song_name='左右为难', **each)
    print(len(info))
    print(info)

    # ximalaya.search_songs(song_name="后来遇见他",proxy=proxies)