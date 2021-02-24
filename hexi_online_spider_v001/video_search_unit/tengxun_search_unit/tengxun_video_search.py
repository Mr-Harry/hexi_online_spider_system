# -*- coding:utf-8 -*- #
# I don't like the world. I just like you
# author : pyl owo,
# time : 2020/7/27
import random
import re

import requests
from lxml import etree
from fake_useragent import UserAgent
from retrying import retry

from video_search_unit.tengxun_search_unit.tenxun_search_movie_tvplay_by_api import search_movie_tvplay_by_api
from audio_tool import get_proxy, md5_use, unify_duration_format, unit_result_clear_for_video, str_to_datetime, \
    re_datetime_str
from video_search_unit.Video_Infringement_Config import config_of_video as config



class TengXunVideo:
    def __init__(self, use_proxy=True):
        self.proxy = get_proxy() if use_proxy else None
        self.base_url = "https://v.qq.com/x/search/?q=%s&cur={}"
        self.api_video_search_key = ""
        self.yangben_dict = []
        self.headers = {
            'authority': 'v.qq.com',
            'upgrade-insecure-requests': '1',
            'user-agent': UserAgent().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
            'sec-fetch-dest': 'document',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'same-origin',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'referer': 'https://v.qq.com/x/search/?ses=qid%3DUyr-x8ATfiJo5mYSn9oibxgFO6JnpIiCA0N3fJwnNk5UJAEBSySemw%26last_query%3D%E8%A5%BF%E6%B8%B8%E8%AE%B0%26tabid_list%3D0%7C2%7C15%7C1%7C106%7C3%7C4%7C11%7C6%7C12%7C21%7C14%7C5%7C17%7C8%7C20%7C7%7C1100%26tabname_list%3D%E5%85%A8%E9%83%A8%7C%E7%94%B5%E8%A7%86%E5%89%A7%7C%E6%95%99%E8%82%B2%7C%E7%94%B5%E5%BD%B1%7C%E5%B0%91%E5%84%BF%7C%E7%BB%BC%E8%89%BA%7C%E5%8A%A8%E6%BC%AB%7C%E6%96%B0%E9%97%BB%7C%E7%BA%AA%E5%BD%95%E7%89%87%7C%E5%A8%B1%E4%B9%90%7C%E6%B1%BD%E8%BD%A6%7C%E4%BD%93%E8%82%B2%7C%E9%9F%B3%E4%B9%90%7C%E6%B8%B8%E6%88%8F%7C%E5%8E%9F%E5%88%9B%7C%E6%AF%8D%E5%A9%B4%7C%E5%85%B6%E4%BB%96%7C%E7%9F%A5%E8%AF%86%26resolution_tabid_list%3D0%7C1%7C2%7C3%7C4%7C5%26resolution_tabname_list%3D%E5%85%A8%E9%83%A8%7C%E6%A0%87%E6%B8%85%7C%E9%AB%98%E6%B8%85%7C%E8%B6%85%E6%B8%85%7C%E8%93%9D%E5%85%89%7CVR&q=%E8%A5%BF%E6%B8%B8%E8%AE%B0&needCorrect=%E8%A5%BF%E6%B8%B8%E8%AE%B0&stag=3&cur=2&cxt=tabid%3D0%26sort%3D0%26pubfilter%3D0%26duration%3D0%26cluster_list%3D26t87ldn2b',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        }

    # 单一请求
    @retry(stop_max_attempt_number=3, wait_fixed=10)
    def get_response_single(self, url):
        return requests.get(url, headers=self.headers, proxies=self.proxy)

    def get_tengx_type_list(self):
        pass

    def search_video(self, search_key: str, **kwargs):
        self.api_video_search_key = search_key
        search_result_temp = []
        if not self.api_video_search_key:
            return search_result_temp

        # 搜索页码search_page
        _start = config["bilibili_video_search_offset"]["start_page"]
        if kwargs.get("page_num"):
            search_page = int(kwargs.get("page_num")) + _start - 1
        else:
            search_page = _start

        # 搜索类别 search_type
        _type = config['video_search_type_default']
        if kwargs.get("search_type"):
            _tengxun_type_list = [kwargs.get("search_type")]
        else:
            _tengxun_type_list = [_type]

        #
        # 搜索时长 search_duration
        #

        search_url_temp = self.base_url % search_key
        search_url = search_url_temp.format(search_page)
        # print(search_url)
        search_response = self.get_response_single(search_url)
        search_result_temp.append(self.parse_search_video(search_response, search_type_list=_tengxun_type_list))
        search_result_temp.append(search_movie_tvplay_by_api(search_key, proxy=self.proxy))
            # if 2 in search_type_list:
            #     movie_api_url = ""
            #     movie_api_response = self.get_response_single(movie_api_url)
            #     search_result_temp.append(self.parse_search_video_movie_api(movie_api_response))
        # if 3 in search_type_list:
        #     pass
        
            # type_name = config.get("tengxun_search_type", {}).get(t_l)
        
        return unit_result_clear_for_video([j for i in search_result_temp for j in i], **kwargs)

    # 搜索视频响应解析
    def parse_search_video(self, response, search_type_list=None) -> list:
        try:
            tree = etree.HTML(response.text)
        except:
            return []
        else:
            # print(response.text)
            result_list = []
            if (0 in search_type_list) or (1 in search_type_list):
                try:
                    short_video_list_data = tree.xpath(
                        "//div[contains(@class,'result_item') and contains(@class,'result_item_h') and contains(@class,'_quickopen')]")
                except:
                    short_video_list_data = []
                for s_v in short_video_list_data:
                    video_dict = dict()
                    video_dict["video2_title"] = "".join(s_v.xpath(".//h2[@class='result_title']/a//text()"))#.replace('<em class="hl">','').replace('</em>','')
                    # print(video_dict)
                    # if not self.check_video_title(video_dict.get("video2_title")):
                    #     continue
                    video_dict["video2_url"] = "".join(s_v.xpath(".//h2[@class='result_title']/a/@href"))
                    if 'v.qq.com' not in video_dict.get('video2_url'):
                        continue
                    lable1 = ''.join(s_v.xpath(".//div[@class='info_item info_item_even']/span[@class='label']/text()"))
                    video_dict["video2_author"] = "".join(s_v.xpath(".//div[@class='info_item info_item_even']/span[@class='content']/a/text()")) if lable1 =='上传者：' else ''
                    video_dict["video2_url_hash"] = md5_use(video_dict.get("video2_url"))
                    video_dict["video2_platform"] = "腾讯视频"
                    video_dict["video2_pubtime"] = re_datetime_str(str_to_datetime("".join(s_v.xpath(".//div[@class='info_item info_item_odd']/span[@class='content']/text()"))))
                    duration_str_temp = "".join(s_v.xpath(".//span[@class='figure_info']/text()"))
                    duration, duration_str = unify_duration_format(duration_str_temp)
                    video_dict["video2_duration"] = duration  # 时长（秒数）
                    video_dict["video2_duration_str"] = duration_str  # 时长（字符串）

                    # 样本数据
                    if self.yangben_dict and isinstance(self.yangben_dict, dict):
                        video_dict["video_title"] = self.yangben_dict.get("video_title")
                        video_dict["video_author"] = self.yangben_dict.get("video_author")
                        video_dict["video_url"] = self.yangben_dict.get("video_url")
                    result_list.append(video_dict)
            if (0 in search_type_list) or (2 in search_type_list) or (3 in search_type_list):
                try:
                    movie_list_data = \
                    tree.xpath("//div[contains(@class,'result_item') and contains(@class,'result_item_v')]")
                    # print(len(movie_list_data))
                except:
                    movie_list_data = []
                for m in movie_list_data:
                    video_dict = dict()
                    video_title_temp = "".join(m.xpath(".//h2[@class='result_title']/a//text()"))
                    # print(video_title_temp.split())
                    video_dict["video2_title"] = video_title_temp.split()[0]
                    # print(video_dict)
                    # video2_type = video_title_temp.split()[-1]
                    # if not (0 in search_type_list) and (2 in search_type_list):
                    #     if video2_type != '电影':
                    #         continue
                    # print(video_dict["video2_title"])
                    # video_dict["video2_title"] = "".join(m.xpath(".//h2[@class='result_title']/a/text()")).replace('<em class="hl">','').replace('</em>','')
                    # print(m.xpath(".//h2[@class='result_title']/a/em/text()"))
                    if not self.check_video_title(video_dict.get("video2_title")):
                        continue

                    video_dict["video2_url"] = "".join(m.xpath(".//h2[@class='result_title']/a/@href")) if len(m.xpath(".//h2[@class='result_title']/a/@href")) == 1 else "".join(m.xpath(".//h2[@class='result_title']/a/@href")[0])
                    if not self.check_video_url(video_dict.get("video2_url")):
                        continue
                    # video_dict["video2_author"] = m.get('author', '')
                    video_dict["video2_url_hash"] = md5_use(video_dict.get("video2_url"))
                    video_dict["video2_platform"] = "腾讯视频"
                    duration_str_temp = "".join(m.xpath(".//span[@class='figure_info']/text()"))
                    duration, duration_str = unify_duration_format(duration_str_temp)
                    video_dict["video2_duration"] = duration  # 时长（秒数）
                    video_dict["video2_duration_str"] = duration_str  # 时长（字符串）
                    # 样本数据
                    if self.yangben_dict and isinstance(self.yangben_dict, dict):
                        video_dict["video_title"] = self.yangben_dict.get("video_title")
                        video_dict["video_author"] = self.yangben_dict.get("video_author")
                        video_dict["video_url"] = self.yangben_dict.get("video_url")
                    result_list.append(video_dict)
            return result_list

    def parse_search_video_movie_api(self, movie_api_response):
        pass
    # 视频搜索结果通过标题模糊 %key% 筛除
    def check_video_title(self, need_check_title: str, search_title_key=""):
        if not search_title_key:
            search_title_key = self.api_video_search_key
        return True if str(need_check_title).find(str(search_title_key)) >= 0 else False

    def check_video_url(self, need_check_url: str):
        buyao = ['/v.qq.com/detail/s', '/v.qq.com/detail/']
        # print(need_check_url)
        for i in buyao:
            if i in need_check_url:
                return False
        return True

    # def get_video_title_from_etree_str(self, video_title_temp_str_data):
    #     # video_title_temp = "".join(video_title_temp_str_data.split())
    #
    #     video_title_temp = re.sub(r'<a.*?>', '', video_title_temp_str_data)
    #     video_title_temp.replace('<em class="hl">', '')
    #     video_title_temp.replace('</em>', '')
    #     video_title_temp.replace('</a>', '')
    #     video_title = re.sub(r'<span class="sub">.*?</span>', '', video_title_temp, flags=re.S)
    #     video_title = re.sub(r'<span class="type">.*?</span>', '', video_title, flags=re.S)
    #     return video_title

search_songs = TengXunVideo(use_proxy=True).search_video

if __name__ == '__main__':
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
        "search_key_words": "班淑传奇",
        # "confirm_key_words": "班淑传奇",
        # "filter_key_words_list": "片花_穿帮_片头曲_片尾曲_预告_插曲_翻唱_翻唱_发布会_演唱_演奏_合唱_专访_合奏_打call_宣传_原唱_cover_原曲_片花_穿帮_音乐_主题歌_有声小说_片头_片尾",
    }
    txv = TengXunVideo(use_proxy=True)
    result = txv.search_video('爱', **kwags)
    print(result)
    print(len(result))