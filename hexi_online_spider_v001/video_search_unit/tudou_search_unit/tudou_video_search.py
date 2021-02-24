# -*- coding:utf-8 -*- #
# I don't like the world. I just like you
# author : pyl owo,
# time : 2020/7/14
import random
from urllib.parse import urlencode

from fake_useragent import UserAgent
from lxml import etree
import requests
from pip._vendor.retrying import retry
from video_search_unit.Video_Infringement_Config import config_of_video as config
from audio_tool import get_proxy, md5_use, unify_duration_format, unit_result_clear_for_video, str_to_datetime, \
    re_datetime_str


class TuDouVideo:

    def __init__(self, use_proxy=True):
        self.search_video_url = "https://www.soku.com/nt/search/q_{}?page={}&lengthtype={}"
        self.headers = {
            'user-agent': UserAgent().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
            'authority': 'www.soku.com',
            'upgrade-insecure-requests': '1',
            # 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-dest': 'document',
            'accept-language': 'zh-CN,zh;q=0.9',
            'cookie': '_uab_collina=160222434027929196672607; cna=bFrvFwgutSkCAXt6ge4H1U4Q; __ayft=1603010694355; __aysid=1603010694356LNe; __ayscnt=1; P_ck_ctl=ED207E7C62C182B3B2CF764C1B209229; xlly_s=1; SK_QUERY=%5B%7B%22q%22%3A%22%25E6%2588%2591%25E7%2588%25B1%25E4%25BD%25A0%22%7D%2C%7B%22q%22%3A%22%25E7%2588%25B1%22%7D%2C%7B%22q%22%3A%22%25E5%25BC%2582%25E6%2580%25A7%22%7D%2C%7B%22q%22%3A%22%25E7%25BB%25BC%25E8%2589%25BA%22%7D%2C%7B%22q%22%3A%22%25E6%2588%2591%22%7D%5D; JSESSIONID=0D0B95B14230EB10EC9A836E4635B6C1; __arpvid=1603011503647ZzNzIt-1603011503661; __aypstp=31; __ayspstp=31; SOKUSESSID=16030115035939Ih; l=eB_uYYpgOBE-VVIsBOfanurza77OSIRYYuPzaNbMiOCP_WfB5RSNWZ5dt4Y6C3GVh6lyR3J42eyzBeYBYQAonxvtaQYs9XHmn; tfstk=caQOB7mdK0AsswddaGEnlkML8KwlwXwvdf9mk71r4ux5Cp1mAab8F-q6GALL9; isg=BGJi2dXOSTFLnVVh3L_Kzg35s-HEs2bNtwGHtKz78lWAfwD5lEIG3PLtrbuD9N5l; JSESSIONID=0B6D8500674E0EE480005406BF907997'
        }
        self.proxy = get_proxy() if use_proxy else None

    @retry(stop_max_attempt_number=3, wait_fixed=10)
    def search_songs(self, song_name = '', **kwargs) -> list:
        
        # 搜索页码search_page
        _start = config["tudou_video_search_offset"]["start_page"]
        if kwargs.get("page_num"):
            # print(1111)
            search_page = int(kwargs.get("page_num")) + _start - 1
        else:
            search_page = _start

        # 搜索类别 search_type
        _type = config['video_search_type_default']
        
        #
        # 搜索时长 search_duration
        _duration = config['video_search_duration_default'] if not kwargs.get("search_duration") else kwargs.get(
            "search_duration")

        search_result_temp = []
        if not song_name:
            return search_result_temp
        search_url = self.search_video_url.format(song_name, search_page, _duration)
        search_response = self.get_response_single(search_url)
        search_result_temp.append(self.parse_search_video_song(search_response))
        # print(search_url)
        return unit_result_clear_for_video([j for i in search_result_temp for j in i], **kwargs)

    # 单一请求
    @retry(stop_max_attempt_number=3, wait_fixed=600)
    def get_response_single(self, url):
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
            tree = etree.HTML(response.text)
        except:
            return []
        else:
            result_list = []
            try:
                video_song_list_data = tree.xpath("//div[@class='sk_result']/div[@class='sk-vlist clearfix']/div")
                # print(len(video_song_list_data))
            except:
                video_song_list_data =[]
            for v_s in video_song_list_data:
                video_dict = dict()
                video_dict["video2_title"] = "".join(v_s.xpath(".//div[@class='v-meta va']/div[@class='v-meta-title']/a/@title"))
                if not self.check_video_title(video_dict.get("video2_title")):
                    continue
                video_dict["video2_url"] = self.url_add_http("".join(v_s.xpath(".//div[@class='v-meta va']/div[@class='v-meta-title']/a/@href")))
                video_dict["video2_author"] = "".join(v_s.xpath(".//div[@class='v-meta va']/div[@class='v-meta-entry']//span[@class='username']/a/text()"))
                # video_dict["video_author_zone"] = "".join(v_s.xpath(".//a[@class='video-meta-user']/@href"))
                video_dict["video2_pubtime"] = re_datetime_str(str_to_datetime("".join(v_s.xpath(".//div[@class='v-meta va']/div[@class='v-meta-entry']//span[@class='r']/text()"))))
                video_dict["video2_url_hash"] = md5_use(video_dict.get("video2_url"))
                video_dict["video2_platform"] = "土豆视频"  # figure_info
                duration_str_temp = "".join(v_s.xpath(".//span[@class='v-time']/text()"))
                duration, duration_str = unify_duration_format(duration_str_temp)
                video_dict["video2_duration"] = duration  # 时长（秒数）
                video_dict["video2_duration_str"] = duration_str  # 时长（字符串）
                result_list.append(video_dict)
                # print(video_dict)

        return result_list

    # 视频搜索结果通过标题模糊 %key% 筛除
    def check_video_title(self, need_check_title: str, search_title_key=""):
        return True

search_songs = TuDouVideo(use_proxy=True).search_songs
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
    print(TuDouVideo().search_songs('班淑传奇', **kwags))
