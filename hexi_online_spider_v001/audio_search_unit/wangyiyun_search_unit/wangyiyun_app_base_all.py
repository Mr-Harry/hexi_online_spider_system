# -*- coding:utf-8 -*-
# Chance favors the prepared mind.
# author : pyllowo,
# time : 2021/1/21

import random

import requests
import traceback
import base64
import json
from Crypto.Cipher import AES
from binascii import b2a_hex, a2b_hex
from urllib.parse import quote

from audio_tool import get_proxy


class EncryptDate:
    def __init__(self):
        self.key = "e82ckenh8dichen8".encode()  # 初始化密钥
        self.length = AES.block_size  # 初始化数据块大小
        self.aes = AES.new(self.key, AES.MODE_ECB)  # 初始化AES,ECB模式的实例
        # 截断函数，去除填充的字符
        self.unpad = lambda date: date[0:-ord(date[-1])]

    def base64_decode(self, text):
        return base64.b64decode(text)

    def pad(self, text):
        """
        #填充函数，使被加密数据的字节码长度是block_size的整数倍
        """
        count = len(text.encode('utf-8'))
        add = self.length - (count % self.length)
        entext = text + (chr(add) * add)
        return entext

    # base64输出

    def encrypt(self, encrData):  # 加密函数
        res = self.aes.encrypt(self.pad(encrData).encode("utf8"))
        # print(res)
        msg = str(base64.b64encode(res), encoding="utf8")
        return msg

    def decrypt(self, decrData):  # 解密函数
        res = base64.b64decode(decrData.encode("utf8"))
        print(len(res))
        print(b2a_hex(res))
        print(res)
        msg = self.aes.decrypt(res).decode(errors='ignore')

        return self.unpad(msg)

    # 16进制输出
    def encrypt_hex(self, encrData):  # 加密函数
        res = self.aes.encrypt(self.pad(encrData).encode())
        # msg = str(base64.b64encode(res), encoding="utf8")
        return b2a_hex(res).decode()

    def decrypt_hex(self, decrData):  # 解密函数
        res = a2b_hex(decrData)
        plain_text = self.aes.decrypt(res)
        return self.unpad(plain_text.decode())


AES_EBC = EncryptDate()
checkToken = ''

def sekiro_get_params(path, DICT):
    for i in range(3):
        try:
            params = {
                "api": path,
                "params": DICT,
                'group': 'wangyiyun',
                'action': 'entrypto'
            }
            url = 'https://www.qxp.red/asyncinvoke'
            try:
                res = requests.get(url, params=params, timeout=1.5, proxies=get_proxy())
                # print(res.json())
                return res.json()['data']
            except:
                res = None
                traceback.print_exc()

        except:
            if res:
                print(res.text)
            traceback.print_exc()
    return None


def req(path, params, COOKIE=False):
    cookies = {}
    if COOKIE:
        cookies = {
            'MUSIC_A': '47e30a9b79cacd30ed7ce0b60997b210034284d2419cf711edfa9aa86c7f414ec8675cd23f75992cafc612a832efee6545bfdd4787ec3fb71b93fb26d3f19882ca280de4c7c76cceb817b16a361a3106e68145f02868e9cc3610685cf7ebf7510edf70a74334194e0127a5e93947a4c663ac4574cbe7e29333a649814e309366',
        }

    headers = {
        'Host': 'interface3.music.163.com',
        'user-agent': 'NeteaseMusic/8.0.40.1610544597(8000041);Dalvik/2.1.0 (Linux; U; Android 8.1.0; AOSP on msm8996 Build/OPM1.171019.011)',
        # 'cmint(page)id': 'SearchActivity',
        'mconfig-info': '{"IuRPVVmc3WWul9fT":{"version":"211","appver":"8.0.40"},"tPJJnts2H31BZXmp":{"version":"135","appver":"2.0.30"},"c0Ve6C0uNl2Am0Rl":{"version":"53","appver":"1.4.30"}}',
        'content-type': 'application/x-www-form-urlencoded',
    }

    data = f'params={params}'
    response = requests.post(
        'https://interface3.music.163.com/e' + path[1:],
        cookies=cookies,
        headers=headers,
        data=data,
        verify=False, proxies=get_proxy())
    return b2a_hex(response.content).decode()


