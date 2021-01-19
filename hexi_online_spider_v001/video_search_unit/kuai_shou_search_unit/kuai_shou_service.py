# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/11/28

"""
Anoyi
大哥就是大哥 android 逆向真的骚
https://www.yuque.com/anoyi/douyin/ysct9r
"""
import random

import requests
from video_search_unit.out_service_config import __out_config__
from audio_tool import Public_Error

class KuaiShouService():
    """
    自己搭建的服务转化类
    """
    API_SEARCH_VIDEO_SEACH = 'https://cloud.anoyi.com/api/dyapp/search/item'
    def __init__(self):
        self.xtoken = __out_config__["X_Token"]
        self.device = __out_config__["device"]
        self.cookie = __out_config__["cookie"]
        self.x_tt_token = __out_config__["x_tt_token"]
        self.common_headers = __out_config__["common_headers"]

    # 返回搜索视频
    def back_search_video(self,task_type,**kwargs):
        keyword = kwargs.get("keyword","") # 搜索关键词
        offset = kwargs.get("offset",0) # 翻页的参数 默认为第一页
        proxies = kwargs.get("proxise",{}) # 代理 默认为空
        # 请求头
        # common_headers = self.common_headers
        # print(kwargs)
        req = {
            # 'url': 'https://apissl.gifshow.com/rest/n/search/feed?mod=Netease%28MuMu%29&lon=121.473721&country_code=CN&kpn=KUAISHOU&oc=GENERIC&egid=DFP95BC6ABC760598F9C9B482862C51170A55F15526D0AA2CB07F79AB415656B&sbh=41&hotfix_ver=&sh=1440&appver=7.6.20.15169&nbh=0&socName=Unknown&newOc=GENERIC&max_memory=192&isp=&kcv=193&browseType=4&kpf=ANDROID_PHONE&ddpi=270&did=ANDROID_4f74435c452648ec&net=WIFI&app=0&ud=0&c=GENERIC&sys=ANDROID_6.0.1&sw=810&ftt=&ll=CQ9kPbX6Oj9AEWub4nFRXl5A&language=zh-cn&darkMode=false&iuid=&lat=31.230388&did_gt=1595949378959&ver=7.6',
            'url': random.choice(__out_config__["kuai_shou_search_url_list"]),
            'method': 'POST',
            'body': {
                'keyword': '%s'%keyword,
                # 'fromPage': "1",
                'pcursor': "%s"%offset,
                'isRecoRequest': 'false',
                # 'kuaishou.api_st': 'Cg9rdWFpc2hvdS5hcGkuc3QSsAEMaySOEfimA3DdPGWcU11ZHox8cDJVp4tedIUj7W-N_w5NgzuNoF4R1pKczoc1NE9WzkPKYQxSAMjo7P7UG9pb-M8Owvja8Q1y_9j6Q88ISnaJiE14cTtI3gcsC1nM_ZO5oeCnd2ISvfbg5gmw1A8PDT_u3lfAB0dfcGtns_LBQPxIjTXeGifvDgOcVwOwwfx8yFXFccxAj05Uys639E7020xj4kYiJquTsc17em_PrxoSRCUg25kRQfGgW7J-1Cb386UHIiBZDCsZSxpb2TiqFFIxK5E_mGM15OalOwwhXIz20yb83ygFMAE',
                # 'token': 'c1c63a70fb2a418e985d65ae11b5e2c2-2011678336',
                'token': random.choice(__out_config__["kuai_shou_token_list"]),
                'client_key': '3c2cd3f3',
                # 'os': 'android'
            }
        }
        # print(req)
        resp = requests.post('https://cloud.anoyi.com/api/ksapp/common',
                             headers={'X-Token': self.xtoken}, json=req).json()
        # print('--------- Anoyi Cloud Service Response -------')
        # print(resp)


        # print('--------- Kuaishou Response -------')
        # print(resp)
        if "body" not in resp:
            raise Public_Error("注意快手的服务是否出现问题 是否是到期了 KuaiShouService -> back_search_video ！！！")

        # print(resp)
        # print(resp["body"])
        # print(resp["url"])
        # # 请求抖音 API
        if proxies:
            #
            print("快手加了代理   fuck！！！")
            resp = requests.post(resp['url'], headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                 data=resp['body'].encode('utf-8'),proxies=proxies)
        elif not proxies:
            resp = requests.post(resp['url'], headers={'Content-Type': 'application/x-www-form-urlencoded'},
                                 data=resp['body'].encode('utf-8'))
        # # 打印返回结果
        # print(resp.text)
        return resp.json()
    #
    def judeg_type_back(self,task_type,**kwargs):
        # 搜索视频
        if task_type==1 or task_type==0:
            return self.back_search_video(task_type,**kwargs)