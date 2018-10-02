#coding=utf-8
import requests
import os
import sys
import re

from email import encoders
from email.header import Header
from email.mime.text import MIMEText
from email.utils import parseaddr, formataddr
import smtplib

def FindTorrent(name):
	filename = sys.path[0]+'/logs/'+name+'_torrents.txt'
	requests_url = "https://npupt.com/torrents.php"
	requests_headers={
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate, br',
		'Accept-Language':'en-US,en;q=0.5',
		'Cache-Control':'max-age=0',
		'Connection':'keep-alive',
		'Cookie':'shb=npubits; _ga=GA1.2.845011111.1538382613; _gid=GA1.2.619374448.1538382613; c_secure_uid=NjEzNTY%3D; c_secure_pass=ed6a36d6ebec98cc84303c746c83cfdb; c_secure_ssl=eWVhaA%3D%3D; c_secure_tracker_ssl=bm9wZQ%3D%3D; c_secure_login=bm9wZQ%3D%3D',
		'Host':'npupt.com',
		'Referer':'https://npupt.com/login.php?returnto=torrents.php',
		'Upgrade-Insecure-Requests':'1',
		'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0'
	}
	requests_para = {
		'incldead':'1',
		'nodupe':'1',
		'search':name,
		'sort':'10'
	}

	z = requests.get(url=requests_url,headers=requests_headers,params=requests_para)
	# temp = open('temp.txt',mode='w')
	# temp.write(z.text)
	num = re.findall(pattern='找到(.*?)条结果',string=z.text)[0]
	counts = int(num)

	if os.path.exists(filename):
		fd = open(filename,mode='r+')
		if counts > int(fd.readline()):
			fd.close()	
			fd = open(filename,mode='w')
			fd.write(num+"\n")
			torrents_list = re.findall(pattern='<td class="rowfollow th-fat"><table class="torrentname" width="100%"><tr><td class="embedded"><a title="(.*?)" href',string=z.text)
			torrents_chinese_list = re.findall(pattern='<small></small><span title=\'(.*?)\'><br />',string=z.text)
			for index in range(0,counts):
				torrent = torrents_list[index]
				torrent_chinese = torrents_chinese_list[index]
				fd.write(torrent+'\n'+torrent_chinese+'\n\n')
			fd.close()	
			return True
	else:
		fd = open(filename,mode='w')
		fd.write(num+"\n")
		torrents_list = re.findall(pattern='<td class="rowfollow th-fat"><table class="torrentname" width="100%"><tr><td class="embedded"><a title="(.*?)" href',string=z.text)
		torrents_chinese_list = re.findall(pattern='<small></small><span title=\'(.*?)\'><br />',string=z.text)
		for index in range(0,counts):
			torrent = torrents_list[index]
			torrent_chinese = torrents_chinese_list[index]
			fd.write(torrent+'\n'+torrent_chinese+'\n\n')
		fd.close()		
		return True

	fd.close()
	return False

def SendEmail(name,e_addr):
	if FindTorrent(name) == True :
		filename = sys.path[0]+'/logs/'+name+'_torrents.txt'
		fd = open(filename,mode='r')
		num = fd.readline()
		num = num.strip('\n')
		contex = '\"'+name+'\" 蒲公英PT上一共有'+num+'个搜索结果:\n\n'
		raw = fd.read()

		msg = MIMEText(contex+raw, 'plain', 'utf-8')
		msg['Subject'] = Header('\"'+name+'\" 在蒲公英PT上的搜索结果', 'utf-8').encode()
		msg['From'] = '<ming_yang_server@163.com>'
		msg['To'] = '<379614985@qq.com>'


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



SendEmail(sys.argv[1],'379614985@qq.com')