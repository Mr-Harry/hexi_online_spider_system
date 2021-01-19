# -*- coding:utf-8 -*-
# Chance favors the prepared mind.
# author : pyl owo,
# time : 2020/10/12
from urllib.parse import urlparse

from engine_search_unit.engine_spider_settings import ENGINE_CONF


def clear_admin_url(qinquan_url_admin):  # 侵权url是否可清除
    for i in ENGINE_CONF.get('clear_admin_dict').keys():
        if i in qinquan_url_admin:
            return True
    return False


def qinquan_list_url_clear(qinquan_list):
    return [i for i in qinquan_list if not clear_admin_url(urlparse(i.get('qinquan_URL')).netloc)]


if __name__ == "__main__":
    url = 'https://www.zhihu.com/question/422753633'
    url1 = 'https://m.weibo.cn/status/JovxCp3xO?entry=thirdapp&wm=90154_90001&luicode=10000360&lfid=ucneirong_9999_0001&launchid=10000360-ucneirong_9999_0001'
    url2 = 'https://www.zhihu.com/question/422753633'
    url3 = 'https://m.baike.com/wiki/%E7%96%AF%E7%8A%AC%E5%B0%91%E5%B9%B4%E7%9A%84%E5%A4%A9%E7%A9%BA/21032817'
    x = [{'qinquan_title': '风犬少年的天空_剧情简介_演职员表-头条百科《风犬少年的天空》是由欢喜传媒集团有限公司、上海拾谷影业有限公司出品，张一白、韩琰、李炳强执导的青春...', 'qinquan_URL': 'https://m.baike.com/wiki/%E7%96%AF%E7%8A%AC%E5%B0%91%E5%B9%B4%E7%9A%84%E5%A4%A9%E7%A9%BA/21032817', 'qinquan_text': '《风犬少年的天空》是由欢喜传媒集团有限公司、上海拾谷影业有限公司出品，张一白、韩琰、李炳强执导的青春...', 'qinquan_platform': '神马搜索'}, {'qinquan_title': '疯犬少年的天空什么时候上映？一共有几集？在哪个平台上...疯犬少年的天空什么时候上映？一共有几集？在哪个平台上播出？电视剧《疯犬少年的天空》是一部青春励志情感...', 'qinquan_URL': 'https://m.ijq.tv/huaxu/158704545926137.html', 'qinquan_text': '疯犬少年的天空什么时候上映？一共有几集？在哪个平台上播出？电视剧《疯犬少年的天空》是一部青春励志情感...', 'qinquan_platform': '神马搜索'}, {'qinquan_title': '如何评价《风犬少年的天空》1-5 集，符合你的期待吗？知乎[最佳答案]人之所以喜欢青春，不也是因为青春像风犬少年那样有无限可能吗！愿我们都能出走半生，归来仍是少年。 ...', 'qinquan_URL': 'https://www.zhihu.com/question/422753633', 'qinquan_text': '[最佳答案]人之所以喜欢青春，不也是因为青春像风犬少年那样有无限可能吗！愿我们都能出走半生，归来仍是少年。 ...', 'qinquan_platform': '神马搜索'}, {'qinquan_title': '风犬少年的天空原型们怎么样了？知乎[最佳答案]钦哥以前还真嘞是个风云人物 影人：张一白（导演）/韩琰（导演）/李炳强（导演）/彭昱畅/张婧仪/梁靖康/...', 'qinquan_URL': 'https://www.zhihu.com/question/422938287/answer/1503114020', 'qinquan_text': '[最佳答案]钦哥以前还真嘞是个风云人物 影人：张一白（导演）/韩琰（导演）/李炳强（导演）/彭昱畅/张婧仪/梁靖康/...', 'qinquan_platform': '神马搜索'}, {'qinquan_title': '《犬风少年的天空》中的马田后来怎么样了？知乎[最佳答案]片头居然有沧桑镜头？自恋学霸温情的甜甜恋爱，会有结果么？求剧透！', 'qinquan_URL': 'https://www.zhihu.com/question/423939715', 'qinquan_text': '[最佳答案]片头居然有沧桑镜头？自恋学霸温情的甜甜恋爱，会有结果么？求剧透！', 'qinquan_platform': '神马搜索'}, {'qinquan_title': '风犬少年的天空：酷得像风，野得像狗风犬少年的天空：酷得像风，野得像狗 ZZ 文艺说事 文艺说事 WeChat ID wyss089 2020-10-11 00:00:00 本来是...', 'qinquan_URL': 'https://mp.weixin.qq.com/s?__biz=MzU5Nzc5NDYzNQ==&mid=2247509548&idx=4&sn=173a60d458dcb13ff9900a6a23282843', 'qinquan_text': '风犬少年的天空：酷得像风，野得像狗 ZZ 文艺说事 文艺说事 WeChat ID wyss089 2020-10-11 00:00:00 本来是...', 'qinquan_platform': '神马搜索'}, {'qinquan_title': '风犬少年的天空# 你看那个人 他好像一.来自新剧-微博风犬少年的天空# “你看那个人 他好像一条狗哦”', 'qinquan_URL': 'https://m.weibo.cn/status/JovxCp3xO?entry=thirdapp&wm=90154_90001&luicode=10000360&lfid=ucneirong_9999_0001&launchid=10000360-ucneirong_9999_0001', 'qinquan_text': '风犬少年的天空# “你看那个人 他好像一条狗哦”', 'qinquan_platform': '神马搜索'}, {'qinquan_title': '风犬少年的天空#剧综汇精彩#【没想到大力娇也 来自第零...在新剧《风犬少年的天空》里，大力娇一角给人女汉子的感觉，她与三位同班男同学常常玩到一块，假小子形象...', 'qinquan_URL': 'https://m.weibo.cn/status/JoY1Iayu3?entry=thirdapp&wm=90154_90001&luicode=10000360&lfid=ucneirong_9999_0001&launchid=10000360-ucneirong_9999_0001', 'qinquan_text': '在新剧《风犬少年的天空》里，大力娇一角给人女汉子的感觉，她与三位同班男同学常常玩到一块，假小子形象...', 'qinquan_platform': '神马搜索'}, {'qinquan_title': '风犬少年的天空#剧综汇精彩#【哇！彭昱畅哭 来自热剧小...张婧仪也是科班出身，《风犬少年的天空》这部剧是她参演的第一部影视剧作品。不过张婧仪是“东申未来”影视...', 'qinquan_URL': 'https://m.weibo.cn/status/JoXDmdKPi?entry=thirdapp&wm=90154_90001&luicode=10000360&lfid=ucneirong_9999_0001&launchid=10000360-ucneirong_9999_0001', 'qinquan_text': '张婧仪也是科班出身，《风犬少年的天空》这部剧是她参演的第一部影视剧作品。不过张婧仪是“东申未来”影视...', 'qinquan_platform': '神马搜索'}, {'qinquan_title': '风犬少年的天空#【周依然 梁靖康】娇娇这回 来自热剧情报...【周依然 梁靖康】 娇娇这回终于开窍了！大力娇（周依然饰）的天生神力与娇羞懵懂集于一身，从小与三个男孩...', 'qinquan_URL': 'https://m.weibo.cn/status/JoS2q9M2F?entry=thirdapp&wm=90154_90001&luicode=10000360&lfid=ucneirong_9999_0001&launchid=10000360-ucneirong_9999_0001', 'qinquan_text': '【周依然 梁靖康】 娇娇这回终于开窍了！大力娇（周依然饰）的天生神力与娇羞懵懂集于一身，从小与三个男孩...', 'qinquan_platform': '神马搜索'}, {'qinquan_title': '《风犬少年》里的真实感动，有着青春剧最美好的模样！手机...像风一样自由，像狗一样奔跑！《风犬少年的天空》文丨旧故麻袋∨回忆高中时期的我们，用几个词可以简单概括...', 'qinquan_URL': 'http://3g.163.com/touch/article.html?docid=FOQDIP4105289FB4', 'qinquan_text': '像风一样自由，像狗一样奔跑！《风犬少年的天空》文丨旧故麻袋∨回忆高中时期的我们，用几个词可以简单概括...', 'qinquan_platform': '神马搜索'}, {'qinquan_title': '风犬少年的天空-豆瓣电影既是少年面对成人世界的第一声呐喊，也是互相扶持共同成长的温暖旅途...酷得像风野得像狗，从而找到一片属于自己的天空。', 'qinquan_URL': 'https://m.douban.com/movie/subject/30413128/', 'qinquan_text': '既是少年面对成人世界的第一声呐喊，也是互相扶持共同成长的温暖旅途...酷得像风野得像狗，从而找到一片属于自己的天空。', 'qinquan_platform': '神马搜索'}]

    print(clear_admin_url(url3))
    print(urlparse(url2).netloc)
    print(qinquan_list_url_clear(x))
