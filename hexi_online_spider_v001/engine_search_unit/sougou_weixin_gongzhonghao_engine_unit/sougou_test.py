import re
import requests


x = 'https://weixin.sogou.com/antispider/?from=%2Flink%3Furl%3Ddn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS7m2ExlKN1HvGVF9Fqj2q3EoWEmfmfZsOFqXa8Fplpd9LtB9c-X1ZF6z3UN4nyXNcVfdauhv2r5e1E3RmYtonlF7DoW0-ipvBhbYUvrg9KcisRjrkC_JLf_BGQjzm0zchtY-_BLb72CX9eE--fmxKeCTGWu9zI2Fr3Hxw9JIeYMaccAZCIzcUqzM3uAnARNcaSz5YWuI6VejYaholCaimoaq3X8EKMKOIA..%26type%3D2%26query%3Dwoaini%26token%3D9B3F29E3288CD5576A6FDB3995B27A976A4C5DC95F92AF65'
# x = 'https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS7m2ExlKN1HvGVF9Fqj2q3EoWEmfmfZsOFqXa8Fplpd9LtB9c-X1ZF6z3UN4nyXNcVfdauhv2r5e1E3RmYtonlF7DoW0-ipvBhbYUvrg9KcisRjrkC_JLf_BGQjzm0zchtY-_BLb72CX9eE--fmxKeCTGWu9zI2Fr3Hxw9JIeYMaccAZCIzcUqzM3uAnARNcaSz5YWuI6VejYaholCaimoaq3X8EKMKOIA..&type=2&query=woaini&token=9B3F29E3288CD5576A6FDB3995B27A976A4C5DC95F92AF65'
# 'https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS55BOgxD20rr1ecOtWkxG5_BSEImF88gEFqXa8Fplpd9MjRCa2A3p0BXj6xT9gO8BmSDtpuVqpFjUjHUqzRmimA3IxoE-GnBK6tcoi4hhy9hEDO06yzLySyoP_NLMwmZrudQtmm4hzhnjGQg_ocB70ca0UTMtxiDQOveSsUgTzcjblyn0j3etusTZblGJiKMox1cn3igmUv2Ax3D331bRmotPujwwRB2Pw..&type=2&query=woaini&token=0F6FA8BDE1DD26275B59EE0C7A0FE0D45CC9B6F65F93C385&k=66&h=X'
# 'https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS55BOgxD20rr1ecOtWkxG5_BSEImF88gEFqXa8Fplpd9MjRCa2A3p0BXj6xT9gO8BmSDtpuVqpFjUjHUqzRmimA3IxoE-GnBK6tcoi4hhy9hEDO06yzLySyoP_NLMwmZrudQtmm4hzhnjGQg_ocB70ca0UTMtxiDQOveSsUgTzcjblyn0j3etusTZblGJiKMox1cn3igmUv2Ax3D331bRmotPujwwRB2Pw..&type=2&query=woaini&token=0F6FA8BDE1DD26275B59EE0C7A0FE0D45CC9B6F65F93C385&k=66&h=X'
# 10-24 14:05
# x= 'https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS55BOgxD20rrP-4Co1ZDFO3BSEImF88gEFqXa8Fplpd9LV_O4snDpR248iUyacQCY5v0J1wDd7gVkDqJvD6xx4MA1EvPEomgk7S8__OmjoqkeEDck9V_OMFBrpXyIgDlrXT7cBJ9LLzp0cWUVzsebVl1xVEG8B42ZDD4w3mla1qXcSbZWg-cTn8Hin_DX-Jz-er_b52teE8zIUSuPVAQIGrFcvUoAZZH7Q..&type=2&query=11&token=0F6AE50DE1DD26275B59EE0C7A0FE0D45CC9B6F65F93C1EA&k=96&h=5'

