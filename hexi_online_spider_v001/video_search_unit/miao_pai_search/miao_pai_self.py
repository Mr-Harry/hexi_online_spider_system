# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/9/16
import datetime
import json
import random
import time
import uuid

import requests

from hashlib import md5
from urllib import parse
from urllib.parse import urlsplit
from urllib.parse import quote
from fake_useragent import UserAgent
from retrying import retry
from video_search_unit.Video_Infringement_Config import config_of_video as config

from audio_tool import get_proxy, md5_use, unify_duration_format, unit_result_clear_for_video


class MiaopaiVideo():
    # 时间戳
    current_ts = str(int(time.time()))
    # 伪造UUID，也叫做GUID(C#)
    fake_uuid = str(uuid.uuid1())
    # APP版本
    app_version = '7.2.60'

    # 搜索接口 key_words 搜索的关键词 默认3
    APISearch = "https://b-api.ins.miaopai.com/1/search/media.json?count=20&page={page}&key={key_words}"

    def __init__(self, use_proxy=True):
        self.proxy = get_proxy() if use_proxy else None

    ###################################
    def get_cpAbid(self):
        s1 = random.randint(1,19)
        s2 = random.randint(1,29)
        if random.randint(0,1):
            return '1-102,{}-100,2-1,{}-101,5-200,2-201'.format(s1,s2)
        else:
            return '1-102,{}-100,2-1,{}-101'.format(s1,s2)

    # md5 加密
    def get_md5(self, source):
        if isinstance(source, str):
            source = source.encode('utf-8')
        return md5(source).hexdigest()

    ###################################

    # 秒拍解密响应
    def _decode_resp_content(self,resp_content):
        """解密请求响应的数据
        :param resp_content: 请求响应的content"""

        def bytes_to_int(data, offset):
            result = 0
            for i in range(4):
                result |= (data[offset + i] & 0xff) << (8 * 1)
            return result

        def reverse_bytes(i):
            return ((i >> 24) & 0xFF) | ((i >> 8) & 0xFF00) | ((i << 8) & 0xFF0000) | (i << 24)

        if len(resp_content) <= 8:
            return ''
        dword0 = bytes_to_int(resp_content, 0)
        dword1 = bytes_to_int(resp_content, 4)
        x = 0
        if (dword0 ^ dword1) == -1936999725:
            x = reverse_bytes(dword1 ^ bytes_to_int(resp_content, 8))
        buffer_size = len(resp_content) - 12 - x
        if buffer_size <= 0:
            return ''
        else:
            buffer = bytearray()
            for index in range(buffer_size):
                buffer.append((resp_content[8 + index] ^ resp_content[12 + index]) & 0xff)
            return buffer.decode('utf8')

    # 获取响应
    def get_response(self,key_words:str="梁家辉",page:int=3,**kwargs):
      # url = "https://b-api.ins.miaopai.com/1/search/media.json?count=20&page=3&key=%E6%A2%81%E5%AE%B6%E8%BE%89"
      # url = "https://b-api.ins.miaopai.com/1/search/media.json?count=20&page=3&key={}".format(quote(key_words))
      url = self.APISearch.format(key_words=quote(key_words),page=page)
      # timestamp = int(datetime.datetime.now().timestamp())

      payload = {}
      # headers = {
      #   'cp-uniqueId': '8ac4508c-ca93-30ac-b310-61d9b4ea91a2',
      #   'cp-os': 'android',
      #   'cp_kid': '0',
      #   'cp-ver': '7.2.78',
      #   'cp-uuid': '8ac4508c-ca93-30ac-b310-61d9b4ea91a2',
      #   'cp-abid': '1-10,2-1',
      #   'cp-channel': 'xiaomi_market',
      #   'cp-time': '1600245983',
      #   'cp-sver': '9',
      #   # 'cp-sign': 'fd3a76b879d6182925add2c5182071de',
      #   'cp-vend': 'miaopai',
      #   'cp-appid': '424',
      #   'Host': 'b-api.ins.miaopai.com',
      #   'User-Agent': 'okhttp/3.3.1',
      #   'Cookie': 'acw_tc=7b39758516002460160502434e5c514791eb6d8c44782e71955cd0f42e2fad'
      # }
      headers = {
          "Accept-Encoding": "gzip",
          'User-Agent': 'okhttp/3.3.1',
          'Connection': 'Keep-Alive',
          "Host": 'b-api.ins.miaopai.com',
          'cp_ver': '7.2.60',
          'cp_appid': '424',
          'cp_sver': '5.1.1',
          'cp_channel': 'xiaomi_market',
          'cp_os': 'android',
          'cp_vend': 'miaopai',
      }

      # cp_uuid = uuid.uuid1().__str__()
      headers['cp_sign'] = self.get_cp_sign(url)
      # print(headers)
      headers['cp_time'] = str(self.current_ts)
      headers['cp_uuid'] = self.fake_uuid
      headers['cp_abid'] = self.get_cpAbid()
      headers['Cache-Control'] = 'no-cache'

      response = requests.get(url, headers=headers, data = payload,verify=False,proxies=self.proxy)

      # print(response.content)
      return response.content

    # 获取cp_sign参数值
    def get_cp_sign(self,target_url: str):
        sign_raw_str = 'url=' + parse.urlparse(target_url).path + \
                       'unique_id=' + self.fake_uuid + \
                       'version=' + self.app_version + \
                       'timestamp=' + self.current_ts + \
                       '4O230P1eeOixfktCk2B0K8d0PcjyPoBC'
        return md5((sign_raw_str.encode(encoding='utf-8'))).hexdigest()

    # 解析秒拍
    def get_parse(self,respose_text):
        # print(respose_text.replace("]}00","]}").replace("]}0","]}"))
        task_list = [] # 解析的结果集
        dic_info = json.loads(respose_text.replace("]}00","]}").replace("]}0","]}"))
        # dic_info = json.loads(respose_text.replace("]}0","]}"))
        # print(dic_info)
        if "result" in dic_info and dic_info["result"]:
            for each in dic_info["result"]:
                video_dict = {}
                video_dict["video2_title"] = each["description"]
                video_dict["video2_id"] = each["smid"]
                video_dict["video2_url"] = "http://n.miaopai.com/media/{}.html".format(each["smid"])
                video_dict["video2_author"] = each["user"]["nick"]
                video_dict["video2_url_hash"] = md5_use(video_dict.get("video2_url"))
                video_dict["video2_platform"] = "秒拍视频"
                video_dict["video2_pubtime"] = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(each.get('created_at', 0)))
                duration_str_temp = each.get('meta_data', [])[0].get('upload', {}).get('length', '') if each.get('meta_data', []) else ''
                duration, duration_str = unify_duration_format(duration_str_temp)
                video_dict["video2_duration"] = duration  # 时长（秒数）
                video_dict["video2_duration_str"] = duration_str  # 时长（字符串）
                task_list.append(video_dict)
            return task_list
    # 获取video的返回值
    def search_video(self,search_key: str,**kwargs):
        _start = config["video_search_offset"]["start"]
        _end = config["video_search_offset"]["end"]
        task_list = []
        if kwargs.get("page_num"):
            if config["video_search_offset"]["start_page"] == 0:
                _start = int(kwargs.get("page_num")) - 1
                _end = int(kwargs.get("page_num"))
            elif config["video_search_offset"]["start_page"] == 1:
                _start = int(kwargs.get("page_num"))
                _end = int(kwargs.get("page_num")) + 1

        for page in range(_start, _end):
            respose_text = self._decode_resp_content(self.get_response(key_words=search_key,page=page))
            # print(respose_text)
            for each in self.get_parse(respose_text):
                task_list.append(each)

        return unit_result_clear_for_video(task_list, **kwargs)
        # return task_list


