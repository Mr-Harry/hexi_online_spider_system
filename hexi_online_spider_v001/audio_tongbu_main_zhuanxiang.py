# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/7/1

import time
import json
from Audio_Infringement_Config import Config_of_audio_infringement as config
from Audio_Infringement_Config import Config_of_audio_infringement as proxies
from concurrent.futures import ThreadPoolExecutor, as_completed
from audio_tool import redis_get_tasks_from_redis
from audio_tool import redis_check_set_already_first
from audio_tool import redis_check_set_already
from audio_tool import redis_check_key_exit
from audio_tool import timestamp_strftime
from audio_tool import mysql_save_to_current_result_table
from multiprocessing import Pool
import importlib

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
    # 小说抓取对应的参数
    __novel_search_function__ = config["__novel_search_function__"]
    # 搜索引擎取对应的参数
    __engine_search_function__ = config["__engine_search_function__"]
    # 漫画抓取对应的参数
    __cartoon_search_function__ = config["__cartoon_search_function__"]

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
        # 漫画类
        elif str(each["task_type"])=="7":
            task_list_normals = []  # 存储最后的结果 dict
            # print("视频")
            # print(each["video_check_platform"]) # 打印对应的监测平台信息 0 all 1，2，。。。。
            # print(task_list_video)
            if str(each["novel_check_platform"]) == "0":
                # print("xyyyyy")
                # task_list_video = []
                for e in audio_plarform_search().__novel_search_function__: # 对应不同函数 都实现相同的函数search_songs
                    detail_info = importlib.import_module(audio_plarform_search().__cartoon_search_function__[e]).search_normals(
                        each["search_key_words"],**each)
                    # print("d到了这里 薛忆阳！！！！！！！！！！！！！！！！！！")
                    # detail_info = list(detail_info)
                    # detail_info = [{'video2_title': '电影《最爱》中章子怡和郭富城的这一段 精彩', 'video2_url': 'https://v.qq.com/x/page/x0930woiryx.html', 'video2_author': '', 'video2_url_hash': '74fc942912844d86209e33dc7ebe0103'}, {'video2_title': '章子怡和郭富城的《最爱》片段，简直是太刺激了，不愧是实力演员', 'video2_url': 'https://v.qq.com/x/page/g0704fjs8ty.html', 'video2_author': '', 'video2_url_hash': '8f5eb480347fd36145cbed246db67735'}, {'video2_title': '电影最爱中郭富城和章子怡最突显演技的一段', 'video2_url': 'https://v.qq.com/x/page/g06077tgojz.html', 'video2_author': '', 'video2_url_hash': '227c718d71e27ea1f80e82fdd1f9401c'}, {'video2_title': '最爱：如果说章子怡郭富城偷情，不如说是两个人内心的救赎！', 'video2_url': 'https://v.qq.com/x/page/x3125slkdr6.html', 'video2_author': '', 'video2_url_hash': '29ec40e3565e63601ea264dc05185cdb'}, {'video2_title': '《左耳》整部剧最爱吧啦的人，却从没被正视过', 'video2_url': 'https://v.qq.com/x/page/j3078gn6gkg.html', 'video2_author': '', 'video2_url_hash': '7d2e7c1277a95729f2b1109d91a7605d'}, {'video2_title': '最爱', 'video2_url': 'https://v.qq.com/x/cover/tt1i4noxcvv2afr.html', 'video2_url_hash': '2c5ad440e8a529dedb413145cdffee30', 'video2_platform': '腾讯视频'}, {'video2_title': '小强最爱看电视', 'video2_url': 'https://v.qq.com/vplus/a447b99aa2c055690f8cf579b9d6066f#uin=a447b99aa2c055690f8cf579b9d6066fhttps://v.qq.com/vplus/a447b99aa2c055690f8cf579b9d6066f#uin=a447b99aa2c055690f8cf579b9d6066f', 'video2_url_hash': '50cfdad4825fdc6ddfe02ff3d0939925', 'video2_platform': '腾讯视频'}]
                    for each_detail_dic in detail_info:
                        task_list_normals.append(dict( each_detail_dic, **each )) # 合并字典
                        # print(len(task_list_novel),"000000000000000")
                    # print("zheliyoumeiyouren!!!!")
                # print(len(task_list_novel),"[[[[[[[[[[[[[[[[[[[[")
                # return task_list_novel
            else:  # 按需求抓取
                for e in each["novel_check_platform"].split('_'):
                    # detail_info = audio_plarform_search().__audio_search_function__[e]().search_songs(
                    #     song_name=each["search_key_words"], proxy=self.proxies)
                    detail_info = importlib.import_module(audio_plarform_search().__cartoon_search_function__[e]).search_normals(
                        each["search_key_words"],**each)
                    for each_detail_dic in detail_info:
                        # task_list.append(each_detail_dic)
                        task_list_normals.append(dict( each_detail_dic, **each )) # 合并字典
            # print("hesrasersaer")
            # print(task_list_normals)
            # print(len(task_list_normals))
            return  task_list_normals
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
        task_info = redis_get_tasks_from_redis(task_name=config["redis_task_set_qq_name_zhuanxiang"],task_numbers=self.task_numbers) # 从redis 获取任务 接下来要进行判断 进行异步请求的包装
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
                try:
                    data = future.result()
                    for i in data:
                        reduce_of_info.append(i)
                except Exception as e:
                    print("线程出现的问题: >>>",e)
                print('*' * 50)
            times = time.time() - begin
        if reduce_of_info:
            print("有{}个结果，第1条数据是\n{}".format(len(reduce_of_info),reduce_of_info[1].keys()))
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
        task = redis_check_set_already_first(result_list=reduce_of_info)
        # print("task >>>>",task)
        mysql_task_list = mysql_save_to_current_result_table(task)
        # print("mysql_task_list>>>>>>>>>>>>>>>>>>>>>",mysql_task_list)
        redis_check_set_already(result_list=mysql_task_list)
        # print(task)
        # print("clerare")
        # 通过任务的类型决定存储方式把
        return 0

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
def err_print(err):
    print("多进程错误信息：--->>>",err)