def req_bodan(djProgramId, path, enparams, COOKIE=False):
    '''
    播单声音的详情页
    :param djProgramId: 声音id
    :return:
    '''
    cookies = {}
    if COOKIE:
        cookies = {
            'MUSIC_A': '47e30a9b79cacd30ed7ce0b60997b210034284d2419cf711edfa9aa86c7f414ec8675cd23f75992cafc612a832efee6545bfdd4787ec3fb71b93fb26d3f19882ca280de4c7c76cceb817b16a361a3106e68145f02868e9cc3610685cf7ebf7510edf70a74334194e0127a5e93947a4c663ac4574cbe7e29333a649814e309366',
        }
    headers = {
        'Host': 'interface3.music.163.com',
        'user-agent': 'NeteaseMusic/8.0.40.1610544597(8000041);Dalvik/2.1.0 (Linux; U; Android 8.1.0; AOSP on msm8996 Build/OPM1.171019.011)',
        'mconfig-info': '{"IuRPVVmc3WWul9fT":{"version":"211","appver":"8.0.40"},"tPJJnts2H31BZXmp":{"version":"135","appver":"2.0.30"},"c0Ve6C0uNl2Am0Rl":{"version":"53","appver":"1.4.30"}}',
        'content-type': 'application/x-www-form-urlencoded',
    }

    params = (
        ('resourceIds', f'[{djProgramId}]'),
        ('resourceType', '1'),
        ('fixliked', 'true'),
        ('needupgradedinfo', 'true'),
    )

    data = f'params={enparams}'
    response = requests.post(
        'https://interface3.music.163.com/e' + path[1:],
        headers=headers,
        params=params,
        data=data,
        cookies=cookies,
        verify=False, proxies=get_proxy()
    )
    return b2a_hex(response.content).decode()


def response_decrypt(res_hex):
    decrypt_text = AES_EBC.decrypt_hex(res_hex)
    return json.loads(decrypt_text)


# @app.get("/wyy/songs/search")
def song_search(keyword, page=1):
    '''
    歌曲搜索列表页
    :param keyword:搜索关键词
    :param int(page):页数
    :return:res.json()
    data = res.json()["result"]['songs']
    for song in data:
        name =song['name']
        songid = song['id']
        print(f"歌曲名称：{name}，歌曲id:{songid}")
    '''
    # print(checkToken)
    offset = str((int(page) - 1) * 20)
    path = '/api/v1/search/song/get'
    DICT = '{"sub":"false","q_scene":"normal","s":"' + keyword + '","offset":"' + offset + \
           '","limit":"20","queryCorrect":"true","checkToken":"' + checkToken + '","strategy":"5","header":"{}","e_r":"true"}'

    params = sekiro_get_params(path, DICT)
    # print(params)
    res_hex = req(path, params)
    decrypt_json = response_decrypt(res_hex)
    # print("歌曲搜索列表:", decrypt_json)
    return decrypt_json


