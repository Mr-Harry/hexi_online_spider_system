# -*- coding:utf-8 -*-
import json
import random
from novel_search_unit.novel_spider_settings import NOVEL_CONF
from novel_search_unit.novel_spider_tools import md5_use, get_proxy, unify_requests, str_similar, clear_text
import requests
from pyquery import PyQuery as pq
from lxml.etree import fromstring
from lxml import etree
from fake_useragent import UserAgent


class ZongHengNovel:
    def __init__(self, use_proxy=True):
        self.proxy = get_proxy() if use_proxy else {}
        self.headers = {
            "user-agent": UserAgent().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
        }

    def get_author(self, author_url):
        response = pq(unify_requests(url=author_url, headers=self.headers).text)
        qin_quan_author_str = response('.name').text().replace('作者', '')
        # print(author_url,qin_quan_author_str)
        return qin_quan_author_str

    def get_title(self, book_url):
        response = pq(unify_requests(url=book_url, headers=self.headers).text)
        qin_quan_title_str = response('.book-name').text()
        return qin_quan_title_str

    def search_novel(self, search_key: str, **kwargs):
        search_result = []
        if not search_key:
            return search_result
        _start = NOVEL_CONF["zongheng_search_offset"]["start"]
        _end = NOVEL_CONF["zongheng_search_offset"]["end"]
        if kwargs.get("page_num"):
            if NOVEL_CONF["zongheng_search_offset"]["start_page"] == 0:
                _start = kwargs.get("page_num") - 1
                _end = kwargs.get("page_num")
            elif NOVEL_CONF["zongheng_search_offset"]["start_page"] == 1:
                _start = kwargs.get("page_num")
                _end = kwargs.get("page_num") + 1
        for page in range(_start, _end):
            search_url = f'http://search.zongheng.com/s?keyword={search_key}&pageNo={page}'
            respose_text = unify_requests(url=search_url, headers=self.headers)
            # print(respose_text.url)
            for each in self.parse_search_novel(respose_text, **kwargs):
                search_result.append(each)
        return search_result

    def parse_search_novel(self, response, **kwargs) -> list:
        result_list = []
        doc = pq(response.text)
        html_str = etree.HTML(response.text)
        div_list = html_str.xpath('//*[@class="search-tab"]/div')[0:-3]
        # print(len(div_list))
        # print(response.text)
        for div in div_list:
            try:
                author_url = "".join(div.xpath('.//div[@class="bookinfo"]/a[1]/@href'))
            except:
                author_url = None
            if author_url:
                qin_quan_author_str = self.get_author(author_url)
            else:
                continue

            qin_quan_url_str = "".join(div.xpath('./div[2]/h2/a/@href'))
            # qin_quan_title_str = self.get_title(qin_quan_url_str)
            qin_quan_title_str =  "".join(div.xpath('./div[2]/h2/a/text()'))
            qin_quan_id_int = int("".join(qin_quan_url_str.split('/')[-1].split('.')[0]))
            qin_quan_mid_str = qin_quan_url_str.split('/')[-1].split('.')[0]
            yangben_id = kwargs.get('id', '')
            novel_dict = dict()
            # novel_dict['author_id_str'] = ''  # 作者ID 字符形式
            novel_dict['yang_ben_author_str'] = kwargs.get('yang_ben_author_str', '')  # 样本作者
            novel_dict['yang_ben_title_str'] = kwargs.get('yang_ben_title_str', '')  # 样本标题
            novel_dict['yang_ben_url_str'] = kwargs.get('yang_ben_url_str', '')  # 样本链接
            novel_dict['yang_ben_id_int'] = kwargs.get('yang_ben_id_int', '')  # 样本ID 数值类型
            novel_dict['yang_ben_mid_str'] = kwargs.get('yang_ben_mid_str', '')  # 样本ID 字符串形式
            novel_dict['yang_ben_task_id_int'] = kwargs.get('yang_ben_task_id_int', '')  # 样本主任务ID
            novel_dict['yang_ben_platform_str'] = kwargs.get('yang_ben_platform_str', '')  # 样本平台
            novel_dict['yang_ben_batch_id_int'] = kwargs.get('yang_ben_batch_id_int', '')  # 样本批次ID
            novel_dict['yang_ben_batch_id_int'] = kwargs.get('yang_ben_batch_id_int', '')  # 样本批次ID
            novel_dict['book_type_str'] = "|".join(div.xpath('.//div[@class="bookinfo"]/a[2]/text()'))

            novel_dict['search_key_words_str'] = kwargs.get('search_key_words_str', '')  # 搜索关键词
            novel_dict['qin_quan_platform_str'] = '纵横中文网'  # 侵权平台
            novel_dict['qin_quan_author_str'] = qin_quan_author_str  # 侵权作者
            novel_dict['qin_quan_title_str'] = qin_quan_title_str  # 侵权标题
            novel_dict['qin_quan_url_str'] = qin_quan_url_str  # 侵权链接
            novel_dict['qin_quan_id_int'] = int(qin_quan_id_int)  # 样本ID 数值类型
            novel_dict['qin_quan_mid_str'] = qin_quan_mid_str  # 侵权ID 字符串形式
            novel_dict['qin_quan_url_hash_str'] = str(yangben_id) + '|' + md5_use(
                qin_quan_url_str)  # 唯一索引，样本task_id 侵权url（md5）

            novel_dict['similar_number_float'] = None  # 作品相似度
            novel_dict['title_similar_number_float'] = str_similar(clear_text(kwargs.get('yang_ben_title_str', '')),
                                                                   clear_text(qin_quan_title_str))  # 标题相似度
            novel_dict['author_similar_number_float'] = str_similar(clear_text(kwargs.get('yang_ben_author_str', '')),
                                                                    clear_text(qin_quan_author_str))  # 作者名称相似度
            novel_dict['qin_quan_type_int'] = 4  # 侵权类型 4 （0 图文，1，视频，2音频）
            novel_dict['qin_quan_platform_id_int'] = ""  # 默认空
            novel_dict["qin_quan_flag_int"] = -1
            if novel_dict["title_similar_number_float"] >= NOVEL_CONF["novel_similar"] and novel_dict[
                "author_similar_number_float"] >= NOVEL_CONF["novel_similar"]:
                novel_dict["qin_quan_flag_int"] = 1
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
            # novel_dict[''] = ''  #
            result_list.append(novel_dict)
        return result_list


search_novels = ZongHengNovel(use_proxy=True).search_novel

if __name__ == '__main__':
    yangben_dict = {
        'id': '10000',
        'yang_ben_author_str': '夏末蔷薇',
        'yang_ben_title_str': '爱',
        'yang_ben_url_str': 'https://t.shuqi.com/cover/6695029',
        'page_num': 2
    }
    # result = search_novels('豪门擒爱：总裁莫贪欢', **yangben_dict)
    # qidian = ZongHengNovel(use_proxy=True)
    result = search_novels(yangben_dict['yang_ben_title_str'], **yangben_dict)
    print(result)
    print(len(result))