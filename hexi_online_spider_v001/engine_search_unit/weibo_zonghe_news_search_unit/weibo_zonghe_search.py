# -*- coding:utf-8 -*- #
# I don't like the world. I just like you
# author : pyl owo,
# time : 2020/7/14
import datetime
import json
import random
from urllib.parse import urlencode

from fake_useragent import UserAgent
from lxml import etree
import requests
from pip._vendor.retrying import retry
# from video_search_unit.Video_Infringement_Config import config_of_video as config
# from video_search_unit.Video_Infringement_Config import config_of_video as config
from engine_search_unit.engine_spider_settings import ENGINE_CONF as config

from audio_tool import get_proxy, md5_use, unit_result_clear_for_video, unify_duration_format
from urllib.parse import unquote,quote

class WeiBoVideo:

    def __init__(self, use_proxy=True):
        self.search_video_url = "https://m.weibo.cn/api/container/getIndex?containerid=100103type%3D1%26q%3D{kw}%26t%3D0&page_type=searchall&page={page}"
        self.headers = {
            'User-Agent': UserAgent().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
            'Connection': 'keep-alive',
            # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'Accept': '*/*',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'no-cors',
            'Sec-Fetch-Dest': 'script',
            # 'Referer': 'https://so.ifeng.com/?q=%E6%88%91&c=1',
            'Accept-Language': 'zh-CN,zh;q=0.9'
        }
        self.proxy = get_proxy() if use_proxy else None

    @retry(stop_max_attempt_number=3, wait_fixed=10)
    def search_songs(self, song_name = '', **kwargs) -> list:
        
        # 搜索页码search_page
        _start = config["weibozonghe_search_offset"]["start_page"]
        if kwargs.get("page_num"):
            # print(1111)
            search_page = int(kwargs.get("page_num")) + _start - 1
        else:
            search_page = _start

        # # 搜索类别 search_type
        # _type = config['video_search_type_default']
        #
        #
        # 搜索时长 search_duration
        #
        search_result_temp = []
        if not song_name:
            return search_result_temp
        search_url = self.search_video_url.format(kw=quote(song_name), page=search_page)
        search_response = self.get_response_single(search_url)
        # print(search_response.text)
        # search_result_temp.append(self.parse_search_video_song(search_response))
        # print(search_url)
        # print(search_result_temp)
        # return unit_result_clear_for_video([j for i in search_result_temp for j in i], **kwargs)
        return self.parse_search_video_song(search_response)
    # 单一请求
    @retry(stop_max_attempt_number=3, wait_fixed=600)
    def get_response_single(self, url):
        # print(url)
        return requests.get(url, headers=self.headers, proxies=self.proxy)
    def url_add_http(self, url: str):
        if not url.startswith('http'):
            url = "https:" + url
        else:
            url = url
        return url
    # 搜索视频响应解析
    def parse_search_video_song(self, response) -> list:
        # print(response.text)
        # print(response.url)
        try:
            tree = json.loads(response.text)

        except Exception as e:
            print(e)
            return []
        else:
            result_list = []
            try:
                video_song_list_data = tree.get('data', {}).get('cards', [])
            except:
                video_song_list_data =[]
            for v_s in video_song_list_data:
                if v_s.get("card_type",{}) ==11: # 什么类型？
                    for each in v_s.get("card_group",[]):
                        if each.get("card_type",{})==9:
                            qin_quan_title_str = each.get("mblog", {}).get("user", {}).get("screen_name", "")
                            qinquan_id_str = each.get("mblog", {}).get("mid", '')
                            qinquan_id_2 = each.get("mblog", {}).get("bid", "")
                            qinquan_user_id = each.get("mblog", {}).get("user", {}).get("id", "")
                            qinquan_user_name = each.get("mblog", {}).get("user", {}).get("screen_name", "")  # 侵权作者名称
                            qin_quan_url_str = "https://www.weibo.com/{}/{}#|xyy|{}".format(qinquan_user_id,
                                                                                            qinquan_id_2,
                                                                                            qinquan_id_str)
                            qin_quan_abstract_str = self.parse_html(each.get("mblog", {}).get("text", ''))
                            engine_dict = dict()
                            engine_dict['qinquan_platform'] = '微博'  # 侵权平台
                            engine_dict['qinquan_title'] = qin_quan_title_str  # 侵权标题
                            engine_dict['qinquan_URL'] = qin_quan_url_str  # 侵权链接
                            engine_dict['qinquan_text'] = qin_quan_abstract_str  # 侵权详情
                            engine_dict['qinquan_id_str'] = qinquan_id_str  # 侵权详情
                            engine_dict['qinquan_author'] = qinquan_user_name  # 侵权作者
                            # print("safdasfasdf")
                            result_list.append(engine_dict)

                if v_s.get("card_type",{}) == 9: # 普通视频类型
                    qin_quan_title_str = v_s.get("mblog",{}).get("user",{}).get("screen_name","")
                    qinquan_id_str = v_s.get("mblog",{}).get("mid",'')
                    qinquan_id_2 = v_s.get("mblog",{}).get("bid","")
                    qinquan_user_id = v_s.get("mblog",{}).get("user",{}).get("id","")
                    qinquan_user_name = v_s.get("mblog",{}).get("user",{}).get("screen_name","") # 侵权作者名称
                    qin_quan_url_str = "https://www.weibo.com/{}/{}#|xyy|{}".format(qinquan_user_id,qinquan_id_2,qinquan_id_str)
                    qin_quan_abstract_str = self.parse_html(v_s.get("mblog",{}).get("text",''))
                    engine_dict = dict()
                    engine_dict['qinquan_platform'] = '微博'  # 侵权平台
                    engine_dict['qinquan_title'] = qin_quan_title_str  # 侵权标题
                    engine_dict['qinquan_URL'] = qin_quan_url_str  # 侵权链接
                    engine_dict['qinquan_text'] = qin_quan_abstract_str  # 侵权详情
                    engine_dict['qinquan_id_str'] = qinquan_id_str  # 侵权详情
                    engine_dict['qinquan_author'] = qinquan_user_name  # 侵权作者
                    result_list.append(engine_dict)
                    # print(video_dict)
        # print(result_list)
        return result_list
    # 解析html 获得其对应的文章内容
    def parse_html(self,res):
        select = etree.HTML(res)
        text = "".join(select.xpath("//text()"))
        return text
    # 视频搜索结果通过标题模糊 %key% 筛除
    def check_video_title(self, need_check_title: str, search_title_key=""):
        return True


