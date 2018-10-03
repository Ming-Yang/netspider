#coding=utf-8
import requests
import os
import sys
import re
from itertools import zip_longest

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib
e_addr='379614985@qq.com'

fd = open("temp.txt")
ab = fd.read()
msg = MIMEText(ab, 'HTML', 'utf-8')
msg['Subject'] = Header('\"''\" 在PT上的搜索结果', 'utf-8').encode()
msg['From'] = '<ming_yang_server@163.com>'
msg['To'] = '<'+e_addr+'>'
from_addr = 'ming_yang_server@163.com'
password = '123abc'
to_addr = e_addr
smtp_server = 'smtp.163.com'

import smtplib
server = smtplib.SMTP(smtp_server, 25)
server.set_debuglevel(1)
server.login(from_addr, password)
server.sendmail(from_addr, [to_addr], msg.as_string())
server.quit()