# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/11/28
import random

# 抖音的 device 文件名称
dou_yin_device_file_name = "dou_yin_device_register.txt"

douyin_x_tt_token_list = [
    # "007af29dc4dfd55c277dcd3456c1506ef55e4f1dc4fa6a6e98c2f7b360985add505417ce5c67a298310afa30e8aa6559",
    "00eddbb9df19a5ef4b058172fda0cbca65044d8ff6223b381f6250d24ea4028aa0773d5c89310dff41efdc9ca3aad3026488e0ed6e1b03fc5347c80cb6eaf41c8c96deb840ee33113bd94b0e2c851ec02c7a4-1.0.0",
    # "00c13f725a9ad285c1cd2122fe250faa520144ebc40cb0c8417844d3316a02fc03b4cfeefce800c9cd83e5a1b2a3b48580c62ef8df31faa23c2bf890c721ca8ee465ff5a054e7d022dcf97796689828a1360d-1.0.0"
]
douyin_cookies_list = [
    # w
    # "install_id=2488947595022199; ttreq=1$26ae0cef57687c00e2e9d7c0ead7927a615915dc; passport_csrf_token=35e610ce541311aa58fb311e4d59fa33; d_ticket=2b15b0fb1bbc8c25c3e8a0b0a880231bf4; odin_tt=9de9114ca806185e8c46e5bae077e6a190ec180f7f300de0c455f67dc8d9ae45051cf8b451d8ab0282b01163a6a7b89c; sid_guard=7af29dc4dfd55c277dcd3456c1506ef5%7C1593071018%7C5184000%7CMon%2C+24-Aug-2020+07%3A43%3A38+GMT; uid_tt=d381bd61e5e2d7dbbd24f1e757bd26b7; uid_tt_ss=d381bd61e5e2d7dbbd24f1e757bd26b7; sid_tt=7af29dc4dfd55c277dcd3456c1506ef5; sessionid=7af29dc4dfd55c277dcd6c1506ef5; sessionid_ss=7af29dc4dfd55c277dc56c1506ef5",
    # lpy
    "install_id=1442180741205867; ttreq=1$bf099e35ebef9715b439ca824fd204699dccdc36; d_ticket=7bb8fc5c006108bd9f8c07e38f9bbe18bc0ef; multi_sids=111327685257%3Aeddbb9df19a5ef4b058172fda0cbca65%7C88751760190%3Ac13f725a9ad285c1cd2122fe250faa52; n_mh=Nizm8Pf8Lt4wVg8JhUCrZEVurprlK-YbOU5_XHzq5sA; sid_guard=c13f725a9ad285c1cd2122fe250faa52%7C1606626914%7C5184000%7CThu%2C+28-Jan-2021+05%3A15%3A14+GMT; uid_tt=b32024892ee5a8b8d0fc1707a23ba318; sid_tt=c13f725a9ad285c1cd2122fe250faa52; sessionid=c13f725a9ad285c1cd2122fe250faa52; odin_tt=68a5dc9d857c1e3a7490c2e35f7a0a9a7bac46327e5106218179d8ed898ad40e4d7e733f9bdf6d12a5cc5b16acf2b617",
    # xyy
    "install_id=1442180741205867; ttreq=1$bf099e35ebef9715b439ca824fd204699dccdc36; d_ticket=a6569ff1c11e8c4266769ef8f1da0362bc0ef; multi_sids=111327685257%3Aeddbb9df19a5ef4b058172fda0cbca65; n_mh=8oI16EvhqjEO5B36DqAY6yj84DHSyhatX1e-2tfBETw; sid_guard=eddbb9df19a5ef4b058172fda0cbca65%7C1606626680%7C5184000%7CThu%2C+28-Jan-2021+05%3A11%3A20+GMT; uid_tt=4c9f45300afb5cabdb6a221640f1b2f7; sid_tt=eddbb9df19a5ef4b058172fda0cbca65; sessionid=eddbb9df19a5ef4b058172fda0cbca65; odin_tt=5b28fc72d0637b2b4864ba5c21a23f5dda0730eb268b857aae3045072b1c3fe28a17422b81c0977f6a862b2af173ed6546ee6d6d580d91d18375055413833bd0",
]
douyin_device_list = [
    "os_api=23&device_type=Redmi%20Note%204&ssmix=a&manifest_version_code=110901&dpi=480&uuid=862805030453020&app_name=aweme&version_name=11.9.0&ts=1606626714&cpu_support64=true&storage_type=1&app_type=normal&ac=wifi&host_abi=armeabi-v7a&update_version_code=11909900&channel=tengxun_new&_rticket=1606626714785&device_platform=android&iid=1442180741205867&version_code=110900&mac_address=AC%3AC1%3AEE%3ADD%3AE2%3ADD&cdid=b2a8ccaa-6646-49c3-bb80-43ca672033a3&openudid=9dfbcdbf08125f22&device_id=53141730645&resolution=1080*1920&os_version=6.0&language=zh&device_brand=Xiaomi&aid=1128",
    # "os_api=23&device_type=Redmi%20Note%204&ssmix=a&manifest_version_code=110901&dpi=480&uuid=862805030453020&app_name=aweme&version_name=11.9.0&ts=1606627010&cpu_support64=true&storage_type=1&app_type=normal&ac=wifi&host_abi=armeabi-v7a&update_version_code=11909900&channel=tengxun_new&_rticket=1606627011233&device_platform=android&iid=1442180741205867&version_code=110900&mac_address=AC%3AC1%3AEE%3ADD%3AE2%3ADD&cdid=b2a8ccaa-6646-49c3-bb80-43ca672033a3&openudid=9dfbcdbf08125f22&device_id=53141730645&resolution=1080*1920&os_version=6.0&language=zh&device_brand=Xiaomi&aid=1128 ",

]
# 随机获取 xtttoken
def get_douyin_x_tt_token():
    return random.choice(douyin_x_tt_token_list)
