# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/11/28

import requests

# req = {
#     'url': 'https://apissl.gifshow.com/rest/n/moment/list?mod=Netease%28MuMu%29&lon=121.473721&country_code=CN&kpn=KUAISHOU&oc=GENERIC&egid=DFP95BC6ABC760598F9C9B482862C51170A55F15526D0AA2CB07F79AB415656B&sbh=41&hotfix_ver=&sh=1440&appver=7.6.20.15169&nbh=0&socName=Unknown&newOc=GENERIC&max_memory=192&isp=&kcv=193&browseType=4&kpf=ANDROID_PHONE&ddpi=270&did=ANDROID_4f74435c452648ec&net=WIFI&app=0&ud=0&c=GENERIC&sys=ANDROID_6.0.1&sw=810&ftt=&ll=CQ9kPbX6Oj9AEWub4nFRXl5A&language=zh-cn&darkMode=false&iuid=&lat=31.230388&did_gt=1595949378959&ver=7.6',
#     'method': 'POST',
#     'body': {
#         'userId': '1291106540',
#         'count': '10',
#         'firstMomentClosed': 'false',
#         'kuaishou.api_st': 'Cg9rdWFpc2hvdS5hcGkuc3QSsAEMaySOEfimA3DdPGWcU11ZHox8cDJVp4tedIUj7W-N_w5NgzuNoF4R1pKczoc1NE9WzkPKYQxSAMjo7P7UG9pb-M8Owvja8Q1y_9j6Q88ISnaJiE14cTtI3gcsC1nM_ZO5oeCnd2ISvfbg5gmw1A8PDT_u3lfAB0dfcGtns_LBQPxIjTXeGifvDgOcVwOwwfx8yFXFccxAj05Uys639E7020xj4kYiJquTsc17em_PrxoSRCUg25kRQfGgW7J-1Cb386UHIiBZDCsZSxpb2TiqFFIxK5E_mGM15OalOwwhXIz20yb83ygFMAE',
#         'token': 'c1c63a70fb2a418e985d65ae11b5e2c2-2011678336',
#         'client_key': '3c2cd3f3',
#         'os': 'android'
#     }
# }
req = {
    # 'url': 'https://apissl.gifshow.com/rest/n/search/feed?mod=Netease%28MuMu%29&lon=121.473721&country_code=CN&kpn=KUAISHOU&oc=GENERIC&egid=DFP95BC6ABC760598F9C9B482862C51170A55F15526D0AA2CB07F79AB415656B&sbh=41&hotfix_ver=&sh=1440&appver=7.6.20.15169&nbh=0&socName=Unknown&newOc=GENERIC&max_memory=192&isp=&kcv=193&browseType=4&kpf=ANDROID_PHONE&ddpi=270&did=ANDROID_4f74435c452648ec&net=WIFI&app=0&ud=0&c=GENERIC&sys=ANDROID_6.0.1&sw=810&ftt=&ll=CQ9kPbX6Oj9AEWub4nFRXl5A&language=zh-cn&darkMode=false&iuid=&lat=31.230388&did_gt=1595949378959&ver=7.6',
    # 'url': " http://api.gifshow.com/rest/n/search/feed?app=0&ver=5.12&c=MYAPP%2C1&mod=Xiaomi%28Redmi%208%29&appver=5.11.3.7670&ftt=&lon=0&language=zh-cn&sys=ANDROID_9&max_memory=192&ud=2124822194&country_code=cn&oc=MYAPP%2C1&hotfix_ver=&did_gt=1603970241874&iuid=&net=WIFI&did=ANDROID_be5c3321db82f40f&lat=0",
    # 'url': " http://api.gifshow.com/rest/n/search/feed?app=0&ver=5.11&c=MYAPP%2C1&mod=Xiaomi%28Redmi%208%29&appver=5.11.3.7670&ftt=&lon=0&language=zh-cn&sys=ANDROID_9&max_memory=192&ud=2124822194&country_code=cn&oc=MYAPP%2C1&hotfix_ver=&did_gt=1603970241874&iuid=&net=WIFI&did=ANDROID_be5c3321db82f40f&lat=0",
    'url': " http://api.gifshow.com/rest/n/search/feed?app=0&ver=5.12&c=MYAPP%2C1&mod=Xiaomi%28Redmi%208%29&appver=5.11.3.7670&ftt=&lon=0&language=zh-cn&sys=ANDROID_9&max_memory=192&ud=2124822194&country_code=cn&oc=MYAPP%2C1&hotfix_ver=&did_gt=1603970241874&iuid=&net=WIFI&did=ANDROID_4f74435c452648ec&lat=0",
    'method': 'POST',
    'body': {
        'keyword': '班淑传奇',
        # 'fromPage': "1",
        'pcursor': "3",
        'isRecoRequest': 'false',
        'kuaishou.api_st': 'Cg9rdWFpc2hvdS5hcGkuc3QSsAEMaySOEfimA3DdPGWcU11ZHox8cDJVp4tedIUj7W-N_w5NgzuNoF4R1pKczoc1NE9WzkPKYQxSAMjo7P7UG9pb-M8Owvja8Q1y_9j6Q88ISnaJiE14cTtI3gcsC1nM_ZO5oeCnd2ISvfbg5gmw1A8PDT_u3lfAB0dfcGtns_LBQPxIjTXeGifvDgOcVwOwwfx8yFXFccxAj05Uys639E7020xj4kYiJquTsc17em_PrxoSRCUg25kRQfGgW7J-1Cb386UHIiBZDCsZSxpb2TiqFFIxK5E_mGM15OalOwwhXIz20yb83ygFMAE',
        # 'token': 'c1c63a70fb2a418e985d65ae11b5e2c2-2011678336',
        # 'token': 'a7eb37a0997b4be4b213b4279b34969e-2124822194-2011678336',
        'token': 'a7eb37a0997b4be4b213b4279b34969e-2124822194',
        'client_key': '3c2cd3f3',
        # 'os': 'android'
    }
}

resp = requests.post('https://cloud.anoyi.com/api/ksapp/common', headers={'X-Token':'ABBC37E62D7311EB950B88E9FE880485'}, json=req).json()
print('--------- Anoyi Cloud Service Response -------')
print(resp)
from Audio_Infringement_Config import proxies
# resp = requests.post(resp['url'], headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=resp['body'].encode('utf-8'),proxies=proxies)
resp = requests.post(resp['url'], headers={'Content-Type': 'application/x-www-form-urlencoded'}, data=resp['body'].encode('utf-8'))
print('--------- Kuaishou Response -------')
print(resp.text)