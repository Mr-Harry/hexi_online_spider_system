# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/6/30
import random

from Crypto.Cipher import AES

import base64
import requests, pprint,json
from Audio_Infringement_Config import Config_of_audio_infringement as config
from audio_tool import md5_use
from audio_tool import unit_result_clear_for_audio
import requests, pprint
from fake_useragent import UserAgent
from hashlib import md5
from retrying import retry
class XiaMi:
    ua = UserAgent()
    DOMAIN = "https://www.xiami.com"

    # 各个API接口地址
    # 每日音乐推荐
    APIDailySongs = "/api/recommend/getDailySongs"
    # 排行榜音乐
    APIBillboardDetail = "/api/billboard/getBillboardDetail"
    # 所有排行榜
    APIBillboardALL = "/api/billboard/getBillboards"
    # 歌曲详情信息
    APISongDetails = "/api/song/getPlayInfo"
    # 搜索音乐接口
    APISearch = "/api/search/searchSongs"
    def __init__(self):
        self.session = requests.Session()
        self.headers = {
            "user-agent": self.ua.random,
            "Proxy-Tunnel": str(random.randint(1, 10000))
        }
        # self.headers = {
        #     "user-agent": self.ua.random,
        #     "Proxy-Tunnel": str(random.randint(1, 10000)),
        #     'authority': 'www.xiami.com',
        #     'accept': 'application/json, text/plain, */*',
        #     'xm-ua': '124#1rzqY0ntxG0xAjWOQ0I6s52l+UOvpMKE1VEG0r7ONfvprBhnKLClYhJAXyTppG62euV0QQJp1cMk0Ypf7Y48nSOgL5oF4i1wfsn33teS6WjUTGqg9EaClo7b7z4TR4wup9B6gwGDVsFHnOJdeaH7rz6OvsSPZv93FZZSMd2u/4u9fviATDi63VOZBI1lYXkI3pezj5z3YahFDVbQFUxRBsX1y98XQzbsFm/Jui33J4jVaIdnhjXvnU6yUVINSi8RR3/OrvJQEWnpLAoF0vWODhXYYUT/GECCVsw9oG3XYsCRSXdBpHqWs/bIau6xwshqoE+h1zysmjfElPnIMIo9znVNZtreRkkTc+PtQ33qJ9F3dzDiJwJ2e6eUO4HPYhdEESnVuvoNUCRjupcGe36i1o+7A2/TuLCucfPm2g7qqJBArgCqmRWRArUflV6Da82UVwdWhBHndfFp+aALa0M3kY1TTP1I5SnxdhvM3EpJP9PnWsfVW+a8GybrajAA6g2wI4K5uwjWFQ7c9hdEWEfxKJWTX7d/NZ2JlRGr1OxoaG13sJ9JmhnWzfhBeoznf/RhMIBqg76YBZJA7iLmCoQzYawufSehQpb1jPYY2DF6jXCDNnL/2rxQIehKJ9DK1suxXZN8GZCfOsV34ddAKQpN75ZG/FwugJUjw2/qzk2gVEllSn/PosQ5e2qYP+o65RaShwo/S3bv1kgqnrFsE+rmO4lV4iHZ4CWvg4iCT4SRRrVewAvZfmN9GGutdzv/iBCFhdCcMvQxryNJ9UCQDVO3TNuwnphima7SvVft7rAcQQx5oJ0YBcbp+rEhP0QzC1kkrgF9Cr4VMI3TBXdXmqtzF9hFrcnz4yb0IbsX/Wkn8kp3K1Mj2t+5z4PYUhcdcXXkQb4bVoN1zLSLRyN2ATgY72kn99HMovjg8l7cntPUEVR7Cn2ZlMsn6KvBIZYLlm9nHBodOllXgTSd7Z5ZlULJ4W4D7C9plmI4mfWZIqbBg5Sd1Z2ZlMXng7OBInYXbw/2m4+ZI8LLgTSd1n2elUX2g7vtIZ/plw/IU4cjIM/Cg/Md1ZIefRE8s16teC/LQmbDm4+egxI84oMYv/yEytt90mCiNViqoldEKOiS/ZONfZNDZmPxf0kFaXVgnmTbvi2jB4KP8AwAA1HsrS+CIUhxv0b5iVCgI51DqvAX3nqNUdvftFchokry+uBtazyd0O5sJq+/ZJxh+Mcz7Z2L9ObOKrq4dVsAkmr+Vsnmx1xIMyzNksGIGUUoRAIyukqBowTrpwJulVUb3QsFI/2oMbr9jeMtK6jxVuRpwlzW1ItdD6HolxB+KzBoj0Ws+Jac0kzE4Lz3xAoanVuLBO9k/1sRBhAMGIJeKBvdQH52sdUqdq8fBV3clPiwDRLmlKU1hvxxd2w5O4/rYv1+xigfkY/+Z2+ENwGc4lbtdIiE/1t4wSj/pjCcnWKifaoXSKc55lMZKZUEThcB2VqWyazVJkM2ZsAup2fByBF+h1e/tkCZzBB8N1LsiK+QrL3CGBDj3VT2DKK8YxbMOTu66JHa/xpO52jUD3qs2NPz9lT4zZo/0sEcfBGMtsl0Eg8ZTq5fpyfwwgTyprOhoMxNrSdGGkJbQzKjzhwW3hghs5vpgjjt3d9rZe9I9qFGO7uyrBdKjq/uRFH4KSn/MERswu3H+SUERHHSo7ulzSWAkplwg4wYg3xJVX/23C/gJ/pHHNC6m0US4pSLc3Z00tqUH92TU2+gaY9wJn7PqLa4Z7NF3jfEWdx5gvXRI/hruG/2nTVbbuQ6GuzxdBV/pEgz',
        #     'sec-fetch-site': 'same-origin',
        #     'sec-fetch-mode': 'cors',
        #     'sec-fetch-dest': 'empty',
        #     'referer': 'https://www.xiami.com/list?scene=search&type=song&query={%22searchKey%22:%22%E9%9A%90%E7%A7%98%E7%9A%84%E8%A7%92%E8%90%BD%22}',
        #     'accept-language': 'zh-CN,zh;q=0.9',
        #     'cookie': 'xmgid=79c4e607-e8d4-44e9-871d-e862e88dd477; _uab_collina=159304893104349314978015; cna=oCosF4OSbEQCAW/G557suopS; gid=159305496851764; _unsign_token=09b21385f4657aeea1b86162b9d5ade9; xm_sg_tk=0e91705153ea37a8ea0424ddae9faca9_1593668677581; xm_sg_tk.sig=NyZ_Ez35f1KDS56FpzBghFqGXcS7POF9VNWzX2fafxE; xm_traceid=0b01fa3e15936686775537312ebe0e; xm_oauth_state=f3c8bc2c5a497e8def0d57707ec7b498; _xm_umtoken=T92F023F6F624EA0FE4713DA070AE5C6DF7BDAF4B096269067E630FC972; _xm_cf_=Q8xp7nitXiIXPO2XT6_XIgkO; l=eBgc2C0gQd94NUVbKO5Z-urza77T2IOfGsPzaNbMiInca6TdZdZ4YNQDR1QModtjgt5VCetros38FRee57U3WxGLyz6zrexmzF96Ra5..; isg=BHV1LNpqR8kWYKN7mC7Ti5lnhPcv8ikEvRUuGvebCuw7zpHAv0AY1aEMGJJ4jkG8',
        # }

        self.session.get(self.DOMAIN)

    def _get_api_url(self, api):
        return self.DOMAIN + api

    # 获取每日推荐的30首歌曲
    def get_daily_songs(self):
        url = self._get_api_url(self.APIDailySongs)
        params = {
            "_s": self._get_params__s(self.APIDailySongs)
        }
        result = self.session.get(url=url, params=params).json()
        self._dispose(result)

    # 获取虾米音乐的音乐排行榜
    def get_billboard_song(self, billboard_id: int = 0):
        '''
        :param billboard_id: 各类型的排行榜
        :return: 排行榜音乐数据
        '''
        if not hasattr(self, "billboard_dict"):
            self._get_billboard_dict_map()

        assert hasattr(self, "billboard_dict"), "billboard_dict获取失败"
        pprint.pprint(self.billboard_dict)
        if billboard_id == 0:
            billboard_id = input("输入对应ID，获取排行榜信息")
        assert billboard_id in self.billboard_dict, "billboard_id错误"

        url = self._get_api_url(self.APIBillboardDetail)
        _q = '{\"billboardId\":\"%s\"}' % billboard_id
        params = {
            "_q": _q,
            "_s": self._get_params__s(self.APIBillboardDetail, _q)
        }
        result = self.session.get(url=url, params=params).json()
        self._dispose(result)

    # 生成一个排行榜对应的字典映射
    def _get_billboard_dict_map(self):
        billboard_dict = {}
        billboards_info = self.get_billboard_all()
        try:
            if billboards_info["code"] == "SUCCESS":
                xiamiBillboards_list = billboards_info["result"]["data"]["xiamiBillboards"]
                for xiamiBillboards in xiamiBillboards_list:
                    for xiamiBillboard in xiamiBillboards:
                        id = xiamiBillboard["billboardId"]
                        name = xiamiBillboard["name"]
                        billboard_dict[id] = name
                self.billboard_dict = billboard_dict
        except Exception:
            pass

    # 获取所有的排行榜信息
    def get_billboard_all(self):
        url = self._get_api_url(self.APIBillboardALL)
        params = {
            "_s": self._get_params__s(self.APIBillboardALL)
        }
        result = self.session.get(url=url, params=params).json()
        self._dispose(result)

    # 获取歌曲详情信息
    def get_song_details(self, *song_ids) -> dict:
        '''
        :param song_ids: 歌曲的id，可以为多个
        :return: 歌曲的详情信息
        '''
        assert len(song_ids) != 0, "参数不能为空"

        for song_id in song_ids:
            if not isinstance(song_id, int):
                raise Exception("每个参数必须为整型")

        url = self._get_api_url(self.APISongDetails)
        _q = "{\"songIds\":%s}" % list(song_ids)
        params = {
            "_q": _q,
            "_s": self._get_params__s(self.APISongDetails, _q)
        }
        result = self.session.get(url=url, params=params).json()
        return self._dispose(result)

    # 获取歌曲的下载地址
    def get_song_download_url(self, *song_ids):
        download_url_dict = {}
        song_details = self.get_song_details(*song_ids)
        songPlayInfos = song_details["result"]["data"]["songPlayInfos"]
        for songPlayInfo in songPlayInfos:
            song_download_url = songPlayInfo["playInfos"][0]["listenFile"] or songPlayInfo["playInfos"][1]["listenFile"]
            song_id = songPlayInfo["songId"]
            download_url_dict[song_id] = song_download_url

        print("歌曲下载地址为:", download_url_dict)

    # 处理爬虫获取到的数据，这里我就输出值
    def _dispose(self, data):
        pprint.pprint(data)
        return data

    # 获取加密字符串_s
    def _get_params__s(self, api: str, _q: str = "") -> str:
        '''
        :param api: URL的地址
        :param _q:  需要加密的参数
        :return: 加密字符串
        '''
        xm_sg_tk = self._get_xm_sg_tk()
        data = xm_sg_tk + "_xmMain_" + api + "_" + _q
        # print("data ",data)
        return md5(bytes(data, encoding="utf-8")).hexdigest()

    # 获取xm_sg_tk的值，用于对数据加密的参数
    def _get_xm_sg_tk(self) -> str:
        xm_sg_tk = self.session.cookies.get("xm_sg_tk", None)
        # xm_sg_tk = "0e91705153ea37a8ea0424ddae9faca9"
        assert xm_sg_tk is not None, "xm_sg_tk获取失败"
        return xm_sg_tk.split("_")[0]

    # 获取虾米搜索结果
    def _get_xm_serch(self,song_name='在希望的田野上',page=2):
        url = self._get_api_url(self.APISearch)
        _q = '{"key":"%s","pagingVO":{"page":%s,"pageSize":30}}'%(song_name,page)
        params = {
            "_q": _q,
            "_s": self._get_params__s(self.APISearch, _q)
        }
        # 测试
        # print(self._get_params__s(self.APISearch, _q)) # 打印   _s
        result = self.session.get(url=url, params=params).json()
        # print(result)
        # self._dispose(result)
        return result

    # 对搜索结果进行解析的函数
    def parms_search_songs(self,info):
        result_list =[]
        if "code" in info and info["code"] == "SUCCESS" and "result" in info and info["result"] and info["result"]["data"] and info["result"]["data"]["songs"]:
            for each in info["result"]["data"]["songs"]:

                if "S_OFF" not in each["bizTags"]: #
                    # print("S_OFF not in 在{}".format(each["bizTags"]))
                    dic_ = {}
                    dic_["audio2_albumName"] = each["albumName"]
                    dic_["audio2_artistName"] = each["singers"]
                    dic_["audio2_songName"] = each["songName"]
                    dic_["audio2_songId"] = each["songId"]
                    dic_["audio2_platform"] = "虾米音乐"
                    dic_["audio2_songStringId"] = each['songStringId'] # 字符形式的ID
                    dic_["audio2_url"] = "https://www.xiami.com/song/{}".format(dic_["audio2_songStringId"])
                    dic_["audio2_url_hash"] = md5_use(text=dic_["audio2_url"])

                    result_list.append(dic_)
                # else:
                #     print("S_OFF 在{}".format(each["bizTags"]))
        return result_list

    # 虾米 容易尝试失败 单独的一次请求
    @retry(stop_max_attempt_number=5,wait_fixed=600)
    def get_response_single(self,url,params,proxy={},num=0):
        if proxy:
            result = self.session.get(url=url, headers=self.headers,params=params,proxies=proxy).json()
        elif not proxy:
            result = self.session.get(url=url, headers=self.headers,params=params).json()
        if "rgv587_flag" in result:
            # print("虾米音乐未获取成功 重新尝试")
            if num < 5:
                self.session = requests.Session()
                self.session.get(self.DOMAIN)
                return self.get_response_single(url,params,proxy=proxy, num=num + 1)
            else:
                print(" 单个页面请求尝试过多")
                return []
        return result
    # 获取虾米搜索结果
    # @retry(stop_max_attempt_number=5,wait_fixed=600)
    def search_songs(self,song_name='在希望的田野上',proxy={},num=0,**kwargs):
        result_list = []
        _start = config["xiami_search_offset"]["start"]
        _end = config["xiami_search_offset"]["end"]

        if kwargs.get("page_num"):
            if config["xiami_search_offset"]["start_page"]==0:
                _start = kwargs.get("page_num")-1
                _end = kwargs.get("page_num")
            elif config["xiami_search_offset"]["start_page"]==1:
                _start = kwargs.get("page_num")
                _end = kwargs.get("page_num") + 1

        for page in range(_start,_end):

            url = self._get_api_url(self.APISearch)
            _q = '{"key":"%s","pagingVO":{"page":%s,"pageSize":30}}'%(song_name,page)
            params = {
                "_q": _q,
                "_s": self._get_params__s(self.APISearch, _q)
            }
            # 测试
            # print(self._get_params__s(self.APISearch, _q)) # 打印   _s
            if proxy:
                result = self.get_response_single(url=url,params=params,proxy=proxy)
            else:
                result = self.get_response_single(url=url,params=params)
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
            # print(result)
            for each in self.parms_search_songs(result):
                result_list.append(each)

        # print(result_list)
        return unit_result_clear_for_audio(result_list=result_list,**kwargs)
    def test(self):
            # self.get_daily_songs()
            # self._get_xm_sg_tk()
            # self.get_billboard_song(332)
            # self.get_billboard_all()
            # self.get_song_details(1813243760)
            # self.get_song_details(1806922983) # 测试 走在田野的路上
            # self.get_song_download_url(1813243760)
            self._get_xm_serch()
            pass
    def back_search_parms(self,name):
        url = self._get_api_url(self.APISearch)
        detail_info_list = []
        for page in range(config["wangyiyun_search_offset"]["start"],config["wangyiyun_search_offset"]["end"]):
            detail_info_dic = {}
            _q = '{"key":"%s","pagingVO":{"page":%s,"pageSize":30}}' % (name, page)
            params = {
                "_q": _q,
                "_s": self._get_params__s(self.APISearch, _q)
            }
            detail_info_dic['params'] = params
            detail_info_dic['headers'] = self.headers
            detail_info_dic['requir_way'] = "GET"
            detail_info_dic['url'] = self._get_api_url(self.APISearch)
            detail_info_list.append(detail_info_dic)
        # print(detail_info_list)
        return detail_info_list

search_songs = XiaMi().search_songs
if __name__ == '__main__':
    xm = XiaMi()
    xm.back_search_parms(name='路在何方')
    # xm.test()
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

    # print(xm.search_songs(song_name='演员',proxy=proxies))
    # print(xm.search_songs(song_name='七里香',proxy=proxies))