# @app.get("/wyy/songs/detail")
def song_detail(songId):
    '''
    歌曲详情页：
    :param songId: 歌曲id
    :return: res.json()
    commentCount =res.json()['/api/resource/commentInfo/list']['data'][0]['commentCount']
    print(f"评论数:{commentCount}")
    '''
    songId = str(songId)
    path = '/api/batch'
    DICT = {
        #  "/api/zone/songplay/entry/get": "{'songIds':[1812467646,33763029,1803462189,574505973,1812488703,464255266,1804320463,1495058484,573615289,33497113,1812750050,1368754688,1426649237,1810021934,1500569811,1447966613,1481164987,1811102198,1804879213,1441758494]}",
        # 歌手评论# "/api/content/exposure/vinyl/comment/entrance/get": "{\"sourceType\":\"4\",\"songId\":\""+songId+"\"}",
        #  "/api/content/exposure/songplay/entrance/animation": "{'songId':"+songId+", 'isNewUser':true}",
        # 明星导师教你唱歌 #  "/api/resource-exposure/config": "{'resourcePosition':'songplay', 'resourceId': '"+songId+"', 'exposureRecords':'[{\"exposureNum\":1,\"exposureTime\":1610957493473,\"resourcePosition\":\"songplay\",\"resourceType\":\"ksongActivity\"}]'}",
        "/api/resource/commentInfo/list": "{'resourceIds':[" + songId + "], 'resourceType':4, 'fixliked':true, 'needupgradedinfo':true}",
        # "/api/mlivestream/entrance/playint(page)/v7/get": "{'artistIds':["+artistIds+"],'songId':"+songId+"}",
        #    "/api/springtone/exist": "{'songid':"+songId+"}",
        #   "/api/usertool/ring/song/check": "{'songId':"+songId+"}",
        "/api/content/exposure/songplay/entrance/ksong": "{'songId':" + songId + ", 'source':'player'}",
        "header": "{}",
        "e_r": "true"}
    # print(json.dumps(DICT))

    params = sekiro_get_params(path, json.dumps(
        DICT))  # 'C561B86F974CBA39FB9AB3222AC3E7715C63C82AF1145798F469307D39A6A7EE8182B236B8BF3A37C843233BF9577149A10DB649C4B497974D0E1263C21EF072B26F09EC116976CBC604C1AE6BDF704E4EF8DEE112E7A631BBCCE3839B4570023ADF134D84A972AC3DC622BB9C5E26A3C24262ADD52BD5BF473C9DE6D86DF2787C769625D8BE536075ABE1D177CC553F939F821EF1A0B53C9EF59899D09148915F364B4369A7A7CD8E919FE3737038D838BFA6001F0B1A106B553B498983EC2E2E62F16145A8F78CCEB1B7F79A87FC97F70AD8E5DD4925AE75BFF7D4E04F59677780033D579CC7ED3BE35A8C342078BEE2B77A8619BAE716BC6586119356276C7A95434966CC5A25DAB4D316B2235F0C27B9080F0A1EE2A3DD543CCEA2EE7D2827D2B039E2AE7A01E01348B5E0F54EF7056B342A55A706A0A2A3851ADD2FB929E93048600F097FB58D1EF759E302C2BFA0AA64105C06D30C12796243CFEFD5D259C9F4D4FE696D0E1ECB0D4C2DB700D163221EAFE4AF694CF4C7D9258633B89BF07DBB9DCB17DA786B7CCF2C12DF1D57A25A87BE253780DF2C2E9C9475E202A881C2CBB639669E33FEABE9214CBFACC2D8EEC233BBE11D74CB7A9939A6A6E5B738D4F95708CC76284929A97E9E2F24AE3A447B0C5122C61FCFB2F9942303E56075395EEA8D824AECCC396EAE09C7728D2913569DBED42B1999A6FC398241615796E8E6C6B02B5AE33A0B545625E00C1D40758464A6EEA783D6C5492A6F1A2B9AD59797D456EBAF8C91747577F0072A44ACF2FFED5A1591F890CA9CD8D35E6911299BDB201BE0B2EC6C74B75536F9DBE55FD32581F0565CDE5F31CFB90EE33E145122DE0DCFEB8B27B68B4806EFF70107E75CDA93641E09455DC63FD111EB8F66654A3D85EF8F0BA36B889269A3AF9A791798C35AB8D53EB547A2D516F8EC4CE3BF233AE4B441FE6BB8B7343791A82CB680FAD1BE7075DBCC2573FEADBC243CD937E9B6406534D3C65933C287285790525A209EA579B7B349390255897B91DCF949CC7791500C6DCFD3340E93D8837F40D9F1D9785261D982B3FFB27E64EAD2631E8D7B11B227FB2444B9BDA3486DBA9C4482D662763C6BDC0C1AD806E0E68DBB11EBD64EB7AFA60921402B9402E5D604243805265C94066BECB3C19A117D0418A257317E72CA1E7581BFC1FECFEC306E78B50F862EC63DC1075B91F7535E73A89BE698E0A9822B742911CC81CE3A215F'
    # print(params)
    res_hex = req(path, params, COOKIE=False)
    decrypt_json = response_decrypt(res_hex)
    # print("歌曲详情:", decrypt_json)
    return decrypt_json