search_engines = WeiBoVideo(use_proxy=True).search_songs
if __name__ == '__main__':
    # 测试微博时间
    # dd = "Fri Nov 09 14:41:35 +0800 2018"
    # GMT_FORMAT = '%a %b %d %H:%M:%S +0800 %Y'
    # print(datetime.datetime.strptime(dd, '%a %b %d %H:%M:%S +0800 %Y'))
    # exit(0)
    kwags = {
        "id": 574979,
        "video_title": "班淑传奇",
        "video_url": "https://v.youku.com/v_show/id_XMTM3MjQ5NjEzMg==.html?spm=a2h0c.8166622.PhoneSokuProgram_1.dselectbutton_1&showid=f2103904e95911e4b2ad#班淑传奇第38集",
        "video_author": "",
        "video_album": "",
        "video_platform": "优酷1030测试电视剧一部4_55_1",
        "video_check_platform": "2",
        "sub_table_name": "sub_4_55",
        "task_type": 1,
        "page_num": 2,
        "search_key_words": "正青春",
        # "confirm_key_words": "班淑传奇",
        # "filter_key_words_list": "片花_穿帮_片头曲_片尾曲_预告_插曲_翻唱_翻唱_发布会_演唱_演奏_合唱_专访_合奏_打call_宣传_原唱_cover_原曲_片花_穿帮_音乐_主题歌_有声小说_片头_片尾",
    }
    info= search_engines(kwags["search_key_words"], **kwags)
    print(len(info))
    print(info)

# 576460752305520640/JFNFPA0Jw
# 'https://www.weibo.com/6511456059/K0nmNlfTD'