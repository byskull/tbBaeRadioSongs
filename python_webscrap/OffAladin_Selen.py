#-*- coding: utf-8 -*-

import sqlite3
import sys
import re
import time

from bs4 import BeautifulSoup
import telepot

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait


# telepot 로 텔레그램 메시지 준비
YOUR_ACCESS_TOKEN = ""  # your toke here
bot = telepot.Bot(YOUR_ACCESS_TOKEN)

# SQLITE 로 서점 책 데이터 읽기
reload(sys)
sys.setdefaultencoding('euc-kr')

AladinBook = []
AladinShop = []
PersonaNonGrata = []

con = sqlite3.connect(r"C:\Users\infomax\Documents\db\AladinChk.sqlite")
cursor = con.execute("select * from OffAladinBook where Value = 0")
for row in cursor:
	print str(unicode(row[0])), str(row[1])
	AladinBook.append( (str(unicode(row[0])), str(row[1])) )

cursor = con.execute("select * from OffAladinShop where Value = 0")
mydata = cursor.fetchall()

for row in mydata :
	print str(unicode(row[0]))
	AladinShop.append( ( str(unicode(row[0])), str(unicode(row[1])) ) )
	
cursor = con.execute("select * from PersonaNonGrata where Value = 0")
mydata = cursor.fetchall()
for row in mydata:
	print str(unicode(row[0])), str(unicode(row[1]))
	PersonaNonGrata.append( (str(unicode(row[0])), str(unicode(row[1]))) )

# selenium 로 브라우저에 접속
	
browser = webdriver.Firefox()

for i in range(len( AladinBook ) ):

	# &KeyTag=A2&
	# A2 종로 A8 대학로 D0 수유
        print  AladinBook[i][0]
    
        browser.get(u"http://www.aladin.co.kr/search/wsearchresult.aspx?SearchTarget=UsedStore&SearchWord=" + AladinBook[i][0].replace(" ", "+")+ "&x=0&y=0")

        time.sleep(1)
    
        soup = BeautifulSoup(browser.page_source, "html5lib")
        cols = soup.findAll( 'a', attrs={ 'class' : "usedshop_off_text3" } )
	

        for col in cols:
            print col.text
            for shop in AladinShop :
                if col.text.find(shop[0]) >= 0 :
                    bcomp = col.parent.parent.parent.parent.parent.find('li').b.text.strip()				                    
                    for Persona in PersonaNonGrata :
                        if Persona[0] == AladinBook[i][0] and bcomp.find(Persona[1] ) >= 0 :
                            print ('in Persona Non Grata List')
                            break
                    else :
                        print ('passed'			)
                        mobileurl = "http://www.aladin.co.kr/m/msearch.aspx?SearchTarget=UsedStore&KeyTag=" + shop[1] + "&SearchWord=" + AladinBook[i][0].replace(" ", "+")
                        bot.sendMessage( 0, col.text + u"에 " + AladinBook[i][0] + u" 입고 되었습니다 \n" + mobileurl)
                    

browser.quit()