if __name__ == '__main__':
    #################
# 测试 小说
#     print(audio_plarform_search().__novel_search_function__)
#     print(importlib.import_module(audio_plarform_search().__novel_search_function__["28"]).search_novels(
#         "爱"))
#     exit(0)
    #################
    # audio_plarform_search().danjinc()
    # exit(0)
    # print(config["__video_search_function__"])
    # # # mod = importlib.import_module('audio_search_unit.wangyiyun_search')
    # # # print(mod.search_songs(song_name="你好",proxy=proxies))
    # exit(0)
    # 测试
    # while 1:
    #     print(">>> 本次任务开始时间 ：{} \n".format(timestamp_strftime(like="%Y-%m-%d %H:%M:%S")))
    #     audio_xyy_man = audio_plarform_search()
    #     start_time = int(time.time())
    #     audio_xyy_man.audio_main()
    #     print("耗时： {}".format(int(time.time()) - start_time))
    #     flag = redis_check_key_exit(task_name=config["redis_task_set_qq_name_zhuanxiang"])
    #     if flag:
    #         pass
    #     else:
    #         print("没有任务了 暂停{}秒".format(config["procces_stop_time"]))
    #         time.sleep(config["procces_stop_time"])

    print(">>> 本次任务开始时间 ：{} \n".format(timestamp_strftime(like="%Y-%m-%d %H:%M:%S")))
    audio_xyy_man = audio_plarform_search()
    start_time = int(time.time())
    audio_xyy_man.audio_main()
    print("耗时： {}".format(int(time.time()) - start_time))
    flag = redis_check_key_exit(task_name=config["redis_task_set_qq_name_zhuanxiang"])
    if flag:
        pass
    else:
        print("没有任务了 暂停{}秒".format(config["procces_stop_time"]))
        time.sleep(config["procces_stop_time"])

''':cvar
main 函数 
'''