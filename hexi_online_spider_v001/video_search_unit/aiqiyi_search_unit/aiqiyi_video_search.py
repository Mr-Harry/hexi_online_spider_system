# -*- coding:utf-8 -*- #
# I don't like the world. I just like you
# author : pyl owo,
# time : 2020/7/29
import json
import random

import requests
from fake_useragent import UserAgent
from lxml import etree
from retrying import retry
from audio_tool import get_proxy, md5_use, unify_duration_format, unit_result_clear_for_video
# from video_search_unit.video_spider_tools import get_proxy, get_video_search_type_list, md5_use
from video_search_unit.Video_Infringement_Config import config_of_video as config


class AiqiyiVideo:
    def __init__(self, use_proxy=True):
        self.proxy = get_proxy() if use_proxy else None
        self.search_video_url = "https://pcw-api.iqiyi.com/graphql"
        self.yangben_dict = dict()
        self.video_search_key = ''
        self.headers = {
            'authority': 'pcw-api.iqiyi.com',
            'accept': 'application/json, text/plain, */*',
            'sec-fetch-dest': 'empty',
            'user-agent': UserAgent().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
            'content-type': 'application/x-www-form-urlencoded',
            'origin': 'https://so.iqiyi.com',
            'sec-fetch-site': 'same-site',
            'sec-fetch-mode': 'cors',
            'accept-language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7'
        }

    # 单一请求
    @retry(stop_max_attempt_number=3, wait_fixed=10)
    def get_response_single(self, url, date=None):
        response = requests.post(url, headers=self.headers, proxies=self.proxy, data=date)
        response.encoding = 'utf-8'
        return response

    @retry(stop_max_attempt_number=3, wait_fixed=10)
    def get_response_single_get(self, url, date=None):
        response = requests.get(url, headers=self.headers, proxies=self.proxy, data=date)
        response.encoding = 'utf-8'
        return response
    def set_video_search_key(self, video_search_key: str):
        self.video_search_key = video_search_key

    def search_video(self, search_key: str, video_search_type="",
                     yangben_dict=None, **kwargs):
        self.yangben_dict = yangben_dict
        self.set_video_search_key(str(search_key))
        # 搜索页码search_page
        _start = config["aiqiyi_video_search_offset"]["start_page"]
        if kwargs.get("page_num"):
            search_page = int(kwargs.get("page_num")) + _start - 1
        else:
            search_page = _start

        if not search_key:
            return []

        #
        # 搜索类别 search_type
        _type = config['video_search_type_default']
        #

        #
        # 搜索时长 search_duration
        #

        query_base_data = """
        query { MMSoResult ( from: "pcw-ssr" if: "video" need_condense: 0 key: "%s" pageNum: %s pageSize: 20 duration_level: 0 need_qc: 0 channel_name: "" site_publish_date_level: "" site: "" mode: 1 bitrate: "" data_type: "6;mustnot" intent_category_type: 1 no_play_control: 0 ip: "" u: "" pu: "" p1: "101" ) { searchO { result_num qc need_qc isreplaced event_id bkt terms search_time real_query intent_pos intent_type intent_result_num intent_action_type scoring_mode index_layer term_query { term field_name } graph_type { type intent_sub_type intent_action_type graph_sub_type } super_serial { serial_info { serial_doc_id super_album_name } } graph_categories { desc field field_name value hit } intent_graph_docinfos { __typename ...on SearchCardGraphT1 { name docid docinfo { description albumImg(size: "_128_128") starinfos { qipu_id starName } } entity_properties { property_value } } ...on SearchCardGraphT2 { name docid docinfo { g_img(size: "_260_360") g_main_link videoDocType series siteId video_lib_meta { entity_id description } } entity_properties { property_value } } ...on SearchCardGraphT8 { name docid docinfo { g_img(size: "_260_360") g_main_link videoDocType series siteId video_lib_meta { entity_id description } } child_nodes { docid docinfo { albumTitle starinfos { qipu_id } } } } ...on SearchCardGraphT3 { docid docinfo { videoDocType siteId g_year } child_nodes { docid docinfo { g_img(size: "_128_128") g_main_link g_title } properties { name } } } ...on SearchCardGraphT5 { docid docinfo { g_img(size: "_128_128") g_main_link g_title } description child_nodes { docid relation docinfo { g_img(size: "_128_128") g_main_link g_title } child_nodes { docid relation docinfo { g_img(size: "_128_128") g_main_link g_title } } } } ...on SearchCardGraphT7 { docid child_nodes { docid docinfo { g_img(size: "_128_128") g_main_link g_title } properties { docinfo { g_title g_main_link } } } } } docinfos { __typename doc_id score pos sort is_from_intent albumDocInfo { videoDocType album_type channel siteId siteName qipu_id g_id g_rec_word_id g_title g_main_link g_black_region } ...on SearchIntentStar { albumDocInfo { g_img(size: "_128_128") videoinfos(size: 1) { itemTitle, itemLink } } } ...on SearchIntentTagVideo { albumDocInfo { g_img(size: "_180_101") g_meta albumId } } ...on SearchIntentTagLive { albumDocInfo { g_img(size: "_180_101") g_corner_mark albumId live_room { presenter_nickname } } } ...on SearchIntentTagRole { albumDocInfo { g_img_link g_img(size: "_180_236") g_focus g_meta g_corner_mark albumId score star video_lib_meta { actor { id name } } live_room { presenter_nickname } } } ...on SearchCardVariety { albumDocInfo { g_img(size: "_260_360") g_corner_mark g_desc g_year g_update_strategy g_rec_word_id qipu_id super_album_order director star video_lib_meta { entity_id director { id name } host { id name } } super_show_cluster(size: 7) { super_show_cluster_info { site_id site_name cluster_tag album_url video_info { itemTitle itemLink year is_vip } site_data_doc_info { siteId siteName docid } } } clusterinfos { siteId siteName docid } videoinfos { year itemTitle subTitle itemshortTitle itemLink is_vip g_corner_mark_s qipu_id timeLength } } } ...on SearchCardEpisodeMuti { albumDocInfo { g_img(size: "_260_360") g_meta g_corner_mark g_year g_update_strategy g_desc qipu_id super_album_order albumAlias score director star video_lib_meta { entity_id director { id name } actor { id name } } clusterinfos { siteId siteName docid } videoinfos { g_corner_mark_s itemNumber itemTitle itemLink is_vip qipu_id timeLength } prevues { g_corner_mark_s itemNumber itemLink qipu_id timeLength } vip_unlock_video { g_corner_mark_s itemNumber itemLink qipu_id timeLength } } } ...on SearchCardSingleVideo { albumDocInfo { g_img(size: "_180_101") g_meta g_update_strategy g_release_time(splitor: "-") g_desc qipu_id super_album_order source_type uploader_auth_mark threeCategory videoinfos { uploader_id uploader_name is_vip qipu_id timeLength } } } ...on SearchCardSerialEmpty { albumDocInfo { g_img(size: "_180_236") g_update_strategy g_release_time g_year g_last_days g_desc super_album_order threeCategory director star video_lib_meta { entity_id category duration director { id name } actor { id name } } prevues { itemLink qipu_id timeLength } related_videos { itemLink qipu_id timeLength } } } ...on SearchCardTopic { albumDocInfo { g_img g_corner_mark g_update_strategy g_desc albumLink director star video_lib_meta { entity_id } } } ...on SearchCardMovie { albumDocInfo { g_img(size: "_260_360") g_img_link g_meta g_corner_mark g_release_time g_update_strategy g_year g_desc g_region super_album_order albumAlias is_third_party_vip score director star video_lib_meta { entity_id director { id name } actor { id name } } clusterinfos { siteId siteName docid } } } ...on SearchCardStar { albumDocInfo { g_img(size: "_128_128") g_desc starinfos { qipu_id alias_name star_english_name occupation height starBirth star_region } recommendation { g_meta_s itemTitle itemLink itemVImage subChannel role_info { role character } qipu_id timeLength } videoinfos { g_meta_s itemTitle itemLink itemVImage subChannel role_info { role character } qipu_id timeLength } } } ...on SearchCardBodan { albumDocInfo { g_img(size: "_260_360") g_img_link g_meta g_corner_mark g_release_time g_desc source_type collection_type effective_start_time effective_end_time uploader_auth_mark videoinfos { g_meta_s itemTitle subTitle itemshortTitle itemLink itemHImage initialIssueTime threeCategory is_vip qipu_id timeLength } clusterinfos { siteId siteName docid } } } ...on SearchCardUgcVerified { albumDocInfo { g_img g_desc verified_user_infos { user_id qipu_id followed_count video_count auth_mark is_verified self_media_content_rating } videoinfos { g_meta_s itemTitle itemHImage itemLink initialIssueTime qipu_id timeLength } } } ...on SearchCardBlank { albumDocInfo { g_img(size: "_180_236") g_img_link g_desc g_corner_mark g_update_strategy g_release_time g_last_days g_year g_region albumAlias albumEnglishTitle star video_lib_meta { entity_id director { id name } actor { id name } category } prevues { itemTitle timeLength itemHImage itemLink qipu_id } related_videos { itemTitle timeLength itemHImage itemLink qipu_id } music_videos { itemTitle timeLength itemHImage itemLink qipu_id } } } ...on SearchCardBook { albumDocInfo { g_img(size: "_260_360") g_desc book { author three_category } biz { button_text } } } ...on SearchCardGame { albumDocInfo { g_img g_desc g_corner_mark app { running_platform } } } ...on SearchCardTvStation { albumDocInfo { g_img g_desc g_corner_mark g_display_mark live_group { live_channel { qipu_id live_type father_live_channel_id live_status live_video { qipu_id title start_play_time stop_play_time } } } } } ...on SearchCardGameRoom { albumDocInfo { g_img g_desc live_room { presenter_nickname } } } } } hotQuery: searchMHotQueryNew(hot_query_type: 1, pagesize: 5) { hot_query_info { query } } relateQuery: searchMRelatedQuery(key: "%s") starGraph: qipuGetRelatedCelebrities{ self_info{ name entity_id imageformat_iqiyi_people } related_celebrity { name entity_id imageformat_iqiyi_people relationship } } starList: qipuGetRelatedCelebritiesOfVideo{ name entity_id imageformat_iqiyi_people } relateVideo: qiyuPortalResys30 { id name display_fields{ picture_url } } hotRank: searchMHotQueryNew { name hot_query_info { query search_trend } } } }
        """
        video_search_type_list = [_type]
        videoDocType_list = []
        if 0 in video_search_type_list:
            pass
        elif 1 in video_search_type_list:
            videoDocType_list.append(1)
        elif (2 in video_search_type_list) or (3 in video_search_type_list):
            videoDocType_list.append(2)
        ####
        # 搜索
        query_data_temp = query_base_data % (search_key, search_page, search_key)
        data = {"query": query_data_temp}
        search_url = self.search_video_url
        # print(search_url)
        # print(data)
        search_response = self.get_response_single(search_url, date=data)
        # print(video_search_type_list)
        return self.parse_search_video(search_response, videoDocType_list, **kwargs)
    def parse_html_url(self, response) -> str:
        try:
            tree = etree.HTML(response.text)
        except:
            return ''
        else:
            href = ''.join(tree.xpath('//a[contains(@class,"albumPlayBtn")]/@href'))
            if href.startswith('javascript:;javascript:;'):
                return href.replace('javascript:;javascript:;http:', '')
            else:
                return href
    # 搜索视频响应解析
    def parse_search_video(self, response, videoDocType_list=None, **kwargs) -> list:
        try:
            # print(response.text)
            response_dict = json.loads(response.text)
            # print(response_dict)
        except:
            return []
        else:
            result_list = []

            try:
                video_list_data = response_dict.get('data', {}).get('MMSoResult', {}).get('searchO', {}).get('docinfos',
                                                                                                             [])
            except:
                video_list_data = []
            if_all = True
            if videoDocType_list:
                if_all = False
            for v_i in video_list_data:
                # print(v_i)
                # print()
                video_dict = dict()
                video_info_dict = v_i.get("albumDocInfo")
                if not if_all:
                    videoDocType = video_info_dict.get("videoDocType")
                    if videoDocType not in videoDocType_list:
                        continue
                video_dict["video2_title"] = video_info_dict.get('g_title')
                if not self.check_video_title(video_dict.get("video2_title")):
                    continue
                video_dict["video2_url"] = "https:" + video_info_dict.get('g_main_link', '')
                if '.iqiyi.com/lib' in video_dict.get('video2_url'):
                    video_dict["video2_url"] = "https:" + video_info_dict.get('g_img_link', '')
                if 'www.iqiyi.com' not in video_dict.get('video2_url'):
                    continue
                if 'www.iqiyi.com/v' not in video_dict.get('video2_url'):
                    url_temp = video_dict.get('video2_url')
                    video_dict["video2_url"] = "https:" + self.parse_html_url(self.get_response_single_get(video_dict.get('video2_url')))
                    if not video_dict.get('video2_url'):
                        video_dict["video2_url"] = url_temp
                def video2_author_tool(uploader_name):
                    if uploader_name:
                        return str(uploader_name)
                    return None
                # print(video_info_dict)
                video_dict["video2_author"] = "/".join(
                    [video2_author_tool(i.get('uploader_name')) for i in video_info_dict.get('videoinfos', []) if
                     i.get('uploader_name')])
                video_dict["video2_url_hash"] = md5_use(video_dict.get("video2_url"))
                video_dict["video2_platform"] = "爱奇艺"
                video_dict["video2_video2_pubtime"] = video_info_dict.get('g_release_time', '')
                duration_str_temp = video_info_dict.get('g_meta', '')
                duration, duration_str = unify_duration_format(duration_str_temp)
                video_dict["video2_duration"] = duration  # 时长（秒数）
                video_dict["video2_duration_str"] = duration_str  # 时长（字符串）

                if not video_dict["video2_url"] or video_dict["video2_url"] == 'https:':
                    continue
                result_list.append(video_dict)
            # return result_list
            # print(result_list)
            return unit_result_clear_for_video(result_list, **kwargs)


    # 视频搜索结果通过标题模糊 %key% 筛除
    def check_video_title(self, need_check_title: str, search_title_key=""):
        return True if str(need_check_title).find(str(search_title_key)) >= 0 else False


# key='西虹市首富'
# page=2
# query_data = """
#
# response = requests.request("POST", url, headers=headers, data = data)
#
# print(response.text)

search_songs = AiqiyiVideo(use_proxy=True).search_video

if __name__ == '__main__':
    import pprint

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
    aiqiyi = AiqiyiVideo()
    video_dict = {}
    video_dict["video_title"] = '34444'
    result = aiqiyi.search_video('班淑传奇', **kwags)
    pprint.pprint(result)
    print(len(result))
