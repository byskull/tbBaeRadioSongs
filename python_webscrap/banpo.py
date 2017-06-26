#-*- coding: utf-8 -*-

import re
import mechanize
import urllib2
import cookielib
from bs4 import BeautifulSoup
import pymysql
import datetime, time

school_id = 1

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1111', db='mysql', charset='utf8')
cur = conn.cursor()


cj = cookielib.CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)
br.set_handle_robots(False)

basedate = datetime.date(datetime.date.today().year, 3, 1 )

td = datetime.timedelta( days=1)

cur.execute('delete from tbAcademicCalendar where School_Id = ' + str(school_id)+ ' and date_format ( RefDate, "%Y" ) >=  "' + str ( datetime.date.today().year ) + '" '  )

for i in range ( 1, 300 ) :	
	basedate = basedate + td
	if basedate.weekday() == 6 :   # 6: sunday
		continue	
	br.open( "http://www.banpo.ms.kr/schedule/schedule.do?cmd=main&y=" + str( basedate.year ) + "&m=" + str( basedate.month ) + "&d=" + str( basedate.day ) + "&scNo=11221" );
		
	soup = BeautifulSoup( br.response().read() )

	cols = soup.findAll( 'div', attrs={ 'style' : re.compile("width: 544px;height: 65px; background-color: #fffaf4; padding-left: 5px;  border: 1px solid #ebebeb; padding-top: 5px;")} )

	for col in cols:
		print col.div.string.strip() #.to_string().decode('utf-8')
		cur.execute( u'insert into tbAcademicCalendar values ( "'+ str( basedate.year) + '/' + str( basedate.month) + '/' + str( basedate.day) + '", ' + str(school_id) + ', "' + col.div.string.strip() + '" , "00","" ) '  )

conn.commit()
			
cur.close()
conn.close()