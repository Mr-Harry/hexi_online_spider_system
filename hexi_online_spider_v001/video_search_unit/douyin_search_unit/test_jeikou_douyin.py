# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/11/23

import requests

# 请求头
common_headers = {
    'X-Token': 'ABBC37E62D7311EB950B88E9FE880485',
    'Content-Type': 'application/json'
}

# 请求体
body = {
    # "device": "os_api=22&device_type=MI%209&ssmix=a&manifest_version_code=110301&dpi=320&uuid=863254103501671&app_name=aweme&version_name=11.3.0&ts=1593072310&cpu_support64=false&app_type=normal&ac=wifi&host_abi=armeabi-v7a&update_version_code=11309900&channel=aweGW&_rticket=1593072311194&device_platform=android&iid=2488947595022199&version_code=110300&mac_address=00%3AE0%3A4C%3A5A%3AA7%3A4B&cdid=bea44ee1-efa0-421f-be06-24242ec2fb09&openudid=caf476e270b258&device_id=16269378842654&resolution=900*1600&os_version=5.1.1&language=zh&device_brand=Xiaomi&aid=1128&mcc_mnc=46007",
    # "device": "os_api=29&device_type=MI%209&ssmix=a&manifest_version_code=100201&dpi=440&uuid=97126462525730483&app_name=aweme&version_name=10.2.0&ts=1598427725&cpu_support64=false&storage_type=2&app_type=normal&appTheme=dark&ac=wifi&host_abi=armeabi&update_version_code=10209900&channel=aweGW&_rticket=1598427725896&device_platform=android&iid=2216255540694632&version_code=100200&mac_address=10%3A2a%3Ab3%3A13%3Abd%3A69&cdid=76bce808-3c97-4bc4-a188-9d1b039eacd3&openudid=6515028521612256&device_id=2005149181288733&resolution=1080*2029&os_version=10&language=zh&device_brand=Xiaomi&aid=1128&mcc_mnc=46000",
    "device": "os_api=23&device_type=Redmi%20Note%204&ssmix=a&manifest_version_code=110901&dpi=480&uuid=862805030453020&app_name=aweme&version_name=11.9.0&ts=1606626714&cpu_support64=true&storage_type=1&app_type=normal&ac=wifi&host_abi=armeabi-v7a&update_version_code=11909900&channel=tengxun_new&_rticket=1606626714785&device_platform=android&iid=1442180741205867&version_code=110900&mac_address=AC%3AC1%3AEE%3ADD%3AE2%3ADD&cdid=b2a8ccaa-6646-49c3-bb80-43ca672033a3&openudid=9dfbcdbf08125f22&device_id=53141730645&resolution=1080*1920&os_version=6.0&language=zh&device_brand=Xiaomi&aid=1128",

    "cookie": "install_id=2488947595022199; ttreq=1$26ae0cef57687c00e2e9d7c0ead7927a615915dc; passport_csrf_token=35e610ce541311aa58fb311e4d59fa33; d_ticket=2b15b0fb1bbc8c25c3e8a0b0a880231bf4; odin_tt=9de9114ca806185e8c46e5bae077e6a190ec180f7f300de0c455f67dc8d9ae45051cf8b451d8ab0282b01163a6a7b89c; sid_guard=7af29dc4dfd55c277dcd3456c1506ef5%7C1593071018%7C5184000%7CMon%2C+24-Aug-2020+07%3A43%3A38+GMT; uid_tt=d381bd61e5e2d7dbbd24f1e757bd26b7; uid_tt_ss=d381bd61e5e2d7dbbd24f1e757bd26b7; sid_tt=7af29dc4dfd55c277dcd3456c1506ef5; sessionid=7af29dc4dfd55c277dcd6c1506ef5; sessionid_ss=7af29dc4dfd55c277dc56c1506ef5",
    "x-tt-token": "007af29dc4dfd55c277dcd3456c1506ef55e4f1dc4fa6a6e98c2f7b360985add505417ce5c67a298310afa30e8aa6559",
    "keyword": "我的国家",
    "offset": 1
}
# body = {
#     "device": "os_api=23&device_type=Redmi%20Note%204&ssmix=a&manifest_version_code=110901&dpi=480&uuid=862805030453020&app_name=aweme&version_name=11.9.0&ts=1606626714&cpu_support64=true&storage_type=1&app_type=normal&ac=wifi&host_abi=armeabi-v7a&update_version_code=11909900&channel=tengxun_new&_rticket=1606626714785&device_platform=android&iid=1442180741205867&version_code=110900&mac_address=AC%3AC1%3AEE%3ADD%3AE2%3ADD&cdid=b2a8ccaa-6646-49c3-bb80-43ca672033a3&openudid=9dfbcdbf08125f22&device_id=53141730645&resolution=1080*1920&os_version=6.0&language=zh&device_brand=Xiaomi&aid=1128",
#     "cookie": "install_id=1442180741205867; ttreq=1$bf099e35ebef9715b439ca824fd204699dccdc36; d_ticket=a6569ff1c11e8c4266769ef8f1da0362bc0ef; multi_sids=111327685257%3Aeddbb9df19a5ef4b058172fda0cbca65; n_mh=8oI16EvhqjEO5B36DqAY6yj84DHSyhatX1e-2tfBETw; sid_guard=eddbb9df19a5ef4b058172fda0cbca65%7C1606626680%7C5184000%7CThu%2C+28-Jan-2021+05%3A11%3A20+GMT; uid_tt=4c9f45300afb5cabdb6a221640f1b2f7; sid_tt=eddbb9df19a5ef4b058172fda0cbca65; sessionid=eddbb9df19a5ef4b058172fda0cbca65; odin_tt=5b28fc72d0637b2b4864ba5c21a23f5dda0730eb268b857aae3045072b1c3fe28a17422b81c0977f6a862b2af173ed6546ee6d6d580d91d18375055413833bd0",
#     "x-tt-token": "00eddbb9df19a5ef4b058172fda0cbca65044d8ff6223b381f6250d24ea4028aa0773d5c89310dff41efdc9ca3aad3026488e0ed6e1b03fc5347c80cb6eaf41c8c96deb840ee33113bd94b0e2c851ec02c7a4-1.0.0",
#     "keyword": "我的国家",
#     "offset": 1
# }

# 计算 XG XR
resp = requests.post('https://cloud.anoyi.com/api/dyapp/search/item', headers=common_headers, json=body).json()["data"]
print(resp)
# ['data']
print(resp["headers"])
print(resp["body"])
print(resp["url"])
# # 请求抖音 API
resp = requests.post(resp['url'], headers=resp['headers'], data=resp['body'])
#
# # 打印返回结果
print(resp.text)