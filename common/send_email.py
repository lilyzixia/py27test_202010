''' 
author:紫夏
Time:2020/10/18 11:43
'''

import smtplib
import os
from email.mime.text import MIMEText
from email.mime.application import MIMEApplication
from email.mime.multipart import MIMEMultipart
from common.handle_path import REPORT_DIR

def send_msg():
    smtp=smtplib.SMTP_SSL(host='smtp.qq.com',port=465)
    smtp.login(user='709737032@qq.com',password='imlnyopfmwgnbchi')

    msg=MIMEMultipart()
    msg['Subject']='测试报告1'
    msg['From']='709737032@qq.com'
    msg['To']='1711179415@qq.com'

    text=MIMEText(_text='您好，测试报告已发，请注意查收！',_charset='utf-8')
    msg.attach(text)

    with open(os.path.join(REPORT_DIR,'portreport.html'), 'rb')as f:
        content=f.read()

    report=MIMEApplication(content)
    report.add_header('content-disposition', 'attachment', filename='report.html')
    msg.attach(report)

    smtp.send_message(msg,from_addr='709737032@qq.com',to_addrs='1711179415@qq.com')
