# -*- coding:utf-8 -*-
# Chance favors the prepared mind.
# author : pyl owo,
# time : 2020/9/22

import json
import random

from fake_useragent import UserAgent
from lxml import etree

from audio_tool import get_proxy, unify_requests, md5_use, clear_text, str_similar, get_parms_value
from cartoon_search_unit.cartoon_spider_settings import CARTOON_CONF


class KuKuDongManCartoon:
    def __init__(self, use_proxy=CARTOON_CONF.get('search_use_proxy')):
        self.proxy = get_proxy() if use_proxy else None
        self.info_proxy = get_proxy() if CARTOON_CONF.get('search_info_proxy') else None
        self.headers = {
            'User-Agent': UserAgent().random,
            "Proxy-Tunnel": str(random.randint(1, 10000)),
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            # 'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Language': 'zh-CN,zh;q=0.9',
            }
        self.api_qin_quan_search_key = ''
        self.search_base_url = "https://so.kukudm.com/search.asp?page={}&kw={}"

    # 搜索侵权
    def search_qin_quan(self, search_key: str, **kwargs):
        _page = kwargs.get("page_num") + CARTOON_CONF["kukudm_search_offset"]["start_page"] - 1 if kwargs.get("page_num") else CARTOON_CONF["kukudm_search_offset"]["start_page"]
        return self.parse_search_qin_quan(unify_requests(url=self.search_base_url.format(self.url_value_to_gb2312_upper(search_key), _page), headers=self.headers, proxies=self.proxy), **kwargs)

    def url_value_to_gb2312_upper(self, value):
        return str(value.replace(' ', '').encode('gb2312')).lstrip("b\'").replace("'", '').replace("\\x", "%").upper()
    # 侵权详情 *
    def qin_quan_info(self, qin_quan_url):
        return unify_requests(url=qin_quan_url, headers=self.headers, proxies=self.info_proxy)

    # 搜索视频响应解析
    def parse_search_qin_quan(self, response, **kwargs) -> list:
        try:
            # print(response.text)
            # response_data = json.loads(response.text)
            response.encoding = 'gbk'
            response_data = etree.HTML(response.text)
        except:
            return []
        else:
            result_list = []

            # qin_quaq_list_data = response_data.get('data')
            qin_quaq_list_data = response_data.xpath('//dl[@id="comicmain"]/dd')
            # print(len(qin_quaq_list_data))
            for q_l in qin_quaq_list_data:
                # xpath_demo = ''.join(q_l.xpath(''))
                qin_quan_url_str = ''.join(q_l.xpath('./a')[2].xpath('./@href'))  # 侵权链接
                try:
                    # response_data = json.loads(response.text)
                    # print(qin_quan_url_str)
                    info_response = self.qin_quan_info(qin_quan_url_str)
                    info_response.encoding = 'gbk'
                    qin_quan_info_data = etree.HTML(info_response.text)
                    qin_quan_info_data = qin_quan_info_data.xpath('//div[@class="sub_r"]/p/text()')
                    # print(etree.tostring(qin_quan_info_data))
                    # print(response_dict)
                except Exception as e:
                    # print(e)
                    continue
                qin_quan_author_str = qin_quan_info_data[0].replace(' ', '') if len(qin_quan_info_data) > 0 else ''  # 侵权作者
                # print(qin_quan_author_str)
                if not qin_quan_author_str:
                    continue
                qin_quan_title_str = ''.join(q_l.xpath('./a')[2].xpath('./text()')).replace('漫画在线手机版', '')  # 侵权标题

                yangben_id = kwargs.get('id', '')

                qin_quan_dict = dict()
                qin_quan_dict['yang_ben_author_str'] = kwargs.get('yang_ben_author_str', '')  # 样本作者
                qin_quan_dict['yang_ben_title_str'] = kwargs.get('yang_ben_title_str', '')  # 样本标题
                qin_quan_dict['yang_ben_url_str'] = kwargs.get('yang_ben_url_str', '')  # 样本链接
                qin_quan_dict['yang_ben_id_int'] = kwargs.get('yang_ben_id_int', '')  # 样本ID 数值类型
                qin_quan_dict['yang_ben_mid_str'] = kwargs.get('yang_ben_mid_str', '')  # 样本ID 字符串形式
                qin_quan_dict['yang_ben_task_id_int'] = kwargs.get('yang_ben_task_id_int', '')  # 样本主任务ID
                qin_quan_dict['yang_ben_platform_str'] = kwargs.get('yang_ben_platform_str', '')  # 样本平台
                qin_quan_dict['yang_ben_batch_id_int'] = kwargs.get('yang_ben_batch_id_int', '')  # 样本批次ID
                qin_quan_dict['yang_ben_batch_id_int'] = kwargs.get('yang_ben_batch_id_int', '')  # 样本批次ID

                qin_quan_dict['search_key_words_str'] = kwargs.get('search_key_words_str', '')  # 搜索关键词
                qin_quan_dict['qin_quan_platform_str'] = 'kukudm'  # 侵权平台
                qin_quan_dict['qin_quan_author_str'] = qin_quan_author_str  # 侵权作者
                qin_quan_dict['qin_quan_title_str'] = qin_quan_title_str  # 侵权标题
                qin_quan_dict['qin_quan_url_str'] = qin_quan_url_str  # 侵权链接
                # qin_quan_dict['qin_quan_id_int'] = qin_quan_id_int  # 样本ID 数值类型
                # qin_quan_dict['qin_quan_mid_str'] = qin_quan_mid_str  # 侵权ID 字符串形式
                qin_quan_dict['qin_quan_url_hash_str'] = str(yangben_id) + '|' + md5_use(
                    qin_quan_url_str)  # 唯一索引，样本task_id 侵权url（md5）

                qin_quan_dict['similar_number_float'] = ''  # 作品相似度
                qin_quan_dict['title_similar_number_float'] = float(str_similar(clear_text(kwargs.get('yang_ben_title_str', '')),
                                                                       clear_text(qin_quan_title_str)))  # 标题相似度
                qin_quan_dict['author_similar_number_float'] = float(str_similar(
                    clear_text(kwargs.get('yang_ben_author_str', '')), clear_text(qin_quan_author_str)))  # 作者名称相似度
                qin_quan_dict['qin_quan_type_int'] = 7  # 侵权类型 4 （0 图文，1，视频，2音频）
                qin_quan_dict['qin_quan_platform_id_int'] = ''  # 默认空
                qin_quan_dict["qin_quan_flag_int"] = -1
                if qin_quan_dict["title_similar_number_float"] >= CARTOON_CONF["qin_quan_similar"] and qin_quan_dict[
                    "author_similar_number_float"] >= CARTOON_CONF["qin_quan_similar"]:
                    qin_quan_dict["qin_quan_flag_int"] = 1
                # qin_quan_dict['all_recommend_str'] = ''  # 总推荐数 str
                # qin_quan_dict['month_recommend_str'] = ''  # 月推荐数 str
                # qin_quan_dict['week_recommend_str'] = ''  # 周推荐数 str
                # qin_quan_dict['all_read_int'] = ''  # 总阅读数 int
                # qin_quan_dict['month_read_int'] = ''  # 月阅读数 int
                # qin_quan_dict['week_read_int'] = ''  # 周阅读数 int
                # qin_quan_dict['all_words_number_int'] = ''  # 总字数
                # qin_quan_dict['book_dian_ji_number_int'] = ''  # 作品点击量
                # qin_quan_dict['book_shou_cang_number_int'] = ''  # 作品收藏量
                qin_quan_dict['book_status_str'] = qin_quan_info_data[2].replace(' ', '') if len(qin_quan_info_data) > 0 else ''  # 书籍状态 （连载，完结，暂无）
                # qin_quan_dict['book_property_str'] = ''  # 书籍属性 （免费，会员，限免）
                # qin_quan_dict['author_type_str'] = ''  # 作者类型 （金牌，签约，独立 默认无）
                # qin_quan_dict['book_lable_str'] = ''  # 书籍标签 （用｜分割的字符串 ''科幻｜现实｜励志''）
                # qin_quan_dict['book_type_str'] = ''  # 书籍分类 （玄幻 ,科幻，言情...）按搜索结果来多个按｜分割
                # qin_quan_dict['book_update_time'] = ''  # 书籍更新日期 年-月-日
                # qin_quan_dict['book_zong_zhang_jie_int'] = ''  # 书籍总的章节 完结的，未完结就填目前的总章节
                # qin_quan_dict['book_zui_xin_zhang_jie_name_str'] = ''  # 最新章节名称
                # qin_quan_dict['book_introduce_text'] = ''.join(q_l.xpath('.//div[@class="desc"]/text()'))  # 书籍简介 text
                # qin_quan_dict['book_cover_image_str'] = ''.join(q_l.xpath('.//div[@class="mh-item-tip"]/a/p/@style'))  # 书籍封面 URL
                # qin_quan_dict['book_detail_url_str'] = ''  # 书籍详情URL
                # qin_quan_dict['book_detail_id_int'] = ''  # 书籍详情ID 数字形式
                # qin_quan_dict['book_detail_id_str'] = ''  # 书籍详情ID 字符形式
                # qin_quan_dict['book_zhan_dian_str'] = ''  # 书籍站点 （男生，女生，暂无）
                # qin_quan_dict['book_publish_str'] = ''  # 出版社 默认侵权平台'
                # qin_quan_dict['book_commeds_int'] = ''  # 书籍评论数
                # qin_quan_dict['author_grade_float'] = ''  # 作者评分
                # qin_quan_dict['author_page_url_str'] = ''  # 作者主页链接
                # qin_quan_dict['author_book_number_int'] = ''  # 作者书籍总数
                # qin_quan_dict['author_likes_int'] = ''  # 作者获赞总数
                # qin_quan_dict['author_all_words_number_str'] = ''  # 作者累计创作字数
                # qin_quan_dict['author_produce_days_str'] = ''  # 作者累计创作天数
                # qin_quan_dict['author_fens_number_int'] = ''  # 作者粉丝数
                # qin_quan_dict['author_head_image_url_str'] = ''  # 作者头像URL
                # qin_quan_dict[''] = ''  #
                result_list.append(qin_quan_dict)
            return result_list


# 统一的调用 search_qin_quans
search_normals = KuKuDongManCartoon().search_qin_quan
if __name__ == "__main__":
    yangben_dict = {
        'id': '10000',
        'yang_ben_author_str': '伊藤伸平神乐坂淳',
        'yang_ben_title_str': '大正野球娘',
        'yang_ben_url_str': 'https://t.shuqi.com/cover/6695029',
        'page_num': 1,

    }
    result = search_normals('我', **yangben_dict)
    # shuqi = ShuQiNovel(use_proxy=True)
    # result = shuqi.search_qin_quan('爱', **yangben_dict)
    print(len(result))
    print(result)
