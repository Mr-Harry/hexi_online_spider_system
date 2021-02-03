# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/7/1
######### 音频脚本
import json

import redis

from audio_search_unit import audio_function_unit # 音频动态导入文件
from video_search_unit import video_function_unit # 视频动态导入文件
from novel_search_unit import novel_function_unit # 小说动态导入文件
from engine_search_unit import engine_function_unit # 搜索引擎动态导入文件
from cartoon_search_unit import cartoon_function_unit # 搜索引擎动态导入文件

Redis_Config = {
    "redis_host": '121.196.126.218',  #
    # "redis_passwd": "7e6d8d12c59cecdb", # 本机器未设置
    # "redis_port": 55379,
    "redis_passwd": "7e6d8d12c59cecdb",  # 本机器未设置
    "redis_port": 56379,
    "redis_struct_db": 0,  # 保存抓取队列的库

}
# 动态调用的redis 名称
Spider_Struct_Dic = "Spider_Struct_Dic"  # 从队列获得抓取队列的key 名称

def redis_get_spider_struct_key_info(task_name=Spider_Struct_Dic,
                            host=Redis_Config["redis_host"], port=Redis_Config["redis_port"], decode_responses=True,
                                            db=Redis_Config["redis_struct_db"], password=Redis_Config["redis_passwd"])->list:
    con = redis.Redis(host=host, port=port, decode_responses=decode_responses, db=db, password=password)
    info = con.get(task_name)
    # print(info,"asdfasdfasdf")
    con.close()
    if info:
        return eval(info)
    else:
        return {}

########## 视频脚本
# audio_task_of_qq_json_set = redis_get_spider_struct_key_info().get("audio_task_of_qq_json_set",
#                                                                  "audio_task_of_qq_json_set")  # 存储任务的json格式到集合中
# redis_task_set_qq_name_zhuanxiang = redis_get_spider_struct_key_info().get("audio_task_of_qq_json_set",
#                                                                             "redis_task_set_qq_name_zhuanxiang")  # 专项的队列
# redis_task_set_qq_name_bendi_test = "task_search_lpy_test6",  # 本地测试的队列
# redis_task_set_qq_name_bendi_test_lpy = redis_get_spider_struct_key_info().get("audio_task_of_qq_json_set",
#                                                                                 "redis_task_set_qq_name_bendi_test_lpy")  # 新增抓取队列 1
# redis_task_set_qq_name_bendi_test_lpy_ = redis_get_spider_struct_key_info().get("audio_task_of_qq_json_set",
#                                                                                  "redis_task_set_qq_name_bendi_test_lpy_")  # 新增抓取队列 2
# redis_task_set_qq_name_bendi_test_lpy__ = redis_get_spider_struct_key_info().get("audio_task_of_qq_json_set", "redis_task_set_qq_name_bendi_test_lpy__")  # 新增抓取队列 3

