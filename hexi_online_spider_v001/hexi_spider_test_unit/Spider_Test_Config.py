# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2021/1/6
from Audio_Infringement_Config import Config_of_audio_infringement as config

# 测试使用配置
Test_Config_Setting = {
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
