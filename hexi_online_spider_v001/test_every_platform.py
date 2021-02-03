# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2021/1/6

import importlib
import time
import json

from Audio_Infringement_Config import Config_of_audio_infringement as config
from Audio_Infringement_Config import Test_Config_Setting as test_config
from audio_tool import timestamp_strftime
from hexi_spider_test_unit.send_emial_hexi import Send_email

# 测试类
class Plarform_Test():
    """
    :cvar
    测试单独板块的脚本是否可用 ，不可用的记录 并且发送邮件 每天定时启动
    """
    def __init__(self,use_proxy=False):
        # 代理
        self.proxy = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": test_config["proxyHost"],
            "port": test_config["proxyPort"],
            "user": test_config["proxyUser"],
            "pass": test_config["proxyPass"],
        }
        # 代理 全局 use_proxy 是否为真
        self.proxies = {
            "http": self.proxy,
            "https": self.proxy,
        } if use_proxy else {}
        # 搜索关键词
        self.search_key = "爱"
        # 未成功获取数据的列表 存储的路径
        self.erro_path = []
        #
        self.log_file_path = "test_email_file_tem"

    # 准备工作
    def setUp(self):
        pass

    # 扫尾工作
    def tearDown(self):
        print("*"*40)
        print("出现问题的平台路径",self.erro_path)
        print("*"*40)
        # 拼接之后的 错误内容 每个错误内容以换行
        text_info = "\n".join(self.erro_path)
        self.save_log(file_path=self.log_file_path, text=text_info)
        # 查看发送什么杨的错误信息
        text_err = test_config["erro_text_info"][1]
        if self.erro_path:
            text_err = test_config["erro_text_info"][2]
        ero_text = text_err+text_info
        # print(text_err)
        return Send_email(erro_text=ero_text,**test_config)

    # 测试代码
    def test_run(self,test_type_list=[1,2,4,5,7]):
        self.setUp()
        # 每一种类型 对应
        for each in test_type_list:
            info_dic = test_config["type_value_dic"][each]  # 字典对应的
            every_platform_dic = {
                'search_parm_name1':"",
                'search_parm_name2':"",
                'search_parm_name3':"",
            }
            # 视频
            if each == 1:
                for ea in info_dic[list(info_dic.keys())[0]]:
                    if int(ea) not in video_no_check:
                        path_pro = info_dic[list(info_dic.keys())[0]][ea]
                        try:
                            # print(ea)
                            detail_info = importlib.import_module(path_pro).search_songs(
                                self.search_key, **{})
                            # print(detail_info)
                            self.single_todo(detail_info, **{"path_pro": path_pro})
                        except Exception as e:
                            self.single_todo([], **{"path_pro": path_pro})

            # 音频
            elif each == 2:
                # print(list(info_dic.keys())[0])
                # print(info_dic)
                for ea in info_dic[list(info_dic.keys())[0]]:
                    # print(ea)
                    if int(ea) not in audio_no_check:

                        path_pro = info_dic[list(info_dic.keys())[0]][ea]

                        try:
                            # print(ea)
                            detail_info = importlib.import_module(path_pro).search_songs(
                                song_name=self.search_key, proxy=self.proxies, **{})
                            # print(detail_info)
                            self.single_todo(detail_info,**{"path_pro":path_pro})
                        except Exception as e:
                            self.single_todo([], **{"path_pro": path_pro})

            # 小说
            elif each == 4:
                for ea in info_dic[list(info_dic.keys())[0]]:
                    if int(ea) not in novel_no_check:

                        path_pro = info_dic[list(info_dic.keys())[0]][ea]
                        try:
                            # print(ea)
                            detail_info = importlib.import_module(path_pro).search_novels(
                                self.search_key, **{})
                            # print(detail_info)
                            self.single_todo(detail_info, **{"path_pro": path_pro})
                        except Exception as e:
                            self.single_todo([], **{"path_pro": path_pro})

            # 搜索引擎
            elif each == 5:
                for ea in info_dic[list(info_dic.keys())[0]]:
                    if int(ea) not in engine_no_check:

                        path_pro = info_dic[list(info_dic.keys())[0]][ea]
                        try:
                            # print(ea)
                            detail_info = importlib.import_module(path_pro).search_engines(
                                self.search_key, **{})
                            # print(detail_info)
                            self.single_todo(detail_info, **{"path_pro": path_pro})
                        except Exception as e:
                            self.single_todo([], **{"path_pro": path_pro})

            # 漫画
            elif each == 7:
                for ea in info_dic[list(info_dic.keys())[0]]:
                    if int(ea) not in cartoon_no_check:

                        path_pro = info_dic[list(info_dic.keys())[0]][ea]
                        try:
                            # print(ea)
                            detail_info = importlib.import_module(path_pro).search_normals(
                                self.search_key, **{})
                            # print(detail_info)
                            self.single_todo(detail_info, **{"path_pro": path_pro})
                        except Exception as e:
                            self.single_todo([], **{"path_pro": path_pro})
        self.tearDown()
    # 每个平台做
    def single_todo(self,info_dic,**kwargs):
        if info_dic:
            print("平台{}>>> 完成".format(kwargs["path_pro"]))
        else:
            self.erro_path.append(kwargs["path_pro"])
    # 保存日志
    def save_log(self,file_path,text):
        with open(file_path,"w") as f:

            f.write(text)





# 执行的主函数
def run(test_type_list=[]):
    Plarform_Test(use_proxy=True).test_run(test_type_list=test_type_list)

if __name__ == '__main__':
    # 测试发送邮件
    # print("开始测试发送邮件！！！")
    # Send_email("test20210121",**test_config)
    # print("ooooo")
    # exit(0)
    # 测试模块
    # [1,2,4,5,7]
    # 2 音频
    # 1 视频
    # 4 小说
    # 7 漫画
    # 5 搜索

    """
        配置将来都是访问特定的API获得对应的参数 进行修改，
    """
    # 需要检测的类型
    test_type_list = test_config["test_type_list"]
    # 视频排除的平台
    video_no_check = test_config["video_no_check"]
    # 音频排除的平台
    audio_no_check = test_config["audio_no_check"]
    # 图文排除的平台
    graphic_no_check = test_config["graphic_no_check"]
    # 卡通排除的平台
    cartoon_no_check = test_config["cartoon_no_check"]
    # 小说排除的平台
    novel_no_check = test_config["novel_no_check"]
    # 搜索引擎排除的平台
    engine_no_check = test_config["engine_no_check"]


    start_run_time = int(time.time()) # 开始的时间
    print("#"*40)
    print("本次测试执行日期 >>> {} \n开始时间: {}".format(timestamp_strftime("%Y-%m-%d %H:%M:%S"),start_run_time))

    run(test_type_list)
    # pass

    end_time =  int(time.time())  # 结束的时间
    end_run_time = end_time - start_run_time # 总共耗时时间
    print("结束时间: {} \n总共耗时 {}".format(end_time,end_run_time))
    print("#"*40)
