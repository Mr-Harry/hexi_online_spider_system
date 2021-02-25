# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/7/10
import datetime

import requests
import time
import hashlib
import random
import json
from urllib.parse import quote
from audio_tool import md5_use
from audio_tool import unit_result_clear_for_audio
from audio_tool import get_duration_str
import requests, pprint
from fake_useragent import UserAgent
from retrying import retry
from Audio_Infringement_Config import Config_of_audio_infringement as config

# 爬取喜马拉雅的音乐的类
class XiMaLaYa(object):

    def __init__(self):
        self.headers = {
            'authority': 'www.ximalaya.com',
            "user-agent": UserAgent().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
            'content-type': 'application/x-www-form-urlencoded;charset=UTF-8',
            'accept': '*/*',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://www.ximalaya.com/search/sound/%E6%88%91%E4%BB%AC%E4%B8%8D%E4%B8%80%E6%A0%B7/p1',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': '_xmLog=xm_kcfizftaiz1m66; s&e=e555bffcf1aa333ff08343f9c1402200; x_xmly_traffic=utm_source%253A%2526utm_medium%253A%2526utm_campaign%253A%2526utm_content%253A%2526utm_term%253A%2526utm_from%253A; device_id=xm_1594343550053_kcfizgitnj74za; Hm_lvt_4a7d8ec50cfd6af753c4f8aee3425070=1594343550; Hm_lpvt_4a7d8ec50cfd6af753c4f8aee3425070=1594344379; s&a=%1F^ZV%08%09%11%04%10Z%0E%02YTL%09%10[WTZT%11Z%1DZ[SXUKSV_ZOTUWROSCRUZMOK[_Z'
        }

    def getServerTime(self):
        """
        获取喜马拉雅服务器的时间戳
        :return:
        """
        # 这个地址就是返回服务器时间戳的接口
        serverTimeUrl = "https://www.ximalaya.com/revision/time"
        response = requests.get(serverTimeUrl,headers = self.headers)
        return response.text

    def getSign(self,serverTime):
        """
        生成 xm-sign
        规则是 md5(ximalaya-服务器时间戳)(100以内随机数)服务器时间戳(100以内随机数)现在时间戳
        :param serverTime:
        :return:
        """
        nowTime = str(round(time.time()*1000))

        # sign = str(hashlib.md5("ximalaya-{}".format(serverTime).encode()).hexdigest()) + "({})".format(str(round(random.random()*100))) + serverTime + "({})".format(str(round(random.random()*100))) + nowTime
        sign = str(hashlib.md5("himalaya-{}".format(serverTime).encode()).hexdigest()) + "({})".format(str(round(random.random()*100))) + serverTime + "({})".format(str(round(random.random()*100))) + nowTime
        # 将xm-sign添加到请求头中
        self.headers["xm-sign"] = sign
        # return sign

    # 统一请求响应函数
    def unify_requests(self,method="GET",url="",headers={},proxies={},data={}):
        if method=="GET":
            response = requests.get(url, headers=headers,proxies=proxies,data=data,timeout=5)
            return response

    def getInfos(self,albumId,pageNum,sort,pageSize):
        # 先调用该方法获取xm-sign
        self.getSign(self.getServerTime())
        # 将访问数据接口的参数写好
        params = {
            'albumId': albumId, # 页面id
            'pageNum': pageNum,
            'sort': sort,
            'pageSize':pageSize,# 一页有多少数据
        }
        # 喜马拉雅数据接口
        # url = "https://www.ximalaya.com/revision/play/album"
        url = "https://www.ximalaya.com/revision/search/main?kw=%E6%88%91%E4%BB%AC%E4%B8%8D%E4%B8%80%E6%A0%B7&page=1&spellchecker=true&condition=relation&rows=20&device=iPhone&core=track&fq=category_id%3A2&paidFilter=false"
        response = requests.get(url,headers=self.headers)
        # infos = json.loads(response.text)
        infos = response.text
        print(self.headers["xm-sign"])
        print(infos)
        return infos

    # 解析搜索的结果的函数
    def parms_search_songs(self,result):
        result = result.text
        info_dic = json.loads(result)
        result_list = []
        # print(type(info_dic))
        #
        if "data" in info_dic and "track" in info_dic["data"] and "docs" in info_dic["data"]["track"] and info_dic["data"]["track"]["docs"]:
            for each in info_dic["data"]["track"]["docs"]:
                if int(each["duration"])<350:
                    dic_ = {}
                    dic_["audio2_albumName"] = each["albumTitle"]
                    dic_["audio2_artistName"] = each["nickname"]
                    dic_["audio2_songName"] = each["title"]
                    dic_["audio2_songId"] = each["id"]
                    dic_["audio2_songtime"] = datetime.datetime.fromtimestamp(int(each["createdAt"]/1000)).strftime("%Y-%m-%d %H:%M:%S") # 时间
                    dic_["audio2_platform"] = "喜马拉雅"
                    dic_["audio2_duration_intsec"] = int(each["duration"]) # 音乐时长 2021 02 25 新加功能 秒
                    dic_["audio2_duration_strsec"] = get_duration_str(seconds=each["duration"]) # 音乐时长 2021 02 25 新加功能 格式化
                    dic_["audio2_albumid"] = each["albumId"]
                    # dic_["audio2_url"] = "https://www.ximalaya.com/yinyue/{album_id}/{song_id}".format(album_id=dic_["audio2_albumid"],song_id=dic_["audio2_songId"])
                    dic_["audio2_url"] = "https://www.ximalaya.com{trackUrl}".format(trackUrl=each["trackUrl"])
                    dic_["audio2_url_hash"] = md5_use(text=dic_["audio2_url"])
                    result_list.append(dic_)
        return result_list

    # 查找歌曲
    def search_songs(self, song_name='在希望的田野上', proxy={}, num=0,**kwargs):
        self.headers["referer"]="https://www.ximalaya.com/search/sound/{}/p1".format(quote(song_name))
        result_list = []
        _start = config["xi_ma_la_ya"]["start"]
        _end = config["xi_ma_la_ya"]["end"]

        if kwargs.get("page_num"):
            if config["xi_ma_la_ya"]["start_page"]==0:
                _start = kwargs.get("page_num")-1
                _end = kwargs.get("page_num")
            elif config["xi_ma_la_ya"]["start_page"]==1:
                _start = kwargs.get("page_num")
                _end = kwargs.get("page_num") + 1

        for page in range(_start,_end):
        # for page in range(config["xi_ma_la_ya"]["start"], config["xi_ma_la_ya"]["end"]):

            # url = "https://www.ximalaya.com/revision/search/main?kw={song_name}&page={page}&spellchecker=true&condition=relation&rows=20&device=iPhone&core=track&fq=category_id%3A2&paidFilter=false".format(song_name=quote(song_name),page=page)
            url = "https://www.ximalaya.com/revision/search/main?kw={song_name}&page={page}&spellchecker=true&condition=recent&rows=20&device=iPhone&core=track&fq=category_id%3A2&paidFilter=false".format(song_name=quote(song_name),page=page)

            # print(url)
            if proxy:
                self.getSign(self.getServerTime())

                result = self.unify_requests(url=url, headers=self.headers,proxies=proxy)
            else:
                self.getSign(self.getServerTime())

                result = self.unify_requests(url=url,headers=self.headers)
            # print(result)
            # self._dispose(result)
            # if "rgv587_flag" in result:
            #     print("虾米音乐未获取成功 重新尝试")
            #     if num<5:
            #         self.session = requests.Session()
            #         self.session.get(self.DOMAIN)
            #         return self.search_songs(song_name=song_name,proxy=proxy,num=num+1)
            #     else:
            #         print("尝试过多")
            #         return []
            for each in self.parms_search_songs(result):
                result_list.append(each)
        # print(result_list)
        return unit_result_clear_for_audio(result_list=result_list,**kwargs)
    def get_single(self):
        pass

search_songs = XiMaLaYa().search_songs
if __name__ == '__main__':
    ximalaya = XiMaLaYa()
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
        "search_key_words": "云与海",
        # "confirm_key_words": "Live",
        # "filter_key_words_list": "片花_穿帮_片头曲_片尾曲_预告_插曲_翻唱_翻唱_发布会_演唱_演奏_合唱_专访_合奏_打call_宣传_原唱_cover_原曲_片花_穿帮_音乐_主题歌_有声小说_片头_片尾",
        # "filter_key_words_list": "演员",

    }

    # print(wy.search_songs(song_name="丑八怪",proxy=proxies))
    info = search_songs(song_name=each["search_key_words"],proxy=proxies, **each)
    print(len(info))
    print(info)

    # ximalaya.search_songs(song_name="后来遇见他",proxy=proxies)
