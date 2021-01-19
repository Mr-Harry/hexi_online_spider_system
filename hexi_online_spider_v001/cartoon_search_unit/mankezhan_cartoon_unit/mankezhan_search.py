# Chance favors the prepared mind.
# author : pyl owo,
# time : 2020/12/15
# Chance favors the prepared mind.
# author : pyl owo,
# time : 2020/12/15
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


class ManKeZhan:
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
            # 'cookie': 'BAIDUID=E86597F7527A8D03D12E08F1BF2BA71B:FG=1; BAIDUID_BFESS=E86597F7527A8D03D12E08F1BF2BA71B:FG=1; BIDUPSID=E86597F7527A8D03D12E08F1BF2BA71B; PSTM=1606967604; BDORZ=FFFB88E999055A3F8A630C64834BD6D0; COMMON_LID=221bc1a347716a4005dfa5a3e93dfe57; Hm_lvt_4aadd610dfd2f5972f1efee2653a2bc5=1606896904,1606974068; BD_SVTK=WteO3EWWnfkYlotW3WZa108dO0fclO0CtlPPl8fZZWAoQnfD9fOj0f00P8tC0P0O0kgA1AQaTA59QnfD9tFb8f0yY0Sq0O0Dfpjrpflkx0fipO85SlF1JtJix0tFpjpTS8OSf8tleWEAQgiYllOz0f18TlEc0P16flPyiBIRkdaYB; hkpcvideolandquery=^%^u5F20^%^u5609^%^u8BD1^%^u5168^%^u5267^%^u6700^%^u5927^%^u80C6^%^u4E00^%^u5E55^%^uFF0C^%^u5413^%^u5F97^%^u95EB^%^u59AE^%^u6000^%^u7591^%^u4EBA^%^u751F^%^uFF0C^%^u5BFC^%^u6F14^%^u662F^%^u771F^%^u6562^%^u62CD; reptileData=^%^7B^%^22data^%^22^%^3A^%^228f5df208d8824678b2c5577a1ca3ef0c9baf035c446ff41d9bc91db4ed0ee44bd56d3f00f7fe4bb7f554b397cc9e5d028f18c0ae718845ee4bc81cced7727ecaefee7bb76085c78512e3343f12c6431bacaf90a763f1f612e995d9baab753f2fe6e363b7090cf973c79943d21bf14cbdd80167cb82776771ec41955c9b082a89f6e6f1ae8e48eef2bbdc88ee1ad62116^%^22^%^2C^%^22key_id^%^22^%^3A^%^2230^%^22^%^2C^%^22sign^%^22^%^3A^%^22b8eaabc3^%^22^%^7D; PC_TAB_LOG=video_details_page; Hm_lpvt_4aadd610dfd2f5972f1efee2653a2bc5=1607049642'

            }
        self.api_qin_quan_search_key = ''
        self.search_base_url = "https://www.mkzhan.com/search/?keyword={}&page={}"
        self.qin_quan_search_url_pre = "https://www.mkzhan.com"
    #转意函数
    # def utf8_str(self,num):
    #     str_u = str(num.encode('utf8')).lstrip("b'").rstrip('\'').replace('\\x', '%').upper()
    #     return str_u
    # 搜索侵权
    def search_qin_quan(self, search_key: str, **kwargs):
        _page = kwargs.get("page_num") - CARTOON_CONF["mankezhan_search_offset"]["start_page"] + 1 if kwargs.get("page_num") else CARTOON_CONF["mankezhan_search_offset"]["start_page"]
        return self.parse_search_qin_quan(unify_requests(url=self.search_base_url.format(search_key,_page), headers=self.headers, proxies=self.proxy), **kwargs)

    # 侵权详情 *
    def qin_quan_info(self, qin_quan_url):
        return unify_requests(url=qin_quan_url, headers=self.headers, proxies=self.info_proxy)

    # 搜索视频响应解析
    def parse_search_qin_quan(self, response, **kwargs) -> list:
        try:
            # print(response.text)
            # response_data = json.loads(response.text)
            response_data = etree.HTML(response.text)
        except:
            return []
        else:
            result_list = []

            # qin_quaq_list_data = response_data.get('data')
            qin_quaq_list_data = response_data.xpath('//div[@class="common-comic-item"]/a[@class="cover"]')
            for q_l in qin_quaq_list_data:
                # xpath_demo = ''.join(q_l.xpath(''))
                qin_quan_url_str = self.qin_quan_search_url_pre + ''.join(q_l.xpath('./@href'))  # 侵权链接
                # >< 由于搜索中没有展示作者名， 所以去详情页找作者 顺便把详情也找到
                try:
                    # response_data = json.loads(response.text)
                    qin_quan_info_data = etree.HTML(self.qin_quan_info(qin_quan_url_str).text)
                    # print(etree.tostring(qin_quan_info_data))
                    # print(response_dict)
                except:
                    continue
                qin_quan_info_temp = qin_quan_info_data.xpath('//div[@class="comic-author"]/span[@class="name"]/a')[0]
                qin_quan_author_str = ''.join(qin_quan_info_temp.xpath('./text()'))  # 侵权作者
                if not qin_quan_author_str:
                    continue
                qin_quan_title_str = ''.join(qin_quan_info_data.xpath('/html/body/div[2]/div[3]/div/p[1]/text()'))  # 侵权标题

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
                qin_quan_dict['qin_quan_platform_str'] = '漫客栈'  # 侵权平台
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
                # qin_quan_dict['book_dian_ji_number_int'] = ''.join(qin_quan_info_temp.xpath('//div[@id="about_kit"]/ul/li')[3].xpath('./text()')).split('(卷)')[-1].replace(' ', '').replace('(', '').replace(')', '')  # 作品点击量
                # qin_quan_dict['book_shou_cang_number_int'] = ''.join(qin_quan_info_temp.xpath('//div[@id="about_kit"]/ul/li')[5].xpath('./text()')).replace('人收藏本漫画', '')  # 作品收藏量
                book_status_str = ''.join(q_l.xpath('.//div[@class="update-info"]/text()'))
                # qin_quan_dict['book_status_str'] = ''.join(qin_quan_info_temp.xpath('//div[@id="about_kit"]/ul/li')[2].xpath('./text()'))  # 书籍状态 （连载，完结，暂无）
                # qin_quan_dict['book_property_str'] = ''  # 书籍属性 （免费，会员，限免）
                # qin_quan_dict['author_type_str'] = ''  # 作者类型 （金牌，签约，独立 默认无）
                # qin_quan_dict['book_lable_str'] = '|'.join(''.join([i for i in q_l.xpath('.//span[@class="tag txt-elip"]/text()') if i]).replace('--', '').split(' '))  # 书籍标签 （用｜分割的字符串 ''科幻｜现实｜励志''）
                # qin_quan_dict['book_type_str'] = ''  # 书籍分类 （玄幻 ,科幻，言情...）按搜索结果来多个按｜分割
                # qin_quan_dict['book_update_time'] = ''.join(qin_quan_info_temp.xpath('//div[@id="about_kit"]/ul/li')[4].xpath('./text()'))  # 书籍更新日期 年-月-日
                # qin_quan_dict['book_zong_zhang_jie_int'] = ''  # 书籍总的章节 完结的，未完结就填目前的总章节
                # qin_quan_dict['book_zui_xin_zhang_jie_name_str'] = ''  # 最新章节名称
                # qin_quan_dict['book_introduce_text'] = ''.join(qin_quan_info_temp.xpath('//div[@id="about_kit"]/ul/li')[-1].xpath('./text()')).replace('人收藏本漫画', '').replace('\r', '').replace('\n', '')  # 书籍简介 text
                # qin_quan_dict['book_cover_image_str'] = ''.join(qin_quan_info_temp.xpath('.//div[@id="about_style"]/img/@src'))  # 书籍封面 URL
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
search_normals = ManKeZhan().search_qin_quan
if __name__ == "__main__":
    yangben_dict = {
        'id': '10000',
        'yang_ben_author_str': '东铁神  望公太',
        'yang_ben_title_str': '我',
        'yang_ben_url_str': 'https://t.shuqi.com/cover/6695029',
        'page_num': 1,
    }
    result = search_normals('无',**yangben_dict)
    # shuqi = ShuQiNovel(use_proxy=True)
    # result = shuqi.search_qin_quan('爱', **yangben_dict)
    print(len(result))
    print(result)
