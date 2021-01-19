# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/7/1
import asyncio
import random
import time
import aiohttp
import pymysql
import redis
from Crypto.Cipher import AES
import threading
import base64
import requests, pprint,json
from Audio_Infringement_Config import Config_of_audio_infringement as config
from Audio_Infringement_Config import Config_of_audio_infringement as proxies
from concurrent.futures import ThreadPoolExecutor, as_completed
from audio_tool import redis_get_tasks_from_redis, chang_ping_ying, md5_use, str_similar, judge_song_type_easy
from audio_tool import redis_check_set_already
from audio_tool import redis_check_key_exit
from audio_tool import timestamp_strftime
from audio_tool import mysql_save_to_current_result_table
from multiprocessing import Pool
import importlib
# mod = importlib.import_module('lib.test')
# __video_search_function__ = config["__video_search_function__"]

class audio_plarform_search():
    """
    :cvar

    """
    # 按需求获得对应的参数 音频
    __audio_search_function__ = config["__audio_search_function__"]
    # 视频抓取对应的参数
    __video_search_function__ = config["__video_search_function__"]
    # 图文抓取对应的参数
    __graphic_search_function__ = config["__graphic_search_function__"]
    # 小说取对应的参数
    __novel_search_function__ = config["__novel_search_function__"]
    # 搜索引擎取对应的参数
    __engine_search_function__ = config["__engine_search_function__"]

    __audio_setting__ = {
            "0":"all",

            '1':"xiami",
            '1_1':"xiami", # 虾米音乐搜索详情解析
            '1_2':"xiami", # 虾米音乐歌曲详情解析

            "2":"wangyiyun",
            "2_1":"wangyiyun", # 网易云音乐搜索详情解析
            "2_2":"wangyiyun", # 网易云音乐歌曲详情解析

            "3":"qianqian",
            "3_1":"qianqian",
            "3_2":"qianqian",

            "4": "ximalaya",
            "4_1": "ximalaya",
            "4_2": "ximalaya",

            "5": "qingka",
            "5_1": "qingka",
            "5_2": "qingka",
                    } # 查看对应的平台于数据库保持对应关系

    def __init__(self): # 本机最佳 任务7 进程4 线程3
        #  获取任务的条数
        self.task_numbers = config["task_numbers"]
        # 多进程主任务数量
        self.task_process = config["task_process"]
        # 多线程线程数量
        self.task_thread = config["task_thread"]
        # 代理
        self.proxy =  "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
                        "host": config["proxyHost"],
                        "port": config["proxyPort"],
                        "user": config["proxyUser"],
                        "pass": config["proxyPass"],
                    }
        self.proxies = {
            "http": self.proxy,
            "https": self.proxy,
        }
        self.params = ""

    # 2020 07 22修改 视频以及音频和图文
    # 按平台和对应的抓取平台来区分
    # 音频 __audio_search_function__
    # 视频 __video_search_function__
    # 图文 __news_search_function__
    # 添加 搜索关键词 以及 类型字段 区分任务类型和搜索关键词，（不能简单的使用标题进行搜索）
    # 同步抓取函数
    def get_search_response(self,each):
        # 音频
        if str(each["task_type"])=="2": # 音频
            task_list_audio = []  # 存储最后的结果 dict
            # print("音频")
            # print(each["audio_check_platform"]) # 打印对应的监测平台信息 0 all 1，2，。。。。
            if str(each["audio_check_platform"]) == "0":
                for e in audio_plarform_search().__audio_search_function__: # 对应不同函数 都实现相同的函数search_songs
                    # detail_info = audio_plarform_search().__audio_search_function__[e]().search_songs(
                    #     song_name=each["search_key_words"], proxy=self.proxies) #proxy=self.proxies
                    detail_info = importlib.import_module(audio_plarform_search().__audio_search_function__[e]).search_songs(
                        song_name=each["search_key_words"], proxy=self.proxies,**each)
                    search_audio_step = each.get("search_audio_step")
                    # 判断是否有步长 默认用配置文件里的
                    if search_audio_step:
                        for each_detail_dic in detail_info[:int(len(detail_info) * search_audio_step) + 1]:
                            # task_list.append(each_detail_dic)
                            task_list_audio.append(dict(each_detail_dic, **each))  # 合并字典

                    else:
                        for each_detail_dic in detail_info[:int(len(detail_info)*config["search_audio_step"])+1]:
                            # task_list.append(each_detail_dic)
                            task_list_audio.append(dict( each_detail_dic, **each )) # 合并字典
                # print(len(task_list))
            else:  # 按需求抓取
                for e in each["audio_check_platform"].split('_'):
                    # detail_info = audio_plarform_search().__audio_search_function__[e]().search_songs(
                    #     song_name=each["search_key_words"], proxy=self.proxies) #proxy=self.proxies
                    detail_info = importlib.import_module(audio_plarform_search().__audio_search_function__[e]).search_songs(
                        song_name=each["search_key_words"], proxy=self.proxies,**each)
                    # print(detail_info)
                    search_audio_step = each.get("search_audio_step")
                    # 判断是否有步长 默认用配置文件里的
                    if search_audio_step:
                        for each_detail_dic in detail_info[:int(len(detail_info) * search_audio_step) + 1]:
                            # task_list.append(each_detail_dic)
                            task_list_audio.append(dict(each_detail_dic, **each))  # 合并字典

                    else:
                        for each_detail_dic in detail_info[:int(len(detail_info)*config["search_audio_step"])+1]:
                            # task_list.append(each_detail_dic)
                            task_list_audio.append(dict( each_detail_dic, **each )) # 合并字典

            # print(task_list_audio)
            # print(len(task_list_audio))
            return  task_list_audio
        # 视频
        elif str(each["task_type"])=="1":
            task_list_video = []  # 存储最后的结果 dict
            # print("视频")
            # print(each["video_check_platform"]) # 打印对应的监测平台信息 0 all 1，2，。。。。
            # print(task_list_video)
            if str(each["video_check_platform"]) == "0":
                # print("xyyyyy")
                # task_list_video = []
                for e in audio_plarform_search().__video_search_function__: # 对应不同函数 都实现相同的函数search_songs

                    # print(len(task_list_video))
                    # detail_info = audio_plarform_search().__audio_search_function__[e]().search_songs(
                    #     song_name=each["search_key_words"], proxy=self.proxies) #proxy=self.proxies
                    detail_info = importlib.import_module(audio_plarform_search().__video_search_function__[e]).search_songs(
                        each["search_key_words"],**each)
                    # detail_info = list(detail_info)
                    # detail_info = [{'video2_title': '电影《最爱》中章子怡和郭富城的这一段 精彩', 'video2_url': 'https://v.qq.com/x/page/x0930woiryx.html', 'video2_author': '', 'video2_url_hash': '74fc942912844d86209e33dc7ebe0103'}, {'video2_title': '章子怡和郭富城的《最爱》片段，简直是太刺激了，不愧是实力演员', 'video2_url': 'https://v.qq.com/x/page/g0704fjs8ty.html', 'video2_author': '', 'video2_url_hash': '8f5eb480347fd36145cbed246db67735'}, {'video2_title': '电影最爱中郭富城和章子怡最突显演技的一段', 'video2_url': 'https://v.qq.com/x/page/g06077tgojz.html', 'video2_author': '', 'video2_url_hash': '227c718d71e27ea1f80e82fdd1f9401c'}, {'video2_title': '最爱：如果说章子怡郭富城偷情，不如说是两个人内心的救赎！', 'video2_url': 'https://v.qq.com/x/page/x3125slkdr6.html', 'video2_author': '', 'video2_url_hash': '29ec40e3565e63601ea264dc05185cdb'}, {'video2_title': '《左耳》整部剧最爱吧啦的人，却从没被正视过', 'video2_url': 'https://v.qq.com/x/page/j3078gn6gkg.html', 'video2_author': '', 'video2_url_hash': '7d2e7c1277a95729f2b1109d91a7605d'}, {'video2_title': '最爱', 'video2_url': 'https://v.qq.com/x/cover/tt1i4noxcvv2afr.html', 'video2_url_hash': '2c5ad440e8a529dedb413145cdffee30', 'video2_platform': '腾讯视频'}, {'video2_title': '小强最爱看电视', 'video2_url': 'https://v.qq.com/vplus/a447b99aa2c055690f8cf579b9d6066f#uin=a447b99aa2c055690f8cf579b9d6066fhttps://v.qq.com/vplus/a447b99aa2c055690f8cf579b9d6066f#uin=a447b99aa2c055690f8cf579b9d6066f', 'video2_url_hash': '50cfdad4825fdc6ddfe02ff3d0939925', 'video2_platform': '腾讯视频'}]
                    for each_detail_dic in detail_info:
                        task_list_video.append(dict( each_detail_dic, **each )) # 合并字典
                        # print(len(task_list_video))
                # print(len(task_list_video))
                # return print("task_list_video")
            else:  # 按需求抓取
                for e in each["video_check_platform"].split('_'):
                    # detail_info = audio_plarform_search().__audio_search_function__[e]().search_songs(
                    #     song_name=each["search_key_words"], proxy=self.proxies)
                    detail_info = importlib.import_module(audio_plarform_search().__video_search_function__[e]).search_songs(
                        each["search_key_words"],**each)
                    for each_detail_dic in detail_info:
                        # task_list.append(each_detail_dic)
                        task_list_video.append(dict( each_detail_dic, **each )) # 合并字典
            # print("hesrasersaer")
            # print(task_list_video)
            # print(len(task_list_video))
            return  task_list_video
        # 电视剧
        elif str(each["task_type"])=="6":
            task_list_video = []  # 存储最后的结果 dict
            # print("电视剧")
            # print(each["video_check_platform"]) # 打印对应的监测平台信息 0 all 1，2，。。。。
            # print(task_list_video)
            if str(each["video_check_platform"]) == "0":
                # print("xyyyyy")
                # task_list_video = []
                for e in audio_plarform_search().__video_search_function__: # 对应不同函数 都实现相同的函数search_songs

                    # print(len(task_list_video))
                    # detail_info = audio_plarform_search().__audio_search_function__[e]().search_songs(
                    #     song_name=each["search_key_words"], proxy=self.proxies) #proxy=self.proxies
                    detail_info = importlib.import_module(audio_plarform_search().__video_search_function__[e]).search_songs(
                        each["search_key_words"],**each)
                    # detail_info = list(detail_info)
                    # detail_info = [{'video2_title': '电影《最爱》中章子怡和郭富城的这一段 精彩', 'video2_url': 'https://v.qq.com/x/page/x0930woiryx.html', 'video2_author': '', 'video2_url_hash': '74fc942912844d86209e33dc7ebe0103'}, {'video2_title': '章子怡和郭富城的《最爱》片段，简直是太刺激了，不愧是实力演员', 'video2_url': 'https://v.qq.com/x/page/g0704fjs8ty.html', 'video2_author': '', 'video2_url_hash': '8f5eb480347fd36145cbed246db67735'}, {'video2_title': '电影最爱中郭富城和章子怡最突显演技的一段', 'video2_url': 'https://v.qq.com/x/page/g06077tgojz.html', 'video2_author': '', 'video2_url_hash': '227c718d71e27ea1f80e82fdd1f9401c'}, {'video2_title': '最爱：如果说章子怡郭富城偷情，不如说是两个人内心的救赎！', 'video2_url': 'https://v.qq.com/x/page/x3125slkdr6.html', 'video2_author': '', 'video2_url_hash': '29ec40e3565e63601ea264dc05185cdb'}, {'video2_title': '《左耳》整部剧最爱吧啦的人，却从没被正视过', 'video2_url': 'https://v.qq.com/x/page/j3078gn6gkg.html', 'video2_author': '', 'video2_url_hash': '7d2e7c1277a95729f2b1109d91a7605d'}, {'video2_title': '最爱', 'video2_url': 'https://v.qq.com/x/cover/tt1i4noxcvv2afr.html', 'video2_url_hash': '2c5ad440e8a529dedb413145cdffee30', 'video2_platform': '腾讯视频'}, {'video2_title': '小强最爱看电视', 'video2_url': 'https://v.qq.com/vplus/a447b99aa2c055690f8cf579b9d6066f#uin=a447b99aa2c055690f8cf579b9d6066fhttps://v.qq.com/vplus/a447b99aa2c055690f8cf579b9d6066f#uin=a447b99aa2c055690f8cf579b9d6066f', 'video2_url_hash': '50cfdad4825fdc6ddfe02ff3d0939925', 'video2_platform': '腾讯视频'}]
                    for each_detail_dic in detail_info:
                        task_list_video.append(dict( each_detail_dic, **each )) # 合并字典
                        # print(len(task_list_video))
                # print(len(task_list_video))
                # return print("task_list_video")
            else:  # 按需求抓取
                for e in each["video_check_platform"].split('_'):
                    # detail_info = audio_plarform_search().__audio_search_function__[e]().search_songs(
                    #     song_name=each["search_key_words"], proxy=self.proxies)
                    detail_info = importlib.import_module(audio_plarform_search().__video_search_function__[e]).search_songs(
                        each["search_key_words"],**each)
                    for each_detail_dic in detail_info:
                        # task_list.append(each_detail_dic)
                        task_list_video.append(dict( each_detail_dic, **each )) # 合并字典
            # print("hesrasersaer")
            # print(task_list_video)
            # print(len(task_list_video))
            return  task_list_video
        # 图文
        elif str(each["task_type"])=="0":
            task_list_graphic = []  # 存储最后的结果 dict
            # print("视频")
            # print(each["video_check_platform"]) # 打印对应的监测平台信息 0 all 1，2，。。。。
            # print(task_list_video)
            if str(each["graphic_check_platform"]) == "0":
                # print("xyyyyy")
                # task_list_video = []
                for e in audio_plarform_search().__graphic_search_function__: # 对应不同函数 都实现相同的函数search_songs

                    # print(len(task_list_video))
                    # detail_info = audio_plarform_search().__audio_search_function__[e]().search_songs(
                    #     song_name=each["search_key_words"], proxy=self.proxies) #proxy=self.proxies
                    detail_info = importlib.import_module(audio_plarform_search().__graphic_search_function__[e]).search_songs(
                        each["search_key_words"],**each)
                    # detail_info = list(detail_info)
                    # detail_info = [{'video2_title': '电影《最爱》中章子怡和郭富城的这一段 精彩', 'video2_url': 'https://v.qq.com/x/page/x0930woiryx.html', 'video2_author': '', 'video2_url_hash': '74fc942912844d86209e33dc7ebe0103'}, {'video2_title': '章子怡和郭富城的《最爱》片段，简直是太刺激了，不愧是实力演员', 'video2_url': 'https://v.qq.com/x/page/g0704fjs8ty.html', 'video2_author': '', 'video2_url_hash': '8f5eb480347fd36145cbed246db67735'}, {'video2_title': '电影最爱中郭富城和章子怡最突显演技的一段', 'video2_url': 'https://v.qq.com/x/page/g06077tgojz.html', 'video2_author': '', 'video2_url_hash': '227c718d71e27ea1f80e82fdd1f9401c'}, {'video2_title': '最爱：如果说章子怡郭富城偷情，不如说是两个人内心的救赎！', 'video2_url': 'https://v.qq.com/x/page/x3125slkdr6.html', 'video2_author': '', 'video2_url_hash': '29ec40e3565e63601ea264dc05185cdb'}, {'video2_title': '《左耳》整部剧最爱吧啦的人，却从没被正视过', 'video2_url': 'https://v.qq.com/x/page/j3078gn6gkg.html', 'video2_author': '', 'video2_url_hash': '7d2e7c1277a95729f2b1109d91a7605d'}, {'video2_title': '最爱', 'video2_url': 'https://v.qq.com/x/cover/tt1i4noxcvv2afr.html', 'video2_url_hash': '2c5ad440e8a529dedb413145cdffee30', 'video2_platform': '腾讯视频'}, {'video2_title': '小强最爱看电视', 'video2_url': 'https://v.qq.com/vplus/a447b99aa2c055690f8cf579b9d6066f#uin=a447b99aa2c055690f8cf579b9d6066fhttps://v.qq.com/vplus/a447b99aa2c055690f8cf579b9d6066f#uin=a447b99aa2c055690f8cf579b9d6066f', 'video2_url_hash': '50cfdad4825fdc6ddfe02ff3d0939925', 'video2_platform': '腾讯视频'}]
                    for each_detail_dic in detail_info:
                        task_list_graphic.append(dict( each_detail_dic, **each )) # 合并字典
                        # print(len(task_list_video))
                # print(len(task_list_video))
                # return print("task_list_video")
            else:  # 按需求抓取
                for e in each["graphic_check_platform"].split('_'):
                    # detail_info = audio_plarform_search().__audio_search_function__[e]().search_songs(
                    #     song_name=each["search_key_words"], proxy=self.proxies)
                    detail_info = importlib.import_module(audio_plarform_search().__graphic_search_function__[e]).search_songs(
                        each["search_key_words"],**each)
                    for each_detail_dic in detail_info:
                        # task_list.append(each_detail_dic)
                        task_list_graphic.append(dict( each_detail_dic, **each )) # 合并字典
            # print("hesrasersaer")
            # print(task_list_video)
            # print(len(task_list_video))
            return  task_list_graphic
        # 小说类
        elif str(each["task_type"])=="4":
            task_list_novel = []  # 存储最后的结果 dict
            # print("视频")
            # print(each["video_check_platform"]) # 打印对应的监测平台信息 0 all 1，2，。。。。
            # print(task_list_video)
            if str(each["novel_check_platform"]) == "0":
                # print("xyyyyy")
                # task_list_video = []
                for e in audio_plarform_search().__novel_search_function__: # 对应不同函数 都实现相同的函数search_songs
                    detail_info = importlib.import_module(audio_plarform_search().__novel_search_function__[e]).search_novels(
                        each["search_key_words"],**each)
                    # print("d到了这里 薛忆阳！！！！！！！！！！！！！！！！！！")
                    # detail_info = list(detail_info)
                    # detail_info = [{'video2_title': '电影《最爱》中章子怡和郭富城的这一段 精彩', 'video2_url': 'https://v.qq.com/x/page/x0930woiryx.html', 'video2_author': '', 'video2_url_hash': '74fc942912844d86209e33dc7ebe0103'}, {'video2_title': '章子怡和郭富城的《最爱》片段，简直是太刺激了，不愧是实力演员', 'video2_url': 'https://v.qq.com/x/page/g0704fjs8ty.html', 'video2_author': '', 'video2_url_hash': '8f5eb480347fd36145cbed246db67735'}, {'video2_title': '电影最爱中郭富城和章子怡最突显演技的一段', 'video2_url': 'https://v.qq.com/x/page/g06077tgojz.html', 'video2_author': '', 'video2_url_hash': '227c718d71e27ea1f80e82fdd1f9401c'}, {'video2_title': '最爱：如果说章子怡郭富城偷情，不如说是两个人内心的救赎！', 'video2_url': 'https://v.qq.com/x/page/x3125slkdr6.html', 'video2_author': '', 'video2_url_hash': '29ec40e3565e63601ea264dc05185cdb'}, {'video2_title': '《左耳》整部剧最爱吧啦的人，却从没被正视过', 'video2_url': 'https://v.qq.com/x/page/j3078gn6gkg.html', 'video2_author': '', 'video2_url_hash': '7d2e7c1277a95729f2b1109d91a7605d'}, {'video2_title': '最爱', 'video2_url': 'https://v.qq.com/x/cover/tt1i4noxcvv2afr.html', 'video2_url_hash': '2c5ad440e8a529dedb413145cdffee30', 'video2_platform': '腾讯视频'}, {'video2_title': '小强最爱看电视', 'video2_url': 'https://v.qq.com/vplus/a447b99aa2c055690f8cf579b9d6066f#uin=a447b99aa2c055690f8cf579b9d6066fhttps://v.qq.com/vplus/a447b99aa2c055690f8cf579b9d6066f#uin=a447b99aa2c055690f8cf579b9d6066f', 'video2_url_hash': '50cfdad4825fdc6ddfe02ff3d0939925', 'video2_platform': '腾讯视频'}]
                    for each_detail_dic in detail_info:
                        task_list_novel.append(dict( each_detail_dic, **each )) # 合并字典
                        # print(len(task_list_novel),"000000000000000")
                    # print("zheliyoumeiyouren!!!!")
                # print(len(task_list_novel),"[[[[[[[[[[[[[[[[[[[[")
                # return task_list_novel
            else:  # 按需求抓取
                for e in each["novel_check_platform"].split('_'):
                    # detail_info = audio_plarform_search().__audio_search_function__[e]().search_songs(
                    #     song_name=each["search_key_words"], proxy=self.proxies)
                    detail_info = importlib.import_module(audio_plarform_search().__novel_search_function__[e]).search_novels(
                        each["search_key_words"],**each)
                    for each_detail_dic in detail_info:
                        # task_list.append(each_detail_dic)
                        task_list_novel.append(dict( each_detail_dic, **each )) # 合并字典
            # print("hesrasersaer")
            # print(task_list_novel)
            # print(len(task_list_novel))
            return  task_list_novel
        # 搜索引擎类
        elif str(each["task_type"])=="5":
            task_list_engine = []  # 存储最后的结果 dict
            # print("视频")
            # print(each["video_check_platform"]) # 打印对应的监测平台信息 0 all 1，2，。。。。
            # print(task_list_video)
            if str(each["engine_check_platform"]) == "0":
                # print("xyyyyy")
                # task_list_video = []
                for e in audio_plarform_search().__engine_search_function__: # 对应不同函数 都实现相同的函数search_songs
                    detail_info = importlib.import_module(audio_plarform_search().__engine_search_function__[e]).search_engines(
                        each["search_key_words"],**each)
                    # print("d到了这里 薛忆阳！！！！！！！！！！！！！！！！！！")
                    # detail_info = list(detail_info)
                    # detail_info = [{'video2_title': '电影《最爱》中章子怡和郭富城的这一段 精彩', 'video2_url': 'https://v.qq.com/x/page/x0930woiryx.html', 'video2_author': '', 'video2_url_hash': '74fc942912844d86209e33dc7ebe0103'}, {'video2_title': '章子怡和郭富城的《最爱》片段，简直是太刺激了，不愧是实力演员', 'video2_url': 'https://v.qq.com/x/page/g0704fjs8ty.html', 'video2_author': '', 'video2_url_hash': '8f5eb480347fd36145cbed246db67735'}, {'video2_title': '电影最爱中郭富城和章子怡最突显演技的一段', 'video2_url': 'https://v.qq.com/x/page/g06077tgojz.html', 'video2_author': '', 'video2_url_hash': '227c718d71e27ea1f80e82fdd1f9401c'}, {'video2_title': '最爱：如果说章子怡郭富城偷情，不如说是两个人内心的救赎！', 'video2_url': 'https://v.qq.com/x/page/x3125slkdr6.html', 'video2_author': '', 'video2_url_hash': '29ec40e3565e63601ea264dc05185cdb'}, {'video2_title': '《左耳》整部剧最爱吧啦的人，却从没被正视过', 'video2_url': 'https://v.qq.com/x/page/j3078gn6gkg.html', 'video2_author': '', 'video2_url_hash': '7d2e7c1277a95729f2b1109d91a7605d'}, {'video2_title': '最爱', 'video2_url': 'https://v.qq.com/x/cover/tt1i4noxcvv2afr.html', 'video2_url_hash': '2c5ad440e8a529dedb413145cdffee30', 'video2_platform': '腾讯视频'}, {'video2_title': '小强最爱看电视', 'video2_url': 'https://v.qq.com/vplus/a447b99aa2c055690f8cf579b9d6066f#uin=a447b99aa2c055690f8cf579b9d6066fhttps://v.qq.com/vplus/a447b99aa2c055690f8cf579b9d6066f#uin=a447b99aa2c055690f8cf579b9d6066f', 'video2_url_hash': '50cfdad4825fdc6ddfe02ff3d0939925', 'video2_platform': '腾讯视频'}]
                    for each_detail_dic in detail_info:
                        task_list_engine.append(dict( each_detail_dic, **each )) # 合并字典
                        # print(len(task_list_novel),"000000000000000")
                    # print("zheliyoumeiyouren!!!!")
                # print(len(task_list_novel),"[[[[[[[[[[[[[[[[[[[[")
                # return task_list_novel
            else:  # 按需求抓取
                for e in each["engine_check_platform"].split('_'):
                    # detail_info = audio_plarform_search().__audio_search_function__[e]().search_songs(
                    #     song_name=each["search_key_words"], proxy=self.proxies)
                    detail_info = importlib.import_module(audio_plarform_search().__engine_search_function__[e]).search_engines(
                        each["search_key_words"],**each)
                    for each_detail_dic in detail_info:
                        # task_list.append(each_detail_dic)
                        task_list_engine.append(dict( each_detail_dic, **each )) # 合并字典
            # print("hesrasersaer")
            # print(task_list_engine)
            # print(len(task_list_engine))
            return  task_list_engine

    # 生成搜索任务 线程运行的函数函数
    def get_search_task(self,tr_name): # 生成异步任务
        print("{}开始".format(tr_name))
        result_list = []
        task_info = redis_get_tasks_from_redis(task_name=config["redis_task_set_qq_name_bendi_test_lpy"],task_numbers=self.task_numbers) # 从redis 获取任务 接下来要进行判断 进行异步请求的包装
        if task_info: # 有任务的时候跑 没有的时候暂停十分钟
            for each in task_info:
                each = json.loads(each)
                # try:
                for i in self.get_search_response(each):
                    result_list.append(i)
            # print(result_list)
            return result_list
        else:
            print("redis没有任务了，请检查任务是否完成 暂时")
            return result_list
    def danjinc(self):
        result_list = []
        task_info = redis_get_tasks_from_redis(task_numbers=self.task_numbers) # 从redis 获取任务 接下来要进行判断 进行异步请求的包装
        if task_info: # 有任务的时候跑 没有的时候暂停十分钟
            for each in task_info:
                each = json.loads(each)
                # try:
                for i in self.get_search_response(each):
                    result_list.append(i)
            # print(result_list)
            return result_list
        else:
            print("redis没有任务了，请检查任务是否完成 暂时")
            return result_list

    # 子进程运行的函数
    def process_function(self,thred_name):
        print("进程name:{}".format(thred_name))
        stop_flag = 1 # 正常运行 1 停止 0
        reduce_of_info = []
        with ThreadPoolExecutor(max_workers=self.task_thread) as t:
            obj_list = []
            begin = time.time()
            for page in range(self.task_thread):
                obj = t.submit(self.get_search_task, "主进程{}下的线程".format(thred_name)+str(page))
                obj_list.append(obj)

            for future in as_completed(obj_list):
                data = future.result()
                # print("1234567")
                # print(data)
                for i in data:
                    reduce_of_info.append(i)

                print('*' * 50)
            times = time.time() - begin
        # print("有{}个结果，第1条数据是\n{}".format(len(reduce_of_info),reduce_of_info[1].keys()))
        print("进程name:{} 抓取总耗时{}".format(thred_name,times))
        # if stop_flag: # 队列还有任务 就
        return self.clear_last_result(reduce_of_info)
        # else:
        #     print("zanting")
        #     time.sleep(config["procces_stop_time"])
        #     return 0
    #########################
    # 数据清洗 并且存md5到redis集合 存完再存mysql 存当天的表
    def clear_last_result(self,reduce_of_info):
        task = redis_check_set_already_lpy(result_list=reduce_of_info)
        # print(task)
        # print("clerare")
        # 通过任务的类型决定存储方式把
        redis_task = mysql_save_to_current_result_table_lpy(task)
        self.redis_set_add(redis_task)

    def redis_set_add(self,redis_task,task_name=config["redis_md5_set_result_url"], result_list=[],
                            host=config["redis_host"], port=config["redis_port"], decode_responses=True,
                                            db=config["redis_task_db"], password=config["redis_passwd"]):
        con = redis.Redis(host=host, port=port, decode_responses=decode_responses, db=db, password=password)
        con.sadd(task_name, *redis_task)

    # 异步爬取主函数
    def audio_main(self):
        ''':cvar 判断哪些平台需要爬取'''
        # 进程池
        p = Pool(self.task_process)
        for i in range(self.task_process):
            p.apply_async(self.process_function, args=("zhu{}".format(i),),error_callback=err_print)
        p.close()
        p.join()
        return 0