search_songs = MiaopaiVideo(use_proxy=True).search_video

if __name__ == '__main__':
    # proxy = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    #     "host": config["proxyHost"],
    #     "port": config["proxyPort"],
    #     "user": config["proxyUser"],
    #     "pass": config["proxyPass"],
    # }
    # proxies = {
    #     "http": proxy,
    #     "https": proxy,
    # }
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
        # "confirm_key_words": "班淑传奇",
        # "filter_key_words_list": "片花_穿帮_片头曲_片尾曲_预告_插曲_翻唱_翻唱_发布会_演唱_演奏_合唱_专访_合奏_打call_宣传_原唱_cover_原曲_片花_穿帮_音乐_主题歌_有声小说_片头_片尾",
    }
    info = search_songs(search_key="周杰伦", **kwags)  # 1109 没数据就对了
    print(info)
    # print(quote("梁家辉"))
    # exit(0)
    # info = MiaopaiVideo(proxies=proxies).get_response(key_words="梁家辉")
    # info = MiaopaiVideo(proxies=proxies)._decode_resp_content(MiaopaiVideo(proxies=proxies).get_response(key_words="梁家辉",page=3))
    # print(info)
    # print(type(info))
    # print(type(json.loads(info.replace("]}00","]}"))))
    # print(type(json.loads(info[:-2])))
    # print(type(eval(info)))
    # import pprint
    # pprint.pprint(info)
    # pprint.pprint(json.loads(info))