# x = 'https://weixin.sogou.com/link?url=dn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS7m2ExlKN1HvCQQWOsC6FhgoWEmfmfZsOFqXa8Fplpd9GbGS1JqNq_766ksD7NrgK0Bs1Tqaxak3vuXMluIRznF1PFtKtyoJAbRHMy1s0PsljK3_XASu0qv_HL3nCCpXj0FUT5xxpHbhNLuTRCT6DxgyOXgfzyQ_5J_k7M0LkyNp7YK0AZfMeXvSJuW3RLjIygC5HgmSXd_pGjYhW5AIvrvvzHZXxeLdyg..&type=2&query=woaini&token=9B5656EBE4F9D9E2A09A12CBD207B432A0B24A125F92B71D'
# cookies = 'ssuid=8070025466; sw_uuid=9687167365; SUID=EE817A7B6A13A00A000000005F6C6CB3; SUV=1602551603046857; ld=lkllllllll2KP5DClllllVMVJ1YlllllWT$RbyllllUlllllRylll5@@@@@@@@@@; LSTMV=332%2C290; LCLKINT=15603; IPLOC=CN1100; SNUID=94AE5253292C9B7EBC993C38293A8E3A; ABTEST=3|1603461129|v1; PHPSESSID=033lficrsg7bu2i82ahg1ac700; refresh=1; SUID=6D837A7B5E1CA00A000000005F850386; ld=kyllllllll2KP5DClllllVMVV8UlllllWT$RbylllltlllllRylll5@@@@@@@@@@; ABTEST=7|1603446573|v1; SNUID=360AF1F08C8E3ED8F3E449AA8CA04A94; IPLOC=CN1100'
cookies = 'ssuid=8070025466; sw_uuid=9687167365; SUID=EE817A7B6A13A00A000000005F6C6CB3; SUV=1602551603046857; ld=lkllllllll2KP5DClllllVMVJ1YlllllWT$RbyllllUlllllRylll5@@@@@@@@@@; LSTMV=332%2C290; LCLKINT=15603; IPLOC=CN1100; SNUID=94AE5253292C9B7EBC993C38293A8E3A; ABTEST=3|1603461129|v1; PHPSESSID=033lficrsg7bu2i82ahg1ac700; refresh=1; SUID=6D837A7B5E1CA00A000000005F850386; ld=kyllllllll2KP5DClllllVMVV8UlllllWT$RbylllltlllllRylll5@@@@@@@@@@; ABTEST=7|1603446573|v1; SNUID=251FE3E3989C2AFD9F030D5B999065B6; IPLOC=CN1100'
# cookies = ''
headers = {
  'Connection': 'keep-alive',
  'Cache-Control': 'max-age=0',
  'Upgrade-Insecure-Requests': '1',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
  'Sec-Fetch-Site': 'none',
  'Sec-Fetch-Mode': 'navigate',
  'Sec-Fetch-User': '?1',
  'Sec-Fetch-Dest': 'document',
  'Accept-Language': 'zh-CN,zh;q=0.9',
  'Cookie': cookies
}


url = "https://weixin.sogou.com/antispider/util/seccode.php?tc=1603462057690"