# 关于音频的存储把这个 判断一下任务的所属类型
def mysql_save_to_current_result_table_lpy(result):
    conn = pymysql.connect(host=config["mysql_host"], port=config["mysql_port"], user=config["mysql_username"],
                           passwd=config["mysql_userpwd"], db=config["mysql_db"],
                           charset='utf8mb4')
    cursor = conn.cursor()
    now_time = timestamp_strftime(like="%Y-%m-%d")
    redis_task = []
    for each in result:
        table_name = each["sub_table_name"]
        # 音频
        if each["task_type"]==2:
            each["qingquan_flag"] = judge_song_type_easy(each) # 判断规则
            # print(each["qingquan_flag"])
            if each["qingquan_flag"]!=-1:
                # print("hree")
                # print(each)
                sql_save_info = "insert into {}(audio_flag_str1,audio_flag_str2,title_similar_number,author_name_similar_number,yangben_URL,yangben_title,yangben_author_name,yangben_text,qinquan_text,qinquan_title,qinquan_author_name,qinquan_URL,qinquan_url_hash,qinquan_platform,yangben_platform,t,qinquan_type,qingquan_flag,flag_int,t_timestamp,qinquan_id_str,yangben_task_id) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                    table_name,timestamp_strftime("%Y%m%d"),each["search_key_words"],str_similar(each["audio2_songName"],each["audio_title"]),str_similar(each["audio_author"],each["audio2_artistName"]),each["audio_url"],pymysql.escape_string(each["audio_title"]),pymysql.escape_string(each["audio_author"]),
                                pymysql.escape_string(each["audio_album"]),pymysql.escape_string(each["audio2_albumName"]),
                                pymysql.escape_string(each["audio2_songName"]),pymysql.escape_string(each["audio2_artistName"]),
                                each["audio2_url"],str(each["id"])+"|"+each["audio2_url_hash"],
                                each["audio2_platform"],each["audio_platform"],now_time,2,each["qingquan_flag"],
                                each["id"],now_time,each["audio2_songId"],each["id"])

                # print(sql_save_info)
                try:
                    # print(sql_save_info)
                    if cursor.execute(sql_save_info):
                        redis_task.append(str(each["id"])+"|"+each["video2_url_hash"])
                    conn.commit()
                except Exception as e:
                    # print(sql_save_info)
                    # print(e)
                    print("重复插入错误")
                    pass
            else:
                # print("无关的音乐->{} 样本音乐->{}".format(each["audio2_songName"],each["audio_title"]))
                pass
        # 视频
        elif each["task_type"]==1:
            # print("dao le zhe li hree",each)
            video2_id = each.get("video2_id","")
            video2_author = each.get("video2_author","")
            each["video2_author"] = video2_author
            # if each["video2_id"]:
            #     video2_id = each["video2_id"]

            # sql_save_info = "insert into {}(audio_flag_str1,audio_flag_str2,title_similar_number,author_name_similar_number,yangben_URL,yangben_title,yangben_author_name,yangben_text,qinquan_text,qinquan_title,qinquan_author_name,qinquan_URL,qinquan_url_hash,qinquan_platform,yangben_platform,t,qinquan_type,qingquan_flag,flag_int,t_timestamp,qinquan_id_str,yangben_task_id) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
            sql_save_info = "insert into {}(audio_flag_str1,audio_flag_str2,title_similar_number,author_name_similar_number,yangben_URL,yangben_title,yangben_author_name,yangben_text,qinquan_text,qinquan_title,qinquan_author_name,qinquan_URL,qinquan_url_hash,qinquan_platform,yangben_platform,t,qinquan_type,qingquan_flag,flag_int,t_timestamp,qinquan_id_str,yangben_task_id,duration_str,duration) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                table_name,timestamp_strftime("%Y%m%d"),each["search_key_words"],str_similar(each["video2_title"],each["video_title"]),str_similar(each["video_author"],each["video2_author"]),each["video_url"], pymysql.escape_string(each["video_title"]),
                pymysql.escape_string(each["video_author"]),
                pymysql.escape_string(''), pymysql.escape_string(''),
                pymysql.escape_string(each["video2_title"]), pymysql.escape_string(each["video2_author"]),
                each["video2_url"], str(each["id"])+"|"+each["video2_url_hash"],
                each["video2_platform"], each["video_platform"], now_time, 1, 0,
                each["id"], now_time, video2_id, each["id"],each["video2_duration_str"],each["video2_duration"])

            # print(sql_save_info)
            try:
                # print(sql_save_info)
                if cursor.execute(sql_save_info):
                    redis_task.append(str(each["id"]) + "|" + each["video2_url_hash"])
                conn.commit()
            except Exception as e:
                # print(sql_save_info)
                # print(e)
                print("重复插入错误")
                pass
        # 小说
        elif each["task_type"]==4:
            # print("asdffagffadasfadsf")
            table = each["sub_table_name"]
            # 获取到一个以键且为逗号分隔的字符串，返回一个字符串
            del each["id"]
            del each["novel_title"]
            del each["novel_url"]
            del each["novel_author"]
            del each["novel_platform"]
            del each["novel_check_platform"]
            del each["sub_table_name"]
            del each["task_type"]
            del each["search_key_words"]
            keys = ','.join(each.keys())
            values = ','.join(['%s'] * len(each))
            sql_save_info = 'INSERT INTO {table}({keys}) VALUES({values})'.format(table=table, keys=keys, values=values)
            # print(sql_save_info)
            # sql_save_info = "insert into {}(audio_flag_str1,audio_flag_str2,title_similar_number,author_name_similar_number,yangben_URL,yangben_title,yangben_author_name,yangben_text,qinquan_text,qinquan_title,qinquan_author_name,qinquan_URL,qinquan_url_hash,qinquan_platform,yangben_platform,t,qinquan_type,qingquan_flag,flag_int,t_timestamp,qinquan_id_str,yangben_task_id) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
            #     table_name,timestamp_strftime("%Y%m%d"),each["search_key_words"],str_similar(each["video2_title"],each["video_title"]),str_similar(each["video_author"],each["video2_author"]),each["video_url"], pymysql.escape_string(each["video_title"]),
            #     pymysql.escape_string(each["video_author"]),
            #     pymysql.escape_string(''), pymysql.escape_string(''),
            #     pymysql.escape_string(each["video2_title"]), pymysql.escape_string(each["video2_author"]),
            #     each["video2_url"], str(each["id"])+"|"+each["video2_url_hash"],
            #     each["video2_platform"], each["video_platform"], now_time, 1, 0,
            #     each["id"], now_time, video2_id, each["id"])

            # print(sql_save_info)
            try:
                # print(sql_save_info)
                if cursor.execute(sql_save_info):
                    redis_task.append(str(each["id"]) + "|" + each["video2_url_hash"])
                conn.commit()
            except Exception as e:
                # print(sql_save_info)
                print(e,"novel "*30)
                print("重复插入错误")
                pass
        # 搜索引擎
        elif each["task_type"]==5:
            # print("dao le zhe li hree",each)
            sql_save_info = "insert into {}(audio_flag_str1,audio_flag_str2,title_similar_number,author_name_similar_number,yangben_URL,yangben_title,yangben_author_name,yangben_text,qinquan_text,qinquan_title,qinquan_author_name,qinquan_URL,qinquan_url_hash,qinquan_platform,yangben_platform,t,qinquan_type,qingquan_flag,flag_int,t_timestamp,qinquan_id_str,yangben_task_id) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                table_name,timestamp_strftime("%Y%m%d"),each["search_key_words"],str_similar(each["qinquan_title"],each["engine_title"]),str_similar(each["engine_author"],""),each["engine_url"], pymysql.escape_string(each["engine_title"]),
                pymysql.escape_string(""),
                pymysql.escape_string(''), pymysql.escape_string(''),
                pymysql.escape_string(each["qinquan_title"]), pymysql.escape_string(""),
                each["qinquan_URL"], str(each["id"])+"|"+md5_use(each["qinquan_URL"]),
                each["qinquan_platform"], each["engine_check_platform"], now_time, 5, 0,
                each["id"], now_time, "", each["id"])

            # print(sql_save_info)
            try:
                # print(sql_save_info)
                if cursor.execute(sql_save_info):
                    redis_task.append(str(each["id"]) + "|" + each["video2_url_hash"])
                conn.commit()
            except Exception as e:
                # print(sql_save_info)
                # print(e)
                print("重复插入错误")
                pass
        # 电视剧
        elif each["task_type"]==6:
            # print("dao le zhe li hree",each)
            video2_id = each.get("video2_id","")
            video2_author = each.get("video2_author","")
            each["video2_author"] = video2_author
            # if each["video2_id"]:
            #     video2_id = each["video2_id"]
            try:

                for each_task_id in each["tvplay_task_list"]: # 获得的是主任务ID

                    sql_save_info = "insert into {}(audio_flag_str1,audio_flag_str2,title_similar_number,author_name_similar_number,yangben_URL,yangben_title,yangben_author_name,yangben_text,qinquan_text,qinquan_title,qinquan_author_name,qinquan_URL,qinquan_url_hash,qinquan_platform,yangben_platform,t,qinquan_type,qingquan_flag,flag_int,t_timestamp,qinquan_id_str,yangben_task_id,duration_str,duration) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                        table_name,timestamp_strftime("%Y%m%d"),each["search_key_words"],str_similar(each["video2_title"],each["video_title"]),str_similar(each["video_author"],each["video2_author"]),each["video_url"], pymysql.escape_string(each["video_title"]),
                        pymysql.escape_string(each["video_author"]),
                        pymysql.escape_string(''), pymysql.escape_string(''),
                        pymysql.escape_string(each["video2_title"]), pymysql.escape_string(each["video2_author"]),
                        each["video2_url"], str(each_task_id)+"|"+each["video2_url_hash"],
                        each["video2_platform"], each["video_platform"], now_time, 1, 0,
                        each_task_id, now_time, video2_id, each["id"],each["video2_duration_str"],each["video2_duration"])

                # print(sql_save_info)
                    # print(sql_save_info)
                    if cursor.execute(sql_save_info):
                        redis_task.append(str(each["id"]) + "|" + each["video2_url_hash"])
                conn.commit()
            except Exception as e:
                # print(sql_save_info)
                # print(e)
                print(str(e))
                pass

    cursor.close()
    conn.close()
    return redis_task