# @app.get("/wyy/mp4/search")
def mp4_search(keyword, page=1):
    '''
    视频列表
    :param keyword:
    :param int(page):
    :return: res.json()
    for mp4 in res.json()['data']['resources']:
        playCount = mp4['baseInfo']['resource']['mlogExtVO']['playCount']
        likedCount = mp4['baseInfo']['resource']['mlogExtVO']['likedCount']
        print(f"播放次数:{playCount}，点赞数：{likedCount}")
    '''
    offset = str((int(page) - 1) * 20)
    path = '/api/search/mlog/get'
    DICT = '{"offset":"' + offset + '","limit":"20","keyword":"' + \
           keyword + '","scene":"normal","header":"{}","e_r":"true"}'

    params = sekiro_get_params(path, DICT)
    # print(params)
    res_hex = req(path, params)
    decrypt_json = response_decrypt(res_hex)
    # print("视频列表:", decrypt_json)

    return decrypt_json


# @app.get("/wyy/mp3/search")
def bodan_search(keyword, page=1):
    '''
    播单列表页（（能获取收藏、评论。没有分享数））
    :param keyword: 播单名称
    :param int(page): 页数
    :return: res.json()
    for mp3 in res['data']['resources']:
        resourceId = mp3['resourceId']
        subCount = mp3['baseInfo']['subCount']
        programCount = mp3['baseInfo']['programCount']
        print(f"播单id:{resourceId},收藏数:{subCount}，评论数：{programCount}")
    '''
    offset = str((int(page) - 1) * 20)
    path = '/api/search/voicelist/get'
    DICT = '{"offset":"' + offset + '","limit":"20","keyword":"' + \
           keyword + '","scene":"normal","header":"{}","e_r":"true"}'

    params = sekiro_get_params(path, DICT)
    # print(params)
    res_hex = req(path, params)
    decrypt_json = response_decrypt(res_hex)
    # print("播单列表:", decrypt_json)

    return decrypt_json


# @app.get("/wyy/mp3/detail")
def bodan_detail(resourceId):
    '''
    播单详情（能获取收藏、评论、分享数））
    :param resourceId:播单id
    :return:res.json()
    data =  res.json()["data"]
    subCount =data['subCount']
    programCount = data['programCount']
    commentCount = data['commentCount']
    shareCount = data['shareCount']
    print(f"播单声音总数：{programCount}，收藏数:{subCount},评论数：{commentCount}，分享数：{shareCount}")

    '''
    path = '/api/djradio/v3/get'
    DICT = '{"id":' + resourceId + ',"header":"{}","e_r":"true"}'

    params = sekiro_get_params(path, DICT)
    res_hex = req(path, params, True)
    decrypt_json = response_decrypt(res_hex)
    # print("播单搜索列表（能获取收藏、评论、分享数）:", decrypt_json)

    return decrypt_json


