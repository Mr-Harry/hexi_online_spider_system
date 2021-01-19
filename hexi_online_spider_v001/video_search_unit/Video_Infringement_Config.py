# -*- coding:utf-8 -*- #
# I don't like the world. I just like you
# author : pyl owo,
# time : 2020/10/9
from Audio_Infringement_Config import Config_of_audio_infringement as config
config_of_video = {
    # 爬取页面配置
    # 秒拍
    "video_search_offset":{"start": 1, "end": 2, "pagesize": 20,"start_page":0},

    # 视频爬取类型总配置
    "video_search_type_default": 0,  # str "0_1_2"格式 为空时使用对应爬虫的默认爬取类型
    "video_search_type_list": [
        0,  # 全部
        1,  # 爬虫默认爬取类型
        2,  # 视频
        3,  # 电影
        4,  # 电视剧
        5,  # 直播
        6,  # 综艺
        9,  # 其他
    ],
    "video_search_duration_default": 0,
    "video_search_duration_list": [
        0, # 全部
        1, # 0-10分钟
        2, # 10-30
        3, # 30-60
        4, # 60 +
    ],

    # 各平台配置
    # 爱奇异爬虫设置
    "aiqiyi_video_search_offset": {"pagesize": 20, "start_page": 1},
    # 哔哩哔哩爬虫配置
    "bilibili_video_search_offset": {"pagesize": 20, "start_page": 1},
    "bilibili_search_parms_types": {
        1: "video",  # 视频
        # 2: "media_ft",  # 影视  (需要修改)
        # 3: "media_bangumi",  # 番剧  (需要修改)
        # # 4: "article",  # 文章
        # # 5: "topic",  # 话题
        # # 6: "bili_user",  # 用户
    },
    # 腾讯爬虫配置
    "tengxun_video_search_offset": {"pagesize": 15, "start_page": 1},
    # 抖音
    "douyin_video_search_offset": {"pagesize": 10, "start_page": 0},
    # 快手
    "kauishou_video_search_offset": {"pagesize": 20, "start_page": 0},
    # 西瓜视频
    "xigau_video_search_offset": {"pagesize": 12, "start_page": 0}, # 翻页 每页12条
    # Acfun爬虫设置
    "acfun_video_search_offset": {"pagesize": 20, "start_page": 1},
    # 好看视频爬虫设置
    "haokan_video_search_offset": {"pagesize": 10, "start_page": 1},
    # 咪咕视频爬虫设置
    "migu_video_search_offset": {"pagesize": 10, "start_page": 1},
    # 搜狐视频爬虫设置
    "souhu_video_search_offset": {"pagesize": 10, "start_page": 1},
    # 网易云音乐视频爬虫设置  只一页
    "wangyiyun_video_search_offset":{"start":0, "end":1, "pagesize":20, "start_page":0},
    # 美拍爬虫设置
    "meipai_video_search_offset": {"pagesize": 20, "start_page": 1},
    # 优酷爬虫设置
    "youku_video_search_offset": {"pagesize": 30, "start_page": 1},
    # 全民小视频爬虫设置
    "quanminxiaoshipin_video_search_offset": {"pagesize": 10, "start_page": 0},
    # 乐视视频爬虫设置
    "leshi_video_search_offset": {"pagesize": 25, "start_page": 1},
    # PPTV爬虫设置
    "pptv_video_search_offset": {"pagesize": 10, "start_page": 1},
    # 芒果tv爬虫设置
    "mangguotv_video_search_offset": {"pagesize": 10, "start_page": 1},
    # 凤凰视频爬虫设置
    "fenghuang_video_search_offset": {"pagesize": 10, "start_page": 1},
    # 土豆视频爬虫设置
    "tudou_video_search_offset": {"pagesize": 20, "start_page": 1},
    # 微博视频爬虫设置
    "weibo_video_search_offset": {"pagesize": 10, "start_page": 1},

    # > 直播
    # 战旗直播爬虫设置
    "zhanqi_video_search_offset": {"pagesize": 20, "start_page": 1},
    # 战旗直播爬虫设置
    "liujianfang_video_search_offset": {"pagesize": 25, "start_page": 1},
    # 代理
    # 10/秒
    "proxyHost": config["proxyHost"],
    "proxyPort": config["proxyPort"],
    # 代理隧道验证信息
    "proxyUser": config["proxyUser"],
    "proxyPass": config["proxyPass"],
}
#
# config_of_video = {
#     # 爬取页面配置
#
#     # 视频爬取类型总配置
#     "video_search_type_default": 0,  # str "0_1_2"格式 为空时使用对应爬虫的默认爬取类型
#     "video_search_type_list": [
#         0,  # 全部
#         1,  # 爬虫默认爬取类型
#         2,  # 视频
#         3,  # 电影
#         4,  # 电视剧
#         5,  # 直播
#         9,  # 其他
#     ],
#     # 虎牙爬虫配置
#     "huya_video_search_offset": {"start": 1, "end": 1, "pagesize": 20},
#     # 斗鱼爬虫配置
#     # cate1_list   3：星秀娱乐   109文娱课堂
#     "douyu_video_search_offset": {"start": 1, "end": 1, "pagesize": 30,
#                                   "cate1_list": [3, 109]},
#     # # 以下加全局配置
#     # 哔哩哔哩爬虫配置
#     "bilibili_video_search_offset": {"start": 1, "end": 1, "pagesize": 20,
#                                      },
#     "bilibili_video_search_type_list": {
#         0: [0, 1, 2],  # 全部
#         1: [0, 1, 2],  # 爬虫默认爬取类型
#         2: [0, ],  # 视频
#         3: [1, ],  # 电影
#         4: [2, ],  # 电视剧
#         9: [],  # 其他
#     },
#     "bilibili_search_type":{
#         0: "video",  # 视频
#         1: "media_ft",  # 影视
#         2: "media_bangumi",  # 番剧
#         # 3: "article",  # 文章
#         # 4: "topic",  # 话题
#         # 5: "bili_user",  # 用户
#     },
#     # 腾讯爬虫配置
#     "tengxun_video_search_offset": {"start": 1, "end": 1, "pagesize": 15,
#                                     "search_type_list": [0, 1, 2]},
#     "tengxun_video_search_type_list": {
#         0: [0, ],  # 全部
#         1: [0, ],  # 爬虫默认爬取类型
#         2: [0, ],  # 视频
#         3: [0, ],  # 电影
#         4: [0, ],  # 电视剧
#         9: [0, ],  # 其他
#     },
#     "tengxun_search_type":{
#         0: "",  # 全部视频（包括短视频，电影，电视剧，以及其他）
#         1: "",  # 短视频
#         2: "",  # 电影
#         3: "",  # 电视剧
#     },
#     # 爱奇异爬虫设置
#     "aiqiyi_video_search_offset": {"start": 1, "end": 1, "pagesize": 20,
#                                     "search_type_list": [0, 1, 2]},
#     "aiqiyi_video_search_type_list": {
#         0: [0,],  # 全部
#         1: [0,],  # 爬虫默认爬取类型
#         2: [1,],  # 视频
#         3: [2, 3 ],  # 电影
#         4: [2, 3 ],  # 电视剧
#
#         9: [0,],  # 其他
#     },
#     "aiqiyi_search_type":{
#         0: "",  # 全部
#         1: "",  # 短视频
#         2: "",  # 电影
#         3: "",  # 电视剧
#     },
#     # # 优酷
#     # "youku_video_search_offset": {"start": 1, "end": 1, "pagesize": 20,
#     #                                 "search_type_list": [0, 1, 2]},
#     # "youku_video_search_type_list": {
#     #     0: [0,],  # 全部
#     #     1: [0,],  # 爬虫默认爬取类型
#     #     2: [0,],  # 视频
#     #     3: [0,],  # 电影
#     #     4: [0,],  # 电视剧
#     #     9: [0,],  # 其他
#     # },
#     # "youku_search_type":{
#     #     0: "",  # 全部
#     # },
#
#     # 优酷
#     "youku_video_search_offset": {"start": 1, "end": 1, "pagesize": 20,},
#     "youku_video_search_type_list": {
#         0: [0, 1, 2],  # 全部
#         1: [0, 1, 2],  # 爬虫默认爬取类型
#         2: [1],  # 视频
#         3: [2],  # 电影
#         4: [2],  # 电视剧
#         9: [0, 1, 2],  # 其他
#     },
#     "youku_search_type":{
#         0: "",  # 全部
#         1: "",  # 短视频
#         2: "",  # 电影电视剧
#     },
#     # ######
#     # 以下视频搜索使用v2版本的类型选择：
#         #  直接使用总的video_search_type_list字典中的类别
#         #     "video_search_type_default": "",  # str "0_1_2"格式 为空时使用对应爬虫的默认爬取类型
#         #     "video_search_type_list": [
#         #         0,  # 全部 #####设置默认的类型选择为全部
#         #         1,  # 爬虫默认爬取类型 #####**舍弃 设置全部为默认爬取
#         #         2,  # 视频
#         #         3,  # 电影
#         #         4,  # 电视剧
#         #         5,  # 直播
#         #         9,  # 其他
#         #     ],
#         #
#
#         # **页码配置修改：开始页码和结束页码的选择修改为*左开右闭*规则  例： start=1 ,end=2 -> [1,2)
#
#     # 龙珠
#     "longzhu_video_search_offset": {"start": 0, "end": 1, "pagesize": 20,},  # 页码从0开始
#     # 秘饭直播
#     "mifan_video_search_offset": {"start": 0, "end": 1, "pagesize": 20, },  # 页码从0开始
#     # 抓饭直播
#     "zhuafan_video_search_offset": {"start": 1, "end": 2, "pagesize": 15, },  # 页码从1开始
#
#     # 代理
#     # 10/秒
#     "proxyHost": config["proxyHost"],
#     "proxyPort": config["proxyPort"],
#     # 代理隧道验证信息
#     "proxyUser": config["proxyUser"],
#     "proxyPass": config["proxyPass"],
#
# }
