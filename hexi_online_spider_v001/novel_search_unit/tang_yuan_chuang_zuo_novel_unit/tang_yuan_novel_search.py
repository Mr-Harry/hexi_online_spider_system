# -*- coding:utf-8 -*-
# Chance favors the prepared mind.
# author : pyl owo,
# time : 2020/9/21

import json
import random
import re

from novel_search_unit.novel_spider_settings import NOVEL_CONF
from novel_search_unit.novel_spider_tools import md5_use, get_proxy, unify_requests, str_similar,clear_text
from fake_useragent import UserAgent
from lxml import etree

class TangYuanNovel():
    def __init__(self, use_proxy=True):
        self.proxy = get_proxy() if use_proxy else None
        self.headers = {
            "user-agent": UserAgent().random,
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
        self.search_base_url = "https://www.itangyuan.com/search/book/{key_words}.html?page={page}"  # 页码page从0开始

        self.novel_url_pre = "https://www.itangyuan.com"
    # 搜索小说
    def search_novel(self, search_key: str, **kwargs):
        search_result = []
        if not search_key:
            return search_result
        _start = NOVEL_CONF["tang_yuan_search_offset"]["start"]
        _end = NOVEL_CONF["tang_yuan_search_offset"]["end"]
        if kwargs.get("page_num"):
            if NOVEL_CONF["tang_yuan_search_offset"]["start_page"] == 0:
                _start = kwargs.get("page_num") - 1
                _end = kwargs.get("page_num")
            elif NOVEL_CONF["tang_yuan_search_offset"]["start_page"] == 1:
                _start = kwargs.get("page_num")
                _end = kwargs.get("page_num") + 1

        for page in range(_start, _end):
            # print(self.search_base_url.format(search_key, page))
            respose_text = unify_requests(url=self.search_base_url.format(key_words=search_key, page=page),headers=self.headers,proxies=self.proxy)
            for each in self.parse_search_novel(respose_text, **kwargs):
                search_result.append(each)
        return search_result

    # 搜索视频响应解析
    def parse_search_novel(self, response, **kwargs) -> list:
        try:
            select = etree.HTML(response.text)

        except:
            return []
        else:
            result_list = []
            book_list = select.xpath("//div[@class='book-list']//div[@class='book']")
            for each in book_list:
                qin_quan_author_str = ''.join(each.xpath(".//p[@class='author']/a//text()")).replace(" ","") # 侵权作者
                qin_quan_title_str = ''.join(each.xpath(".//p[@class='bname']//text()")).replace(" ","")  # 侵权标题
                qin_quan_url_str = self.novel_url_pre+''.join(each.xpath("./a/@href")).replace(" ","")  # 侵权链接
                qin_quan_id_int = ''.join(each.xpath("./a/@href")).replace("/book/","").replace(".html","")# 样本ID 数值类型
                qin_quan_mid_str = ''  # 侵权ID 字符串形式

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
                novel_dict['qin_quan_platform_str'] = '汤圆创作'  # 侵权平台
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
                # novel_dict['all_recommend_str'] = ''  # 总推荐数 str
                # novel_dict['month_recommend_str'] = ''  # 月推荐数 str
                # novel_dict['week_recommend_str'] = ''  # 周推荐数 str
                # novel_dict['all_read_int'] = ''  # 总阅读数 int
                # novel_dict['month_read_int'] = ''  # 月阅读数 int
                # novel_dict['week_read_int'] = ''  # 周阅读数 int
                # novel_dict['all_words_number_int'] = ''  # 总字数
                # novel_dict['book_status_str'] = ''  # 书籍状态 （连载，完结，暂无）
                # novel_dict['book_property_str'] = ''  # 书籍属性 （免费，会员，限免）
                # novel_dict['author_type_str'] = ''  # 作者类型 （金牌，签约，独立 默认无）
                # novel_dict['book_lable_str'] = ''  # 书籍标签 （用｜分割的字符串 ''科幻｜现实｜励志''）
                # novel_dict['book_type_str'] = ''  # 书籍分类 （玄幻 ,科幻，言情...）按搜索结果来多个按｜分割
                # novel_dict['book_update_time'] = ''  # 书籍更新日期 年-月-日
                # novel_dict['book_zong_zhang_jie_int'] = ''  # 书籍总的章节 完结的，未完结就填目前的总章节
                # novel_dict['book_zui_xin_zhang_jie_name_str'] = ''  # 最新章节名称
                # novel_dict['book_introduce_text'] = ''  # 书籍简介 text
                # novel_dict['book_cover_image_str'] = ''  # 书籍封面 URL
                # novel_dict['book_detail_url_str'] = ''  # 书籍详情URL
                # novel_dict['book_detail_id_int'] = ''  # 书籍详情ID 数字形式
                # novel_dict['book_detail_id_str'] = ''  # 书籍详情ID 字符形式
                # novel_dict['book_zhan_dian_str'] = ''  # 书籍站点 （男生，女生，暂无）
                # novel_dict['book_publish_str'] = ''  # 出版社 默认侵权平台'
                # novel_dict['book_commeds_int'] = ''  # 书籍评论数
                # novel_dict['author_grade_float'] = ''  # 作者评分
                # novel_dict['author_page_url_str'] = ''  # 作者主页链接
                # novel_dict['author_book_number_int'] = ''  # 作者书籍总数
                # novel_dict['author_likes_int'] = ''  # 作者获赞总数
                # novel_dict['author_all_words_number_str'] = ''  # 作者累计创作字数
                # novel_dict['author_produce_days_str'] = ''  # 作者累计创作天数
                # novel_dict['author_fens_number_int'] = ''  # 作者粉丝数
                # novel_dict['author_head_image_url_str'] = ''  # 作者头像URL
                # novel_dict['author_id_str'] = ''  # 作者ID 字符形式
                # novel_dict[''] = ''  #
                result_list.append(novel_dict)
            return result_list

# 统一的调用 search_novels
search_novels = TangYuanNovel(use_proxy=True).search_novel
if __name__ == "__main__":
    yangben_dict = {
        'id': '10000',
        'yang_ben_author_str': '夏末蔷薇',
        'yang_ben_title_str': '豪门擒爱：总裁莫贪欢',
        'yang_ben_url_str': 'https://t.shuqi.com/cover/6695029',
    }
    result = search_novels('我的好', **yangben_dict)
    # shuqi = ShuQiNovel(use_proxy=True)
    # result = shuqi.search_novel('爱', **yangben_dict)
    print(len(result))
    print(result)