payload = {}
headers2 = {
  'Connection': 'keep-alive',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
  'Accept': 'image/avif,image/webp,image/apng,image/*,*/*;q=0.8',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'no-cors',
  'Sec-Fetch-Dest': 'image',
  'Referer': 'https://weixin.sogou.com/antispider/?from=%2Flink%3Furl%3Ddn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS7m2ExlKN1HvGVF9Fqj2q3EoWEmfmfZsOFqXa8Fplpd9LtB9c-X1ZF6z3UN4nyXNcVfdauhv2r5e1E3RmYtonlF7DoW0-ipvBhbYUvrg9KcisRjrkC_JLf_BGQjzm0zchtY-_BLb72CX9eE--fmxKeCTGWu9zI2Fr3Hxw9JIeYMaccAZCIzcUqzM3uAnARNcaSz5YWuI6VejYaholCaimoaq3X8EKMKOIA..%26type%3D2%26query%3Dwoaini%26token%3D9B3F29E3288CD5576A6FDB3995B27A976A4C5DC95F92AF65',
  'Accept-Language': 'zh-CN,zh;q=0.9',
  'Cookie': cookies,
}
headers3 = {
  'Connection': 'keep-alive',
  'Accept': 'application/json, text/javascript, */*; q=0.01',
  'X-Requested-With': 'XMLHttpRequest',
  'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.75 Safari/537.36',
  'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
  'Origin': 'https://weixin.sogou.com',
  'Sec-Fetch-Site': 'same-origin',
  'Sec-Fetch-Mode': 'cors',
  'Sec-Fetch-Dest': 'empty',
  'Referer': 'https://weixin.sogou.com/antispider/?from=%2Flink%3Furl%3Ddn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS7m2ExlKN1HvGVF9Fqj2q3EoWEmfmfZsOFqXa8Fplpd9LtB9c-X1ZF6z3UN4nyXNcVfdauhv2r5e1E3RmYtonlF7DoW0-ipvBhbYUvrg9KcisRjrkC_JLf_BGQjzm0zchtY-_BLb72CX9eE--fmxKeCTGWu9zI2Fr3Hxw9JIeYMaccAZCIzcUqzM3uAnARNcaSz5YWuI6VejYaholCaimoaq3X8EKMKOIA..%26type%3D2%26query%3Dwoaini%26token%3D9B3F29E3288CD5576A6FDB3995B27A976A4C5DC95F92AF65',
  'Accept-Language': 'zh-CN,zh;q=0.9',
  'Cookie': cookies,
}
# response = requests.request("GET", url, headers=headers, data = payload)

# print(response.text.encode('utf8'))

r = requests.get(url=x,headers=headers)

rurl = r.url
print(rurl)
print(r.text)
yy = re.findall("url \+= \'(.*?)\';",r.text)

print(''.join(yy).replace('@', ''))
if 'weixin.sogou.com/antispider/' in rurl:
    auuid = re.search('var auuid = \"(.*?)\";', r.text, re.M | re.S).group(1)
    url = "https://weixin.sogou.com/antispider/util/seccode.php"
    response = requests.request("GET", url, headers=headers2)
    print('111111111111111111111111111111111111111')
    # print(response.text)
    print(auuid)
    with open('picture.jpg', 'wb') as file:
        file.write(response.content)
        print('xx')
    url2 = "https://weixin.sogou.com/antispider/thank.php?tc=1234565644"
    x = input()
    payload = "c={}&r=%252Flink%253Furl%253Ddn9a_-gY295K0Rci_xozVXfdMkSQTLW6cwJThYulHEtVjXrGTiVgS7m2ExlKN1HvGVF9Fqj2q3EoWEmfmfZsOFqXa8Fplpd9LtB9c-X1ZF6z3UN4nyXNcVfdauhv2r5e1E3RmYtonlF7DoW0-ipvBhbYUvrg9KcisRjrkC_JLf_BGQjzm0zchtY-_BLb72CX9eE--fmxKeCTGWu9zI2Fr3Hxw9JIeYMaccAZCIzcUqzM3uAnARNcaSz5YWuI6VejYaholCaimoaq3X8EKMKOIA..%2526type%253D2%2526query%253Dwoaini%2526token%253D9B3F29E3288CD5576A6FDB3995B27A976A4C5DC95F92AF65&v=5&suuid=&" \
              "auuid={}".format(x, auuid)
    print(payload)
    response2 = requests.request("POST", url2, headers=headers3, data=payload)
    print('111111111111111111111111111111111111111')
    print(response2.text)

# {"code": 0,"msg": "è§£å°æåï¼æ­£å¨ä¸ºæ¨è·³è½¬æ¥æºå°å...", "id": "9AB941403A3E885E027B57693B32B5EF"}<<<
# # id为cookies的SNUID <<<<


# import requests
# r = requests.get('https://mp.weixin.qq.com/s?src=11&timestamp=1603448677&ver=2662&signature=9WuV5IlC-mIGoOqCv-tz1fQ9N6vcSfsr1wk7b8ecAcsYLwOv9QEwCxzJwpqVJpoiYg-iekojde5FzB983X4DQA2fsqef-rhT5GGV-tXDPuYg25pKsVVXC1kCb32QNSdi&new=1')
#
#
# print(r.text)