# -*- coding:utf-8 -*-
# 享受雷霆感受雨露
# author xyy,time:2021/1/7

"""

发送邮件：

    发送固定文件内容

要求 ：

    1，可更改 发送人 以及收件人
    2，收件人是一群人 可以有白名单
    3，无论什么情况都会发送邮件
    ## 后期实现的 需求排期
        需要确认？后期需求
            接口 点击了 进行查看
"""

import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.header import Header
from Audio_Infringement_Config import  Test_Config_Setting as test_config
#
# ind = {
#     # 邮箱服务
#     "smtpserver" : "",
#     # 用户名称
#     "username" :"",
#     # 用户密码 开启功能后的密码 非正常密码
#     "password" :"",
#     # 发送人
#     "sender" :"",
#     # 接受人
#     "receiver" :"",
#     # 主题
#     "subject" :"",
#
# }

def Send_email(erro_text="",**kwargs):
    # 设置smtplib所需的参数
    # 下面的发件人，收件人是用于邮件传输的。
    smtpserver = kwargs["smtpserver"]
    username = kwargs["username"]
    password = kwargs["password"]
    sender = kwargs["sender"]
    # receiver='XXX@126.com'
    # 收件人为多个收件人
    receiver = kwargs["receiver"]

    subject = kwargs["subject"]
    # 通过Header对象编码的文本，包含utf-8编码信息和Base64编码信息。以下中文名测试ok
    # subject = '中文标题'
    # subject=Header(subject, 'utf-8').encode()

    # 构造邮件对象MIMEMultipart对象
    # 下面的主题，发件人，收件人，日期是显示在邮件页面上的。
    msg = MIMEMultipart('mixed')
    msg['Subject'] = subject
    msg['From'] = '{} <{}>'.format(sender, sender)
    # msg['To'] = 'XXX@126.com'
    # 收件人为多个收件人,通过join将列表转换为以;为间隔的字符串
    msg['To'] = ";".join(receiver)
    # msg['Date']='2012-3-16'

    # 构造文字内容
    # text = "Hi!\nHow are you?\nHere is the link you wanted:\nhttp://www.baidu.com"
    text = erro_text
    text_plain = MIMEText(text, 'plain', 'utf-8')
    msg.attach(text_plain)

    # 构造图片链接
    # sendimagefile = open(r'/Users/quanlifang/Desktop/yulu_/test1.jpg', 'rb').read()
    # image = MIMEImage(sendimagefile)
    # image.add_header('Content-ID', '<image1>')
    # image["Content-Disposition"] = 'attachment; filename="testimage.png"'
    # msg.attach(image)

    # 构造html
    # 发送正文中的图片:由于包含未被许可的信息，网易邮箱定义为垃圾邮件，报554 DT:SPM ：<p><img src="cid:image1"></p>
    # html = """
    # <html>
    #   <head></head>
    #   <body>
    #     <p>Hi!<br>
    #        How are you?<br>
    #        Here is the <a href="http://www.baidu.com">link</a> you wanted.<br>
    #     </p>
    #   </body>
    # </html>
    # """
    # text_html = MIMEText(html, 'html', 'utf-8')
    # text_html["Content-Disposition"] = 'attachment; filename="texthtml.html"'
    # msg.attach(text_html)

    # 构造附件
    sendfile = open(
        r'test_email_file_tem',
        'rb').read()
    text_att = MIMEText(sendfile, 'base64', 'utf-8')
    text_att["Content-Type"] = 'application/octet-stream'
    # 以下附件可以重命名成aaa.txt
    # text_att["Content-Disposition"] = 'attachment; filename="aaa.txt"'
    # 另一种实现方式
    text_att.add_header('Content-Disposition', 'attachment', filename='hexi_online_spider_erro.txt')
    # 以下中文测试不ok
    # text_att["Content-Disposition"] = u'attachment; filename="中文附件.txt"'.decode('utf-8')
    msg.attach(text_att)

    # 发送邮件
    smtp = smtplib.SMTP()
    smtp.connect(smtpserver)
    # 我们用set_debuglevel(1)就可以打印出和SMTP服务器交互的所有信息。
    # smtp.set_debuglevel(1)
    smtp.login(username, password)
    smtp.sendmail(sender, receiver, msg.as_string())
    smtp.quit()

if __name__ == '__main__':
    Send_email(erro_text="test",**test_config)