# 服务上线（测试机）
Config_of_audio_infringement = {
    # 清洗视频标题的列表
    "clear_video_title_way_list":["|","/","-"," ",",",".","，","。","<",">","《","》","？","?","[","]","【","】","：",
                                  "；",":",";","、","!","！","「","」","","~","`","@","#","$","%","^","&","*","(",")",
                                  "_","+","-","=","·","'",'"','”','...'],
    ######################
    # 关于音乐平台的配置信息 （将来是字典操作）
    "wangyiyun_search_offset":{"start":0,"end":1,"pagesize":30,"start_page":0},# 0 开始 网易云
    "xi_ma_la_ya":{"start":1,"end":2,"pagesize":30,"start_page":1},# 0 开始 喜马拉雅
    "xiami_search_offset":{"start":1,"end":2,"pagesize":30,"start_page":1},# 1 开始 虾米音乐
    "qianqian_search_offset":{"start":0,"end":1,"pagesize":20,"start_page":0},# 0 开始 翻页pagesize*offset 千千音乐
    "qingka_search_offset":{"start":0,"end":1,"pagesize":20,"start_page":0},# 0 开始 翻页pagesize*offset 千千音乐
    ######################

    ######################
    # 视频的配置信息
    ######################

    # ######################
    # 小说的配置信息
    ######################

    # ######################
    # 图文的配置信息
    ######################







    # 加强版 10/秒
    "proxyHost": "u4748.10.tp.16yun.cn",
    "proxyPort": "6446",
    # 代理隧道验证信息
    "proxyUser": "16YZSZLD",
    "proxyPass": "039923",
    # 5/秒
    # "proxyHost": "u4748.10.tn.16yun.cn",
    # "proxyPort": "6442",
    # # 代理隧道验证信息
    # "proxyUser": "16BEFXMP",
    # "proxyPass": "708166",

    "search_audio_step":0.5, # 查询音乐平台侵权的列表搜索比例（一页10条数据取其中百分之多少）
    "redis_host": Redis_Config["redis_host"],  #
    # "redis_passwd": "7e6d8d12c59cecdb", # 本机器未设置
    # "redis_port": 55379,
    "redis_passwd": Redis_Config["redis_passwd"], # 本机器未设置
    "redis_port": Redis_Config["redis_port"],
    "redis_task_db":1, # 音频redis 保存
    "redis_struct_db":Redis_Config["redis_struct_db"], # 保存抓取队列的库
    "redis_task_set_qq_name":redis_get_spider_struct_key_info().get("audio_task_of_qq_json_set",
                                                                 "audio_task_of_qq_json_set") , # 存储任务的json格式到集合中
    "redis_task_set_qq_name_zhuanxiang":redis_get_spider_struct_key_info().get("redis_task_set_qq_name_zhuanxiang",
                                                                            "redis_task_set_qq_name_zhuanxiang"), # 专项的队列
    "redis_task_set_qq_name_bendi_test":"redis_task_set_qq_name_bendi_test", # 本地测试的队列
    "redis_task_set_qq_name_bendi_test_lpy":redis_get_spider_struct_key_info().get("redis_task_set_qq_name_bendi_test_lpy",
                                                                                "audio_task_of_qq_json_set") , # 新增抓取队列 1
    "redis_task_set_qq_name_bendi_test_lpy_":redis_get_spider_struct_key_info().get("redis_task_set_qq_name_bendi_test_lpy_",
                                                                                "audio_task_of_qq_json_set"), # 新增抓取队列 2
    "redis_task_set_qq_name_bendi_test_lpy__":redis_get_spider_struct_key_info().get("redis_task_set_qq_name_bendi_test_lpy__",
                                                                                "audio_task_of_qq_json_set"), # 新增抓取队列 3
    "redis_md5_set_result_url":"audio_md5_url_set", # 存储侵权音频url的md5到集合里 （如果存在集合里就不保存了）

    "mysql_port": 55306,
    "mysql_username": 'root',  # 用户名 本地是root Xueyiyang
    "mysql_userpwd": 'Xueyiyang',  # 用户密码
    # test
    "mysql_host": '121.196.126.218',  # 本地地址 localhost
    "mysql_db": "migrate_test",  # 数据库名称
    "mysql_task_qq_table":"audio_task2020",  # 音频任务表 qq音乐先用这个
    "mysql_result_table_name":"result_data_normal_",  # 音频结果表 后面拼接当天的时间 20200702
    "mysql_result_table_name_test":"", # 如果该配置为空 默认存到当天数据表格

    "song_name_similar":0.21, # 两个歌曲的名字的相似度 来判断这歌有没有必要判断
    "procces_stop_time":600, # 如果任务队列为空 暂停多久

    ############## 本地做测试的时候用 每次只取一个
    # "task_numbers":2, # 每次获取的任务 432
    # "task_process":1, # 多进程
    # "task_thread":1, # 多线程
    ##############

   "task_numbers":4, # 每次获取的任务 432
    "task_process":3, # 多进程
    "task_thread":2, # 多线程

    "__audio_search_function__":audio_function_unit.__audio_search_function__, # 音频动态导入
    "__video_search_function__":video_function_unit.__video_search_function__, # 视频动态导入
    "__graphic_search_function__":video_function_unit.__video_search_function__, # 图文动态导入
    "__novel_search_function__":novel_function_unit.__novel_search_function__, # 小说动态导入
    "__engine_search_function__":engine_function_unit.__engine_search_function__, # 小说动态导入
    "__cartoon_search_function__":cartoon_function_unit.__cartoon_search_function__, # 漫画动态导入
}