# @app.get("/wyy/mp3/radiolist")
def bodan_song_list(resourceId, page=1):
    '''
    播单声音列表页，可获取每声音点赞和评论

    :param radioId: 播单id
    :return:res.json()
    for programs in res.json()['/api/v3/dj/program/byradio']['data']['programs']:
        likedCount = programs['likedCount']
        commentCount = programs['commentCount']
        print(f"点赞：{likedCount}，评论{commentCount}")
    '''
    path = '/api/batch'
    offset = str(int(page) - 1 * 200)
    DICT = {
        "/api/v3/dj/program/byradio": "{\"filterlikeplay\":true,\"limit\":200,\"offset\":" + offset + ",\"radioId\":" +
                                      resourceId +
                                      "}",
        # "/api/dj/playrecord/radio/get": "{\"asc\":0,\"limit\":500,\"offset\":0,\"radioId\":" +
        # radioId +
        # "}",
        "header": "{}",
        "e_r": "true"}

    params = sekiro_get_params(path, json.dumps(DICT))
    # print(params)
    res_hex = req(path, params)
    decrypt_json = response_decrypt(res_hex)
    # print("播单声音列表页:", decrypt_json)

    return decrypt_json


def test():
    cookies = {
        'EVNSM': '1.0.0',
        'osver': '8.1.0',
        'deviceId': 'MzUyNTMxMDg3NjkzMTM5CTQwOjRlOjM2OmIxOmI4OjRjCWFmZmM0MTQwZGQ0MDdiMTcJNDY3NzNiMDk5OWY4YzEzNg%3D%3D',
        'appver': '8.0.40',
        'NMDI': 'Q1NKTQkBDACaLlj4QKC5B6n0epxrAAAAS4yUCDsxX%2Bi9NIha9fGO%2BH2%2BnFGkZy2IBlqbyL%2FDbcf45fpjprFgZpxZ%2FqJWGUhEQKmNXI4o9KZdMp7GGIzZE8IdwDeTqNZNRSA%2FIJ4PV%2B%2Br3R3cw0KXVesQckiVunVR4hxj56K0XSJlR7Q%3D',
        'ntes_kaola_ad': '1',
        'NMCID': 'xuezrt.1610940086967.01.4',
        'versioncode': '8000041',
        'mobilename': 'AOSPonmsm8996',
        'URS_APPID': '37FB90FD8DBCE1F0503EA5D26E2E0A6CED76ACCB4E7DABA33C22F75E40976C40B6F0E44087D61EFC06BE92279CD6EEC6',
        'buildver': '1610544597',
        'resolution': '1794x1080',
        '__csrf': '9ed4fd42b73076a534be8d673e1a2df9',
        'NMTID': '00OfVmaiDu6JAZMvkRMvRJZkJbQJOgAAAF3GKuPsQ',
        'os': 'android',
        'channel': 'huawei1',
        'MUSIC_A': '47e30a9b79cacd30ed7ce0b60997b210034284d2419cf711edfa9aa86c7f414ec8675cd23f75992cafc612a832efee6545bfdd4787ec3fb71b93fb26d3f19882ca280de4c7c76cceb817b16a361a3106e68145f02868e9cc3610685cf7ebf7510edf70a74334194e0127a5e93947a4c663ac4574cbe7e29333a649814e309366',
    }

    headers = {
        'Host': 'interface3.music.163.com',
        'user-agent': 'NeteaseMusic/8.0.40.1610544597(8000041);Dalvik/2.1.0 (Linux; U; Android 8.1.0; AOSP on msm8996 Build/OPM1.171019.011)',
        'cmint(page)id': 'VoiceListDetailActivity',
        'mconfig-info': '{"IuRPVVmc3WWul9fT":{"version":"211","appver":"8.0.40"},"tPJJnts2H31BZXmp":{"version":"135","appver":"2.0.30"},"c0Ve6C0uNl2Am0Rl":{"version":"53","appver":"1.4.30"}}',
        'content-type': 'application/x-www-form-urlencoded',
    }

    data = 'params=C561B86F974CBA39FB9AB3222AC3E7712CE8CD849F5866B8EA44615B1B346839AE0BF1C2C9E5514864E70B347C8112E401C120BE1DC744567207F9DED9DFF00549BEBA0A7B782BE0DF5106BB771756E2DFD8CBD7F6EA18C715B431B63345132DC1F33ED4D693922CC2ACB0D7DF96AEA54572D6DA72EB79DC22A1EA8D9E7737B2A4E894322189ADB2FCDB732DBB155F9024733C951ABFA8BC1D2680570CA14045B79FF0C52641F0AF792569B31EAEC469D1EB08E8BC86DE3EC5AB9A07492FDB877E5A058DE2844C62D23A1A6F5B79DDABCA71D2D32E57D0C5144C048F98FC52B65518F3C8E001135AC2DDD8CCA73DC146860608CC5F0794AD9030DE727CCEA21859673AB0678EBAE858DBA900C954256C5030CB3E593D79834C26896FA6AADED94F8F9D0389123B52C1CDE6E0EB5E2630'

    response = requests.post('https://interface3.music.163.com/eapi/batch', verify=False, headers=headers,
                             cookies=cookies, data=data, proxies=get_proxy())

    return b2a_hex(response.content).decode()