# 随机获取 cookie
def get_douyin_cookie():
    return random.choice(douyin_cookies_list)
# 随机获取 device
def get_douyin_device():
    return random.choice(douyin_device_list)
# 第二套方案
def get_douyin_device_():
    with  open("{}".format(dou_yin_device_file_name)) as f:
        device_info = f.read()
        # print(device_info)
        f.close()
        return device_info
# 外部服务
__out_config__ = {
    # 公共的请求头
    "common_headers":{
                    'X-Token': 'ABBC37E62D7311EB950B88E9FE880485',
                    'Content-Type': 'application/json'
                    },
    'X_Token': 'ABBC37E62D7311EB950B88E9FE880485',
    # "device": "os_api=22&device_type=MI%209&ssmix=a&manifest_version_code=110301&dpi=320&uuid=863254103501671&app_name=aweme&version_name=11.3.0&ts=1593072310&cpu_support64=false&app_type=normal&ac=wifi&host_abi=armeabi-v7a&update_version_code=11309900&channel=aweGW&_rticket=1593072311194&device_platform=android&iid=2488947595022199&version_code=110300&mac_address=00%3AE0%3A4C%3A5A%3AA7%3A4B&cdid=bea44ee1-efa0-421f-be06-24242ec2fb09&openudid=caf476e270b258&device_id=16269378842654&resolution=900*1600&os_version=5.1.1&language=zh&device_brand=Xiaomi&aid=1128&mcc_mnc=46007",
    # "device": get_douyin_device(),
    "device": get_douyin_device(),
    # "cookie": "install_id=2488947595022199; ttreq=1$26ae0cef57687c00e2e9d7c0ead7927a615915dc; passport_csrf_token=35e610ce541311aa58fb311e4d59fa33; d_ticket=2b15b0fb1bbc8c25c3e8a0b0a880231bf4; odin_tt=9de9114ca806185e8c46e5bae077e6a190ec180f7f300de0c455f67dc8d9ae45051cf8b451d8ab0282b01163a6a7b89c; sid_guard=7af29dc4dfd55c277dcd3456c1506ef5%7C1593071018%7C5184000%7CMon%2C+24-Aug-2020+07%3A43%3A38+GMT; uid_tt=d381bd61e5e2d7dbbd24f1e757bd26b7; uid_tt_ss=d381bd61e5e2d7dbbd24f1e757bd26b7; sid_tt=7af29dc4dfd55c277dcd3456c1506ef5; sessionid=7af29dc4dfd55c277dcd6c1506ef5; sessionid_ss=7af29dc4dfd55c277dc56c1506ef5",
    "cookie": get_douyin_cookie(),
    # "x_tt_token": "007af29dc4dfd55c277dcd3456c1506ef55e4f1dc4fa6a6e98c2f7b360985add505417ce5c67a298310afa30e8aa6559",
    "x_tt_token": get_douyin_x_tt_token(),

    # 快手 搜索url 列表 防止次数太快
    "kuai_shou_search_url_list":[
        # 列子1 先暂时不用
        # 'https://apissl.gifshow.com/rest/n/search/feed?mod=Netease%28MuMu%29&lon=121.473721&country_code=CN&kpn=KUAISHOU&oc=GENERIC&egid=DFP95BC6ABC760598F9C9B482862C51170A55F15526D0AA2CB07F79AB415656B&sbh=41&hotfix_ver=&sh=1440&appver=7.6.20.15169&nbh=0&socName=Unknown&newOc=GENERIC&max_memory=192&isp=&kcv=193&browseType=4&kpf=ANDROID_PHONE&ddpi=270&did=ANDROID_4f74435c452648ec&net=WIFI&app=0&ud=0&c=GENERIC&sys=ANDROID_6.0.1&sw=810&ftt=&ll=CQ9kPbX6Oj9AEWub4nFRXl5A&language=zh-cn&darkMode=false&iuid=&lat=31.230388&did_gt=1595949378959&ver=7.6',
        # self1
        " http://api.gifshow.com/rest/n/search/feed?app=0&ver=5.11&c=MYAPP%2C1&mod=Xiaomi%28Redmi%208%29&appver=5.11.3.7670&ftt=&lon=0&language=zh-cn&sys=ANDROID_9&max_memory=192&ud=2124822194&country_code=cn&oc=MYAPP%2C1&hotfix_ver=&did_gt=1603970241874&iuid=&net=WIFI&did=ANDROID_be5c3321db82f40f&lat=0"
    ],
    "kuai_shou_token_list":[
        # xyy
        "a7eb37a0997b4be4b213b4279b34969e-2124822194"
    ],

}

if __name__ == '__main__':
    get_douyin_device()