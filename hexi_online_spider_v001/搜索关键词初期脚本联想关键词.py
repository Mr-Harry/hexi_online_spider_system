# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/11/12

""":cvar
    各个抓取平台联想关键词 接口：
    # acfun https://www.acfun.cn/rest/pc-direct/search/suggest?count=6&keyword=%E9%B9%BF%E9%BC%8E%E8%AE%B0&callback=xyy&_=1604901301053 # jsonp xyy
    爱奇艺 https://suggest.video.iqiyi.com/?key=%E7%8F%AD%E6%B7%91%E4%BC%A0%E5%A5%87&platform=11&rltnum=10&uid=b8f7b44e2640d95adbd949e34d871483&ppuid=2396487192&callback=xyy # jsonp xyy
    好看视频 https://haokan.baidu.com/videoui/api/searchsug?query=%E6%88%91%E7%9A%84
    腾讯视频 https://s.video.qq.com/smartbox?callback=xyy&plat=2&ver=0&num=10&otype=json&query=%E7%8F%AD%E6%B7%91%E4%BC%A0%E5%A5%87&uid=7580c998-297d-43fa-baa6-94428279a60f&_=1604910492265
    土豆网 https://tip.tudou.soku.com/v1/search_tip?jsoncallback=xyy&query=%E7%8F%AD%E6%B7%91%E4%BC%A0%E5%A5%87&site=4&rm=C9214D78F86000018DEE127D15516D20-3&h=16
    搜狐网 https://tip.tv.sohu.com/s?encode=utf8&key=%E9%B9%BF%E9%BC%8E%E8%AE%B0&callback=xyy&_=1604910212765
"""

headers = {
    'Connection': 'keep-alive',
    'Pragma': 'no-cache',
    'Cache-Control': 'no-cache',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.183 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Sec-Fetch-Site': 'none',
    'Sec-Fetch-Mode': 'navigate',
    'Sec-Fetch-User': '?1',
    'Sec-Fetch-Dest': 'document',
    'Accept-Language': 'zh-CN,zh;q=0.9',
}
import requests
import re
import json

# 统一请求响应函数
def unify_requests(method="GET", url="",headers={},proxies={},data={},verify=False,cookies={}):
    if method=="GET":
        response = requests.get(url, headers=headers,proxies=proxies,data=data,cookies=cookies,timeout=5)
        return response
    else:
        response = requests.post(url, headers=headers,proxies=proxies,data=data,verify=verify,cookies=cookies,timeout=5)
        return response

# 爱奇艺接口
def back_key_words_aiqiyi(search_key_words,**kwargs):
    ACFUN_API = "https://suggest.video.iqiyi.com/?key={key_words}&platform=11&rltnum=10&uid=b8f7b44e2640d95adbd949e34d871483&ppuid=2396487192&callback=xyy"
    response = unify_requests(url=ACFUN_API.format(key_words=search_key_words),headers=headers)
    # print(response.text)
    info = re.findall(r"xyy\((.*?)\)",response.text)
    if info:
        res = info[0]
        # res = eval(res)
        res = json.loads(res)
        # print(res)

        return [j for j in [i.get("name","") for i in res["data"]] if j]
    else:
        print("aiqiyi 没有获取到关键词 错误！！！")
# 好看视频接口
def back_key_words_haokan(search_key_words,**kwargs):
    ACFUN_API = "https://haokan.baidu.com/videoui/api/searchsug?query={key_words}"
    response = unify_requests(url=ACFUN_API.format(key_words=search_key_words),headers=headers)
    # print(response.text)
    info = response.text

    res = json.loads(info)
    # print(res)

    return  res["data"]["response"]["words"]
# 腾讯视频接口
def back_key_words_tenxun(search_key_words,**kwargs):
    ACFUN_API = "https://s.video.qq.com/smartbox?callback=xyy&plat=2&ver=0&num=10&otype=json&query={key_words}&uid=7580c998-297d-43fa-baa6-94428279a60f&_=1604910492265"
    response = unify_requests(url=ACFUN_API.format(key_words=search_key_words),headers=headers)
    # print(response.text)
    info = re.findall(r"xyy\((.*?)\)",response.text)
    if info:
        res = info[0]
        # res = eval(res)
        res = json.loads(res)
        # print(res)

        return [j for j in [i.get("word","") for i in res["item"]] if j]
    else:
        print("tenxun 没有获取到关键词 错误！！！")
# 土豆视频接口
def back_key_words_tudou(search_key_words,**kwargs):
    ACFUN_API = "https://tip.tudou.soku.com/v1/search_tip?jsoncallback=xyy&query={key_words}&site=4&rm=C9214D78F86000018DEE127D15516D20-3&h=16"
    response = unify_requests(url=ACFUN_API.format(key_words=search_key_words),headers=headers)
    # print(response.text)
    info = re.findall(r"xyy*.\((.*?)\)",response.text)
    if info:
        res = info[0]
        # res = eval(res)
        res = json.loads(res)
        # print(res)

        return [j for j in [i.get("w","") for i in res["r"]] if j]
    else:
        print("tudou 没有获取到关键词 错误！！！")
# 搜狐视频接口
def back_key_words_souhu(search_key_words,**kwargs):
    ACFUN_API = "https://tip.tv.sohu.com/s?encode=utf8&key={key_words}&callback=xyy&_=1604910212765"
    response = unify_requests(url=ACFUN_API.format(key_words=search_key_words),headers=headers)
    # print(response.text)
    info = re.findall(r"xyy*.\((.*?)\)",response.text)
    if info:
        res = info[0]
        # res = eval(res)
        res = json.loads(res)
        # print(res)

        return [j for j in [i.get("t","") for i in res["r"]] if j]
    else:
        print("tudou 没有获取到关键词 错误！！！")

#
def get_key_words_back_similar_keys(search_key_words:str,**kwargs):
    """:cvar
    :return list [key1,key2,key3....]
    """

    # info = back_key_words_aiqiyi(search_key_words)
    #
    # info = back_key_words_haokan(search_key_words)
    # info = back_key_words_tenxun(search_key_words)
    # info = back_key_words_tudou(search_key_words)
    # info = back_key_words_souhu(search_key_words)

    # 在list 里添加函数
    info = [back_key_words_aiqiyi(search_key_words),back_key_words_haokan(search_key_words),
            back_key_words_tenxun(search_key_words),back_key_words_tudou(search_key_words),
            back_key_words_souhu(search_key_words)]
    back_set = set()
    for i in info:
        for j in i:
            back_set.add(j)
    print(list(back_set))
    return list(back_set)
if __name__ == '__main__':
    get_key_words_back_similar_keys("鹿鼎记")