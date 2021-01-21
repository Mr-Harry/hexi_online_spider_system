# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/7/1

import datetime
import difflib
import re
import time
import redis
import pymysql
import requests
import copy

from Audio_Infringement_Config import Config_of_audio_infringement as config, proxies
from hashlib import md5
from xpinyin import Pinyin

# 普通异常 类
class Public_Error(Exception):
    def __init__(self,ErrorInfo):
        super().__init__(self) #初始化父类
        self.errorinfo=ErrorInfo
    def __str__(self):
        return self.errorinfo

# 关于mysql的操作集合
###################################################### mysql    ######################################################

# 关于音频的存储把这个 判断一下任务的所属类型
def mysql_save_to_current_result_table(result):
    conn = pymysql.connect(host=config["mysql_host"], port=config["mysql_port"], user=config["mysql_username"],
                           passwd=config["mysql_userpwd"], db=config["mysql_db"],
                           charset='utf8mb4')
    task_list = []
    cursor = conn.cursor()
    now_time = timestamp_strftime(like="%Y-%m-%d")
    for each in result:
        # each_bf = each
        each_bf = copy.deepcopy(each) # 深拷贝 浅拷贝，del了值，只是浅拷贝 导致对于小说动漫来说 没有存到值
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
                    cursor.execute(sql_save_info)
                    conn.commit()
                    task_list.append(each_bf)
                except Exception as e:
                    # print(sql_save_info)
                    # print(e)
                    print("重复插入错误")
                    pass
            else:
                # print("无关的音乐->{} 样本音乐->{}".format(each["audio2_songName"],each["audio_title"]))
                pass
        # 漫画
        elif each["task_type"]==7:
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
            if "book_update_time" in each and not each.get("book_update_time",""):
                del each["book_update_time"]
            if "page_num" in each:
                del each["page_num"]
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
                cursor.execute(sql_save_info,tuple(each.values()))
                conn.commit()
                task_list.append(each_bf)
            except Exception as e:
                # print(sql_save_info)
                print(e,"cartoon "*30)
                print("重复插入错误")
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
            sql_save_info = "insert into {}(qinquan_pub_time,audio_flag_str1,audio_flag_str2,title_similar_number,author_name_similar_number,yangben_URL,yangben_title,yangben_author_name,yangben_text,qinquan_text,qinquan_title,qinquan_author_name,qinquan_URL,qinquan_url_hash,qinquan_platform,yangben_platform,t,qinquan_type,qingquan_flag,flag_int,t_timestamp,qinquan_id_str,yangben_task_id,duration_str,duration) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                table_name,each["video2_pubtime"],timestamp_strftime("%Y%m%d"),each["search_key_words"],str_similar(each["video2_title"],each["video_title"]),str_similar(each["video_author"],each["video2_author"]),each["video_url"], pymysql.escape_string(each["video_title"]),
                pymysql.escape_string(each["video_author"]),
                pymysql.escape_string(''), pymysql.escape_string(''),
                pymysql.escape_string(each["video2_title"]), pymysql.escape_string(each["video2_author"]),
                each["video2_url"], str(each["id"])+"|"+each["video2_url_hash"],
                each["video2_platform"], each["video_platform"], now_time, 1, 0,
                each["id"], now_time, video2_id, each["id"],each["video2_duration_str"],each["video2_duration"])

            # print(sql_save_info)
            try:
                # print(sql_save_info)
                cursor.execute(sql_save_info)
                conn.commit()
                task_list.append(each_bf)

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
            if "book_update_time" in each and not each.get("book_update_time",""):
                del each["book_update_time"]
            if "page_num" in each:
                del each["page_num"]

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
                cursor.execute(sql_save_info,tuple(each.values()))
                conn.commit()
                task_list.append(each_bf)
            except Exception as e:
                # print(sql_save_info)
                print(e,"novel "*30)
                print("重复插入错误")
                pass
        # 搜索引擎
        elif each["task_type"]==5:
            # print("dao le zhe li hree",each)
            sql_save_info = "insert into {}(audio_flag_str1,audio_flag_str2,title_similar_number,author_name_similar_number,yangben_URL,yangben_title,yangben_author_name,yangben_text,qinquan_text,qinquan_title,qinquan_author_name,qinquan_URL,qinquan_url_hash,qinquan_platform,yangben_platform,t,qinquan_type,qingquan_flag,flag_int,t_timestamp,qinquan_id_str,yangben_task_id) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                table_name,timestamp_strftime("%Y%m%d"),each["search_key_words"],str_similar(each["qinquan_title"][:28],each["engine_title"][:28]),str_similar(each["engine_author"],""),each["engine_url"], pymysql.escape_string(each["engine_title"]),
                pymysql.escape_string(""),
                pymysql.escape_string(''), pymysql.escape_string(''),
                pymysql.escape_string(each["qinquan_title"]), pymysql.escape_string(""),
                each["qinquan_URL"], str(each["id"])+"|"+md5_use(each["qinquan_URL"]),
                each["qinquan_platform"], each["engine_check_platform"], now_time, 5, 0,
                each["id"], now_time, "", each["id"])

            # print(sql_save_info)
            try:
                # print(sql_save_info)
                cursor.execute(sql_save_info)
                conn.commit()
                task_list.append(each_bf)

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

                    sql_save_info = "insert into {}(qinquan_pub_time,audio_flag_str1,audio_flag_str2,title_similar_number,author_name_similar_number,yangben_URL,yangben_title,yangben_author_name,yangben_text,qinquan_text,qinquan_title,qinquan_author_name,qinquan_URL,qinquan_url_hash,qinquan_platform,yangben_platform,t,qinquan_type,qingquan_flag,flag_int,t_timestamp,qinquan_id_str,yangben_task_id,duration_str,duration) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
                        table_name,each["video2_pubtime"],timestamp_strftime("%Y%m%d"),each["search_key_words"],str_similar(each["video2_title"],each["video_title"]),str_similar(each["video_author"],each["video2_author"]),each["video_url"], pymysql.escape_string(each["video_title"]),
                        pymysql.escape_string(each["video_author"]),
                        pymysql.escape_string(''), pymysql.escape_string(''),
                        pymysql.escape_string(each["video2_title"]), pymysql.escape_string(each["video2_author"]),
                        each["video2_url"], str(each_task_id)+"|"+each["video2_url_hash"],
                        each["video2_platform"], each["video_platform"], now_time, 1, 0,
                        each_task_id, now_time, video2_id, each["id"],each["video2_duration_str"],each["video2_duration"])

                # print(sql_save_info)
                    # print(sql_save_info)
                    cursor.execute(sql_save_info)
                    task_list.append(each_bf)
                conn.commit()
            except Exception as e:
                # print(sql_save_info)
                # print(e)
                print(str(e))
                pass

    cursor.close()
    conn.close()
    return task_list
###################################################### mysql    ######################################################


# 关于redis的操作集合
###################################################### REDIS    ######################################################

# 指定redis集合取指定条，如果空了 返回值是空[]
def redis_get_tasks_from_redis(task_name=config["redis_task_set_qq_name"],task_numbers=1,host=config["redis_host"],port=config["redis_port"],decode_responses=True,db=config["redis_task_db"],password=config["redis_passwd"]):
    con = redis.Redis(host=host,port=port,decode_responses=decode_responses,db=db,password=password)
    task_list = []
    for each in range(task_numbers):
        res = con.spop(task_name)
        if res:
            task_list.append(res)
    print(task_list)
    # print(type(res))
    return task_list

# 判断某个key是否存在
def redis_check_key_exit(task_name=config["redis_task_set_qq_name"],
                            host=config["redis_host"], port=config["redis_port"], decode_responses=True,
                                            db=config["redis_task_db"], password=config["redis_passwd"])->list:
    con = redis.Redis(host=host, port=port, decode_responses=decode_responses, db=db, password=password)
    ifexit = con.exists(task_name)
    if ifexit:
        return True
    else:
        return False

