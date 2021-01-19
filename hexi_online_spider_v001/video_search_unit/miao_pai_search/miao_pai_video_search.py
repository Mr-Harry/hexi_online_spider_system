# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/9/16
import datetime
import random
import uuid
# from urllib import request
import requests
# 用户贴子列表
from hashlib import md5
from urllib.parse import urlsplit


suid = "YL916B9pGDWbmzEh"
url = 'http://b-api.ins.miaopai.com/1/user/medias.json?count=20&page=1&suid={}'
headers = {
    "Accept-Encoding": "gzip",
    'User-Agent': 'okhttp/3.3.1',
    'Connection': 'Keep-Alive',
    "Host": 'b-api.ins.miaopai.com',
    'cp_ver': '7.1.70',
    'cp_appid': '424',
    'cp_sver': '5.1.1',
    'cp_channel': 'xiaomi_market',
    'cp_os': 'android',
    'cp_vend': 'miaopai',
}
# 处理sign
class SignGenerateDownloaderMiddleware(object):
    def __init__(self, *args, **kwargs):
        super(SignGenerateDownloaderMiddleware, self).__init__(*args, **kwargs)
        self.version = '7.1.70'
        self.string_format = 'url={}unique_id={}version={}timestamp={}4O230P1eeOixfktCk2B0K8d0PcjyPoBC'

    def process_request(self, request, spider=""):
        timestamp = int(datetime.datetime.now().timestamp())
        cp_uuid = request.meta.get('uuid') or uuid.uuid1().__str__()
        request.headers['cp_sign'] = self.get_sign(request, timestamp, cp_uuid)
        request.headers['cp_time'] = str(timestamp)
        request.headers['cp_uuid'] = cp_uuid
        request.headers['cp_abid'] = self.get_cpAbid()
        request.headers['Cache-Control'] = 'no-cache'
        print(request.urlopen(url.format(suid)))
        return
    def get_cpAbid(self):
        s1 = random.randint(1,19)
        s2 = random.randint(1,29)
        if random.randint(0,1):
            return '1-102,{}-100,2-1,{}-101,5-200,2-201'.format(s1,s2)
        else:
            return '1-102,{}-100,2-1,{}-101'.format(s1,s2)

    def get_sign(self, request, timestamp, unique_id):
        path = urlsplit(request.url).path
        source = self.string_format.format(path, unique_id, self.version, timestamp)
        sign = self.get_md5(source)
        return sign

    def get_md5(self, source):
        if isinstance(source, str):
            source = source.encode('utf-8')
        return md5(source).hexdigest()
if __name__ == '__main__':
    miaopai = SignGenerateDownloaderMiddleware()
    miaopai.process_request()