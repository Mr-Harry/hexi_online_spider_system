# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/7/10
import requests
import time
import hashlib
import random
import json
from urllib.parse import quote
from audio_tool import md5_use
from audio_tool import unit_result_clear_for_audio
import requests, pprint
from fake_useragent import UserAgent
from retrying import retry
from Audio_Infringement_Config import Config_of_audio_infringement as config
requests.packages.urllib3.disable_warnings()
# 爬取喜马拉雅的音乐的类
class QingKa(object):

    def __init__(self):
        self.headers = {
            'Host': 'app.imqk.cn',
            'Content-Type': 'application/x-javascript; charset=UTF-8',
            "user-agent": UserAgent().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
            # 'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            # 'accept': '*/*',
            # 'sec-fetch-site': 'same-origin',
            # 'sec-fetch-mode': 'cors',
            # 'sec-fetch-dest': 'empty',
            # 'referer': 'https://www.ximalaya.com/search/sound/%E6%88%91%E4%BB%AC%E4%B8%8D%E4%B8%80%E6%A0%B7/p1',
            # 'accept-language': 'zh-CN,zh;q=0.9',
            # 'cookie': '_xmLog=xm_kcfizftaiz1m66; s&e=e555bffcf1aa333ff08343f9c1402200; x_xmly_traffic=utm_source%253A%2526utm_medium%253A%2526utm_campaign%253A%2526utm_content%253A%2526utm_term%253A%2526utm_from%253A; device_id=xm_1594343550053_kcfizgitnj74za; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1594343550; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1594344379; s&a=%1F^ZV%08%09%11%04%10Z%0E%02YTL%09%10[WTZT%11Z%1DZ[SXUKSV_ZOTUWROSCRUZMOK[_Z'
        }



    # 统一请求响应函数
    def unify_requests(self,method="GET",url="",headers={},proxies={},data={},verify=False,cookies={}):
        if method=="GET":
            response = requests.get(url, headers=headers,proxies=proxies,data=data,cookies=cookies,timeout=5)
            return response
        else:
            response = requests.post(url, headers=headers,proxies=proxies,data=data,verify=verify,cookies=cookies,timeout=5)
            return response


    # 解析搜索的结果的函数
    def parms_search_songs(self,result):
        result = result.text
        info_dic = json.loads(result)
        result_list = []
        # print(type(info_dic))
        # print((info_dic))
        #
        if "data" in info_dic and "program_list" in info_dic["data"] and info_dic["data"]["program_list"] :
            # print("here")
            for each in info_dic["data"]["program_list"]:
                if int(each["program_dur"])<600000:
                    dic_ = {}
                    dic_["audio2_albumName"] = ""
                    dic_["audio2_artistName"] = each["anchor_name"]
                    dic_["audio2_songName"] = each["program_name"]
                    dic_["audio2_songId"] = each["program_id"]
                    dic_["audio2_songtime"] = ""  # 时间
                    dic_["audio2_platform"] = "情咖FM"
                    dic_["audio2_albumid"] = each["anchor_uid"]
                    dic_["audio2_url"] = each["audio_url"]
                    dic_["audio2_url_hash"] = md5_use(text=dic_["audio2_url"])
                    result_list.append(dic_)
        return result_list

    # 查找歌曲
    def search_songs(self, song_name='在希望的田野上', proxy={}, num=0,**kwargs):
        self.headers["referer"]="https://www.ximalaya.com/search/sound/{}/p1".format(quote(song_name))
        result_list = []
        _start = config["qingka_search_offset"]["start"]
        _end = config["qingka_search_offset"]["end"]

        if kwargs.get("page_num"):
            if config["qingka_search_offset"]["start_page"]==0:
                _start = kwargs.get("page_num")-1
                _end = kwargs.get("page_num")
            elif config["qingka_search_offset"]["start_page"]==1:
                _start = kwargs.get("page_num")
                _end = kwargs.get("page_num") + 1

        for page in range(_start, _end):

            cookies = {
                'JSESSIONID': '65_-77137987026_38575794',
            }

            # headers = {
            #     'Content-Type': 'application/x-javascript; charset=UTF-8',
            #     'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 9; Redmi 8 MIUI/V10.3.6.0.PCNCNXM)',
            #     'Host': 'app.imqk.cn',
            # }

            # data = '{"version":{"pv":"0.0.4","cv":"2.3.2"},"ct":2,"did":"865055042835395__1594607435432","src_uid":38575794,"keyword":"%s","type":1,"page":%s}'%(str(song_name.encode()).strip('b').strip("'"),page)
            data = '{"version":{"pv":"0.0.4","cv":"2.3.2"},"ct":2,"did":"865055042835395__1594607435432","src_uid":38575794,"keyword":"%s","type":1,"page":%s}'%(json.dumps(song_name).strip('"'),page)
            # response = requests.post('https://app.imqk.cn/doc/record/search.json', headers=self.headers, cookies=cookies,
            #                          data=data, verify=False)
            # print(data)
            # print(response.text)
            url = 'https://app.imqk.cn/doc/record/search.json'
            # print(url)
            if proxy:

                result = self.unify_requests(url=url, headers=self.headers,proxies=proxy,method='POST',verify=False,data=data, cookies=cookies)
            else:

                result = self.unify_requests(url=url, headers=self.headers,proxies=proxy,method='POST',verify=False,data=data, cookies=cookies)
            for each in self.parms_search_songs(result):
                result_list.append(each)
        # print(result_list)
        return unit_result_clear_for_audio(result_list=result_list,**kwargs)
    def get_single(self):
        pass
search_songs = QingKa().search_songs
if __name__ == '__main__':
    qingka = QingKa()
    # print(ximalaya.getInfos('3544633','1','1','30'))
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
        "search_key_words": "七里香",
        # "confirm_key_words": "Live",
        # "filter_key_words_list": "片花_穿帮_片头曲_片尾曲_预告_插曲_翻唱_翻唱_发布会_演唱_演奏_合唱_专访_合奏_打call_宣传_原唱_cover_原曲_片花_穿帮_音乐_主题歌_有声小说_片头_片尾",
        # "filter_key_words_list": "演员",

    }

    # print(wy.search_songs(song_name="丑八怪",proxy=proxies))
    info = search_songs(song_name=each["search_key_words"],proxy=proxies, **each)
    print(len(info))
    print(info)

    # qingka.search_songs(song_name="告白气球",proxy=proxies)
