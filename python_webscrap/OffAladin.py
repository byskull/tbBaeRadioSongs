#-*- coding: utf-8 -*-

import sqlite3
import sys
import re
import mechanize
import urllib2
import cookielib
from bs4 import BeautifulSoup
import telepot

# telepot 로 텔레그램 메시지 준비
YOUR_ACCESS_TOKEN = ""

bot = telepot.Bot(YOUR_ACCESS_TOKEN)

#print bot.getMe()["username"]
#print bot.getMe()["first_name"]

#bot.sendMessage( 24060268, u"이것보게")

# SQLITE 로 서점 책 데이터 읽기
reload(sys)
sys.setdefaultencoding('euc-kr')

AladinBook = []
AladinShop = []

con = sqlite3.connect("C:\Users\infomax\Documents\db\AladinChk.sqlite")
cursor = con.execute("select * from OffAladinBook where Value = 0")
for row in cursor:
	print str(unicode(row[0])), str(row[1])
	AladinBook.append( (str(unicode(row[0])), str(row[1])) )


cursor = con.execute("select * from OffAladinShop where Value = 0")

mydata = cursor.fetchall()

for row in mydata :
	print str(unicode(row[0]))
	AladinShop.append( ( str(unicode(row[0])), str(unicode(row[1])) ) )

# mechanize 로 브라우저에 접속
	
cj = cookielib.CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)
br.set_handle_robots(False)

for i in range(len( AladinBook ) ):

	# &KeyTag=A2&
	# A2 종로 A8 대학로 D0 수유

	br.open( "http://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=UsedStore&SearchWord=" + AladinBook[i][1]+ "&x=0&y=0"  )

	#mobileurl = "http://www.aladin.co.kr/m/msearch.aspx?SearchTarget=UsedStore&SearchWord=" + AladinBook[i][0].replace(" ", "+")
	
	soup = BeautifulSoup( br.response().read(), "html5lib" )

	cols  = soup.findAll( 'a', attrs={ 'class' : "usedshop_off_text3" } )
	
	print AladinBook[i][0]
	
	for col in cols:
		print col.text
		for shop in AladinShop :
			if col.text.find(shop[0]) >= 0 :
				mobileurl = "http://www.aladin.co.kr/m/msearch.aspx?SearchTarget=UsedStore&KeyTag=" + shop[1] + "&SearchWord=" + AladinBook[i][0].replace(" ", "+")
				bot.sendMessage( 0, col.text + u"에 " + AladinBook[i][0] + u" 입고 되었습니다 \n" + mobileurl)
				

