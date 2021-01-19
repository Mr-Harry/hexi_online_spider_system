# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/7/31

# from audio_search_unit.wangyiyun_search import WangYiYun
# from audio_search_unit.xiami_search import XiaMi
# from audio_search_unit.qianqian_search import QianQian
# from audio_search_unit.ximalaya_spider import XiMaLaYa
# from audio_search_unit.qingka import QingKa
__audio_search_function__ = {
        '1':"audio_search_unit.xiami_search_unit.xiami_search", # 虾米搜索
        '2':"audio_search_unit.wangyiyun_search_unit.wangyiyun_search", # 网易云搜索
        '3':"audio_search_unit.qianqian_search_unit.qianqian_search", # 千千音乐搜索
        '4':"audio_search_unit.ximalaya_search_unit.ximalaya_search", # 喜马拉雅搜索
        '5':"audio_search_unit.qingka_search_unit.qingka_search", # 情咖搜索
    }