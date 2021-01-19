# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/11/28

"""
Anoyi
大哥就是大哥 android 逆向真的骚
https://www.yuque.com/anoyi/douyin/ysct9r
"""
import requests
from video_search_unit.out_service_config import __out_config__
from audio_tool import Public_Error

class DouYinService():
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

    # 返回新的注册结果 get_douyin_device
    def back_device_register(self):
        import requests

        # 请求头
        common_headers = self.common_headers
        # "Proxy-Authorization": "Basic MTZDR1ZKWEs6NDc2NzIw",

        # common_headers["Proxy-Authorization"] = "Basic MTZDR1ZKWEs6NDc2NzIw"
        # 设备注册（不使用代理）
        # resp = requests.get('https://cloud.anoyi.com/api/dyapp/device/register', headers=common_headers).json()

        # 设备注册（使用代理）
        resp = requests.get('https://cloud.anoyi.com/api/dyapp/device/register?ip=59.173.75.113&port=23666',
                            headers=common_headers)
        # resp = requests.get('https://cloud.anoyi.com/api/dyapp/device/register',
        #                     headers=common_headers)

        # 打印返回结果
        print(resp.text)

    # 返回搜索视频
    def back_search_video(self,task_type,**kwargs):
        keyword = kwargs.get("keyword","") # 搜索关键词
        offset = kwargs.get("offset",0) # 翻页的参数 默认为第一页
        proxies = kwargs.get("proxise",{}) # 代理 默认为空
        # 请求头
        common_headers = self.common_headers

        # 请求体
        body = {
            "device": self.device,
            "cookie": self.cookie,
            "x-tt-token":self.x_tt_token,
            "keyword": keyword,
            "offset": offset
        }

        # 计算 XG XR
        resp = requests.post(self.API_SEARCH_VIDEO_SEACH, headers=common_headers, json=body).json()
        if "data" not in resp:
            raise Public_Error("注意抖音的服务是否出现问题 是否是到期了 DouYinService -> back_search_video ！！！")

        else:
            resp = resp["data"]
        # print(resp["headers"])
        # print(resp["body"])
        # print(resp["url"])
        # # 请求抖音 API
        if proxies:
            print("抖音 加了代理")
            resp = requests.post(resp['url'], headers=resp['headers'], data=resp['body'],proxies=proxies)
        elif not proxies:
            resp = requests.post(resp['url'], headers=resp['headers'], data=resp['body'])
        #
        # # 打印返回结果
        # print(resp.text)
        info = resp.json()
        if "aweme_list" not in info:
            print("返回的接口里出现了问题！！！ 返回结果为{}".format(info),"重新生成抖音device 文件")

        return resp.json()
    #
    def judeg_type_back(self,task_type,**kwargs):
        # 搜索视频
        if task_type==1 or task_type==0:
            return self.back_search_video(task_type,**kwargs)

if __name__ == '__main__':
    # pass
    DouYinService().back_device_register()