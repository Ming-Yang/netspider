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

def FindTorrentNpu(name):
	filename = sys.path[0]+'/logs/'+name+'_npupt.txt'
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
			for (torrent,torrent_chinese) in zip_longest(torrents_list,torrents_chinese_list):
				fd.write(torrent+'\n'+str(torrent_chinese)+'\n\n')
			fd.close()	
			return True
	else:
		fd = open(filename,mode='w')
		fd.write(num+"\n")
		torrents_list = re.findall(pattern='<td class="embedded"><a title="(.*?)" href',string=z.text)
		torrents_chinese_list = re.findall(pattern='<small></small><span title=\'(.*?)\'><br />',string=z.text)
		for (torrent,torrent_chinese) in zip_longest(torrents_list,torrents_chinese_list):
			fd.write(torrent+'\n'+str(torrent_chinese)+'\n\n')
		fd.close()		
		return True

	fd.close()
	return False

def FindTorrentByr(name):
	filename = sys.path[0]+'/logs/'+name+'_byrpt.txt'
	requests_url = "https://bt.byr.cn/torrents.php"
	requests_headers={
		'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
		'Accept-Encoding':'gzip, deflate, br',
		'Accept-Language':'en-US,en;q=0.5',
		'Cache-Control':'max-age=0',
		'Connection':'keep-alive',
		'Cookie':'_ga=GA1.2.664242068.1538545546; _gid=GA1.2.240869996.1538545546; c_secure_uid=Mjc2NzAy; c_secure_pass=646ca397654c5bbdec5ccc57e99dbe8d; c_secure_ssl=eWVhaA%3D%3D; c_secure_tracker_ssl=bm9wZQ%3D%3D; c_secure_login=bm9wZQ%3D%3D; _gat=1',
		'Host':'bt.byr.cn',
		'Referer':'https://bt.byr.cn/torrents.php?search=%E7%94%9F%E6%B4%BB%E5%A4%A7%E7%88%86%E7%82%B8&notnewword=1',
		'TE':'Trailers',
		'Upgrade-Insecure-Requests':'1',
		'User-Agent':'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:62.0) Gecko/20100101 Firefox/62.0'
	}
	requests_para = {
		'inclbookmarked':'0',
		'incldead':'0',
		'search':name,
		'search_area':'0',
		'search_mode':'0',
		'spstate':'0'
	}

	z = requests.get(url=requests_url,headers=requests_headers,params=requests_para)
	# temp = open(sys.path[0]+'/logs/temp.txt',mode='w')
	# temp.write(z.text)
	num = re.findall(pattern='&nbsp;-&nbsp;(.*?)</b></font></p>',string=z.text)[0]
	counts = int(num)

	if os.path.exists(filename):
		fd = open(filename,mode='r+')
		if counts > int(fd.readline()):
			fd.close()	
			fd = open(filename,mode='w')
			fd.write(num+"\n")
			torrents_list = re.findall(pattern='<td class="embedded"><a title="(.*?)"  href',string=z.text)
			torrents_chinese_list = re.findall(pattern='</font>]</b><br />(.*?) </td>',string=z.text)
			for (torrent,torrent_chinese) in zip_longest(torrents_list,torrents_chinese_list):
				fd.write(torrent+'\n'+str(torrent_chinese)+'\n\n')
			fd.close()	
			return True
	else:
		fd = open(filename,mode='w')
		fd.write(num+"\n")
		torrents_list = re.findall(pattern='<td class="embedded"><a title="(.*?)"  href',string=z.text)
		torrents_chinese_list = re.findall(pattern='</font>]</b><br />(.*?) </td>',string=z.text)
		for (torrent,torrent_chinese) in zip_longest(torrents_list,torrents_chinese_list):
			fd.write(torrent+'\n'+str(torrent_chinese)+'\n\n')
		fd.close()		
		return True

	fd.close()
	return False










def SendEmail(name,e_addr='379614985@qq.com'):
	refresh_npu = refresh_byr = False
	if FindTorrentNpu(name) == True :
		filename = sys.path[0]+'/logs/'+name+'_npupt.txt'
		fd = open(filename,mode='r')
		num = fd.readline()
		num = num.strip('\n')
		contex_npu = '\"'+name+'\" 蒲公英PT上一共有'+num+'个搜索结果\n\n'
		raw_npu = fd.read()
		refresh_npu = True

	if FindTorrentByr(name) == True:
		filename = sys.path[0]+'/logs/'+name+'_byrpt.txt'
		fd = open(filename,mode='r')
		num = fd.readline()
		num = num.strip('\n')
		contex_byr = '\"'+name+'\" 北邮人PT上一共有'+num+'个搜索结果\n\n'
		raw_byr = fd.read()
		refresh_byr = True

	if(refresh_npu | refresh_byr):
		if(refresh_npu & refresh_byr):
			msg = MIMEText(contex_npu+contex_byr+raw_npu+'===================================\n\n'+raw_byr, 'plain', 'utf-8')
		elif(refresh_npu):
			msg = MIMEText(contex_npu+raw_npu, 'plain', 'utf-8')
		elif(refresh_byr):
			msg = MIMEText(contex_byr+raw_byr, 'plain', 'utf-8')

		msg['Subject'] = Header('\"'+name+'\" 在PT上的搜索结果', 'utf-8').encode()
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



SendEmail(sys.argv[1])