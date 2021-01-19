# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/9/25

import datetime
import json
import random

from fake_useragent import UserAgent

from novel_search_unit.novel_spider_settings import NOVEL_CONF
from novel_search_unit.novel_spider_tools import md5_use, get_proxy, unify_requests, str_similar, clear_text,timestamp_strftime


class HongShuNovel():
    def __init__(self, use_proxy=True):
        self.proxy = get_proxy() if use_proxy else None
        self.headers = {
            'User-Agent': UserAgent().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),

            'authority': 'read.xiaoshuo1-sm.com',
            'cache-control': 'max-age=0',
            'upgrade-insecure-requests': '1',
            # 'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'sec-fetch-site': 'none',
            'sec-fetch-mode': 'navigate',
            'sec-fetch-user': '?1',
            'sec-fetch-dest': 'document',
            'accept-language': 'zh-CN,zh;q=0.9'
}
        self.api_novel_search_key = ''
        self.search_base_url = "https://g.hongshu.com/bookajax/search.do?keyword={key_words}&keywordtype=1&free=0&finish=0&charnum=0&updatetime=0&order=0&copyright=1&pagesize=10&sex_flag=nv&pagenum={page}&classids=0&_=1600999803393&callback=jsonp3"
        self.novel_url_pre = "https://g.hongshu.com"

    # 搜索小说
    def search_novel(self, search_key: str, **kwargs):
        search_result = []
        if not search_key:
            return search_result
        _start = NOVEL_CONF["hong_shu_wang_search_offset"]["start"]
        _end = NOVEL_CONF["hong_shu_wang_search_offset"]["end"]
        if kwargs.get("page_num"):
            if NOVEL_CONF["hong_shu_wang_search_offset"]["start_page"] == 0:
                _start = kwargs.get("page_num") - 1
                _end = kwargs.get("page_num")
            elif NOVEL_CONF["hong_shu_wang_search_offset"]["start_page"] == 1:
                _start = kwargs.get("page_num")
                _end = kwargs.get("page_num") + 1

        for page in range(_start, _end):
            respose_text = unify_requests(url=self.search_base_url.format(key_words=search_key, page=page), headers=self.headers, proxies=self.proxy)
            # print(respose_text.text[7:-1])
            for each in self.parse_search_novel(respose_text, **kwargs):
                search_result.append(each)
        return search_result

    # 搜索视频响应解析
    def parse_search_novel(self, response, **kwargs) -> list:
        try:
            response_dict = json.loads(response.text[7:-1])
            # print(response_dict)
        except:
            return []
        else:
            result_list = []
            novel_list_data = response_dict.get('bookinfo', []) if response_dict.get('bookinfo', []) else []
            for n_l in novel_list_data:
                qin_quan_author_str = n_l.get('authorname')  # 侵权作者
                qin_quan_title_str = n_l.get('catename')  # 侵权标题
                qin_quan_url_str = self.novel_url_pre + str(n_l.get('bid', ''))  # 侵权链接
                qin_quan_id_int = n_l.get('bid')  # 样本ID 数值类型
                qin_quan_mid_str = n_l.get('bid')  # 侵权ID 字符串形式
                # print(qin_quan_mid_str,qin_quan_author_str,qin_quan_title_str)

                yangben_id = kwargs.get('id', '')

                novel_dict = dict()
                novel_dict['yang_ben_author_str'] = kwargs.get('yang_ben_author_str', '')  # 样本作者
                novel_dict['yang_ben_title_str'] = kwargs.get('yang_ben_title_str', '')  # 样本标题
                novel_dict['yang_ben_url_str'] = kwargs.get('yang_ben_url_str', '')  # 样本链接
                novel_dict['yang_ben_id_int'] = kwargs.get('yang_ben_id_int', '')  # 样本ID 数值类型
                novel_dict['yang_ben_mid_str'] = kwargs.get('yang_ben_mid_str', '')  # 样本ID 字符串形式
                novel_dict['yang_ben_task_id_int'] = kwargs.get('yang_ben_task_id_int', '')  # 样本主任务ID
                novel_dict['yang_ben_platform_str'] = kwargs.get('yang_ben_platform_str', '')  # 样本平台
                novel_dict['yang_ben_batch_id_int'] = kwargs.get('yang_ben_batch_id_int', '')  # 样本批次ID
                novel_dict['yang_ben_batch_id_int'] = kwargs.get('yang_ben_batch_id_int', '')  # 样本批次ID

                novel_dict['search_key_words_str'] = kwargs.get('search_key_words_str', '')  # 搜索关键词
                novel_dict['qin_quan_platform_str'] = '红薯小说'  # 侵权平台
                novel_dict['qin_quan_author_str'] = qin_quan_author_str  # 侵权作者
                novel_dict['qin_quan_title_str'] = qin_quan_title_str  # 侵权标题
                novel_dict['qin_quan_url_str'] = qin_quan_url_str  # 侵权链接
                novel_dict['qin_quan_id_int'] = qin_quan_id_int  # 样本ID 数值类型
                novel_dict['qin_quan_mid_str'] = qin_quan_mid_str  # 侵权ID 字符串形式
                novel_dict['qin_quan_url_hash_str'] = str(yangben_id) + '|' + md5_use(qin_quan_url_str) # 唯一索引，样本task_id 侵权url（md5）

                novel_dict['similar_number_float'] = ''  # 作品相似度
                novel_dict['title_similar_number_float'] = str_similar(clear_text(kwargs.get('yang_ben_title_str', '')), clear_text(qin_quan_title_str))  # 标题相似度
                novel_dict['author_similar_number_float'] = str_similar(clear_text(kwargs.get('yang_ben_author_str', '')), clear_text(qin_quan_author_str))  # 作者名称相似度
                novel_dict['qin_quan_type_int'] = 4  # 侵权类型 4 （0 图文，1，视频，2音频）
                novel_dict['qin_quan_platform_id_int'] = ''  # 默认空
                novel_dict["qin_quan_flag_int"] = -1
                if novel_dict["title_similar_number_float"] >= NOVEL_CONF["novel_similar"] and novel_dict["author_similar_number_float"] >= NOVEL_CONF["novel_similar"]:
                    novel_dict["qin_quan_flag_int"] =1
                novel_dict["qin_quan_spider_time"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                novel_dict['all_recommend_str'] = n_l.get('total_fav','')  # 总推荐数 str
                # novel_dict['month_recommend_str'] = ''  # 月推荐数 str
                # novel_dict['week_recommend_str'] = ''  # 周推荐数 str
                # novel_dict['all_read_int'] = ''  # 总阅读数 int
                # novel_dict['month_read_int'] = ''  # 月阅读数 int
                # novel_dict['week_read_int'] = ''  # 周阅读数 int
                novel_dict['all_words_number_int'] = n_l.get('charnum','')  # 总字数
                novel_dict['book_status_str'] = n_l.get('finish','')  # 书籍状态 （连载，完结，暂无） finish
                novel_dict['book_status_str'] = "完结" if int(novel_dict['book_status_str'])==1 else "连载"
                novel_dict['book_property_str'] = n_l.get('shouquanname','')  # 书籍属性 （免费，会员，限免）
                novel_dict['book_grade_str'] = n_l.get('star','')  # 书籍评分
                novel_dict['book_grade_str'] = n_l.get('total_hit','')  # 点击数
                # novel_dict['author_type_str'] = ''  # 作者类型 （金牌，签约，独立 默认无）
                novel_dict['book_lable_str'] = "|".join(n_l.get('tag',''))  # 书籍标签 （用｜分割的字符串 ''科幻｜现实｜励志''）
                novel_dict['book_type_str'] = "|".join(n_l.get('tag',''))  # 书籍分类 （玄幻 ,科幻，言情...）按搜索结果来多个按｜分割
                novel_dict['book_update_time'] = timestamp_strftime("%Y-%m-%d",n_l.get('updatetime',''))  # 书籍更新日期 年-月-日
                # novel_dict['book_zong_zhang_jie_int'] = ''  # 书籍总的章节 完结的，未完结就填目前的总章节
                novel_dict['book_zui_xin_zhang_jie_name_str'] = n_l.get('last_update_title','')  # 最新章节名称
                novel_dict['book_introduce_text'] = n_l.get('intro','')  # 书籍简介 text
                novel_dict['book_cover_image_str'] = n_l.get('bookface','')  # 书籍封面 URL
                novel_dict['book_detail_url_str'] = "https://g.hongshu.com/books/{}.html".format(n_l.get('bid',''))  # 书籍详情URL
                novel_dict['book_detail_id_int'] = n_l.get('bid','')  # 书籍详情ID 数字形式
                novel_dict['book_detail_id_str'] = n_l.get('bid','')  # 书籍详情ID 字符形式
                # novel_dict['book_zhan_dian_str'] = ''  # 书籍站点 （男生，女生，暂无）
                novel_dict['book_publish_str'] = '红薯小说'  # 出版社 默认侵权平台'
                # novel_dict['book_commeds_int'] = ''  # 书籍评论数
                # novel_dict['author_grade_float'] = ''  # 作者评分
                # novel_dict['author_page_url_str'] = ''  # 作者主页链接
                # novel_dict['author_book_number_int'] = ''  # 作者书籍总数
                # novel_dict['author_likes_int'] = ''  # 作者获赞总数
                # novel_dict['author_all_words_number_str'] = ''  # 作者累计创作字数
                # novel_dict['author_produce_days_str'] = ''  # 作者累计创作天数
                # novel_dict['author_fens_number_int'] = ''  # 作者粉丝数
                # novel_dict['author_head_image_url_str'] = ''  # 作者头像URL
                # novel_dict[''] = ''  #
                result_list.append(novel_dict)
            return result_list


# 统一的调用 search_novels
search_novels = HongShuNovel(use_proxy=True).search_novel
if __name__ == "__main__":
    yangben_dict = {
        'id': '10000',
        'yang_ben_author_str': '夏末蔷薇',
        'yang_ben_title_str': '豪门擒爱：总裁莫贪欢',
        'yang_ben_url_str': 'https://t.shuqi.com/cover/6695029',
        'page_num': 5,

    }
    result = search_novels('爱', **yangben_dict)
    # shuqi = ShuQiNovel(use_proxy=True)
    # result = shuqi.search_novel('爱', **yangben_dict)
    print(len(result))
    print(result[0])
