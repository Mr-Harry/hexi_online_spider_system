# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/11/29
import requests

headers = {
    'authority': 'www.ixigua.com',
    'pragma': 'no-cache',
    'cache-control': 'no-cache',
    'sec-ch-ua': '"Chromium";v="86", "\\"Not\\\\A;Brand";v="99", "Google Chrome";v="86"',
    'accept': 'application/json, text/plain, */*',
    'x-should-verify': 'false',
    'sec-ch-ua-mobile': '?0',
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.198 Safari/537.36',
    'sec-fetch-site': 'same-origin',
    'sec-fetch-mode': 'cors',
    'sec-fetch-dest': 'empty',
    'referer': 'https://www.ixigua.com/search/%E6%88%91%E7%9A%84%E4%B8%96%E7%95%8C/?logTag=n7jK4619SWjA12WeN689f&keyword=%25E5%25B0%258F%25E5%2580%25A9%25E7%259A%2584%25E5%2586%259C%25E6%259D%2591%25E7%2594%259F%25E6%25B4%25BB',
    'accept-language': 'zh-CN,zh;q=0.9',
    'cookie': 'wafid=e02aef89-102b-451a-8f10-b1ec4b075fa7; wafid.sig=jw5oTB6uik9gfyYe2i-cHULMii4; tt_webid=6829168726999565838; ttwid=6862590409865545230; ttwid.sig=9ZpvYVo4MNNm_DBy1JjHEp6At7c; xiguavideopcwebid=6862590409865545230; xiguavideopcwebid.sig=EpBDxz5zmyc1_3mvWb1K4GzYKhU; _ga=GA1.2.1290196361.1597821354; MONITOR_WEB_ID=76cae0f5-5325-4873-9f7d-645cdaed9258; ttcid=c5c0b9fc25964f5b909cb9bfaf9b4eae22; __ac_signature=_02B4Z6wo00f01RkX8nwAAIBCFG4t6J-8vB0ZEvbAABnV57; ixigua-a-s=1; _gid=GA1.2.261246931.1606638191; Hm_lvt_db8ae92f7b33b6596893cdf8c004a1a2=1606638191; Hm_lpvt_db8ae92f7b33b6596893cdf8c004a1a2=1606638340',
}

params = (
    ('search_id', '202011291625380100290550661446110'),
    ('debug_model', 'false'),
    ('_signature', '_02B4Z6wo00f013g4.-wAAIBAdUEgeYhdjtd4PftAAIHVe6'),
)

response = requests.get('https://www.ixigua.com/api/searchv2/complex/中国好/13', headers=headers, params=params)

print(response.text)