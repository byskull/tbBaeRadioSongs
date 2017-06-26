#-*- coding: utf-8 -*-

import sqlite3
import sys
import time
import re
import mechanize
import urllib2
import cookielib
from bs4 import BeautifulSoup
import telepot

# telepot 로 텔레그램 메시지 준비
YOUR_ACCESS_TOKEN = ""

bot = telepot.Bot(YOUR_ACCESS_TOKEN)

reload(sys)
sys.setdefaultencoding('euc-kr')

# 파일에 내용 저장

PastTitle = []

try :
	f1 = open("Denma.text","rt")
except IOError :
	pass
else :
	for s in f1 :
		PastTitle.append(s.strip())

# mechanize 로 브라우저에 접속
	
cj = cookielib.CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)
br.set_handle_robots(False)

while True :
	br.open("http://comic.naver.com/webtoon/list.nhn?titleId=119874")
	#"http://comic.naver.com/webtoon/list.nhn?titleId=119874&weekday=tue"

	soup = BeautifulSoup( br.response().read(), "html5lib" )

	cols  = soup.findAll( 'td', attrs={ 'class' : "title" } )

	print time.strftime('%X %x %Z')
	
	for col in cols :
		if col.text.strip() not in PastTitle and len(col.text) > 3 :	
			print col.text.strip()
			f2 = open("Denma.text", "a")
			f2.write( col.text.strip() )
			f2.write('\n')
			bot.sendMessage( 0, u"덴마 업데이트 \n" + col.text.strip() +"\n" + "http://comic.naver.com" + col.a['href'] )
			sys.exit()					
	
	time.sleep(300)
	