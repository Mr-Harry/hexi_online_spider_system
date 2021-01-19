# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/6/30
import random

from Crypto.Cipher import AES

import base64
import json
from Audio_Infringement_Config import Config_of_audio_infringement as config
from audio_tool import md5_use
from audio_tool import unit_result_clear_for_audio
import requests, pprint
from fake_useragent import UserAgent
from retrying import retry
class WangYiYun():

    def __init__(self):
        self.params = ""
        self._i = "l6Brr86UeZ6C3Bsw" # 默认使用此字符串
        # 使用默认_i 配套的encSecKey
        self.encSecKey = "7ca9b5ba8b13044f47ed74c388df912ac84758122acbedc64111f2ac83232b01d3ce16f7195a39c7e064b4c0240b5c1d52624dc13c22ec820d76dfe32db43e496aeacced5be3ca9108c78a85bb389f1edf8d8c9fced02024ba9490401b4ce062cc50764d0a24294e07bb229271391b5a3640e924ee1ed15435dc6e288f1fa873"
        self.headers =  {
            'authority': 'music.163.com',
            'user-agent': UserAgent().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
            'content-type': 'application/x-www-form-urlencoded',
            'accept': '*/*',
            'origin': 'https://music.163.com',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'cors',
            'sec-fetch-dest': 'empty',
            'referer': 'https://music.163.com/song?id=1426301364',
            'accept-language': 'zh-CN,zh;q=0.9',
            # 'cookie': '_iuqxldmzr_=32; _ntes_nnid=5f8ee04e745645d13d3f711c76769afe,1593048942478; _ntes_nuid=5f8ee04e745645d13d3f711c76769afe; WM_TID=XqvK2%2FtWaSBEUBRBEEN7XejGE%2FL0h6Vq; WM_NI=iN6dugAs39cIm2K2R9ox28GszTm5oRjcvJCcyIuaI1dccEVSjaHEwhc8FuERfkh3s%2FFP0zniMA5P4vqS4H3TJKdQofPqezDPP4IR5ApTjuqeNIJNZkCvHMSY6TtEkCZUS3k%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeb2e57dbababf88b879a8b08fa2d84f869f9fbaaa50a3f599a5d650939b8dadd52af0fea7c3b92aab92fa85f86d83adfddae243afee85d3d133ada8fed9c679ba8ca3d6ee5aaabdbaabc269bb97bb82cc3ba8bdada6d559aabf88a6f664a1e88a96c85aa6b5a8d4f2258690009bed638f9ffbb1b77eb38dfca9b2608a95acb2ee6e94afab9bc75c94ec87b3b84bb48ca696f46f8e9786afd96181aa88aed253f68cbca6ea499a8b9dd4ea37e2a3; JSESSIONID-WYYY=tI8MIKMCRBuyCYnUJMCyUTlp%2Fufv5xIfCquvp7PJ4%2BuXod%5CXH%5CB0icDZw8TNlwHUHOW%2B2t%2BCuXyC4VZ%5C19OrzaDE%5Ck0F0dAZQh7KcVxUoHKpqUdiVzPu8NxCK9cJRG%5C%5CPTvtqxjFerd1%2BBa4%2F%5C8PESa4pvvRaQF6jljjsibX%5CrcPsH0I%3A1593347447142',
            # 'cookie': '_iuqxldmzr_=32; _ntes_nnid=474cdac11e28542e8ef8e079a46725c8,1574167157959; _ntes_nuid=474cdac11e28542e8ef8e079a46725c8; WM_TID=IbY1DOb8iUdAAEFFUUY47dAf2LTYB55E; ntes_kaola_ad=1; mail_psc_fingerprint=1de574c411f6e715dbf66c8f168b658d; nts_mail_user=daybreak_lpy@163.com:-1:1; P_INFO=daybreak_lpy@163.com|1596422302|0|163|00&99|bej&1596159242&mail163#bej&null#10#0#0|&0|mail163|daybreak_lpy@163.com; vinfo_n_f_l_n3=f1666c5df82c0744.1.0.1596422276768.0.1596423848279; JSESSIONID-WYYY=Wtbu%2B6%2Fu%2Faydehr2gtC2xTUuW2aP3QMIg1RCSi%5Ciuq2zAddd04ncYagHYXlxg9ff7hRhl5TuzMeFtYFZtQVhmqZUYHzIPJkB11H2ek8dPO8XsWKMK%2BEFcW82rUOgT%2FkkX2HZIjZINrJNdOdSvTv0%2BTRl7JCzk%2BXBnzIdO7fzATk1YC2N%3A1596609805224; WM_NI=QzV1378M8rNdFEh09tXovaNJ%2Fs%2FGSaJqyjfatPGy30iqI04xqKa2pHUWru8KoxK8ZuZAAGdffIZ7hWGSPkB%2BjfKRrwm%2F4RqN0K85U2UMlUfERj54G23iCOlBW5XnCCNiYmg%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6ee93ae67878b8583f44fb29a8fa2d14e939e8abab65df8afa2afd559f3a7b8d8e52af0fea7c3b92a93a69ad2b23dfc93f893cd70869ba8d1bc809cb1ba82cd42edade1a8d26b8aafb78be56bb890899ab23cabaf87d1b774b395afd3f3449789be96bb41ada885d9d97f9a9f8fa8e76ea69796d8eb5d858da08cc121aaba85b3f17daff1fcb3f446f495f8d6d83a9793a4b6e54f92b6fbd5c63af1b78db0ef4a95eb988fc2498eb7978ee637e2a3',
            # 'cookie':"_ntes_nnid=5f8ee04e745645d13d3f711c76769afe,1593048942478; _ntes_nuid=5f8ee04e745645d13d3f711c76769afe; WM_TID=XqvK2%2FtWaSBEUBRBEEN7XejGE%2FL0h6Vq; nts_mail_user=18188108851@163.com:-1:1; mail_psc_fingerprint=b6a29041eb57bb1af6103a40edd5b48e; _iuqxldmzr_=32; NMTID=00OCcA8F8NsNRW2uEwNi3kIfSVRS8YAAAF1JslvIg; ntes_kaola_ad=1; NTES_CMT_USER_INFO=119735308%7C%E8%93%81%E8%93%81%E7%9A%84%E9%93%BA%E5%AD%90%7Chttp%3A%2F%2Fdingyue.ws.126.net%2FVZwS1GNb2%3DPaXpm5dGikutfPXjoYTJL%3DoU2k4kxNZ7aI41507628769922.jpg%7Cfalse%7CbTE4MTg4MTA4ODUxQDE2My5jb20%3D; UM_distinctid=17548c0b0b4bea-010a9c9f6741c6-163d6152-1ea000-17548c0b0b5cee; playliststatus=visible; WEVNSM=1.0.0; WNMCID=mjcndh.1605576156154.01.0; playerid=71514275; _antanalysis_s_id=1606205353864; ne_analysis_trace_id=1607582683524; s_n_f_l_n3=aa9f917bf8b510d11607582683532; vinfo_n_f_l_n3=aa9f917bf8b510d1.1.2.1596418844177.1603243506514.1607582751770; NTES_SESS=0..jWlpCkBRei9BJX8GEvDsEM2ISxBgNYtZSF6XAfFRKfD7CfFQYXm6BWXtcZVhqzDlpeSFBPbeAipdvXlXIBNBw7PDC3e37fBuQaka2EbgZ1a9FwH_8CPTNfzrjluh48Bz8Ab9RKNr5DfzCuaFtgUMq4HoxDIIcLon86ihnPhhieZR4r4jehssfPDXwDryqNcWbptb.UkWeyHFJiv1PBZdP415QOAdKv; NTES_PASSPORT=nQ_Hwenev3IZ4IprwIk1a_t3lQvmk0ruKbE0zvYqwWbowsISwc4gjpLxUjN.OvGzTFs1LFTmzmFQcdoyiCrFmbLfQeFNevT9P5Te1s7TWJ1HToULlTg38N6PAl7aB0rR2VT9N.7i28Is8pjVhLF8VhuNTlbD3sWqOYrZUCMwMJ.PpFmbDFNydRR6yr6sDf9IP; S_INFO=1608100321|0|3&80##|m18188108851#daybreak_xyy; P_INFO=m18188108851@163.com|1608100321|1|mail163|00&99|bej&1608100282&carddav#bej&null#10#0#0|181851&1||18188108851@163.com; MUSIC_EMAIL_U=28b7a7e60c196de52c9d3dcbd24a52a58ba689fefc8b4f08956b9cc3e6423b1b58173c632e0825dd7d59bd32aeefd290c3061cd18d77b7a0; SERVER_ID=14; TOKEN=OZc4OoAm4mTXySZB; JSESSIONID-WYYY=SoDUaBQRo%5CtsRaqaPsIzgV5ezFgOCtncJuIrUzSj7gbZAcApXJ3YOSijjJSoFaRO5T%2FcKE%2BroTJWqw2DiJA%2Bx5gE6i2YWxCaHnPMs4%2BP3j6Rw4zjutiXNhROMPoklkKkvNjxUo1HKgfn0fyZ298vmflrjgxrf59%5Cm1%2Bdz58yrWjuAlNI%3A1608202191288; WM_NI=WypX3at7Zd%2BnMGc0EAotEJC%2BGT8ASvxjMYJhQTOXHPs2YBP5iSFPUwg%2Bxc92d3rPAczrj5lniwShFNHfwTxiIr9qiiOiWNN94B9jhiw2iMLix52R%2F96kvKIymOvnpEQOdUk%3D; WM_NIKE=9ca17ae2e6ffcda170e2e6eeafd57ff7e7b7a5d57f83868fb3d54a828f9e84f56b95b09ea4fc6792b084bbf82af0fea7c3b92a95a7c0b9b26bb8e99685aa668f99add1c84badac8babc221858cf8a2d27ebcb683bac964938c81b9cb5cb1ee97a3d33fab8d8ab1d87da5f5b884bc3aa8edbeb1c469baaea6d6ef66aba99d89c5468cbab9b5fb638baef792ec638db799afcd33f89ef78beb63b5eea7aecf63bcebfeb3ae33f6b5baaccc73af91ba8ff34f9391acb6ea37e2a3; MUSIC_U=ecfd18dca00c8af834b56d49ed12899f4fbbdb8a1321a6c2a6d82146ad22a70f55101a1cdc52edafba89105e534c754b80c0aec9ee0dd676e381395bf06ec255; __csrf=114ae8179ac020091c837134a9ff2376"
        }

    # 搜索歌曲接口
    API_Serch_Songs = 'https://music.163.com/weapi/cloudsearch/get/web?csrf_token='
    # 歌曲评论
    API_Comments_Song = 'https://music.163.com/weapi/v1/resource/comments/R_SO_4_{}?csrf_token=' # 音乐ID可替换
    # 歌曲歌词
    API_Lyric_Songs = 'https://music.163.com/weapi/song/lyric?csrf_token='

    # crypt_js_complex python 复写cryptjs
    def crypt_js_complex(self,text):
        BS = AES.block_size
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode('utf-8')
        unpad = lambda s: s[0:-s[-1]]

        key = bytes(self._i, encoding="utf-8")
        text = text.encode("utf-8")
        IV = b'0102030405060708'

        cipher = AES.new(key, mode=AES.MODE_CBC, IV=IV)
        # cipher2 = AES.new(key, mode=AES.MODE_CBC, IV=IV)  # 加密和解密，cipher对象只能用一次

        # print(text)
        encrypted = pad(text)
        # print(encrypted)
        encrypted = cipher.encrypt(encrypted)
        # print(encrypted)
        encrypted = base64.b64encode(encrypted).decode("utf-8")
        # print("第二次加密结果", encrypted)

        return encrypted

    # crypt_js_complex 的基础
    def crypt_js_complex_base(self,text):
        BS = AES.block_size
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS).encode('utf-8')
        unpad = lambda s: s[0:-s[-1]]

        key = b'0CoJUm6Qyw8W8jud'
        text = text.encode("utf-8")
        IV = b'0102030405060708'

        cipher = AES.new(key, mode=AES.MODE_CBC, IV=IV)
        # cipher2 = AES.new(key, mode=AES.MODE_CBC, IV=IV)  # 加密和解密，cipher对象只能用一次

        # print(text)
        encrypted = pad(text)
        # print(encrypted)
        encrypted = cipher.encrypt(encrypted)
        # print(encrypted)
        encrypted = base64.b64encode(encrypted).decode("utf-8")
        # print("第一次加密结果", encrypted)
        return encrypted

    # 获得parms参数值
    def get_params(self,text):
        return self.crypt_js_complex(
            self.crypt_js_complex_base(text),)

    # 毫秒转分钟
    def change_haomiao(self,hm_second):
        m, s = divmod(int(hm_second/1000), 60)
        return "%02d:%02d" % (m, s)
    # 对搜索结果进行解析的函数
    def parms_search_songs(self,info):
        result_list =[]
        # print(info)
        if 'code' in info and str(info["code"]) == "200" and info["result"] and info["result"]["songs"]:
            # pprint.pprint(info["result"]["songs"]) # json 打印
            for each in info["result"]["songs"]:
                # 添加条件 不能播放的就不要了 song下面的每条信息 privilege 下面的st 为-200 就是无法播放
                # print(each["privilege"]["st"])
                if str(each["privilege"]["st"])==str(0):
                    # print("此条信息为可用的{}".format(each["privilege"]["st"]))
                    dic_ = {}
                    dic_["audio2_albumName"] = each["al"]["name"]
                    dic_["audio2_artistName"] = "/".join([name["name"] for name in each["ar"]])
                    dic_["audio2_songName"] = each["name"]
                    dic_["audio2_songId"] = each["id"]
                    dic_["audio2_songtime"] = self.change_haomiao(hm_second=each["dt"]) # 时间
                    dic_["audio2_platform"] = "网易云音乐"
                    dic_["audio2_url"] = "https://music.163.com/#/song?id={}".format(dic_["audio2_songId"])
                    dic_["audio2_url_hash"] = md5_use(text=dic_["audio2_url"])
                    result_list.append(dic_)
                # else:
                #     print("不可播放")
                #     print(each["privilege"]["st"])
        return result_list

    # 获得响应的函数
    @retry(stop_max_attempt_number=5,wait_fixed=600)
    def get_single(self, params,data,proxy):
        response = requests.post(self.API_Serch_Songs, headers=self.headers, params=params,
                  data=data, proxies=proxy)
        return response
    # 搜索歌曲接口
    def search_songs(self,song_name,proxy={},**kwargs):
        """
        :param name:str
        :param offset:int 偏移量 默认第一页 例如 0 30 60 90
        :return 接口数据
        """
        # print(song_name)
        # print(proxy)
        result_list = []
        _start = config["wangyiyun_search_offset"]["start"]
        _end = config["wangyiyun_search_offset"]["end"]

        if kwargs.get("page_num"):
            if config["wangyiyun_search_offset"]["start_page"]==0:
                _start = kwargs.get("page_num")-1
                _end = kwargs.get("page_num")
            elif config["wangyiyun_search_offset"]["start_page"]==1:
                _start = kwargs.get("page_num")
                _end = kwargs.get("page_num") + 1

        for each in range(_start,_end):

            text = '{"hlpretag":"<span class=\\"s-fc7\\">","hlposttag":"</span>","#/discover":"","s":"%s","type":"1","offset":"%s","total":"false","limit":"30","csrf_token":""}'%(song_name,each*30)
            # payload = 'params={params}&encSecKey={encSecKey}'.format(params=self.get_params(text),encSecKey=self.encSecKey)
            # print(text)
            params = (
                ('csrf_token', ''),
            )

            data = {
                'params': self.get_params(text),
                'encSecKey': self.encSecKey
            }
            if proxy:
                # response = requests.post(self.API_Serch_Songs, headers=self.headers, params=params,
                #                      data=data,proxies=proxy)
                response = self.get_single(params=params,data=data,proxy=proxy)
            else:
                response = self.get_single(params=params,data=data,proxy=proxy)

                # response = requests.post(self.API_Serch_Songs, headers=self.headers, params=params,
                #                      data=data)
            # print(proxy)
            # print(response.text)
            for each in self.parms_search_songs(json.loads(response.text)):
                result_list.append(each)
        # print(result_list)

        return unit_result_clear_for_audio(result_list=result_list,**kwargs)
    # 歌曲评论抓取
    def comment_song(self,songid:str,offset:int=0):
        """"
        :param songid：str 歌曲ID
        :param offset：int 翻页 默认第一页 0 20 40
        :return 接口数据
        """
        text = '{"rid":"R_SO_4_%s","offset":"%s","total":"true","limit":"20","csrf_token":""}'%(songid,offset*20)


        params = (
            ('csrf_token', ''),
        )

        data = {
            'params': self.get_params(text),
            'encSecKey': self.encSecKey
        }
        response = requests.post(self.API_Comments_Song.format(songid), headers=self.headers,
                                 params=params, data=data)
        self._dispose(json.loads(response.text))
    # 歌词爬取
    def lyric_song(self,songid:str):
        """
        :param songid str 歌曲ID
        :return 接口数据
        """
        # 歌词接口加密参数原型
        text = '{"id":"%s","lv":-1,"tv":-1,"csrf_token":""}'%(songid)

        params = (
            ('csrf_token', ''),
        )

        data = {
            'params': self.get_params(text),
            'encSecKey': self.encSecKey
        }

        response = requests.post(self.API_Lyric_Songs, headers=self.headers, params=params, data=data)
        self._dispose(json.loads(response.text))

    # 处理爬虫获取到的数据，这里我就输出值
    def _dispose(self, data):
        pprint.pprint(data)
        return data

    # 主函数 测试
    def wangyi_main(self):
        # 搜索接口
        self.search_songs("旧账",0)
        #歌曲评论接口
        # self.comment_song("25639331",0)
        # 歌词接口
        # self.lyric_song("1351615757") # 旧账
        pass