# 传入列表 判断其中的每一条数据 是否存在于某个集合中 ,返回md5值不存在的结果
def redis_check_set_already_bf(task_name=config["redis_md5_set_result_url"], result_list=[],
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
                con.sadd(task_name,str(each["id"])+"|"+each["audio2_url_hash"])
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
                con.sadd(task_name, str(each["id"])+"|"+each["video2_url_hash"])
                task_list.append(each)
        elif each["task_type"]==4 or each["task_type"]==7:
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
                con.sadd(task_name, each["qin_quan_url_hash_str"])
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
                con.sadd(task_name, str(each["id"])+"|"+md5_use(each["qinquan_URL"]))
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
                con.sadd(task_name, str(each["id"])+"|"+each["video2_url_hash"])
                task_list.append(each)
    return task_list
# 传入列表 判断其中的每一条数据 是否存在于某个集合中 ,返回md5值不存在的结果
def redis_check_set_already(task_name=config["redis_md5_set_result_url"], result_list=[],
                            host=config["redis_host"], port=config["redis_port"], decode_responses=True,
                                            db=config["redis_task_db"], password=config["redis_passwd"])->list:
    con = redis.Redis(host=host, port=port, decode_responses=decode_responses, db=db, password=password)
    task_list = []
    # 2020 07 14 新增 不同的任务使用不同的 redis队列
    old_task_name = task_name # 之前的默认的名字
    for each in result_list: # 判断value 是否存在集合中 存在 返回1 不存在或者集合不存在 返回0
        # 音频
        if each["task_type"]==2:
            task_name = old_task_name + "_" + chang_ping_ying(text=each["audio_platform"])
            con.sadd(task_name,str(each["id"])+"|"+each["audio2_url_hash"])
            task_list.append(each)
        # 视频
        elif each["task_type"]==1:
            task_name = old_task_name + "_" + chang_ping_ying(text=each["video_platform"])
            con.sadd(task_name, str(each["id"])+"|"+each["video2_url_hash"])
            task_list.append(each)
        # 小说和漫画
        elif each["task_type"]==4 or each["task_type"]==7:
            task_name = old_task_name + "_" + chang_ping_ying(text=each["novel_platform"])
            con.sadd(task_name, each["qin_quan_url_hash_str"])
            task_list.append(each)
        # 搜索引擎字段
        elif each["task_type"]==5:
            task_name = old_task_name + "_" + chang_ping_ying(text=each["engine_platform"])
            con.sadd(task_name, str(each["id"])+"|"+md5_use(each["qinquan_URL"]))
            task_list.append(each)
        # 电视剧
        elif each["task_type"]==6:
            task_name = old_task_name + "_" + chang_ping_ying(text=each["video_platform"])
            con.sadd(task_name, str(each["id"])+"|"+each["video2_url_hash"])
            task_list.append(each)
    return task_list
# 传入列表 判断其中的每一条数据 是否存在于某个集合中 只判断在不在
def redis_check_set_already_first(task_name=config["redis_md5_set_result_url"], result_list=[],
                            host=config["redis_host"], port=config["redis_port"], decode_responses=True,
                                            db=config["redis_task_db"], password=config["redis_passwd"])->list:
    con = redis.Redis(host=host, port=port, decode_responses=decode_responses, db=db, password=password)
    task_list = []
    # print("到redis这里了")
    # 2020 07 14 新增 不同的任务使用不同的 redis队列
    old_task_name = task_name # 之前的默认的名字
    for each in result_list: # 判断value 是否存在集合中 存在 返回1 不存在或者集合不存在 返回0
        # print("xyyyyyyyasdfasdfasdf",type(each["task_type"]),each["task_type"])
        # 音频
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
                task_list.append(each)
        # 视频
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
                # print("存了东西 艹")
                task_list.append(each)
        # 小说和漫画
        elif each["task_type"]==4 or each["task_type"]==7:
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
                task_list.append(each)
    return task_list
###################################################### REDIS    ######################################################








# 对应的不同平台对应不同的初期的筛选规则
######################################################  search judge   ######################################################

# 比较千千音乐平台
def judge_qianqian_platform(each_json):
    pass
# 比较网易云音乐平台
def judge_wangyiyun_platform(each_json):
    pass
# 比较虾米音乐平台
def judge_xiami_platform(each_json):
    pass
# 比较喜马拉雅平台
def judge_ximalaya_platform(each_json):
    pass
#######
# 上面是PC #
# 下面是APP #
#######

# 比较情咖平台
def judge_qingka_platform(each):
    if each["audio_title"] in each["audio2_songName"]:
        return 0
    else:
        return 0
######################################################  search judge   ######################################################











# 普通的用到的一些函数
######################################################  normal   ######################################################
#判断相似度的方法，用到了difflib库 返回bool值
def check_song_title_similar(str1, str2,similar=config["song_name_similar"])->bool:
    """:cvar
    相似 True
    不相似 False
    similar 的值就是相似值 返回的值大于相似值返回True
    """
    similar_number = difflib.SequenceMatcher(None, str1, str2).quick_ratio()
    if 1-similar_number<(1-similar):
        return True
    else:
        return False

# Md5 加密函数 32 返回32位的加密结果
def md5_use(text:str)->str:
    result = md5(bytes(text, encoding="utf-8")).hexdigest()
    # print(result)
    return result

# 返回当前时间 格式为 %Y%m%d 年月日 拼接数据库表
def timestamp_strftime(like):
    return datetime.datetime.fromtimestamp(int(time.time())).strftime(like)

# 清洗一串字符删除不要的 符号 \n\t\r....
def clear_text(text,way_list=[ "\n", "\t", "\r", "　　　　", "　　", "    ", " "]):
    for each in way_list:
        if each != '"':
            text = text.replace("{}".format(each), "")
        else:
            text = text.replace("{}".format(each), "")
    # print(text)
    return text

# 汉语转拼音
def chang_ping_ying(text,way="_"):
    p = Pinyin()
    text = p.get_pinyin(text,way)
    return text
# 判断原唱的规则
def yuan_chang(each):
    # 如果歌手名字相等 并且歌曲名字相似
    if clear_text(each["audio_author"],way_list=["|","/","-"," "]) == clear_text(each["audio2_artistName"],way_list=["|","/","-"," "]):
        # similar = check_song_title_similar(each["audio_title"], each["audio2_songName"]) # 比较的相似度在配置文件里

        # if similar: # 相似度 大于 0.22
        #     return 1
        if clear_text(each["audio_title"],way_list=["|","/","-"," "]) == clear_text(each["audio2_songName"],way_list=["|","/","-"," "]):
            return 1
        else:
            return 0
    else:
        return 0
# 判断原唱还是翻唱或者未判断 1 原唱 2 翻唱 0 满足歌名相似但是无法判断  -1 完全没关系丢掉（可能专辑是这个名字才找到 都是综合查找）
def judge_song_type_easy(each):
    # similar = check_song_title_similar(each["audio_title"],each["audio2_songName"] )
    # 如果 名字一样 专辑一样 歌手一样 原唱 存1
    # 又一个判断原唱的模版
    # if clear_text(each["audio_title"],way_list=["《","》"," "]) == clear_text(each["audio2_songName"],way_list=["《","》","《","》"," "]) and each["audio_author"] == each["audio2_artistName"] and clear_text(each["audio2_albumName"],way_list=["《","》","《","》"]) == clear_text(each["audio_album"],way_list=["《","》","《","》"]):
    #     return 1
    if each["audio2_platform"]=="千千音乐" or each["audio2_platform"]=="网易云音乐" or each["audio2_platform"]=="虾米音乐":
        if yuan_chang(each):
            return 1
        # 如果 名字满足条件 并且带翻自 以及原歌手名字 /Cover cover 以及原歌手名字 翻唱
        elif each["audio_title"] in each["audio2_songName"] and "翻自" in each["audio2_songName"] and each["audio_author"] in each["audio2_songName"]:
            return 2
        elif each["audio_title"] in each["audio2_songName"] and "cover" in each["audio2_songName"] and each[
                "audio_author"] in each["audio2_songName"]:
            return 2
        elif each["audio_title"] in each["audio2_songName"] and "Cover" in each["audio2_songName"] and each[
                "audio_author"] in each["audio2_songName"]:
            return 2
        elif re.findall('^{}'.format(each["audio_title"][0]), each["audio2_songName"]):
            return 0

        else:
            return -1

    # elif similar: # 不用名字的相似度计算了 正则匹配 以样本开头的 才比较 （原唱和翻唱 ）
    #     return 0
    # 除开喜马拉雅 其他的用其他的规则
    elif each["audio2_platform"]=="喜马拉雅":
        if each["audio_title"] in each["audio2_songName"]:
            return 0
        else:
            return 0
    elif each["audio2_platform"] == "情咖FM":
        return judge_qingka_platform(each)
    # 名字相似度满足条件才存 0
# 判断歌曲名字和歌手名字相似度
def str_similar(str1: str, str2: str, ndigits=2):
    similar_number1 = difflib.SequenceMatcher(None, clear_text(str1, config.get('clear_video_title_way_list')), clear_text(str2, config.get('clear_video_title_way_list'))).quick_ratio()
    # print(similar_number1)
    return str(round(similar_number1, ndigits))

def get_parms_value(qin_quan_url_str, parms_key):
    try:
        parms_str_list = qin_quan_url_str.split('?')[-1].split('&')
        for ps in parms_str_list:
            if ps.split('=')[0] == parms_key:
                return ps.split('=')[-1]
    except:
        return ''
    return ''
# 获取代理
# 获得代理函数
def get_proxy():
    return proxies


# 统一请求响应函数
def unify_requests(method="GET", url="",headers={},proxies={},data={},verify=False,cookies={}):
    if method=="GET":
        response = requests.get(url, headers=headers,proxies=proxies,data=data,cookies=cookies,timeout=5)
        return response
    else:
        response = requests.post(url, headers=headers,proxies=proxies,data=data,verify=verify,cookies=cookies,timeout=5)
        return response

# 通过时间获得一个固定格式的 时长格式
def get_duration_str(seconds:float,like:str="%02d:%02d:%02d"):
    """
    71  -> 01:11
    """
    m, s = divmod(float(seconds), 60)
    h, m = divmod(m, 60)
    # print(like % (h, m, s))
    return like % (h, m, s)

# 通过时间字符形式 返回时长格式
def unify_duration_format(duar_str_or_s: str):
    """
    01:11 -> 71,'00:01:11'
    00:01:11 -> 71,'00:01:11'
    :param duar_str: '01:11' or '00:01:11'
    :return:  71, '00:01:11'
    """
    error = 0, ''

    def hms(m: int, s: int, h=0):
        if s > 60:
            m += 1
        if m > 60:
            h += 1
        return h * 60 * 60 + m * 60 + s, str(h).zfill(2) + ':' + str(m).zfill(2) + ':' + str(s).zfill(2)
    try:
        s = int(duar_str_or_s)
    except:
        pass
    else:
        return hms(m=s % 3600//60, s=s % 60, h=s//3600)
    try:
        if duar_str_or_s:
            duar_list = duar_str_or_s.split(':')
            if len(duar_list) == 2:
                return hms(m=int(duar_list[0]), s=int(duar_list[1]))
            elif len(duar_list) == 3:
                return hms(m=int(duar_list[1]), s=int(duar_list[2]), h=int(duar_list[0]))
            else:
                return error
        else:
            return error
    except Exception as e:
        return error

# 视频过滤步骤
def unit_video_filter(result_list:list=[], **kwargs):
    """:param
    retutn ： list

    """
    unit_video_filter_newlist_tempo = list()
    for each_dict in result_list:
        if title_filter_words(each_dict, **kwargs):
            unit_video_filter_newlist_tempo.append(each_dict)
    return unit_video_filter_newlist_tempo

# 核对标题的是否存需要过滤
def title_filter_words(each_dict:dict={}, **kwargs):
    # 视频平台的过滤
    if kwargs.get('task_type')==1:
        # 确认的关键词
        filter_key_words_list = kwargs.get('filter_key_words_list').lower().split("_")
        yangben_title_clear = clear_text(kwargs.get("video_title"),way_list=config["clear_video_title_way_list"]).lower()
        qingquan_title_clear = clear_text(each_dict.get("video2_title"),way_list=config["clear_video_title_way_list"]).lower()
        for each_needs_filter in filter_key_words_list:
            filter_key_words = clear_text(each_needs_filter,way_list=config["clear_video_title_way_list"])
            filter_key_words.lower()
            # 筛选的关键词 先过滤 如果
            if filter_key_words not in yangben_title_clear and filter_key_words in qingquan_title_clear:
                return False
        return True
    # 音频平台的过滤
    if kwargs.get('task_type')==2:
        # 确认的关键词
        filter_key_words_list = kwargs.get('filter_key_words_list').lower().split("_")
        yangben_title_clear = clear_text(kwargs.get("audio_title"),way_list=config["clear_video_title_way_list"]).lower()
        qingquan_title_clear = clear_text(each_dict.get("audio2_songName"),way_list=config["clear_video_title_way_list"]).lower()
        for each_needs_filter in filter_key_words_list:
            filter_key_words = clear_text(each_needs_filter,way_list=config["clear_video_title_way_list"])
            filter_key_words.lower()
            # 筛选的关键词 先过滤 如果
            if filter_key_words not in yangben_title_clear and filter_key_words in qingquan_title_clear:
                return False
        return True
    if kwargs.get('task_type')==5:
        # 确认的关键词
        filter_key_words_list = kwargs.get('filter_key_words_list').lower().split("_")
        yangben_title_clear = clear_text(kwargs.get("audio_title"),way_list=config["clear_video_title_way_list"]).lower()
        qingquan_title_clear = clear_text(each_dict.get("audio_author"),way_list=config["clear_video_title_way_list"]).lower()
        for each_needs_filter in filter_key_words_list:
            filter_key_words = clear_text(each_needs_filter,way_list=config["clear_video_title_way_list"])
            filter_key_words.lower()
            # 筛选的关键词 先过滤 如果
            if filter_key_words not in yangben_title_clear and filter_key_words in qingquan_title_clear:
                return False
        return True

# 核对标题的是否存在
def title_confirm_words(each_dict: dict={}, **kwargs):
    if kwargs.get('task_type')==1:
        # 确认的关键词
        confirm_key_words = replace_number_to_chines_number(kwargs.get('confirm_key_words'))
        qinquan_title_clear = replace_number_to_chines_number(clear_text(each_dict.get("video2_title"), way_list=config["clear_video_title_way_list"]).lower())
        # 确认关键词 下划线_连接 只要有一个确认就可以
        for confirm_key_words_ in confirm_key_words.split("_"):
            confirm_key_words_clear__ = clear_text(confirm_key_words_, way_list=config["clear_video_title_way_list"]).lower()
            # print(qinquan_title_clear)
            # print(confirm_key_words_clear__)
            if confirm_key_words_clear__ in qinquan_title_clear:
                return True

        return False
    elif kwargs.get('task_type')==2:
        # print(kwargs)
        confirm_key_words = replace_number_to_chines_number(kwargs.get('confirm_key_words'))
        qinquan_title_clear = replace_number_to_chines_number(clear_text(each_dict.get("audio2_songName"), way_list=config["clear_video_title_way_list"]).lower())
        # 确认关键词 下划线_连接 只要有一个确认就可以
        for confirm_key_words_ in confirm_key_words.split("_"):
            confirm_key_words_clear__ = clear_text(confirm_key_words_,
                                                   way_list=config["clear_video_title_way_list"]).lower()
            if confirm_key_words_clear__ in qinquan_title_clear:
                # print(qinquan_title_clear)
                # print(confirm_key_words_clear__)
                # print("确实在里面")
                return True

        return False
    elif kwargs.get('task_type')==5:
        # print(kwargs)
        confirm_key_words = kwargs.get('confirm_key_words')
        qinquan_title_clear = clear_text(each_dict.get("qinquan_title"), way_list=config["clear_video_title_way_list"]).lower()
        # 确认关键词 下划线_连接 只要有一个确认就可以
        for confirm_key_words_ in confirm_key_words.split("_"):
            confirm_key_words_clear__ = clear_text(confirm_key_words_,
                                                   way_list=config["clear_video_title_way_list"]).lower()
            if confirm_key_words_clear__ in qinquan_title_clear:
                # print(qinquan_title_clear)
                # print(confirm_key_words_clear__)
                # print("确实在里面")
                return True

        return False


# 视频确认步骤
def unit_video_confirm(result_list:list=[], **kwargs):
    """:param
    :return  ： list
    """
    # 中间列表
    unit_video_confirm_newlist_tempo = list()
    # print("xxxx",result_list)
    for each_dict in result_list:
        # print("hhhh")
        if title_confirm_words(each_dict, **kwargs): # 核对标题的是否存在
            unit_video_confirm_newlist_tempo.append(each_dict)
    return unit_video_confirm_newlist_tempo

# 替换标题中的 阿拉伯数字替换为中文
def replace_number_to_chines_number(text,type_choose=1):
    info_list = []
    """
    :param
    choose =1 默认是阿拉伯替换中文
    choose =2 中文替换阿拉伯
    1 -> 一
    2 -> 二
    
    """
    info_dic_number_chines = {
                            "零":"0",
                            "一":"1",
                            "二":"2",
                            "三":"3",
                            "四":"4",
                            "五":"5",
                            "六":"6",
                            "七":"7",
                            "八":"8",
                            "九":"9",
                            }
    info_dic_number_alb = {
                        "0":"零",
                        "1":"一",
                        "2":"二",
                        "3":"三",
                        "4":"四",
                        "5":"五",
                        "6":"六",
                        "7":"七",
                        "8":"八",
                        "9":"九",
                    }
    # 默认是阿拉伯替换中文
    if type_choose==1:
        for each in text:
            if each in info_dic_number_alb:
                info_list.append(info_dic_number_alb[each])
            else:
                info_list.append(each)
    # 中文替换阿拉伯
    elif type_choose==2:
        for each in text:
            if each in info_dic_number_chines:
                info_list.append(info_dic_number_alb[each])
            else:
                info_list.append(each)
    return "".join(info_list)
#  清洗的规则 （清洗返回的视频）
def unit_result_clear_for_video(result_list:list=[], **kwargs):

    # # 确认的关键词
    confirm_key_words = kwargs.get('confirm_key_words',"")
    # # 过滤的关键词 列表？
    filter_key_words_list = kwargs.get('filter_key_words_list',"")

    if not (confirm_key_words or filter_key_words_list):
        return result_list
    # print(result_list)
    # # 中间列表
    # newlist_tempo = list()
    # result_list = list()
    # 第一步 筛选确认的
    if confirm_key_words:
        unit_video_confirm_list = unit_video_confirm(result_list, **kwargs)
    else:
        unit_video_confirm_list = result_list
    # print("unit_video_confirm_list ")
    # 第二步 筛选过滤的
    if filter_key_words_list:
        # print(filter_key_words_list)
        unit_video_filter_list = unit_video_filter(unit_video_confirm_list, **kwargs)
    else:
        unit_video_filter_list = unit_video_confirm_list
    # print("unit_video_filter_list ")
    return unit_video_filter_list

#   清洗的规则 （清洗返回的音频）
def unit_result_clear_for_audio(result_list:list=[], **kwargs):
    # # 确认的关键词
    confirm_key_words = kwargs.get('confirm_key_words',"")
    # # 过滤的关键词 列表？
    filter_key_words_list = kwargs.get('filter_key_words_list',"")

    if not (confirm_key_words or filter_key_words_list):
        return result_list
    # print("asdf",result_list)
    # # 中间列表
    # newlist_tempo = list()
    # result_list = list()
    # 第一步 筛选确认的
    if confirm_key_words:
        unit_audio_confirm_list = unit_video_confirm(result_list, **kwargs)
    else:
        unit_audio_confirm_list = result_list
    # print("unit_video_confirm_list ")
    # 第二步 筛选过滤的
    if filter_key_words_list:
        # print(filter_key_words_list)
        unit_audio_filter_list = unit_video_filter(unit_audio_confirm_list, **kwargs)
    else:
        unit_audio_filter_list = unit_audio_confirm_list
    # print("unit_video_filter_list ")
    return unit_audio_filter_list



def url_value_to_gb2312_upper(value):
    return str(value.replace(' ', '').encode('gb2312')).lstrip("b\'").replace("'", '').replace("\\x", "%").upper()

# 时间格式的万能公式
def get_format_date(newsTime,format_time='%a, %d %b %Y %H:%M:%S'):
    """
    # https://docs.python.org/3/library/time.html # 时间
    :arg
        %a  语言环境的缩写工作日名称。
        %A  语言环境的完整工作日名称。
        %b  语言环境的缩写月份名称。
        %B  语言环境的完整月份名称。
        %c  语言环境的适当日期和时间表示。
        %d  以十进制数[01,31]表示的月份中的一天。
        %H  小时（24小时制），为十进制数字[00,23]。
        %I  小时（12小时制）为十进制数字[01,12]。
        %j  一年中的天，以十进制数字[001,366]为准。
        %m  以十进制数字[01,12]表示的月份。
        %M  以小数形式分钟[00,59]。
        %p  相当于AM或PM的语言环境。
        %S  第二个十进制数字[00,61]。
        %U  一年中的周号（星期日为一周的第一天），以十进制数[00,53]。新年中第一个星期日之前的所有天均视为第0周。
        %w  工作日为十进制数字[0（Sunday），6]。
        %W  一年中的星期号（星期一为星期的第一天），以十进制数[00,53]。第一个星期一之前的新的一年中的所有天均视为在第0周。
        %x  语言环境的适当日期表示形式。
        %X  语言环境的适当时间表示形式。
        %y  没有世纪的年份作为十进制数字[00,99]。
        %Y  以世纪作为十进制数字的年份。
        %z  时区偏移量，表示与UTC / GMT的正或负时差，格式为+ HHMM或-HHMM，其中H代表十进制小时数字，M代表十进制分钟数字[-23：59，+23：59]。
        %Z  时区名称（如果不存在时区，则没有字符）。
        %%  文字'%'字符。
    """
    # newsTime = 'Sun, 23 Apr 2017 05:15:05 GMT'
    # GMT_FORMAT = '%a, %d %b %Y %H:%M:%S GMT'
    newsTime = datetime.datetime.strptime(newsTime, format_time)
    # print(newsTime)  # 2017-04-23 05:15:05
    return newsTime

if __name__ == '__main__':
    # 测试阿拉伯替换的问题 数字中文之间的转换
    info_s = replace_number_to_chines_number("班淑传奇1")
    print(info_s)
    exit(0)
    # 测试 导入mysql的问题
    info= [{'video2_title': '超级柴油发动机-如何建造13600马力的发动机', 'video2_url': 'http://www.le.com/ptv/vplay/69998021.html', 'video2_author': '', 'video2_pubtime': '', 'video2_url_hash': '070e3942f62456ded46922107f724317', 'video2_platform': '乐视视频', 'video2_duration': 2942, 'video2_duration_str': '00:49:02', 'id': 826371, 'video_title': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站', 'video_url': 'http://weibo.com/5274804556/JtJzkBDJp', 'video_author': '银河系讲解员', 'video_album': '首发', 'video_platform': '新浪短视频1123测试二百5_70_1', 'video_check_platform': '14', 'sub_table_name': 'sub_5_70', 'task_type': 1, 'search_key_words': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站'}, {'video2_title': '亚丁湾护航十年 美国叙利亚战略 俄罗斯建造强悍护卫舰', 'video2_url': 'http://www.le.com/ptv/vplay/69717972.html', 'video2_author': '', 'video2_pubtime': '', 'video2_url_hash': 'f30612557d05eba17da2f63f6b71a728', 'video2_platform': '乐视视频', 'video2_duration': 2777, 'video2_duration_str': '00:46:17', 'id': 826371, 'video_title': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站', 'video_url': 'http://weibo.com/5274804556/JtJzkBDJp', 'video_author': '银河系讲解员', 'video_album': '首发', 'video_platform': '新浪短视频1123测试二百5_70_1', 'video_check_platform': '14', 'sub_table_name': 'sub_5_70', 'task_type': 1, 'search_key_words': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站'}, {'video2_title': '建造航母到底有多难？', 'video2_url': 'http://www.le.com/ptv/vplay/69718371.html', 'video2_author': '', 'video2_pubtime': '', 'video2_url_hash': '8d17b842dddac5fd5862d0c4575daf16', 'video2_platform': '乐视视频', 'video2_duration': 2574, 'video2_duration_str': '00:42:54', 'id': 826371, 'video_title': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站', 'video_url': 'http://weibo.com/5274804556/JtJzkBDJp', 'video_author': '银河系讲解员', 'video_album': '首发', 'video_platform': '新浪短视频1123测试二百5_70_1', 'video_check_platform': '14', 'sub_table_name': 'sub_5_70', 'task_type': 1, 'search_key_words': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站'}, {'video2_title': '皮卡解说明日之后手游：建造庇护所，防御丧尸追击！', 'video2_url': 'http://www.le.com/ptv/vplay/70321896.html', 'video2_author': '', 'video2_pubtime': '', 'video2_url_hash': '596055abd664cd9b934f2cd29620ff04', 'video2_platform': '乐视视频', 'video2_duration': 1307, 'video2_duration_str': '00:21:47', 'id': 826371, 'video_title': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站', 'video_url': 'http://weibo.com/5274804556/JtJzkBDJp', 'video_author': '银河系讲解员', 'video_album': '首发', 'video_platform': '新浪短视频1123测试二百5_70_1', 'video_check_platform': '14', 'sub_table_name': 'sub_5_70', 'task_type': 1, 'search_key_words': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站'}, {'video2_title': '迷你世界 建造院墙 第15集', 'video2_url': 'http://www.le.com/ptv/vplay/69822820.html', 'video2_author': '', 'video2_pubtime': '', 'video2_url_hash': '5d169e3caca5e94c620fc9273805668d', 'video2_platform': '乐视视频', 'video2_duration': 1425, 'video2_duration_str': '00:23:45', 'id': 826371, 'video_title': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站', 'video_url': 'http://weibo.com/5274804556/JtJzkBDJp', 'video_author': '银河系讲解员', 'video_album': '首发', 'video_platform': '新浪短视频1123测试二百5_70_1', 'video_check_platform': '14', 'sub_table_name': 'sub_5_70', 'task_type': 1, 'search_key_words': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站'}, {'video2_title': '皮卡解说我的世界搞笑《TNT大陆》第三集：建造TNT刷怪塔', 'video2_url': 'http://www.le.com/ptv/vplay/70236136.html', 'video2_author': '', 'video2_pubtime': '', 'video2_url_hash': '9e294fbec4f6b594803f3efcc721714f', 'video2_platform': '乐视视频', 'video2_duration': 1111, 'video2_duration_str': '00:18:31', 'id': 826371, 'video_title': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站', 'video_url': 'http://weibo.com/5274804556/JtJzkBDJp', 'video_author': '银河系讲解员', 'video_album': '首发', 'video_platform': '新浪短视频1123测试二百5_70_1', 'video_check_platform': '14', 'sub_table_name': 'sub_5_70', 'task_type': 1, 'search_key_words': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站'}, {'video2_title': '局座张召忠：075开始下饺子，至少建造20艘，震慑台独这个管用！【局座时评6】', 'video2_url': 'http://www.le.com/ptv/vplay/70626741.html', 'video2_author': '', 'video2_pubtime': '', 'video2_url_hash': 'eda15107322d014d444c520cdcf97002', 'video2_platform': '乐视视频', 'video2_duration': 768, 'video2_duration_str': '00:12:48', 'id': 826371, 'video_title': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站', 'video_url': 'http://weibo.com/5274804556/JtJzkBDJp', 'video_author': '银河系讲解员', 'video_album': '首发', 'video_platform': '新浪短视频1123测试二百5_70_1', 'video_check_platform': '14', 'sub_table_name': 'sub_5_70', 'task_type': 1, 'search_key_words': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站'}, {'video2_title': '我的世界 钻石大陆建造农场 第4集', 'video2_url': 'http://www.le.com/ptv/vplay/69825352.html', 'video2_author': '', 'video2_pubtime': '', 'video2_url_hash': 'a3d89f94b068ca78eea0f7dc43b275cf', 'video2_platform': '乐视视频', 'video2_duration': 1380, 'video2_duration_str': '00:23:00', 'id': 826371, 'video_title': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站', 'video_url': 'http://weibo.com/5274804556/JtJzkBDJp', 'video_author': '银河系讲解员', 'video_album': '首发', 'video_platform': '新浪短视频1123测试二百5_70_1', 'video_check_platform': '14', 'sub_table_name': 'sub_5_70', 'task_type': 1, 'search_key_words': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站'}, {'video2_title': 'Roblox建造大战怪物！打造摩天大厦！阻止灭霸军团入侵地球？', 'video2_url': 'http://www.le.com/ptv/vplay/70283344.html', 'video2_author': '', 'video2_pubtime': '', 'video2_url_hash': 'a559714254edf5056793995954a07723', 'video2_platform': '乐视视频', 'video2_duration': 1053, 'video2_duration_str': '00:17:33', 'id': 826371, 'video_title': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站', 'video_url': 'http://weibo.com/5274804556/JtJzkBDJp', 'video_author': '银河系讲解员', 'video_album': '首发', 'video_platform': '新浪短视频1123测试二百5_70_1', 'video_check_platform': '14', 'sub_table_name': 'sub_5_70', 'task_type': 1, 'search_key_words': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站'}, {'video2_title': 'Roblox建造大战怪物！星河战队躲避僵尸怪物军团？面面解说', 'video2_url': 'http://www.le.com/ptv/vplay/70283332.html', 'video2_author': '', 'video2_pubtime': '', 'video2_url_hash': 'd52ba81f92e113130b40a6d9c48c0c4c', 'video2_platform': '乐视视频', 'video2_duration': 1046, 'video2_duration_str': '00:17:26', 'id': 826371, 'video_title': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站', 'video_url': 'http://weibo.com/5274804556/JtJzkBDJp', 'video_author': '银河系讲解员', 'video_album': '首发', 'video_platform': '新浪短视频1123测试二百5_70_1', 'video_check_platform': '14', 'sub_table_name': 'sub_5_70', 'task_type': 1, 'search_key_words': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站'}, {'video2_title': '僵尸家族《无人小镇》39，建造工作台，茶水间桌子和椅子', 'video2_url': 'http://www.le.com/ptv/vplay/70472721.html', 'video2_author': '', 'video2_pubtime': '', 'video2_url_hash': 'ab09d65e85494a492337c0c92c30a522', 'video2_platform': '乐视视频', 'video2_duration': 846, 'video2_duration_str': '00:14:06', 'id': 826371, 'video_title': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站', 'video_url': 'http://weibo.com/5274804556/JtJzkBDJp', 'video_author': '银河系讲解员', 'video_album': '首发', 'video_platform': '新浪短视频1123测试二百5_70_1', 'video_check_platform': '14', 'sub_table_name': 'sub_5_70', 'task_type': 1, 'search_key_words': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站'}, {'video2_title': '超级牛的纯手工建造大师！房子泳池带花园，10分钟修建完毕！', 'video2_url': 'http://www.le.com/ptv/vplay/70596784.html', 'video2_author': '', 'video2_pubtime': '', 'video2_url_hash': '444fc2137f09ca8ac5e52606293212de', 'video2_platform': '乐视视频', 'video2_duration': 756, 'video2_duration_str': '00:12:36', 'id': 826371, 'video_title': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站', 'video_url': 'http://weibo.com/5274804556/JtJzkBDJp', 'video_author': '银河系讲解员', 'video_album': '首发', 'video_platform': '新浪短视频1123测试二百5_70_1', 'video_check_platform': '14', 'sub_table_name': 'sub_5_70', 'task_type': 1, 'search_key_words': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站'}, {'video2_title': '木筏求生联机-极限生存给海鸥建造一个家 这样不怕风吹雨淋了', 'video2_url': 'http://www.le.com/ptv/vplay/69990667.html', 'video2_author': '', 'video2_pubtime': '', 'video2_url_hash': '401ee7060eb562a1a88eb7b4793903b4', 'video2_platform': '乐视视频', 'video2_duration': 1122, 'video2_duration_str': '00:18:42', 'id': 826371, 'video_title': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站', 'video_url': 'http://weibo.com/5274804556/JtJzkBDJp', 'video_author': '银河系讲解员', 'video_album': '首发', 'video_platform': '新浪短视频1123测试二百5_70_1', 'video_check_platform': '14', 'sub_table_name': 'sub_5_70', 'task_type': 1, 'search_key_words': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站'}, {'video2_title': '大海解说 我的世界建造我的王国 泰坦生物可怕的毁图死机模组', 'video2_url': 'http://www.le.com/ptv/vplay/70677560.html', 'video2_author': '', 'video2_pubtime': '', 'video2_url_hash': 'f00194dec48e7d092e98c90772a591b6', 'video2_platform': '乐视视频', 'video2_duration': 635, 'video2_duration_str': '00:10:35', 'id': 826371, 'video_title': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站', 'video_url': 'http://weibo.com/5274804556/JtJzkBDJp', 'video_author': '银河系讲解员', 'video_album': '首发', 'video_platform': '新浪短视频1123测试二百5_70_1', 'video_check_platform': '14', 'sub_table_name': 'sub_5_70', 'task_type': 1, 'search_key_words': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站'}, {'video2_title': '面面解说Roblox怪物大亨！建造瘦长鬼影基地！专属武器收割灵魂？', 'video2_url': 'http://www.le.com/ptv/vplay/70282311.html', 'video2_author': '', 'video2_pubtime': '', 'video2_url_hash': 'd6a73e49a6e9b1a0ad2ee42670bffd1e', 'video2_platform': '乐视视频', 'video2_duration': 973, 'video2_duration_str': '00:16:13', 'id': 826371, 'video_title': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站', 'video_url': 'http://weibo.com/5274804556/JtJzkBDJp', 'video_author': '银河系讲解员', 'video_album': '首发', 'video_platform': '新浪短视频1123测试二百5_70_1', 'video_check_platform': '14', 'sub_table_name': 'sub_5_70', 'task_type': 1, 'search_key_words': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站'}, {'video2_title': '大海解说 我的世界建造我的王国 古代战争模组介绍', 'video2_url': 'http://www.le.com/ptv/vplay/70578787.html', 'video2_author': '', 'video2_pubtime': '', 'video2_url_hash': 'e5244a12c9150b9bd2c8aff447e021e8', 'video2_platform': '乐视视频', 'video2_duration': 722, 'video2_duration_str': '00:12:02', 'id': 826371, 'video_title': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站', 'video_url': 'http://weibo.com/5274804556/JtJzkBDJp', 'video_author': '银河系讲解员', 'video_album': '首发', 'video_platform': '新浪短视频1123测试二百5_70_1', 'video_check_platform': '14', 'sub_table_name': 'sub_5_70', 'task_type': 1, 'search_key_words': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站'}, {'video2_title': '小格解说 Roblox元素龙大亨：建造龙的世界！奇幻魔法武器大乱斗！', 'video2_url': 'http://www.le.com/ptv/vplay/69947499.html', 'video2_author': '', 'video2_pubtime': '', 'video2_url_hash': '14b662bff16d569bd5e0ddb2f103f1b8', 'video2_platform': '乐视视频', 'video2_duration': 1137, 'video2_duration_str': '00:18:57', 'id': 826371, 'video_title': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站', 'video_url': 'http://weibo.com/5274804556/JtJzkBDJp', 'video_author': '银河系讲解员', 'video_album': '首发', 'video_platform': '新浪短视频1123测试二百5_70_1', 'video_check_platform': '14', 'sub_table_name': 'sub_5_70', 'task_type': 1, 'search_key_words': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站'}, {'video2_title': '我的世界 钻石大陆 建造树屋 第68集', 'video2_url': 'http://www.le.com/ptv/vplay/69823222.html', 'video2_author': '', 'video2_pubtime': '', 'video2_url_hash': 'c340b3fe40ab7c46b8ddf66c03f6bebb', 'video2_platform': '乐视视频', 'video2_duration': 1273, 'video2_duration_str': '00:21:13', 'id': 826371, 'video_title': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站', 'video_url': 'http://weibo.com/5274804556/JtJzkBDJp', 'video_author': '银河系讲解员', 'video_album': '首发', 'video_platform': '新浪短视频1123测试二百5_70_1', 'video_check_platform': '14', 'sub_table_name': 'sub_5_70', 'task_type': 1, 'search_key_words': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站'}, {'video2_title': '这才叫建造界的高人！纯手工操作，野外生存界的扛把子！', 'video2_url': 'http://www.le.com/ptv/vplay/70596902.html', 'video2_author': '', 'video2_pubtime': '', 'video2_url_hash': '760dcf6814cd4ac53d2dfea32fc23f54', 'video2_platform': '乐视视频', 'video2_duration': 679, 'video2_duration_str': '00:11:19', 'id': 826371, 'video_title': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站', 'video_url': 'http://weibo.com/5274804556/JtJzkBDJp', 'video_author': '银河系讲解员', 'video_album': '首发', 'video_platform': '新浪短视频1123测试二百5_70_1', 'video_check_platform': '14', 'sub_table_name': 'sub_5_70', 'task_type': 1, 'search_key_words': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站'}, {'video2_title': '从零开始完全建造川崎两冲程变速卡丁车！', 'video2_url': 'http://www.le.com/ptv/vplay/70547620.html', 'video2_author': '', 'video2_pubtime': '', 'video2_url_hash': '65f712cce87923dca227c55dbf917291', 'video2_platform': '乐视视频', 'video2_duration': 721, 'video2_duration_str': '00:12:01', 'id': 826371, 'video_title': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站', 'video_url': 'http://weibo.com/5274804556/JtJzkBDJp', 'video_author': '银河系讲解员', 'video_album': '首发', 'video_platform': '新浪短视频1123测试二百5_70_1', 'video_check_platform': '14', 'sub_table_name': 'sub_5_70', 'task_type': 1, 'search_key_words': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站'}, {'video2_title': '面面解说 Roblox建造模拟器2！购买设计蓝图自己造飞机？', 'video2_url': 'http://www.le.com/ptv/vplay/70343106.html', 'video2_author': '', 'video2_pubtime': '', 'video2_url_hash': 'aaaa7de7e36743c18f3eee92012564f1', 'video2_platform': '乐视视频', 'video2_duration': 898, 'video2_duration_str': '00:14:58', 'id': 826371, 'video_title': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站', 'video_url': 'http://weibo.com/5274804556/JtJzkBDJp', 'video_author': '银河系讲解员', 'video_album': '首发', 'video_platform': '新浪短视频1123测试二百5_70_1', 'video_check_platform': '14', 'sub_table_name': 'sub_5_70', 'task_type': 1, 'search_key_words': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站'}, {'video2_title': '我的世界 钻石大陆 建造树屋 第70集', 'video2_url': 'http://www.le.com/ptv/vplay/69823099.html', 'video2_author': '', 'video2_pubtime': '', 'video2_url_hash': '9a8fa94515a56db5e3549e2635eb07ee', 'video2_platform': '乐视视频', 'video2_duration': 1244, 'video2_duration_str': '00:20:44', 'id': 826371, 'video_title': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站', 'video_url': 'http://weibo.com/5274804556/JtJzkBDJp', 'video_author': '银河系讲解员', 'video_album': '首发', 'video_platform': '新浪短视频1123测试二百5_70_1', 'video_check_platform': '14', 'sub_table_name': 'sub_5_70', 'task_type': 1, 'search_key_words': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站'}, {'video2_title': '我的世界 侏罗纪公园 建造牛圈 第21集', 'video2_url': 'http://www.le.com/ptv/vplay/69825937.html', 'video2_author': '', 'video2_pubtime': '', 'video2_url_hash': 'b91d6bb223cd32746d196c80bb83f963', 'video2_platform': '乐视视频', 'video2_duration': 1240, 'video2_duration_str': '00:20:40', 'id': 826371, 'video_title': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站', 'video_url': 'http://weibo.com/5274804556/JtJzkBDJp', 'video_author': '银河系讲解员', 'video_album': '首发', 'video_platform': '新浪短视频1123测试二百5_70_1', 'video_check_platform': '14', 'sub_table_name': 'sub_5_70', 'task_type': 1, 'search_key_words': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站'}, {'video2_title': 'Roblox农民模拟器！建造自己的农场！成为土豪？面面解说', 'video2_url': 'http://www.le.com/ptv/vplay/70345330.html', 'video2_author': '', 'video2_pubtime': '', 'video2_url_hash': 'c2d1584a73b2cf0576a2671a04bc6211', 'video2_platform': '乐视视频', 'video2_duration': 887, 'video2_duration_str': '00:14:47', 'id': 826371, 'video_title': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站', 'video_url': 'http://weibo.com/5274804556/JtJzkBDJp', 'video_author': '银河系讲解员', 'video_album': '首发', 'video_platform': '新浪短视频1123测试二百5_70_1', 'video_check_platform': '14', 'sub_table_name': 'sub_5_70', 'task_type': 1, 'search_key_words': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站'}, {'video2_title': 'Roblox油管大亨！建造youtube主播室赚取百万美金？面面解说', 'video2_url': 'http://www.le.com/ptv/vplay/70282782.html', 'video2_author': '', 'video2_pubtime': '', 'video2_url_hash': 'dd9cfc9819c9b330977a4f2cb7a06387', 'video2_platform': '乐视视频', 'video2_duration': 922, 'video2_duration_str': '00:15:22', 'id': 826371, 'video_title': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站', 'video_url': 'http://weibo.com/5274804556/JtJzkBDJp', 'video_author': '银河系讲解员', 'video_album': '首发', 'video_platform': '新浪短视频1123测试二百5_70_1', 'video_check_platform': '14', 'sub_table_name': 'sub_5_70', 'task_type': 1, 'search_key_words': '国际空间站是如何建造的？哪个小男孩不想亲手造一个空间站'}]
    mysql_save_to_current_result_table(info)
    exit(0)
    # 测试视频过滤的规则
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
        "confirm_key_words": "A班淑传奇",
        "filter_key_words_list": '花絮_采访_片头曲_片尾曲_主题曲_预告_插曲_发布会_翻唱_演唱_演奏_合唱_专访_合奏_bgm(大小写)_ost(大小写)_打call_cover_宣传_宣传视频_原唱_原曲_片花_穿帮_穿帮镜头_音乐_主题歌_原创音乐_剧透_mv_有声小说_片头_片尾',
    }

    info_list = [{'video2_title': '【111】景甜女汉子彪悍征服男猪脚', 'video2_url': 'https://www.acfun.cn/v/ac2537520',
                  'video2_author': 'kkkkkva', 'video2_pubtime': '2016-02-16', 'video2_url_hash': '3f362ce69a6f6b3b6841bc8c2d398043',
                  'video2_platform': 'AcFun', 'video2_duration': 81, 'video2_duration_str': '00:01:21'},
                 {'video2_title': '《班淑传奇》片花曝光 于正张巍再造励志传奇', 'video2_url': 'https://www.acfun.cn/v/ac13826829',
                  'video2_author': '剧兔吐剧RabbitTalks', 'video2_pubtime': '2020-03-14', 'video2_url_hash': '1ff28ce2044f37f4f0e08347aae9a564',
                  'video2_platform': 'AcFun', 'video2_duration': 643, 'video2_duration_str': '00:10:43'},
                 {'video2_title': '《a班淑传奇》幕后制作', 'video2_url': 'https://www.acfun.cn/v/ac13825770', 'video2_author': '剧兔吐剧RabbitTalks',
                  'video2_pubtime': '2020-03-14', 'video2_url_hash': '6427d328455037a4f63b5225946083fd', 'video2_platform': 'AcFun',
                  'video2_duration': 123, 'video2_duration_str': '00:02:03'},
                 {'video2_title': '《班淑传奇》片尾曲 景甜《心上人》', 'video2_url': 'https://www.acfun.cn/v/ac13836521', 'video2_author': '剧兔吐剧RabbitTalks',
                  'video2_pubtime': '2020-03-14', 'video2_url_hash': 'de649838b3a79d86608f13a25d74274c', 'video2_platform': 'AcFun',
                  'video2_duration': 129, 'video2_duration_str': '00:02:09'}]
    list_new_info = unit_result_clear_for_video(result_list=info_list,**kwags)
    print(list_new_info)
    print(len(list_new_info))
    exit(0)
    print(md5_use('appid=803DFBB483094BFCBBF78ADDFECE0622&novelid=1194NXG6LVbWMV5ZYZK7IPBRESK96GLPOHRM').upper()) # 02D8EDC32B1554BCCAC58BF6C707E48A
    exit(0)
    # redis_get_tasks_from_redis(task_name='tou_tiao_qin_quan_erro_task_set',db=4,task_numbers=2)
    # redis_check_set_already(result_list=[{"audio2_url_hash":1},{"audio2_url_hash":2},{"audio2_url_hash":3}])

    # 数据库插入设置
    # task = [{'audio2_albumName': 'Meditation & Sleep Music – Healing Sounds for Total Relax, Deep Sleep Music, Daily Yoga Meditation, Relaxing Music, Stress Relief', 'audio2_artistName': 'Bedtime Songs Sanctuary', 'audio2_songName': 'Moonlight Live (Therapy Music)', 'audio2_songId': 1809511249, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'xNY4k3bd564', 'audio2_url': 'https://www.xiami.com/song/xNY4k3bd564', 'audio2_url_hash': '1057fe7e8e9934e08fe2dc6d57dce36e', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': "What's moumoon?", 'audio2_artistName': 'moumoon', 'audio2_songName': 'moonlight (Live)', 'audio2_songId': 1803050970, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'xN7x80cb431', 'audio2_url': 'https://www.xiami.com/song/xN7x80cb431', 'audio2_url_hash': 'd4b6ae1c514330268ae045a7592171c1', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'SNH48 GROUP第四届偶像年度人气总决选Live版', 'audio2_artistName': 'SNH48', 'audio2_songName': 'Moonlight  (Live)', 'audio2_songId': 1796785067, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'bf2jaLN2f6ed', 'audio2_url': 'https://www.xiami.com/song/bf2jaLN2f6ed', 'audio2_url_hash': '05c81cc4ae3b93058ffaf32ff3b6cb10', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Return to Live', 'audio2_artistName': 'Labyrinth', 'audio2_songName': 'Moonlight (Live)', 'audio2_songId': 1807314392, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'xNPqFsc66b4', 'audio2_url': 'https://www.xiami.com/song/xNPqFsc66b4', 'audio2_url_hash': 'eaec78c4cbc66775a92c67facdbbf0b1', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Back in the Ring', 'audio2_artistName': 'Macadam Crocodile', 'audio2_songName': 'Moonlight (Live)', 'audio2_songId': 2100551574, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'yhFFdqdf2a5', 'audio2_url': 'https://www.xiami.com/song/yhFFdqdf2a5', 'audio2_url_hash': '68710e0966bc58f2e8f44fb6632a8f65', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'LOVE TRiCKY LIVE TOUR 2015～ヘルシーミュージックで体重減るしー～', 'audio2_artistName': '大塚愛', 'audio2_songName': 'MOONLIGHT (Live)', 'audio2_songId': 1776243162, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'mQXUNQ60230', 'audio2_url': 'https://www.xiami.com/song/mQXUNQ60230', 'audio2_url_hash': 'a0a442dfdb0cda599ed3cc71b98e655a', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': '创使者世界巡回演唱会 LIVE', 'audio2_artistName': '潘玮柏', 'audio2_songName': 'Moonlight (Live)', 'audio2_songId': 2101144915, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'yhIjzrd47c3', 'audio2_url': 'https://www.xiami.com/song/yhIjzrd47c3', 'audio2_url_hash': 'd5dc192ef6de8f3b98d16ae84f0beddb', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': '中国新说唱 第12期', 'audio2_artistName': '潘玮柏 / 袁娅维', 'audio2_songName': 'Moonlight (Live)', 'audio2_songId': 1805982933, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'mSYH3984120', 'audio2_url': 'https://www.xiami.com/song/mSYH3984120', 'audio2_url_hash': '6c9d3e901be8ad86e1327e9eada2bd12', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': '大音乐+超级现场 第1期', 'audio2_artistName': '潘玮柏', 'audio2_songName': 'Moonlight (Live)', 'audio2_songId': 1806915797, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'mTcCjL79506', 'audio2_url': 'https://www.xiami.com/song/mTcCjL79506', 'audio2_url_hash': '738e50ef58eedb75fe6ed58ef495e154', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': "EXO PLANET #3 - The EXO'rDIUM[dot]-Live Album", 'audio2_artistName': 'EXO', 'audio2_songName': '월광 (Moonlight) (Live)', 'audio2_songId': 1796915782, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'mSwEHm6728f', 'audio2_url': 'https://www.xiami.com/song/mSwEHm6728f', 'audio2_url_hash': 'a41ce5e76b74155e3c1bf9bf7ae59791', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'EXOLOGY CHAPTER 1: THE LOST PLANET', 'audio2_artistName': 'EXO', 'audio2_songName': '월광 (Moonlight) (Live)', 'audio2_songId': 1773811186, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'mQNIi069c17', 'audio2_url': 'https://www.xiami.com/song/mQNIi069c17', 'audio2_url_hash': '9ad7ffb0de6c6d66a8d3c924348b902e', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'SNH48 FAMILY GROUP 暨 SNH48出道五周年纪念演唱会 (上)', 'audio2_artistName': 'SNH48_7SENSES', 'audio2_songName': 'Moon Light (Live)', 'audio2_songId': 1801822822, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'b1sagXe42aeb', 'audio2_url': 'https://www.xiami.com/song/b1sagXe42aeb', 'audio2_url_hash': '31af957135addd4aeb83dcc5ba17066d', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'EXO PLANET #4 –The EℓyXiOn (dot)– Live Album', 'audio2_artistName': 'EXO', 'audio2_songName': '월광 (Moonlight)', 'audio2_songId': 1809781443, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'mToDDR615d4', 'audio2_url': 'https://www.xiami.com/song/mToDDR615d4', 'audio2_url_hash': '229345d70fa6204099633e1d97e3b451', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'THE PARADE ～30th anniversary～', 'audio2_artistName': 'BUCK-TICK', 'audio2_songName': 'MOON LIGHT (Live)', 'audio2_songId': 1806508338, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'bqx8Ndu39f24', 'audio2_url': 'https://www.xiami.com/song/bqx8Ndu39f24', 'audio2_url_hash': 'ec15411f57d94a415bd1c84cf4c50294', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': '国民美少女 第六期', 'audio2_artistName': '国民美少女', 'audio2_songName': 'Moon Light (Live)', 'audio2_songId': 1775689018, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'mQVAEc6c643', 'audio2_url': 'https://www.xiami.com/song/mQVAEc6c643', 'audio2_url_hash': '243f90c70ff99fe4dae98302b8afd61e', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'The Unheard Of Chyi', 'audio2_artistName': '齐豫', 'audio2_songName': 'Moonlight Flower (Live)', 'audio2_songId': 138726, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'CvyO44601', 'audio2_url': 'https://www.xiami.com/song/CvyO44601', 'audio2_url_hash': '1958ef82f8b18e3fdf526aab46eebb04', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'True Music 1st Flight Live 2003', 'audio2_artistName': '卢巧音', 'audio2_songName': 'Moonlight Shadow (Live)', 'audio2_songId': 132950, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'rvk4233c2', 'audio2_url': 'https://www.xiami.com/song/rvk4233c2', 'audio2_url_hash': '768cdc2a504b6848c8b5ef32058fa59a', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Live [Seventh Wave]', 'audio2_artistName': 'Suzanne Ciani', 'audio2_songName': 'Life in the Moonlight (Live)', 'audio2_songId': 2784954, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'RDWW67059', 'audio2_url': 'https://www.xiami.com/song/RDWW67059', 'audio2_url_hash': 'e55367bbc488a04d9b53527693894746', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'LIVE TOUR 2017 ON THE ROAD', 'audio2_artistName': '平井大', 'audio2_songName': 'MOONLIGHT SATELLITE (Live)', 'audio2_songId': 1803223477, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'xN8g0Nb45ad', 'audio2_url': 'https://www.xiami.com/song/xN8g0Nb45ad', 'audio2_url_hash': '084baeb847587467e3794522ff8c3ed1', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': "Ain't No Moonlight", 'audio2_artistName': 'Buck & Evans', 'audio2_songName': "Ain't No Moonlight (Live at Rockfield Studios)", 'audio2_songId': 1798158539, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'xNmQOpcbf74', 'audio2_url': 'https://www.xiami.com/song/xNmQOpcbf74', 'audio2_url_hash': 'ced723bbc51f69a703375316651117d7', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'MTV Unplugged in Athens', 'audio2_artistName': 'Scorpions', 'audio2_songName': 'Dancing with the Moonlight (MTV Unplugged) (Live)', 'audio2_songId': 1772341474, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'xL26BYc210a', 'audio2_url': 'https://www.xiami.com/song/xL26BYc210a', 'audio2_url_hash': 'a056a611f0294c44abc61f7a8140abb8', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'The Singles', 'audio2_artistName': 'The Doors', 'audio2_songName': 'Moonlight Drive (Live)', 'audio2_songId': 1796778704, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'mSwfcq71d1d', 'audio2_url': 'https://www.xiami.com/song/mSwfcq71d1d', 'audio2_url_hash': '5d802dc4017653c2a48ebbfe8ab7147c', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Sticky Fingers Live', 'audio2_artistName': 'The Rolling Stones', 'audio2_songName': 'Moonlight Mile (Live)', 'audio2_songId': 1774475574, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'xLB3MWb0f8b', 'audio2_url': 'https://www.xiami.com/song/xLB3MWb0f8b', 'audio2_url_hash': 'c3714bb0b7c1b01d8021302c67773345', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Video Games Live: Level 1', 'audio2_artistName': 'Slovak National Symphony Orchestra', 'audio2_songName': 'Castlevania Rock (Live): Beginning / Wicked Child / Vampire Killer / Moonlight Nocturne', 'audio2_songId': 1769186202, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'xLprM4bc935', 'audio2_url': 'https://www.xiami.com/song/xLprM4bc935', 'audio2_url_hash': 'c19abb499b9248f2e3df86c9e8692db9', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'In the Evening By the Moonlight', 'audio2_artistName': 'Nina Simone', 'audio2_songName': 'In the Evening By the Moonlight (Live)', 'audio2_songId': 1811415426, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'mTv4I05d7f8', 'audio2_url': 'https://www.xiami.com/song/mTv4I05d7f8', 'audio2_url_hash': '31342b4bee1327b5771394042c0075eb', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'FM Broadcasts Blondie & Iggy Pop', 'audio2_artistName': 'Blondie', 'audio2_songName': 'Moonlight Drive (Live)', 'audio2_songId': 2101195877, 'audio2_platform': '虾米音乐', 'audio2_songStringId': '9c3v3Pe295e', 'audio2_url': 'https://www.xiami.com/song/9c3v3Pe295e', 'audio2_url_hash': 'ab36547032e53748a399f4e5e9489ae7', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Best of Poland 1999', 'audio2_artistName': 'Mike Oldfield', 'audio2_songName': 'Moonlight Shadow (live)', 'audio2_songId': 1901398166, 'audio2_platform': '虾米音乐', 'audio2_songStringId': '8OXaYged0b4', 'audio2_url': 'https://www.xiami.com/song/8OXaYged0b4', 'audio2_url_hash': '7ca55c5f754f4ddd5d4c75b373caf1c1', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'FM Broadcasts Talking Heads & Blondie', 'audio2_artistName': 'Blondie', 'audio2_songName': 'Moonlight Drive (Live)', 'audio2_songId': 2100943889, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'nmWusv84f73', 'audio2_url': 'https://www.xiami.com/song/nmWusv84f73', 'audio2_url_hash': '0396757fb7ac2811ed545a13f77dbb48', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': '들국화 Live Concert', 'audio2_artistName': '들국화', 'audio2_songName': 'Moonlight Flower (Live)', 'audio2_songId': 1795413492, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'xNbuHs9cdc3', 'audio2_url': 'https://www.xiami.com/song/xNbuHs9cdc3', 'audio2_url_hash': '9ab94455c213f1175b66fab2f239f07d', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Best of Kitaro (4CD Box Set)', 'audio2_artistName': '喜多郎', 'audio2_songName': 'Heaven & Earth (Live)', 'audio2_songId': 1770410157, 'audio2_platform': '虾米音乐', 'audio2_songStringId': '8Gfzare5fc5', 'audio2_url': 'https://www.xiami.com/song/8Gfzare5fc5', 'audio2_url_hash': 'ee8c8aa7c3e64156b5d366ee3e8c0046', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'MoonLight.', 'audio2_artistName': '政学(Zed-X)', 'audio2_songName': 'Moonlight (Live)（翻自 lil MILK）', 'audio2_songId': 1458160303, 'audio2_songtime': '01:28', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1458160303', 'audio2_url_hash': '35c7d6bb8f73c5d940ee34ffee161e06', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': '中国新说唱 第12期', 'audio2_artistName': '潘玮柏/袁娅维', 'audio2_songName': 'Moonlight (Live)', 'audio2_songId': 1313107593, 'audio2_songtime': '03:15', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1313107593', 'audio2_url_hash': '6d61a736e6653616e7b35396c2383771', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Moonlight (Live)', 'audio2_artistName': 'Interdeer', 'audio2_songName': 'Moonlight (Live)', 'audio2_songId': 1458075409, 'audio2_songtime': '04:56', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1458075409', 'audio2_url_hash': 'd2afba1c63e7bdc45fa7296de4e4a293', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Moonlight (Live)', 'audio2_artistName': 'lil_kaiiii', 'audio2_songName': 'Moonlight (Live)（翻自 lil MILK）', 'audio2_songId': 1459745076, 'audio2_songtime': '01:23', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1459745076', 'audio2_url_hash': '2ace26cab74d21871758def7297f079f', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': '叁', 'audio2_artistName': 'Key_kan', 'audio2_songName': 'Moonlight(Live)（翻自 Lil Milk）', 'audio2_songId': 1457126622, 'audio2_songtime': '01:25', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1457126622', 'audio2_url_hash': '7325678a85b9f3e394e7f7aaed8a9501', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': '创使者世界巡回演唱会 LIVE', 'audio2_artistName': '潘玮柏', 'audio2_songName': 'Moonlight (Live)', 'audio2_songId': 1452805832, 'audio2_songtime': '03:36', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1452805832', 'audio2_url_hash': '0a8bb056889de2f2e61c5cc3e984e47b', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Legends - The Beatles (The Early Days)', 'audio2_artistName': 'The Beatles', 'audio2_songName': 'Mister Moonlight (Live)', 'audio2_songId': 1374771631, 'audio2_songtime': '02:20', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1374771631', 'audio2_url_hash': '1363223f8df6e54fcec1049c1d3ea569', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Legends - The Beatles (The Early Days)', 'audio2_artistName': 'The Beatles', 'audio2_songName': 'Mister Moonlight (Live at Star-Club, Hamburg, Germany)', 'audio2_songId': 1374771645, 'audio2_songtime': '02:18', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1374771645', 'audio2_url_hash': 'f190c16c5195a6846e46b110ae2fa365', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Moonlight(Live)', 'audio2_artistName': 'C_xxxL', 'audio2_songName': 'Moonlight(Live)（翻自 Lil Milk）', 'audio2_songId': 1457974730, 'audio2_songtime': '01:25', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1457974730', 'audio2_url_hash': '135e0ba109d26ff9d85e6f93f1575e12', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'One cold Winters Night', 'audio2_artistName': 'Kamelot', 'audio2_songName': 'Moonlight (live)', 'audio2_songId': 19012051, 'audio2_songtime': '05:10', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=19012051', 'audio2_url_hash': 'd82ba111e414f71d4591924bfe6b752c', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'moonlight', 'audio2_artistName': '音', 'audio2_songName': 'Moonlight(Live)（翻自 lil MILK）', 'audio2_songId': 1457522078, 'audio2_songtime': '01:25', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1457522078', 'audio2_url_hash': 'ef0b392bce31986de4c0778a46cf5c8b', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': '孤', 'audio2_artistName': 'Nick.', 'audio2_songName': 'Moonlight(Live)（翻自 Lil Milk）', 'audio2_songId': 1457312917, 'audio2_songtime': '01:25', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1457312917', 'audio2_url_hash': 'f420909d7a3ef958a8137df703631850', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': '片段', 'audio2_artistName': '额滴伟呀', 'audio2_songName': 'Moonlight(Live)（翻自 lil milk）', 'audio2_songId': 1458771411, 'audio2_songtime': '01:24', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1458771411', 'audio2_url_hash': '77129fc72f5acdfb58d54a1ce7aaccce', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': '翻唱杂集', 'audio2_artistName': 'Ych一寸灰', 'audio2_songName': 'Moonlight(Live)（翻自 lil MILK）', 'audio2_songId': 1457897122, 'audio2_songtime': '01:25', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1457897122', 'audio2_url_hash': '1b1b862b3cac4a871dbe81f76d9869c4', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'one', 'audio2_artistName': 'TK', 'audio2_songName': 'Moonlight(Live)（翻自 Lil Milk）', 'audio2_songId': 1457667652, 'audio2_songtime': '01:26', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1457667652', 'audio2_url_hash': '7bf759c0baf57218e90b948c719f9344', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': '口卡口卡热门翻唱合集', 'audio2_artistName': 'K.A咔咔', 'audio2_songName': 'Moonlight（咔咔live版）（翻自 lil MILK）', 'audio2_songId': 1458615328, 'audio2_songtime': '01:09', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1458615328', 'audio2_url_hash': 'a2349ad312daed8bdcc6c878cc2dda3c', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Moonlight', 'audio2_artistName': '咖喱盖盖', 'audio2_songName': 'Moonlight（Live）（翻自 lil MILK）', 'audio2_songId': 1457468688, 'audio2_songtime': '01:25', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1457468688', 'audio2_url_hash': 'd17049d4cbfc82d745001aebbd9b08b9', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': '翻唱', 'audio2_artistName': '#0871', 'audio2_songName': 'Moonlight（Live）（翻自 lil MILK）', 'audio2_songId': 1459407817, 'audio2_songtime': '01:26', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1459407817', 'audio2_url_hash': 'bbe6679cf62e2bdf716601845beb001b', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'RENDEZ-VOUS (Live)', 'audio2_artistName': '任炫植', 'audio2_songName': 'MOONLIGHT (Live)', 'audio2_songId': 1419790383, 'audio2_songtime': '04:28', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1419790383', 'audio2_url_hash': 'f18ec227a4e0c80d9d6771c6c88fcabd', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'A new Friend', 'audio2_artistName': 'Nina Simone', 'audio2_songName': 'In the Evening By the Moonlight (live)', 'audio2_songId': 1377228318, 'audio2_songtime': '06:09', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1377228318', 'audio2_url_hash': 'a1e0284c8d0a11011831c220e61ff256', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Preserve The Good', 'audio2_artistName': 'Nina Simone', 'audio2_songName': 'In the Evening By the Moonlight (live)', 'audio2_songId': 1348011334, 'audio2_songtime': '06:09', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1348011334', 'audio2_url_hash': 'd19f22bad326d2604259c476edf2613c', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'In the Evening By the Moonlight', 'audio2_artistName': 'Nina Simone', 'audio2_songName': 'In the Evening By the Moonlight (Live)', 'audio2_songId': 1346500378, 'audio2_songtime': '06:09', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1346500378', 'audio2_url_hash': '843ff602a1744287b7dc7d711cb5a088', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Express Yourself', 'audio2_artistName': 'Nina Simone', 'audio2_songName': 'In the Evening By the Moonlight (live)', 'audio2_songId': 1304683027, 'audio2_songtime': '06:09', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1304683027', 'audio2_url_hash': '1ed281def7b043fdeaef8ea3c52bb4d0', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Amusement Park', 'audio2_artistName': 'Nina Simone', 'audio2_songName': 'In the Evening By the Moonlight (live)', 'audio2_songId': 1304878182, 'audio2_songtime': '06:09', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1304878182', 'audio2_url_hash': 'fefc7fc4f17dd6d9dae00ec3df0e34c2', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Collect Seashells', 'audio2_artistName': 'Nina Simone', 'audio2_songName': 'In the Evening By the Moonlight (live)', 'audio2_songId': 1324361923, 'audio2_songtime': '06:09', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1324361923', 'audio2_url_hash': 'e55eadc73d47d058e8904b1be85b76ff', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Ice Landscape', 'audio2_artistName': 'Nina Simone', 'audio2_songName': 'In the Evening By the Moonlight (live)', 'audio2_songId': 1323644520, 'audio2_songtime': '06:09', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1323644520', 'audio2_url_hash': '41b72b193fb95849bf761be94b9aed50', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Christmas Stars', 'audio2_artistName': 'Nina Simone', 'audio2_songName': 'In The Evening By The Moonlight (Live Version)', 'audio2_songId': 1375291993, 'audio2_songtime': '06:09', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1375291993', 'audio2_url_hash': '5402c236c26c33f7657c1021f8a70c33', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Classic Jazz Icons - Nina Simone', 'audio2_artistName': 'Nina Simone', 'audio2_songName': 'In the Evening By the Moonlight (Live Version)', 'audio2_songId': 1315358426, 'audio2_songtime': '06:09', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1315358426', 'audio2_url_hash': 'd735e066e794a795c2e2a4b129283adc', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'The Jazz Masters - Nina Simone', 'audio2_artistName': 'Nina Simone', 'audio2_songName': 'In the Evening By the Moonlight (Live Version)', 'audio2_songId': 1316352398, 'audio2_songtime': '06:09', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1316352398', 'audio2_url_hash': '6c02c52bc27d19f2fea33f80b036e7a8', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'The Strange Fruit Collection (Forever Jazz)', 'audio2_artistName': 'Billie Holiday', 'audio2_songName': 'What a Little Moonlight Can Do (Live)', 'audio2_songId': 1323934858, 'audio2_songtime': '02:45', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1323934858', 'audio2_url_hash': '1eb11e6a48a45170afd8f8bfd22fe96d', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Still (Re-mastered Re-issues)', 'audio2_artistName': 'Joy Division', 'audio2_songName': 'Sister Ray (Live at the Moonlight Club, London April 1980) [2007 Remaster]', 'audio2_songId': 1349964504, 'audio2_songtime': '07:35', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1349964504', 'audio2_url_hash': '28082471c10f774bbacdfb768fa92e0d', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'SNH48 GROUP第四届偶像年度人气总决选 (Live版)', 'audio2_artistName': 'SNH48', 'audio2_songName': 'Moonlight (live)', 'audio2_songId': 507192442, 'audio2_songtime': '03:40', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=507192442', 'audio2_url_hash': 'c25c408017e0427197e043ac4f8de633', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'The Glenn Miller Carnegie Hall Concert (Live)', 'audio2_artistName': 'Glenn Miller', 'audio2_songName': 'Moonlight Serenade / Running Wild (Live)', 'audio2_songId': 556064198, 'audio2_songtime': '03:48', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=556064198', 'audio2_url_hash': 'e789f566632a481412149938566d40fa', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'The Glenn Miller Carnegie Hall Concert (Live)', 'audio2_artistName': 'Glenn Miller', 'audio2_songName': 'Bugle Call Rag / Moonlight Serenade (Live)', 'audio2_songId': 556066040, 'audio2_songtime': '04:37', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=556066040', 'audio2_url_hash': 'c7d842ce8c8735bc6942a22e16fa0539', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Live in Tokyo (So Much Music Too Little Time)', 'audio2_artistName': 'Frank Sinatra/Bill Miller Sextet', 'audio2_songName': 'Moonlight In Vermont', 'audio2_songId': 1328280659, 'audio2_songtime': '03:34', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1328280659', 'audio2_url_hash': '2cc560e5551791d60ab312522c54f38a', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Moonlight Crackles - Fire Sparkles', 'audio2_artistName': 'Lively Fire Nature Music', 'audio2_songName': 'Wonderful Fire Night', 'audio2_songId': 1456815851, 'audio2_songtime': '02:46', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1456815851', 'audio2_url_hash': 'dbc49afd9317cd019223bd2749e90c74', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Moonlight City - Fire and Nature Element Effects', 'audio2_artistName': 'Lively Flames Nature Music', 'audio2_songName': 'The Dreamland and Forest', 'audio2_songId': 1456829718, 'audio2_songtime': '02:28', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1456829718', 'audio2_url_hash': 'f512e7377eeef68a70fcd1524e228389', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'The Beauty of the Beach - White Noise Music for Healthy Living', 'audio2_artistName': 'Eternal Nature', 'audio2_songName': 'Moonlight and the Ocean', 'audio2_songId': 1456238706, 'audio2_songtime': '01:57', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1456238706', 'audio2_url_hash': '260b6726ae9d7336657c27e2137522b9', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Moonlight City - Fire and Nature Element Effects', 'audio2_artistName': 'Flames Seed Nature Sounds', 'audio2_songName': 'Live Streaming Water', 'audio2_songId': 1456837104, 'audio2_songtime': '02:13', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1456837104', 'audio2_url_hash': '2af610a41b30ac34cef866d37df4790f', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'In My Head', 'audio2_artistName': 'Lost Count', 'audio2_songName': 'Moonlight (Live)', 'audio2_songId': 1388484399, 'audio2_songtime': '05:36', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1388484399', 'audio2_url_hash': 'ba57d35e380943e37f7a75c045622206', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Mountain Tale', 'audio2_artistName': 'Pekka Tiilikainen & Beatmakers', 'audio2_songName': 'Moonlight (Live)', 'audio2_songId': 569316713, 'audio2_songtime': '02:24', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=569316713', 'audio2_url_hash': 'e1e8c4d19d1eea724c197195da3f2504', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Back in the Ring (Live)', 'audio2_artistName': 'Macadam Crocodile', 'audio2_songName': 'Moonlight (Live)', 'audio2_songId': 1445800659, 'audio2_songtime': '03:58', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1445800659', 'audio2_url_hash': 'e88ff0ccbcca685023cc92bc134974b8', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'John Dig**** (Live in Montreal)', 'audio2_artistName': 'Eagles & Butterflies', 'audio2_songName': 'Moonlight (Live)', 'audio2_songId': 1320231751, 'audio2_songtime': '08:04', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1320231751', 'audio2_url_hash': '1bc3e335552a4e636071efedf155c35c', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'John Dig**** (Live in Montreal)', 'audio2_artistName': 'Eagles & Butterflies', 'audio2_songName': 'Moonlight (Live)', 'audio2_songId': 1320235493, 'audio2_songtime': '08:04', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1320235493', 'audio2_url_hash': '889dbd54d93612d31cfe63dcf97835e4', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Vinyly Live Session', 'audio2_artistName': 'Yokan', 'audio2_songName': 'Moonlight (Live)', 'audio2_songId': 1323646478, 'audio2_songtime': '04:05', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1323646478', 'audio2_url_hash': '338a255ecc75be3bc2af698897031129', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Live Session - Vol.1', 'audio2_artistName': 'Full Nothing', 'audio2_songName': 'Moonlight (Live)', 'audio2_songId': 1443295286, 'audio2_songtime': '04:05', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1443295286', 'audio2_url_hash': '63966d3cba63d9bb9e687757f0a01020', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Return to Live', 'audio2_artistName': 'Labyrinth', 'audio2_songName': 'Moonlight (Live)', 'audio2_songId': 1419261598, 'audio2_songtime': '08:39', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1419261598', 'audio2_url_hash': 'e8c9ced7c48cdff6fd457aceafffbfbd', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': '1985 - 1990', 'audio2_artistName': 'Element of Crime', 'audio2_songName': 'Moonlight (Live)', 'audio2_songId': 39311069, 'audio2_songtime': '06:19', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=39311069', 'audio2_url_hash': '88497b0ab703d25fbc035f1d6845fb5e', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Live in Concert', 'audio2_artistName': 'National Academy Orchestra of Canada/Terra Lightfoot', 'audio2_songName': 'Moonlight (Live)', 'audio2_songId': 562969869, 'audio2_songtime': '03:46', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=562969869', 'audio2_url_hash': '333fc0171cfe21d75a7428d6c8295e81', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'John Digweed Live in Brooklyn New York', 'audio2_artistName': 'Bog', 'audio2_songName': 'Moonlight (Live)', 'audio2_songId': 1374666031, 'audio2_songtime': '07:36', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1374666031', 'audio2_url_hash': 'd411e4a1c982d3b6cd5b51f24a2896b4', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'The Remedy: Lethal Potion / Sovereign Remedy / Elixir Live', 'audio2_artistName': 'Elixir', 'audio2_songName': 'Moonlight (Live)', 'audio2_songId': 1437708981, 'audio2_songtime': '04:15', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1437708981', 'audio2_url_hash': '5d8c7862715a230476366dbaae050982', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'In the Evening By the Moonlight', 'audio2_artistName': 'Nina Simone', 'audio2_songName': 'Porgy (Live)', 'audio2_songId': 1346500377, 'audio2_songtime': '05:10', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1346500377', 'audio2_url_hash': '8cd40ce465795298cd3f3956981fdcf0', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'In the Evening By the Moonlight', 'audio2_artistName': 'Nina Simone', 'audio2_songName': 'Trouble in Mind (Live)', 'audio2_songId': 1346500376, 'audio2_songtime': '05:41', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1346500376', 'audio2_url_hash': '4fb7c82dfbc7ca8458c2415bc6623419', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'In the Evening By the Moonlight', 'audio2_artistName': 'Nina Simone', 'audio2_songName': "Nina's Blues (Live)", 'audio2_songId': 1346495510, 'audio2_songtime': '06:10', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1346495510', 'audio2_url_hash': 'be147a8bf9f39fa0e9468f5613540807', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'In the Evening By the Moonlight', 'audio2_artistName': 'Nina Simone', 'audio2_songName': 'Flo Me La (Live)', 'audio2_songId': 1346495509, 'audio2_songtime': '07:12', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1346495509', 'audio2_url_hash': 'd3659c5886f1a5b15acd5390aa4e7cb9', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'In the Evening By the Moonlight', 'audio2_artistName': 'Nina Simone', 'audio2_songName': "You'd Be So Nice to Come Home To (Live)", 'audio2_songId': 1346495508, 'audio2_songtime': '05:24', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1346495508', 'audio2_url_hash': 'adaf658d4ac928b2358c4f2ce0b34247', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'In the Evening By the Moonlight', 'audio2_artistName': 'Nina Simone', 'audio2_songName': 'Little Liza Jane (Live)', 'audio2_songId': 1346495507, 'audio2_songtime': '04:31', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1346495507', 'audio2_url_hash': 'a399f729b884b74562580a287334703a', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'The Essential Billie Holiday: Carnegie Hall Concert Recorded Live (Original Album plus Bonus)', 'audio2_artistName': 'Billie Holiday/Chico Hamilton Quintet', 'audio2_songName': 'What a Little Moonlight Can Do', 'audio2_songId': 1328321183, 'audio2_songtime': '02:48', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1328321183', 'audio2_url_hash': 'aa61449780228a75507588b746c54dbd', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'Living For The Moment', 'audio2_artistName': 'Les Paul And Mary Ford', 'audio2_songName': 'Moonlight And Shadows', 'audio2_songId': 1319235527, 'audio2_songtime': '02:55', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1319235527', 'audio2_url_hash': '0493ca40848312e30ba454002be2411a', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}, {'audio2_albumName': 'The Greatest Hits of Mr. B', 'audio2_artistName': 'Billy Eckstine', 'audio2_songName': 'Moonlight in Vermont (Live Version)', 'audio2_songId': 1315270003, 'audio2_songtime': '02:56', 'audio2_platform': '网易云音乐', 'audio2_url': 'https://music.163.com/#/song?id=1315270003', 'audio2_url_hash': 'bed6243ade94f20eeed8cf5c38b9c0ee', 'id': 26, 'audio_title': 'Moonlight (Live)', 'audio_url': 'https://y.qq.com/n/yqq/song/003B7rdt1WjPFp.html', 'audio_id': '003B7rdt1WjPFp', 'audio_author': 'lil milk', 'audio_album': '说唱听我的 第2期', 'audio_introduce': None, 'audio_platform': 'qq音乐', 'audio_check_platform': '0'}]
    # mysql_save_to_current_result_table(task)
    each = {'audio2_albumName': '爱已欠费', 'audio2_artistName': '王绍博', 'audio2_songName': '爱已欠费', 'audio2_songId': 2079503, 'audio2_platform': '虾米音乐', 'audio2_songStringId': 'OG0H4f556', 'audio2_url': 'https://www.xiami.com/song/OG0H4f556', 'audio2_url_hash': '9d4d743eb974bd003a1cd92b61bebbd1', 'id': 279907, 'audio_title': '爱已欠费', 'audio_url': 'https://y.qq.com/n/yqq/song/004B8JUC3d1Qb1.html', 'audio_author': '王绍博', 'audio_album': None, 'audio_platform': '独家歌单27w第一批3w', 'audio_check_platform': '1_2_3', 'sub_table_name': 'sub_1_25_base', 'task_type': 2, 'search_key_words': '爱已欠费', 'qingquan_flag': 1}
    ti = "insert into {}(audio_flag_str1,audio_flag_str2,title_similar_number,author_name_similar_number,yangben_URL,yangben_title,yangben_author_name,yangben_text,qinquan_text,qinquan_title,qinquan_author_name,qinquan_URL,qinquan_url_hash,qinquan_platform,yangben_platform,t,qinquan_type,qingquan_flag,flag_int,t_timestamp,qinquan_id_str,yangben_task_id) values('{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}','{}')".format(
        "table_name", timestamp_strftime("%Y%m%d"), each["search_key_words"],
        str_similar(each["audio2_songName"], each["audio_title"]),
        str_similar(each["audio_author"], each["audio2_artistName"]), each["audio_url"],
        pymysql.escape_string(each["audio_title"]), pymysql.escape_string(each["audio_author"]),
        pymysql.escape_string(each["audio_album"]), pymysql.escape_string(each["audio2_albumName"]),
        pymysql.escape_string(each["audio2_songName"]), pymysql.escape_string(each["audio2_artistName"]),
        each["audio2_url"], str(each["id"]) + "|" + each["audio2_url_hash"],
        each["audio2_platform"], each["audio_platform"], "now_time", 2, each["qingquan_flag"],
        each["id"], "now_time", each["audio2_songId"], each["id"])
    print(ti)
    exit(0)
    # 比较 简洁的判读 原创和翻唱
    each = {
        "audio_title":"安和桥",
        "audio_author":"宋东野",
        "audio_album": "安和桥北",
        "audio2_artistName":"李嘉宁",
        "audio2_albumName":"安和桥北",
        "audio2_songName": "安和桥 (Cover 宋东野)",


    }
    print(judge_song_type_easy(each))