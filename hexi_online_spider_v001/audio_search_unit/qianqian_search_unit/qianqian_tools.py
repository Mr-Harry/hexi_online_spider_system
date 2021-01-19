# -*- coding:utf-8 -*-
# Chance favors the prepared mind.
# author : pyl owo,
# time : 2020/9/18
from Audio_Infringement_Config import Config_of_audio_infringement as config


def get_proxy():
    proxy = "%(user)s:%(pass)s@%(host)s:%(port)s" % {
        "host": config["proxyHost"],
        "port": config["proxyPort"],
        "user": config["proxyUser"],
        "pass": config["proxyPass"],
    }
    proxies = {
        'http': 'http://' + proxy,
        'https': 'https://' + proxy,
    }
    return proxies