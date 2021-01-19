# -*- coding:utf-8 -*-
# Chance favors the prepared mind.
# author : pyl owo,
# time : 2020/11/4
# from jpype import *
#
# startJVM(getDefaultJVMPath())
# java.lang.System.out.println('hello world')
# shutdownJVM()  # 关闭 java 虚拟机，或者python运行完会自动关闭

# !/usr/bin/env python
# coding : utf-8
import os

from jpype import *
jarpath = os.path.join(os.path.abspath('.'), '/home/lpy/lpy/file/pyproject/hexikeji_all/hexi_online_spider_v001'
                                             '/novel_search_unit/caihongmianfei_novel_unit/')
jvmpath = getDefaultJVMPath()
startJVM(jvmpath, "-ea", "-Djava.class.path=%s" % (jarpath + 'SearchApiStr.jar'))
TA = JPackage('SearchApiStr').SearchApiStr


def get_search_md5str(keyword: str, page: str, appid='803DFBB483094BFCBBF78ADDFECE0622'):
    jd = TA()
    md5temp = 'appid={}&keyword={}&pageindex={}&pagesize=15NXG6LVbWMV5ZYZK7IPBRESK96GLPOHRM'.format(appid, keyword, page)
    md5str = jd.md5(md5temp)
    return md5str


def get_detail_md5str(novelid: str, appid='803DFBB483094BFCBBF78ADDFECE0622'):
    jd = TA()
    md5temp = 'appid={}&novelid={}NXG6LVbWMV5ZYZK7IPBRESK96GLPOHRM'.format(appid, novelid)
    md5str = jd.md5(md5temp)
    return md5str

if __name__ == "__main__":
    # print(get_search_md5str('刘鹏遥', '1'))
    print(get_detail_md5str('1194'))
