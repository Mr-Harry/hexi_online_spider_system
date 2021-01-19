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


class ZhuaFanVideo:
    def __init__(self, use_proxy=True):
        self.proxy = get_proxy() if use_proxy else None
        self.headers = {
            'Connection': 'keep-alive',
            'Accept': 'application/json, text/javascript, */*; q=0.01',
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
            'X-Requested-With': 'XMLHttpRequest',
            'Referer': 'http://www.zhuafan.live/searchpage',
            'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
            # 'Cookie': 'uni_id=z2eu1gvy36268247ztfgl4g431600517; UM_distinctid=173b2bd201b32f-0160dacba52029-3972095d-1fa400-173b2bd201c44b; c=aWdyYOnm-1596431610684-204ef64ec552b-636495533; Hm_lvt_86cd7453114a91ce02d1b3484d69496e=1596431884,1596432665,1596437022,1596715870; sensorsdata2015jssdkcross=%7B%22distinct_id%22%3A%22173b2bd29ce439-01036eccee7b5f-3972095d-2073600-173b2bd29cf361%22%2C%22first_id%22%3A%22%22%2C%22props%22%3A%7B%22%24latest_traffic_source_type%22%3A%22%E7%9B%B4%E6%8E%A5%E6%B5%81%E9%87%8F%22%2C%22%24latest_search_keyword%22%3A%22%E6%9C%AA%E5%8F%96%E5%88%B0%E5%80%BC_%E7%9B%B4%E6%8E%A5%E6%89%93%E5%BC%80%22%2C%22%24latest_referrer%22%3A%22%22%7D%2C%22%24device_id%22%3A%22173b2bd29ce439-01036eccee7b5f-3972095d-2073600-173b2bd29cf361%22%7D; y_id=j5rfwvkb412324608cf6bawj16069264; CNZZDATA1275285685=1482899456-1596429072-null%7C1596715974; vipFrame=%5B%7B%22vipLevel%22%3A1%2C%22name%22%3A%22%u7537%u7235%22%2C%22bedge%22%3A%22http%3A//img.justfun.live/vip/badge/1.png%22%2C%22frame%22%3A%22http%3A//img.justfun.live/upload/1595991443799291.png%22%2C%22animation%22%3A%22animation_1542874002352%22%2C%22animationPC%22%3A%22animation_1542874033464%22%2C%22svgaAnimation%22%3A%22http%3A//img.justfun.live/gift/svga/xuancaimotuo_400x300.svga%22%2C%22svgaAnimationPC%22%3A%22http%3A//img.justfun.live/gift/svga/xuancaimotuo_750x550.svga%22%2C%22bgColor%22%3A%22%23000000%22%2C%22opacity%22%3A%2270%22%2C%22labelPicture%22%3Anull%2C%22openvipBarrageBackground%22%3A%22http%3A//img.justfun.live/vip/barrageBackground/bg1.png%22%7D%2C%7B%22vipLevel%22%3A2%2C%22name%22%3A%22%u4F2F%u7235%22%2C%22bedge%22%3A%22http%3A//img.justfun.live/vip/badge/2.png%22%2C%22frame%22%3A%22http%3A//img.justfun.live/upload/1595991469551361.png%22%2C%22animation%22%3A%22animation_1542874055087%22%2C%22animationPC%22%3A%22animation_1542874079231%22%2C%22svgaAnimation%22%3A%22http%3A//img.justfun.live/gift/svga/zunlamborghini_400.svga%22%2C%22svgaAnimationPC%22%3A%22http%3A//img.justfun.live/gift/svga/zunlamborghini_750.svga%22%2C%22bgColor%22%3A%22%23000000%22%2C%22opacity%22%3A%2270%22%2C%22labelPicture%22%3Anull%2C%22openvipBarrageBackground%22%3A%22http%3A//img.justfun.live/vip/barrageBackground/bg2.png%22%7D%2C%7B%22vipLevel%22%3A3%2C%22name%22%3A%22%u4FAF%u7235%22%2C%22bedge%22%3A%22http%3A//img.justfun.live/vip/badge/3.png%22%2C%22frame%22%3A%22http%3A//img.justfun.live/upload/1595991493621751.png%22%2C%22animation%22%3A%221%22%2C%22animationPC%22%3A%221%22%2C%22svgaAnimation%22%3A%22http%3A//img.justfun.live/gift/svga/car_400x300.svga%22%2C%22svgaAnimationPC%22%3A%22http%3A//img.justfun.live/gift/svga/car_750.svga%22%2C%22bgColor%22%3A%22%23000000%22%2C%22opacity%22%3A%2270%22%2C%22labelPicture%22%3Anull%2C%22openvipBarrageBackground%22%3A%22http%3A//img.justfun.live/vip/barrageBackground/bg3.png%22%7D%2C%7B%22vipLevel%22%3A4%2C%22name%22%3A%22%u516C%u7235%22%2C%22bedge%22%3A%22http%3A//img.justfun.live/upload/1542250228773241.png%22%2C%22frame%22%3A%22http%3A//img.justfun.live/vip/barrageBackground/bg4.png%22%2C%22animation%22%3Anull%2C%22animationPC%22%3Anull%2C%22svgaAnimation%22%3Anull%2C%22svgaAnimationPC%22%3Anull%2C%22bgColor%22%3Anull%2C%22opacity%22%3Anull%2C%22labelPicture%22%3Anull%2C%22openvipBarrageBackground%22%3Anull%7D%2C%7B%22vipLevel%22%3A5%2C%22name%22%3A%22%u4EB2%u738B%22%2C%22bedge%22%3A%22http%3A//img.justfun.live/upload/154224898097311.png%22%2C%22frame%22%3A%22http%3A//img.justfun.live/vip/barrageBackground/bg5.png%22%2C%22animation%22%3Anull%2C%22animationPC%22%3Anull%2C%22svgaAnimation%22%3Anull%2C%22svgaAnimationPC%22%3Anull%2C%22bgColor%22%3Anull%2C%22opacity%22%3Anull%2C%22labelPicture%22%3Anull%2C%22openvipBarrageBackground%22%3Anull%7D%2C%7B%22vipLevel%22%3A6%2C%22name%22%3A%22%u7687%u5E1D%22%2C%22bedge%22%3A%22http%3A//img.justfun.live/upload/1542249005816161.png%22%2C%22frame%22%3A%22http%3A//img.justfun.live/vip/barrageBackground/bg6.png%22%2C%22animation%22%3Anull%2C%22animationPC%22%3Anull%2C%22svgaAnimation%22%3Anull%2C%22svgaAnimationPC%22%3Anull%2C%22bgColor%22%3Anull%2C%22opacity%22%3Anull%2C%22labelPicture%22%3Anull%2C%22openvipBarrageBackground%22%3Anull%7D%5D; worldColor=%7B%22color%22%3A%22%23ffffff%3B%23F86319%3B%2389F3A5%3B%23EEB049%3B%23F75CC5%3B%23C57CFD%3B%2377B9FB%22%2C%22colors%22%3A%5B%22%23000%22%2C%22%23F86319%22%2C%22%2389F3A5%22%2C%22%23EEB049%22%2C%22%23F75CC5%22%2C%22%23C57CFD%22%2C%22%2377B9FB%22%5D%7D; JSESSIONID=3b3601f08f5c347daa27789179a7; Hm_lpvt_86cd7453114a91ce02d1b3484d69496e=1596716180; _fmdata=Qq5bPVQ%2BMR5Nf1aBOat3Hv7U3cNz3pZc5C5oNiEuYQnbz%2BmajsYxmpwjjcm2IJQFrlpsMi5qPZ2mK7mLa%2BGhShRbgz5LfkzxokZ%2FJIG0BYI%3D; _xid=1LkzV3oJo%2Fuky8UFZJ9ezUFndiig34Ze6F2Gf%2FkFTStRIMu0ezJHt0%2FluXULqpZcqGWvcxB6Tg4mesR3fOgnhw%3D%3D'
        }
        self.api_video_search_key = ''
        self.yangben_dict = {}
        self.video_search_live_base_url = "http://www.zhuafan.live/live-search/search/query/data?keyword=%s&page=1&num=%s&searchType=cname&uid=null&from=pc"  # 页码page从1开始

    def search_video(self, search_key: str, video_search_type="",
                     start_page=config.get("zhuafan_video_search_offset", {}).get("start", 0),
                     end_page=config.get("zhuafan_video_search_offset", {}).get("end", 1),
                     page_size=config.get("zhuafan_video_search_offset", {}).get("pagesize", 20),
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
            live_url_temp = self.video_search_live_base_url % (search_key, page_size)
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
            video_list_data = response_dict.get('cObj', {}).get('cList', []) if response_dict.get('cObj', {}) else []
            for v_i in video_list_data:
                video_dict = dict()
                live_status = v_i.get('onlinescore', 0)
                if not live_status:
                    continue
                video_dict["video2_title"] = v_i.get('cname', '').replace('<em>', '').replace('</em>', '')
                if not check_video_title(video_dict.get("video2_title"), self.api_video_search_key):
                    continue
                video_dict["video2_url"] = "http://www.zhuafan.live/" + str(v_i.get('url', ''))
                video_dict["video2_author"] = v_i.get('uname', '')
                video_dict["video2_url_hash"] = md5_use(video_dict.get("video2_url"))
                video_dict["video2_platform"] = "抓饭直播"
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
    zhuafan = ZhuaFanVideo(use_proxy=True)
    result = zhuafan.search_video('世锦赛')
    print(len(result))
    print(result)