################################ 以下是统一的类返回函数 都有两个至少 ########################
    # 返回搜索的参数 包含URL headers parms 请求类型get/post 返回列表[]
    def back_search_parms(self,name):
        detail_info_list = []
        for each in range(config["wangyiyun_search_offset"]["start"],config["wangyiyun_search_offset"]["end"]):
            detail_info_dic = {}
            text = '{"hlpretag":"<span class=\\"s-fc7\\">","hlposttag":"</span>","#/discover":"","s":"%s","type":"1","offset":"%s","total":"false","limit":"30","csrf_token":""}' % (
            name, each * 30)
            # payload = 'params={params}&encSecKey={encSecKey}'.format(params=self.get_params(text),encSecKey=self.encSecKey)

            params = {
                'csrf_token': ''
            }

            data = {
                'params': self.get_params(text),
                'encSecKey': self.encSecKey
            }
            detail_info_dic['params'] = params
            detail_info_dic['headers'] = self.headers
            detail_info_dic['data'] = data
            detail_info_dic['requir_way'] = "POST"
            detail_info_dic['url'] = self.API_Serch_Songs
            detail_info_list.append(detail_info_dic)
        # print(detail_info_list)
        return detail_info_list

search_songs = WangYiYun().search_songs
if __name__ == '__main__':
    wy = WangYiYun()
    # wy.back_search_parms(name='路在何方')
    # wy.wangyi_main()
    proxy = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": config["proxyHost"],
        "port": config["proxyPort"],
        "user": config["proxyUser"],
        "pass": config["proxyPass"],
    }
    proxies = {
        "http": proxy,
        "https": proxy,
    }
    each = {
        "id": 165806,
        "audio_title": "丑八怪",
        "audio_url": "https://y.qq.com/n/yqq/song/001yus1q2xXSf0.html",
        "audio_author": "伦桑",
        "audio_album": "",
        "audio_platform": "8000任务新增九千",
        "audio_check_platform": "1_2_3",
        "sub_table_name": "sub_1_17",
        "task_type": 2,
        "page_num": 1,
        "search_key_words": "丑八怪",
        # "confirm_key_words": "Live",
        # "filter_key_words_list": "片花_穿帮_片头曲_片尾曲_预告_插曲_翻唱_翻唱_发布会_演唱_演奏_合唱_专访_合奏_打call_宣传_原唱_cover_原曲_片花_穿帮_音乐_主题歌_有声小说_片头_片尾",
        # "filter_key_words_list": "演员",

    }

    # print(wy.search_songs(song_name="丑八怪",proxy=proxies))
    info = search_songs(song_name=each["search_key_words"],proxy=proxies, **each)
    print(len(info))
    print(info)
    # print(wy.search_songs(song_name=each["search_key_words"],proxy=proxies, **each))