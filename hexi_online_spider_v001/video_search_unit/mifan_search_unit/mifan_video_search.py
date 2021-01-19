# -*- coding:utf-8 -*- #
# I don't like the world. I just like you
# author : pyl owo,
# time : 2020/8/6
import json

import requests
from retrying import retry

from video_search_unit.Video_Infringement_Config import config_of_video as config
from video_search_unit.video_spider_tools import get_video_search_type_list_v2, check_video_title, md5_use
from video_spider_tools import get_proxy


class MiFanVideo:
    def __init__(self, use_proxy=True):
        self.proxy = get_proxy() if use_proxy else None
        self.headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/plain, */*',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'Origin': 'https://www.imifanlive.com',
            'Sec-Fetch-Site': 'same-site',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Dest': 'empty',
            'Referer': 'https://www.imifanlive.com/search?searchContent=%E6%95%B0%E5%AD%97%E5%93%A5',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
        }
        self.api_video_search_key = ''
        self.yangben_dict = {}
        self.video_search_live_base_url = "https://api.imifanlive.com/mifan-search/v1/channels/search?from=&keyword=%s&page=0"  # 页码page从0开始

    def search_video(self, search_key: str, video_search_type="",
                     start_page=config.get("mifan_video_search_offset", {}).get("start", 0),
                     end_page=config.get("mifan_video_search_offset", {}).get("end", 1),
                     # page_size=config.get("mifan_video_search_offset", {}).get("pagesize", 20),
                     yangben_dict=None):
        search_result = []
        if not search_key:
            return search_result
        self.api_video_search_key = str(search_key)
        self.yangben_dict = yangben_dict
        ####
        video_search_type_list = get_video_search_type_list_v2(video_search_type)
        ####
        # 直播搜索
        if (0 in video_search_type_list) or (5 in video_search_type_list):
            live_url_temp = self.video_search_live_base_url % (search_key)
            for i in range(start_page, end_page):
                live_url = live_url_temp.format(i)
                # print(live_url)
                search_response = self.get_response_single(live_url)
                search_result.append(self.parse_search_video(search_response))
        return [j for i in search_result for j in i]

    # 搜索视频响应解析
    def parse_search_video(self, response) -> list:
        try:
            response_dict = json.loads(response.text)
            # print(response_dict)
        except:
            return []
        else:
            result_list = []
            video_list_data = response_dict.get('data', {}).get('items', []) if response_dict.get('data',
                                                                                                  {}) else []
            for v_i in video_list_data:
                video_dict = dict()
                live_status = v_i.get('living', False)
                if not live_status:
                    continue
                video_dict["video2_title"] = v_i.get('cname', '')
                if not check_video_title(video_dict.get("video2_title"), self.api_video_search_key):
                    continue
                video_dict["video2_url"] = "https://www.imifanlive.com/" + str(v_i.get('id', ''))
                video_dict["video2_author"] = v_i.get('uname', '')
                video_dict["video2_url_hash"] = md5_use(video_dict.get("video2_url"))
                video_dict["video2_platform"] = "秘饭直播"
                video_dict["video2_type"] = 5
                # 样本数据
                if self.yangben_dict and isinstance(self.yangben_dict, dict):
                    video_dict["video_title"] = self.yangben_dict.get("video_title")
                    video_dict["video_author"] = self.yangben_dict.get("video_author")
                    video_dict["video_url"] = self.yangben_dict.get("video_url")
                result_list.append(video_dict)
            return result_list
    # 单一请求
    @retry(stop_max_attempt_number=3, wait_fixed=10)
    def get_response_single(self, url):
        return requests.get(url, headers=self.headers, proxies=self.proxy)


if __name__ == "__main__":
    mifan = MiFanVideo(use_proxy=True)
    result = mifan.search_video('数字哥')
    print(len(result))
    print(result)
