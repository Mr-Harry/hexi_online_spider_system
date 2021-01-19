# -*- coding:utf-8 -*-
# Chance favors the prepared mind.
# author : pyl owo,
# time : 2020/9/21
import datetime
import difflib
import re
from hashlib import md5

import requests

from Audio_Infringement_Config import  proxies

# @retry(stop_max_attempt_number=3, wait_fixed=10)
# def get_response_single(self, url):
#     return requests.get(url, headers=self.headers, proxies=self.proxy)
# 统一请求响应函数
def unify_requests(method="GET",url="",headers={},proxies={},data={},verify=False,cookies={}):
    if method=="GET":
        response = requests.get(url, headers=headers,proxies=proxies,data=data,cookies=cookies,timeout=5)
        return response
    else:
        response = requests.post(url, headers=headers,proxies=proxies,data=data,verify=verify,cookies=cookies,timeout=5)
        return response

# 两个字符串的相似度
def str_similar(str1, str2):
    return round(difflib.SequenceMatcher(None, str(str1), str(str2)).quick_ratio(), 2)

# 清洗一串字符删除不要的 符号 \n\t\r....
def clear_text(text,way_list=[ "\n", "\t", "\r", "　　　　", "　　", "    ", " "]):
    for each in way_list:
        if each != '"':
            text = text.replace("{}".format(each), "")
        else:
            text = text.replace("{}".format(each), "")
    # print(text)
    return text

# 获得代理函数
def get_proxy():

    return proxies

# 获得日期格式
def get_date(content):
    # if isinstance(content, unicode):
    # content = content.encode(encoding='UTF-8')
    pattern = r'(20\d{2})年(\d{1,2})月(\d{1,2})日'
    m = bool(re.search(pattern, content))
    if m:
        result = list(re.findall(pattern, content)[0])
        # print(result)
        for a in range(1, 3):
            if len(result[a]) == 1:
                result[a] = '0' + result[a]

        result_str = '-'.join(result)
        # print(result_str)
        clien_date = result_str
        return result_str
    # 匹配2020-6-20
    pattern = r'(20\d{2})-(\d{1,2})-(\d{1,2})'
    m = bool(re.search(pattern, content))
    if m:
        result = list(re.findall(pattern, content)[0])
        # print(result)
        for a in range(1, 3):
            if len(result[a]) == 1:
                result[a] = '0' + result[a]

        result_str = '-'.join(result)
        # print(result_str)
        return result_str
    # 匹配2017.6.20
    pattern = r'(20\d{2})\.(\d{1,2})\.(\d{1,2})'
    m = bool(re.search(pattern, content))
    if m:
        result = list(re.findall(pattern, content)[0])
        # print(result)
        for a in range(1, 3):
            if len(result[a]) == 1:
                result[a] = '0' + result[a]

        result_str = '-'.join(result)
        # print(result_str)
        return result_str
    # 匹配2020/6/20
    pattern = r'(20\d{2})/(\d{1,2})/(\d{1,2})'
    m = bool(re.search(pattern, content))
    if m:
        result = list(re.findall(pattern, content)[0])
        # print(result)
        for a in range(1, 3):
            if len(result[a]) == 1:
                result[a] = '0' + result[a]

        result_str = '-'.join(result)
        # print(result_str)
        return result_str
    # 匹配6月20日
    pattern = r'(\d{1,2})月(\d{1,2})日'
    m = bool(re.search(pattern, content))
    if m:
        result = list(re.findall(pattern, content)[0])
        # print(result)
        for a in range(0, 2):
            if len(result[a]) == 1:
                result[a] = '0' + result[a]

        result_str = '2020-' + '-'.join(result)
        # print(result_str)
        return result_str
    pattern = r'(\d{1,2})-(\d{1,2})'
    m = bool(re.search(pattern, content))
    if m:
        result = list(re.findall(pattern, content)[0])
        # print(result)
        for a in range(0, 2):
            if len(result[a]) == 1:
                result[a] = '0' + result[a]

        result_str = '2020-' + '-'.join(result)
        # print(result_str)
        return result_str
    return u''

# Md5 加密函数 32 返回32位的加密结果
def md5_use(text: str) -> str:
    result = md5(bytes(text, encoding="utf-8")).hexdigest()
    # print(result)
    return result

# 返回当前时间 格式为 %Y%m%d 年月日 拼接数据库表
def timestamp_strftime(like,time_stamp):
    return datetime.datetime.fromtimestamp(int(str(time_stamp)[:10])).strftime(like)
