# -*- coding:utf-8 -*- #
# I don't like the world. I just like you
# author : pyl owo,
# time : 2020/7/14
import datetime
import random
import re
from urllib.parse import urlencode

from fake_useragent import UserAgent
from lxml import etree
import requests
from pip._vendor.retrying import retry
from video_search_unit.Video_Infringement_Config import config_of_video as config
from audio_tool import get_proxy, md5_use, unit_result_clear_for_video, unify_duration_format, re_datetime_str


class MeiPaiVideo:

    def __init__(self, use_proxy=True):
        self.search_video_url = "https://www.meipai.com/search/mv?q={}&page={}"
        self.headers = {
            'User-Agent': UserAgent().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
            'Connection': 'keep-alive',
            'Upgrade-Insecure-Requests': '1',
            # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Sec-Fetch-Site': 'cross-site',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-User': '?1',
            'Sec-Fetch-Dest': 'document',
            'Referer': 'http://www.meipai.com/search/mv?q=%E6%88%91&page=2',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            # 'Cookie': 'MUSID=82rk47sjqg8ebhsu2bm5fmogr2; MP_WEB_GID=853630598920642; virtual_device_id=ecdcd5c14f66e4ce2ed51f213415384d; pvid=elSvyPswPdIj%2FH92c8ryQ5J8wsqKjSmT; sid=82rk47sjqg8ebhsu2bm5fmogr2'

        }
        self.proxy = get_proxy() if use_proxy else None

    @retry(stop_max_attempt_number=3, wait_fixed=10)
    def search_songs(self, song_name = '', **kwargs) -> list:
        
        # 搜索页码search_page
        _start = config["meipai_video_search_offset"]["start_page"]
        if kwargs.get("page_num"):
            # print(1111)
            search_page = int(kwargs.get("page_num")) + _start - 1
        else:
            search_page = _start

        # 搜索类别 search_type
        _type = config['video_search_type_default']
        
        #
        # 搜索时长 search_duration
        #

        search_result_temp = []
        if not song_name:
            return search_result_temp
        search_url = self.search_video_url.format(song_name, search_page)
        search_response = self.get_response_single(search_url)
        search_result_temp.append(self.parse_search_video_song(search_response))
        # print(search_url)
        return unit_result_clear_for_video([j for i in search_result_temp for j in i], **kwargs)

    # 单一请求
    @retry(stop_max_attempt_number=3, wait_fixed=600)
    def get_response_single(self, url):
        return requests.get(url, headers=self.headers, proxies=self.proxy)

    # 搜索视频响应解析
    def parse_search_video_song(self, response) -> list:
        # print(response.text)
        # print(response.url)
        try:
            tree = etree.HTML(response.text)
        except:
            return []
        else:
            result_list = []
            try:
                video_song_list_data = tree.xpath("//ul[@class='content-l-ul search-video-list clearfix']/li")
            except:
                video_song_list_data =[]
            for v_s in video_song_list_data:
                video_dict = dict()
                video_dict["video2_title"] = "".join(v_s.xpath(".//a[@class='content-l-p pa']/@title")).replace('\n', '')
                if not self.check_video_title(video_dict.get("video2_title")):
                    continue
                video_dict["video2_url"] = "https://www.meipai.com" + "".join(v_s.xpath(".//a[@class='content-l-p pa']/@href"))
                video_dict["video2_author"] = "".join(v_s.xpath(".//p[@class='content-name  pa']/a/@title"))
                # video_dict["video_author_zone"] = "".join(v_s.xpath(".//a[@class='video-meta-user']/@href"))
                # video_dict["video2_pubtime"] = ""
                video_dict["video2_url_hash"] = md5_use(video_dict.get("video2_url"))
                video_dict["video2_platform"] = "美拍"
                dada = re.search('(\d{4}-\d{1,2}-\d{1,2}(T\d{1,2}:\d{1,2}:\d{1,2})?)', "".join(v_s.xpath(".//meta[@itemprop='uploadDate']/@content")), re.S)
                try:
                    pubtime = dada.group()
                except:
                    pubtime = ''
                else:
                    pubtime = pubtime.replace('T', ' ')
                video_dict["video2_pubtime"] = pubtime
                duration_str_temp = ''
                duration, duration_str = unify_duration_format(duration_str_temp)
                video_dict["video2_duration"] = duration  # 时长（秒数）
                video_dict["video2_duration_str"] = duration_str  # 时长（字符串）
                result_list.append(video_dict)
                # print(video_dict)

        return result_list

    # 视频搜索结果通过标题模糊 %key% 筛除
    def check_video_title(self, need_check_title: str, search_title_key=""):
        return True

search_songs = MeiPaiVideo(use_proxy=True).search_songs
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
        "confirm_key_words": "班淑传奇",
        "filter_key_words_list": "片花_穿帮_片头曲_片尾曲_预告_插曲_翻唱_翻唱_发布会_演唱_演奏_合唱_专访_合奏_打call_宣传_原唱_cover_原曲_片花_穿帮_音乐_主题歌_有声小说_片头_片尾",
    }
    res = MeiPaiVideo().search_songs('班淑传奇', **kwags)
    print(res)
    print(len(res))