def get_params(params_text):
    for i in range(5):
        try:
            params={
                "params":params_text,
                'group':'wangyiyuntest',
                'action':'native_encrypt'
            }
            url = 'https://www.qxp.red/asyncInvoke'
            try:
                res = requests.get(url,params=params,timeout=1.5, proxies=get_proxy())
               # print(res.json())
                return res.json()['data']
            except:
                res=None
                traceback.print_exc()

        except:
            if res:
                print(res.text)
            traceback.print_exc()
    return None
def res_decrypto(restext):
    for i in range(5):
        try:
            params={
                "restext":restext,
                'group':'wangyiyuntest',
                'action':'native_decrypt'
            }
           # url = 'https://www.qxp.red/asyncInvoke?group=wangyiyuntest&action=native_decrypt'
            url = 'https://www.qxp.red/asyncInvoke'
            try:
                res = requests.post(url, data=params, timeout=2, proxies=get_proxy())
                #print(res.text)
                return res.json()['data']
            except:
                res=None
                traceback.print_exc()

        except:
            if res:
                print(res.text)
            traceback.print_exc()
    return None

wyy_cookies = {
        'apphost': 'IuRPVVmc3WWul9fT',
        'appkey': 'c0Ve6C0uNl2Am0Rl',
        'MUSIC_A': '47e30a9b79cacd30ed7ce0b60997b210034284d2419cf711edfa9aa86c7f414ec8675cd23f75992cafc612a832efee6545bfdd4787ec3fb71b93fb26d3f19882ca280de4c7c76cceb817b16a361a3106e68145f02868e9cc3610685cf7ebf7510edf70a74334194e0127a5e93947a4c663ac4574cbe7e29333a649814e309366',
    }
