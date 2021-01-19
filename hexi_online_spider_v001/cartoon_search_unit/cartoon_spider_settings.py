# -*- coding:utf-8 -*-
# Chance favors the prepared mind.
# author : pyl owo,
# time : 2020/11/28

# 漫画配置
CARTOON_CONF = {
    "qin_quan_similar": 1,  # 侵权字符串相似度
    "search_use_proxy": False,  # 在类的初始化中  类/搜索 是否使用代理
    "info_use_proxy": False,  # 在搜索详情方法中  详情是否使用代理
    # 豆丁漫画
    "douding_search_offset": {"pagesize": 10, "start_page": 1},
    # 一拳漫画  （无翻页）
    "yiquan_search_offset": {"pagesize": 30},
    # mangabz
    "mangabz_search_offset": {"pagesize": 12, "start_page": 1},
    # 哔咔哔咔
    "bikabika_search_offset": {"pagesize": 35, "start_page": 1},
    # 凑漫
    "couhan_search_offset": {"pagesize": 10, "start_page": 1},
    # 咚漫
    "dongman_search_offset": {"pagesize": 18, "start_page": 1},
    # 动漫屋
    "dongmanwu_search_offset": {"pagesize": 10, "start_page": 1},
    # 憨憨漫画
    "hanhan_search_offset": {"pagesize": 10, "start_page": 1},
    # 汉化吧   （无翻页：网页翻页参数错误）
    "hanhuaba_search_offset": {"pagesize": 40},
    # 奇漫屋  （无翻页）
    "qimanwu_search_offset": {"pagesize": 30},
    # 漫画之家
    "manhuazhijia_search_offset": {"pagesize": 20, "start_page": 1},
    # Xmanhua
    "xmanhua_search_offset": {"pagesize": 12, "start_page": 1},
    # 极速漫画
    "jisu_search_offset": {"pagesize": 21, "start_page": 1},
    # 动漫屋5
    "dongman5_search_offset": {"pagesize": 35, "start_page": 1},
    # 百万漫画
    "baiwan_search_offset": {"pagesize": 35, "start_page": 1},
    # 2020漫画
    "manhua2020_search_offset": {"pagesize": 10, "start_page": 1},
    # 517漫画网
    "manhua517_search_offset": {"pagesize": 30, "start_page": 1},
    # 57漫画网
    "manhua57_search_offset": {"pagesize": 10, "start_page": 1},
    # 秀十八漫画
    "xiushiba_search_offset": {"pagesize": 30, "start_page": 1},
    # 一念漫画
    "yinian_search_offset": {"pagesize": 30, "start_page": 1},
    # 36漫画网
    "manhua36_search_offset": {"pagesize": 36, "start_page": 1},
    # 漫画透 (无翻页，只要30个 最多102个)
    "manhuatou_search_offset": {"pagesize": 102, "max_size": 30},
    # 89漫画网
    "manhua89_search_offset": {"pagesize": 120, "start_page": 1},

    # cc漫画
    "ccmanhua_search_offset": {"pagesize": 21, "start_page": 1},
    # 池鱼漫画
    "chiyumanhua_search_offset": {"pagesize": 21, "start_page": 1},
    # 古风漫画
    "gufengmanhua_search_offset": {"pagesize": 21, "start_page": 1},
    # 古古漫画
    "gugugmanhua_search_offset": {"pagesize": 21, "start_page": 1},
    # 芝士豪八 (无翻页)

    # 36漫画app
    "manhua36app_search_offset": {"pagesize": 50, "start_page": 1},
    # kuku漫画网
    "kukudm_search_offset": {"pagesize": 12, "start_page": 1},
    # 今日头条搜索站外漫画情况
    "jinri_search_offset": {"pagesize": 20, "start_page": 0},
    # 半次元  (无翻页)
    # # 多多漫画
    # "duoduo_search_offset": {"pagesize": 36, "start_page": 1},
    # 爱优漫
    "aiyouman_search_offset": {"pagesize": 30, "start_page": 1},
    # 爱漫画
    "aimanhua_search_offset": {"pagesize": 10, "start_page": 1},
    # 酷漫屋” （无翻页）
    "kumanwu_search_offset": {'start_page': 1},
    # 起司画
    "qisimanhua_search_offset": {"pagesize": 30, "start_page": 1},
    # 搜漫画
    "soumanhua_search_offset": {"pagesize": 20, "start_page": 1},
    # 塔多漫画
    'taduo_search_offset': {'pagesize': 21, 'start_page': 0},
    # 土蛋漫画
    "tudanmanhua_search_offset": {"pagesize": 20, "start_page": 1},
    # 侠漫画
    "xiamanhua_search_offset": {"pagesize": 20, "start_page": 1},
    # 我要去漫画
    "woyaoqu_search_offset": {"pagesize": 20, "start_page": 1},
    # 奇妙漫画
    "qimiaomanhua_search_offset": {"pagesize": 33, "start_page": 1},
    # 漫客栈
    'mankezhan_search_offset': {'pagesize': 24, 'start_page': 1},
    # 前未漫画
    'qianweimanhua_search_offset': {'pagesize': 40, 'start_page': 1},
    # 图库漫画
    'tukumanhua_search_offset': {'pagesize': 20, 'start_page': 1},
    # 小木屋漫画
    'xiaomuwu_search_offset': {'pagesize': 11, 'start_page': 1},
    # 漫画1234
    'manhua1234_search_offset': {'pagesize': 36, 'start_page': 1},
    # 来漫画
    "laimanhua_search_offset": {"pagesize": 30, "start_page": 1},
    # 慢慢睇漫画
    "manmantaimanhua_search_offset": {"pagesize": 42, "start_page": 1},
    # x18漫画
    'X18manhua_search_offset': {'pagesize': 30, 'start_page': 1},
    # 漫画狂
    'manhuakuang_search_offset': {'pagesize': 98, 'start_page': 1},
    # 漫画DB
    'manhuaDB_search_offset': {'pagesize': 48, 'start_page': 1},
    # 160漫画
    "yiliulingmanhua_search_offset": {"pagesize": 20, "start_page": 1},
    # 好123漫画
    "haomanhua_search_offset": {"pagesize": 42, "start_page": 1},
    # 卡推漫画
    "ktmanhua_search_offset": {"pagesize": 42, "start_page": 1},
    # 狂人漫画
    "kuangrenmanhua_search_offset": {"pagesize": 42, "start_page": 1},
    # 漫画牛
    "niumanhua_search_offset": {"pagesize": 42, "start_page": 1},
    # 漫画皮
    "pimanhua_search_offset": {"pagesize": 42, "start_page": 1},
    # 漫画库
    'manhuaku_search_offset': {'pagesize': 30, 'start_page': 1},
    # 漫画天堂
    'manhuatiantang_search_offset': {'pagesize': 10, 'start_page': 1},
    # 漫画库cc
    'manhuaku_cc_search_offset':{'pagesize':30,'start_page':1},
    # 快岸漫画
    'kuaianmanhua_search_offset':{'pagesize':12,'start_page':2},
    # 爱看漫画网
    'aikanmanhuawang_search_offset':{'pagesize':30,'start_page':0},
    # 爱看鱼
    'aikanyu_search_offset':{'pagesize':42,'start_page':1},
    # 阿里漫画
    'alimanhua_search_offset':{'pagesize':21,'start_page':0},
    # 久久五叔
    'jiujiuwushu_search_offset':{'pagesize':30,'start_page':1},
    # 漫本动漫
    'manbendongman_search_offset':{'pagesize':20,'start_page':1},
    # 7E漫画
    '7emanhua_search_offset': {'pagesize': 10, 'start_page': 1},
    # 88漫画
    '88manhua_search_offset':{'pagesize':20,'start_page':1},
    # 92漫画
    '92manhua_search_offset':{'pagesize':20,'start_page':1},
    # 98漫画网
    '98manhua_search_offset':{'pagesize':30,'start_page':1},
    # 522漫画
    '522manhua_search_offset':{'pagesize':30,'start_page':1},
    # 笔趣阁漫画
    'biquge_search_offset':{'pagesize':30,'start_page':1},
    # 漫画吧
    'manhuaba_search_offset':{'pagesize':30,'start_page':1},
    # 亲亲漫画
    'qinqinmanhua_search_offset': {'pagesize': 36, 'start_page': 1},
    # 733漫画
    'qisansan_search_offset': {'pagesize': 0, 'start_page': 1},
    # 兔兔漫画
    'tutu1manhua_search_offset':{'pagesize':30,'start_page':1},
    # wu22漫画
    'wu22manhua_search_offset':{'pagesize':30,'start_page':1},
}