# 传入列表 判断其中的每一条数据 是否存在于某个集合中 ,返回md5值不存在的结果
def redis_check_set_already_lpy(task_name=config["redis_md5_set_result_url"], result_list=[],
                            host=config["redis_host"], port=config["redis_port"], decode_responses=True,
                                            db=config["redis_task_db"], password=config["redis_passwd"])->list:
    con = redis.Redis(host=host, port=port, decode_responses=decode_responses, db=db, password=password)
    task_list = []
    # print("到redis这里了")
    # 2020 07 14 新增 不同的任务使用不同的 redis队列
    old_task_name = task_name # 之前的默认的名字
    for each in result_list: # 判断value 是否存在集合中 存在 返回1 不存在或者集合不存在 返回0
        if each["task_type"]==2:
            task_name = old_task_name + "_" + chang_ping_ying(text=each["audio_platform"])
            ifexit = con.exists(task_name)
            # print("dao le zheli nihao ")
            if not ifexit:
                con.sadd(task_name, "xueyiyang_audio")

            isexit = con.sismember(task_name,str(each["id"])+"|"+each["audio2_url_hash"]) # 判断数据中字段 audio2_url_hash
            if isexit:
                # 测试环境
                # print("此歌曲已存在 {}".format(each["audio_title"]))
                pass
            else:
                # con.sadd(task_name,str(each["id"])+"|"+each["audio2_url_hash"])
                task_list.append(each)
        elif each["task_type"]==1:
            task_name = old_task_name + "_" + chang_ping_ying(text=each["video_platform"])
            ifexit = con.exists(task_name)
            # print("dao le zheli nihao ")
            if not ifexit:
                con.sadd(task_name, "xueyiyang_video")

            isexit = con.sismember(task_name, str(each["id"])+"|"+each["video2_url_hash"])  # 判断数据中字段 audio2_url_hash
            if isexit:
                # 测试环境
                # print("此歌曲已存在 {}".format(each["audio_title"]))
                pass
            else:
                # con.sadd(task_name, str(each["id"])+"|"+each["video2_url_hash"])
                task_list.append(each)
        elif each["task_type"]==4:
            task_name = old_task_name + "_" + chang_ping_ying(text=each["novel_platform"])
            ifexit = con.exists(task_name)
            # print("dao le zheli nihao ")
            if not ifexit:
                con.sadd(task_name, "xueyiyang_novel")

            # isexit = con.sismember(task_name, str(each["id"])+"|"+each["video2_url_hash"])  # 判断数据中字段 audio2_url_hash
            isexit = con.sismember(task_name, each["qin_quan_url_hash_str"])  # 判断数据中字段 audio2_url_hash
            if isexit:
                # 测试环境
                # print("此歌曲已存在 {}".format(each["audio_title"]))
                pass
            else:
                # con.sadd(task_name, each["qin_quan_url_hash_str"])
                task_list.append(each)
        # 搜索引擎字段
        elif each["task_type"]==5:
            task_name = old_task_name + "_" + chang_ping_ying(text=each["engine_platform"])
            ifexit = con.exists(task_name)
            # print("dao le zheli nihao ")
            if not ifexit:
                con.sadd(task_name, "xueyiyang_engine")

            isexit = con.sismember(task_name, str(each["id"])+"|"+md5_use(each["qinquan_URL"]))  # 判断数据中字段 audio2_url_hash
            # isexit = con.sismember(task_name, each["qin_quan_url_hash_str"])  # 判断数据中字段 audio2_url_hash
            if isexit:
                # 测试环境
                # print("此歌曲已存在 {}".format(each["audio_title"]))
                pass
            else:
                # con.sadd(task_name, str(each["id"])+"|"+md5_use(each["qinquan_URL"]))
                task_list.append(each)
        elif each["task_type"]==6:
            task_name = old_task_name + "_" + chang_ping_ying(text=each["video_platform"])
            ifexit = con.exists(task_name)
            # print("dao le zheli nihao ")
            if not ifexit:
                con.sadd(task_name, "xueyiyang_video")

            isexit = con.sismember(task_name, str(each["id"])+"|"+each["video2_url_hash"])  # 判断数据中字段 audio2_url_hash
            if isexit:
                # 测试环境
                # print("此歌曲已存在 {}".format(each["audio_title"]))
                pass
            else:
                # con.sadd(task_name, str(each["id"])+"|"+each["video2_url_hash"])
                task_list.append(each)
    return task_list