# @app.get("/wyy/ksong/search")
def wyy_kge(keyword,page=1):

    headers = {
        'mconfig-info': '{"IuRPVVmc3WWul9fT":{"version":"213","appver":"8.0.40"},"tPJJnts2H31BZXmp":{"version":"140","appver":"2.0.30"},"c0Ve6C0uNl2Am0Rl":{"version":"53","appver":"1.4.30"}}',
        'user-agent': 'NeteaseMusic/8.0.40.1610544597(8000041);Dalvik/2.1.0 (Linux; U; Android 8.1.0; AOSP on msm8996 Build/OPM1.171019.011)',
        'x-er': '258',
        'cmpageid': 'nk/search/entry',
        'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    cursor = str((int(page) - 1) * 20)
    text = 'key='+keyword+'&page={"size":20,"cursor":"' + cursor + '","more":true}&filterSegment=0'


    params_text = quote(text, "utf-8").replace("%3D", '=').replace("%26", '&')
    #print(params_text)
    params = get_params(params_text)
    data = params#'Q1NKTQEBDACXuexEy4OPUlQaDFgQHN/H0rIrs0aA4xkGkk9/3nwAAABQZX1gRgcXFB0mwpv1/6xj0/MOkv5lqU1NgbxyNB3EM54b6LRTzz1Oa49M2UQaAgKUebSEmWPPVI01m1zAfafPhDilgotcLcr7thvOsgLzch9/j3iAN/XSkNEqSukqmLN1ttUtcJyE4u6k41JEP64a+DaKnjiDwPAORupW'

    response = requests.post('https://api.k.163.com/neapi/ksong/picksong/accompany/search', headers=headers,
                             cookies=wyy_cookies, data=data, proxies=get_proxy())

    res = json.loads(res_decrypto(response.text))
    # print(res)
    return res


#网易云k个排行榜：
# @app.get("/wyy/ksong/toplist")
def wyy_ksong_toplist(ksongId):
    '''
    :param ksongId: 演唱歌曲id
    :return: res
    for i in res.json()['data']['topList']:
        ksongId = i["opusInfo"]['id']
        hotValue = i['hotValue']
        userRoleList = i["opusInfo"]['userRoleList']
        userist = '+'.join([user['nickname'] for user in userRoleList])
        userid = ','.join([user['id'] for user in userRoleList])
        print(f"演唱者:{userist},userid:{userid},热度:{hotValue},详情ksongId:{ksongId}")
    '''

    headers = {
        'mconfig-info': '{"IuRPVVmc3WWul9fT":{"version":"215","appver":"8.0.40"},"tPJJnts2H31BZXmp":{"version":"140","appver":"2.0.30"},"c0Ve6C0uNl2Am0Rl":{"version":"53","appver":"1.4.30"}}',
        'user-agent': 'NeteaseMusic/8.0.40.1610544597(8000041);Dalvik/2.1.0 (Linux; U; Android 8.1.0; AOSP on msm8996 Build/OPM1.171019.011)',
        'x-er': '258',
        'cmpageid': 'nk/accompaniment/detail',
        'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    text = f'accompId={ksongId}&userId={random.randint(1,10)}044783277'

    params_text = text
    # print(params_text)
    params = get_params(params_text)
    data = params#'Q1NKTQEBDADDBjQ7FvI1KTactngQCdcinkhP15v04/71NM3VoVQAAAAeLS8yEYTnD1TYU0z+qUPHXu86CN7g5qHdyFSnz+W7K3UbGDKGCspTCvTLc7wSx0PY/L4RG28ftu1/e1oEASzDlk29BQaBUyCGhb2SxGiTDVU4GTw='

    response = requests.post('https://api.k.163.com/neapi/ksong/accompany/sing/toplist', headers=headers,
                             cookies=wyy_cookies, data=data,verify=False, proxies=get_proxy())
    res = json.loads(res_decrypto(response.text))
    # print(res)
    return res

#演唱榜详情
# @app.get("/wyy/ksong/detail")
def wyy_ksong_detail(opusId):
    '''
    演唱榜详情
    :param opusId: 演唱榜详情Id
    :return:
    '''

    headers = {
        'mconfig-info': '{"IuRPVVmc3WWul9fT":{"version":"215","appver":"8.0.40"},"tPJJnts2H31BZXmp":{"version":"140","appver":"2.0.30"},"c0Ve6C0uNl2Am0Rl":{"version":"53","appver":"1.4.30"}}',
        'user-agent': 'NeteaseMusic/8.0.40.1610544597(8000041);Dalvik/2.1.0 (Linux; U; Android 8.1.0; AOSP on msm8996 Build/OPM1.171019.011)',
        'x-er': '258',
        'cmpageid': 'nk/opus/detail',
        'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    text = f'opusId={opusId}&privateToken='

    params_text = text
    # print(params_text)
    params = get_params(params_text)
    data =params# 'Q1NKTQEBDACbkJCAA4Gi3muocAYQN4+rQhCmBcnFzT/v9u8IqU4AAADOrynvmt8Wp0CUyUQinOagmEOhX3rdYtZTeg2KxfOpQEYtEUVH1OTGpgaQ97kymktI94XOiIcNmZHpqAPog8cld27TPMK4nE/7vRrNtcY='

    response = requests.post('https://api.k.163.com/neapi/ksong/opus/detail', headers=headers, cookies=wyy_cookies,
                             data=data,verify=False, proxies=get_proxy())


    res = json.loads(res_decrypto(response.text))
    # print(res)
    return res


# 演唱详情评论接口
# @app.get("/wyy/ksong/comments")
def wyy_comments(opusId,page=1):
    '''
        评论
        :param opusId: 演唱榜详情Id
        :param page: 页数
        :return: res.json()
        评论总数：data['page']['recordCount']
        评论列表 data['records']
        评论内容:for record in data['records']:
                    content = record['content']
        '''
    headers = {
        'mconfig-info': '{"IuRPVVmc3WWul9fT":{"version":"215","appver":"8.0.40"},"tPJJnts2H31BZXmp":{"version":"140","appver":"2.0.30"},"c0Ve6C0uNl2Am0Rl":{"version":"53","appver":"1.4.30"}}',
        'user-agent': 'NeteaseMusic/8.0.40.1610544597(8000041);Dalvik/2.1.0 (Linux; U; Android 8.1.0; AOSP on msm8996 Build/OPM1.171019.011)',
        'x-er': '258',
        'content-type': 'application/x-www-form-urlencoded; charset=utf-8',
    }
    cursor =  (int(page) - 1) * 20
    if cursor ==0:
        cursor =''
    text = 'page={"size":20,"cursor":"'+str(cursor)+'","more":true}&resourceId='+opusId+'&resourceType=1004'
    #print(text)
    from urllib.parse import quote

    params_text = quote(text, "utf-8").replace("%3D", '=').replace("%26", '&')
   # print(params_text)
    params = get_params(params_text)
    data = params#'Q1NKTQEBDADz19nME6AvXVbmmScQ7ocgIe1vdpHRuEjwl4PGcIMAAADbdnWuE1PVPN699aThwAk4u4wKjmmMI7dmgh2IusjnAdNixcIj+wfiB9me6OL5cLWjDqMxj9BwokMVddTyeyzkU3FTFvAn4aLX6a021YDpAsUyIpcoRMBVrYH/i+fr1YUsPu9JHeyN+tG+t4n/EDIfEAV7g9CD01OKOkwix5vvxOy6/w=='

    response = requests.post('https://api.k.163.com/neapi/ksong/comment/resource/comments/smart', headers=headers,
                             cookies=wyy_cookies, data=data,verify=False, proxies=get_proxy())
    res = json.loads(res_decrypto(response.text))
    # print(res)
    return res
if __name__ == "__main__":
    info = mp4_search("告白气球")
    print(info)
    pass
    # # keyword = '告白气球'
    # # page = 1
    # AES_EBC = EncryptDate()
    # checkToken = ''  # '9ca17ae2e6fbcda170e2e6eeb7ed3fa8e7fbd4b2468fb08bb6d55e968b9ebaf16ea5bdab8aca4d87eaa4d1f52af0feaec3b92aa5b1c08be53fb38d94d0cb3f839f9eb6d85a838694d0ce6da8edfed1e64af5a99ed9a128e2aceedba16a9284e191b85fb4be97d5ca7393b4aeb2c47caa8ab888c037e2a3'
    # # #歌曲搜索列表
    # #  song_search(keyword, int(page))
    # #
    # #  songId = 536570450
    # #  #歌曲详情（获取评论数）
    # #  song_detail(str(songId))
    # #  #视频列表（获取视频发布时间/播放次数/点赞数）
    # #  mp4_search(keyword, int(page))
    # #  #播单搜索列表（能获取收藏和评论，没有分享数）
    # #  bodan_search(keyword, int(page))
    # #  #播单id
    # #  radioid = 349888065
    # #  ##播单搜索列表（能获取收藏、评论、分享数）
    # #  bodan_detail(str(radioid))
    # #  #播单歌曲列表页
    # #  bodan_song_list(str(radioid))
    #
    # # uvicorn.run(app=app, host="0.0.0.0", port=5001)
    # print(song_search('告白气球'))