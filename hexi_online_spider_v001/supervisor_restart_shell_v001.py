# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2020/9/14

""":cvar
supervisorctl 阻塞的问题解决 查看status状态 判断 是否大于
"""

import os

# 获得脚本的内容 [line]
import time

time_out = 22

def get_shell_info():
    info = os.popen("supervisorctl status")
    info = info.read()
    shell_info = [i for i in info.split("\n") if i]  # 每一行 确保是非空
    # return ['supervisor_down_load_sub:supervisor_down_load_sub_00                       RUNNING   pid 1901907, uptime 4 days, 0:06:03', 'supervisor_down_load_sub:supervisor_down_load_sub_01                       RUNNING   pid 1907435, uptime 1:08:50', 'supervisor_down_load_task:supervisor_down_load_task_00                     RUNNING   pid 1910719, uptime 0:04:41', 'supervisor_genera_sub_fingerprint:supervisor_genera_sub_fingerprint_00     RUNNING   pid 1914184, uptime 0:40:24', 'supervisor_genera_sub_fingerprint:supervisor_genera_sub_fingerprint_01     RUNNING   pid 1914310, uptime 04:31:14', 'supervisor_genera_sub_fingerprint:supervisor_genera_sub_fingerprint_02     RUNNING   pid 1914341, uptime 0:32:13', 'supervisor_genera_task_fingerprint:supervisor_genera_task_fingerprint_00   RUNNING   pid 1914441, uptime 0:00:07', 'supervisor_genera_task_toredis                                             RUNNING   pid 1914442, uptime 0:00:07', 'supervisor_genera_task_toredis_file_name                                   RUNNING   pid 1914480, uptime 0:00:04']
    return shell_info

#

# 判断内容是否需要重启
def restart_supervisor(shell_info:list):
    need_restsart = []
    # print(shell_info)
    for each in shell_info:
        if "uptime" in each:
            commond = each.split(" ")[0] # 命令command
            run_time = each.split("uptime")[1] # 时间
            if "days" in run_time:
                fen_time = run_time.split(':')[1]  # 分钟
                shi_time = run_time.split(",")[1].split(":")[0].replace(" ","") # 小时

            else:
                fen_time = run_time.split(':')[1]  # 分钟
                shi_time = run_time.split(':')[0].replace(" ","")  # 小时


            # print(commond)
            # print(run_time)
            # print(fen_time)
            if "day" in run_time or int(fen_time)>time_out or int(shi_time)>1:
                print("超时间了！！！")
                need_restsart.append("supervisorctl restart {}".format(commond))
            else:
                pass
    return need_restsart
def run():
    need_restsart = restart_supervisor(get_shell_info())
    for each in need_restsart:
        print("执行 {}".format(each))
        os.system(each)
if __name__ == '__main__':
    #大于一个小时 大于多少分钟以上的
    run()
    time.sleep(30)