def err_print(err):
    print("多进程错误信息：--->>>",err)
if __name__ == '__main__':
    # 测试 视频代码 proxies not define
#     each = {'id': 563430, 'video_title': '风犬少年的天空', 'video_url': 'https://www.bilibili.com/bangumi/play/ep340226', 'video_author': '', 'video_album': '', 'video_platform': '风犬少年的天空1016测试', 'video_check_platform': '10', 'sub_table_name': 'sub_3_47', 'task_type': 1, 'search_key_words': '风犬少年的天空'}
# # 4 5 8 9 11 12
#     infor = importlib.import_module(audio_plarform_search().__video_search_function__["12"]).search_songs(
#         each["search_key_words"], **each)
#     print(infor[:2])
#     exit(0)

    # 测试 神马搜索
    # each  = {'id': 560002, 'engine_title': '风犬少年的天空', 'engine_url': 'https://www.bilibili.com/bangumi/play/ep340226', 'engine_author': '', 'engine_platform': '搜索引擎风犬少年1014测试3_45_5', 'engine_check_platform': '2', 'sub_table_name': 'sub_3_45', 'task_type': 5, 'page_num': 1, 'search_key_words': '风犬少年的天空'}
    # importlib.import_module(audio_plarform_search().__engine_search_function__["2"]).search_engines(
    #     each["search_key_words"], **each)
    # exit(0)
    #################
# 测试 小说
#     print(audio_plarform_search().__novel_search_function__)
#     print(importlib.import_module(audio_plarform_search().__novel_search_function__["18"]).search_novels(
#         "锦色佳年"))
#     exit(0)
    #################
    # audio_plarform_search().danjinc()
    # exit(0)
    # print(config["__video_search_function__"])
    # # # mod = importlib.import_module('audio_search_unit.wangyiyun_search')
    # # # print(mod.search_songs(song_name="你好",proxy=proxies))
    # exit(0)

    # 测试
    while 1:
        print(">>> 本次任务开始时间 ：{} \n".format(timestamp_strftime(like="%Y-%m-%d %H:%M:%S")))
        audio_xyy_man = audio_plarform_search()
        start_time = int(time.time())
        audio_xyy_man.audio_main()
        print("耗时： {}".format(int(time.time()) - start_time))
        flag = redis_check_key_exit(task_name=config["redis_task_set_qq_name_bendi_test_lpy"])
        if flag:
            pass
        else:
            print("没有任务了 暂停{}秒".format(config["procces_stop_time"]))
            time.sleep(config["procces_stop_time"])


''':cvar
main 函数 
'''