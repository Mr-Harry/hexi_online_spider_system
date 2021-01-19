# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/7/1
######### 音频脚本
from audio_search_unit import audio_function_unit # 音频动态导入文件
from video_search_unit import video_function_unit # 视频动态导入文件
from novel_search_unit import novel_function_unit # 小说动态导入文件
from engine_search_unit import engine_function_unit # 搜索引擎动态导入文件
from cartoon_search_unit import cartoon_function_unit # 搜索引擎动态导入文件
########## 视频脚本

# 服务上线（测试机）
Config_of_audio_infringement = {
    # 清洗视频标题的列表
    "clear_video_title_way_list":["|","/","-"," ",",",".","，","。","<",">","《","》","？","?","[","]","【","】","：",
                                  "；",":",";","、","!","！","「","」","","~","`","@","#","$","%","^","&","*","(",")",
                                  "_","+","-","=","·","'",'"','”'],
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







    # 普通版10/秒
    # "proxyHost" : "61.132.93.14",
    # "proxyPort" : "6442",
    # # 代理隧道验证信息
    # "proxyUser" : "16BEFXMP",
    # "proxyPass" : "708166",
    # 加强版 5/秒
    # "proxyHost" : "115.227.49.100",
    # "proxyPort" : "6445",
    # # 代理隧道验证信息
    # "proxyUser" : "16CGVJXK",
    # "proxyPass" : "476720",
    # 加强版 10/秒
    "proxyHost": "115.227.49.100",
    "proxyPort": "6446",
    # 代理隧道验证信息
    "proxyUser": "16YZSZLD",
    "proxyPass": "039923",

    "search_audio_step":0.5, # 查询音乐平台侵权的列表搜索比例（一页10条数据取其中百分之多少）
    "redis_host": '121.196.126.218',  #
    # "redis_passwd": "7e6d8d12c59cecdb", # 本机器未设置
    # "redis_port": 55379,
    "redis_passwd": "7e6d8d12c59cecdb", # 本机器未设置
    "redis_port": 56379,
    "redis_task_db":1, # 音频redis 保存
    "redis_task_set_qq_name":"audio_task_of_qq_json_set", # 存储任务的json格式到集合中
    "redis_task_set_qq_name_zhuanxiang":"redis_task_set_qq_name_zhuanxiang", # 专项的队列
    "redis_task_set_qq_name_bendi_test":"redis_task_set_qq_name_bendi_test__", # 本地测试的队列
    "redis_task_set_qq_name_bendi_test_lpy":"redis_task_set_qq_name_bendi_test_lpy", # 本地测试的队列 lpy专属
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




# 本地测试配置
# Config_of_audio_infringement = {
#
#     "wangyiyun_search_offset":{"start":0,"end":1,"pagesize":30},# 0 开始 网易云
#     "xi_ma_la_ya":{"start":1,"end":2,"pagesize":30},# 0 开始 喜马拉雅
#     "xiami_search_offset":{"start":1,"end":2,"pagesize":30},# 1 开始 虾米音乐
#     "qianqian_search_offset":{"start":0,"end":1,"pagesize":20},# 0 开始 翻页pagesize*offset 千千音乐
#     "qingka_search_offset":{"start":0,"end":1,"pagesize":20},# 0 开始 翻页pagesize*offset 千千音乐
#
#     # 10/秒
#     "proxyHost" : "61.132.93.14",
#     "proxyPort" : "6442",
#     # 代理隧道验证信息
#     "proxyUser" : "16BEFXMP",
#     "proxyPass" : "708166",
#
#     "redis_host": "localhost",  #
#     # "redis_passwd": "7e6d8d12c59cecdb", # 本机器未设置
#     # "redis_port": 55379,
#     "redis_passwd": "7e6d8d12c59cecdb", # 本机器未设置
#     "redis_port": 55379,
#     "redis_task_db":1, # 音频redis 保存
#     "redis_task_set_qq_name":"audio_task_of_qq_json_set", # 存储任务的json格式到集合中
#     "redis_task_set_qq_name_zhuanxiang": "redis_task_set_qq_name_zhuanxiang",  # 专项的队列

#     "redis_md5_set_result_url":"audio_md5_url_set", # 存储侵权音频url的md5到集合里 （如果存在集合里就不保存了）
#
#     "mysql_port": 3306,
#     "mysql_username": 'root',  # 用户名 本地是root Xueyiyang
#     "mysql_userpwd": 'Xueyiyang',  # 用户密码
#     # test
#     "mysql_host": 'localhost',  # 本地地址 localhost
#     "mysql_db": "hexi_qinquan_task_2020_all",  # 数据库名称
#     "mysql_task_qq_table":"audio_task2020",  # 音频任务表 qq音乐先用这个
#     "mysql_result_table_name":"result_data_normal_",  # 音频结果表 后面拼接当天的时间 20200702
#     "mysql_result_table_name_test":"", # 如果该配置为空 默认存到当天数据表格
#
#     "song_name_similar":0.16, # 两个歌曲的名字的相似度 来判断这歌有没有必要判断
#     "procces_stop_time":600, # 如果任务队列为空 暂停多久
#     "task_numbers":2, # 每次获取的任务
#     "task_process":4, # 多进程
#     "task_thread":2, # 多线程
# "__audio_search_function__": audio_function_unit.__audio_search_function__,  # 音频动态导入
# "__video_search_function__": video_function_unit.__video_search_function__,  # 视频动态导入
#
#
# }
#
#
#
#
#
# 代理勿动

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

if __name__ == '__main__':
    print(Config_of_audio_infringement["__video_search_function__"])