proxy = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
    "host": Config_of_audio_infringement["proxyHost"],
    "port": Config_of_audio_infringement["proxyPort"],
    "user": Config_of_audio_infringement["proxyUser"],
    "pass": Config_of_audio_infringement["proxyPass"],
}
proxies = {
    "http": proxy,
    "https": proxy,
}
config = Config_of_audio_infringement


# 测试使用配置
Test_Config_Setting = {
                    # 添加测试使用的代理 5/秒
                    # 5/秒
                    "proxyHost": "61.132.93.14",
                    "proxyPort": "6442",
                    # 代理隧道验证信息
                    "proxyUser": "16BEFXMP",
                    "proxyPass": "708166",

                    # 每种类型对应的配置路径
                    "type_value_dic" :{
                                    # type>int {调用关键词 对应的配置文件}

                                    # 音频抓取对应的参数
                                    2 : {"search_songs":config["__audio_search_function__"]},
                                    # 视频抓取对应的参数
                                    1 : {"search_songs":config["__video_search_function__"]},
                                    # 图文抓取对应的参数
                                    # __graphic_search_function__ = config["__graphic_search_function__"],
                                    # 小说抓取对应的参数
                                    4 : {"search_novels":config["__novel_search_function__"]},
                                    # 搜索引擎取对应的参数
                                    5 : {"search_engines":config["__engine_search_function__"]},
                                    # 漫画抓取对应的参数
                                    7 : {"search_normals":config["__cartoon_search_function__"]},

                                    },
                    # 邮箱服务
                    "smtpserver" : 'smtp.163.com',
                    # 用户名称
                    "username" :'18188108851@163.com',
                    # 用户密码 开启功能后的密码 非正常密码
                    "password" :'BPJBNWIMXOWMKBEB',
                    # 发送人
                    "sender" :'18188108851@163.com',
                    # 接受人
                    "receiver" :['1287986063@qq.com', 'daybreak_xyy@163.com','1311641164@qq.com',
                                 'wivianemail@163.com','Z2281102662@163.com'],
                    # 主题
                    "subject" :'hexi_online_spider_v001 TEST UNIT',
                    # 错误回复格式
                    "erro_text_info":{
                                1:"和晞社区 \n没有发现错误 可忽略！！！\n",
                                2:"和晞社区 \n看吧果然有问题 查看附件 是那个平台那个负责的脚本！！！\n",
                                3:"",
                                },
                    # 需要检测的类型
                    # [1,2,4,5,7]
                    # 2 音频
                    # 1 视频
                    # 4 小说
                    # 7 漫画
                    # 5 搜索
                    "test_type_list" : [1,2,4,5,7],
                    # "test_type_list" : [7],
                    # 视频排除的平台
                    "video_no_check" : [18, 19, 200, 201],
                    # 音频排除的平台
                    "audio_no_check" : [],
                    # 图文排除的平台
                    "graphic_no_check" : [],
                    # 卡通排除的平台
                    "cartoon_no_check" : [],
                    # 小说排除的平台
                    "novel_no_check" : [],
                    # 搜索引擎排除的平台
                    "engine_no_check" : [],
}


if __name__ == '__main__':
    print(Config_of_audio_infringement)
    print(Config_of_audio_infringement["__video_search_function__"])
    # """:arg
    
    i = {
    "redis_task_set_qq_name":"audio_task_of_qq_json_set", # 存储任务的json格式到集合中
    "redis_task_set_qq_name_zhuanxiang":"redis_task_set_qq_name_zhuanxiang", # 专项的队列
    "redis_task_set_qq_name_bendi_test":"redis_task_set_qq_name_bendi_test__", # 本地测试的队列
    "redis_task_set_qq_name_bendi_test_lpy":"redis_task_set_qq_name_bendi_test_lpy", # 新增抓取队列 1
    "redis_task_set_qq_name_bendi_test_lpy_":"redis_task_set_qq_name_bendi_test_lpy_", # 新增抓取队列 2
    "redis_task_set_qq_name_bendi_test_lpy__":"xxxxxxxxxxx", # 新增抓取队列 3

    }
    # "redis_task_set_qq_name_bendi_test_lpy__":"redis_task_set_qq_name_bendi_test_lpy__", # 新增抓取队列 3
    #
    # """