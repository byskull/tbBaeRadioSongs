#-*- coding: utf-8 -*-

import re
import mechanize
import urllib2
import cookielib
from bs4 import BeautifulSoup
import pymysql
import datetime, time

school_id = 2

conn = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='1111', db='mysql', charset='utf8')
cur = conn.cursor()


cj = cookielib.CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)
br.set_handle_robots(False)

basedate = datetime.date(datetime.date.today().year, 3, 1 )

tdelta = datetime.timedelta( days=1)

cur.execute('delete from tbAcademicCalendar where School_Id = ' + str(school_id)+ ' and date_format ( RefDate, "%Y" ) >=  "' + str ( datetime.date.today().year ) + '" '  )

for i in range ( 1, 5 ) :	
	
	br.open("http://www.se-hwa.hs.kr/mbs/kr/jsp/academic_calender/academic_calender.jsp?academicIdx=564922&bungi=" + str(i) + "&year=" + str ( datetime.date.today().year ) + "&id=kr_040101000000" );
	
	soup = BeautifulSoup( br.response().read() )

	datefrom = []
	dateto = []
	content = []
	
	cols = soup.findAll( 'th' )
		
	for col in cols:				
		if col.string <> None  :
			if bool( re.match( ".*~.*", col.string.strip().replace(' ', '').replace('\n', '' ).replace('\t','') ) ) :				
				d1, d2 = col.string.strip().replace(' ', '').replace('\n', '').replace('\t','').split('~')
				datefrom.append (  d1 )
				dateto.append ( d2 )
		
	cols = soup.findAll( 'td' , attrs={ 'class' : 'last'} )
	
	for col in cols:
		#print col.string.strip() 
		content.append ( col.string.strip()  )
		
	for i in range ( 0, len( datefrom)  ) :
		print ( datefrom[i] + "~" + dateto[i] + " " + content[i] )
		
		dm, dd = datefrom[i].split(".")		
		fd = datetime.date(datetime.date.today().year, int(dm), int(dd) )
		dm, dd = dateto[i].split(".")		
		td = datetime.date(datetime.date.today().year, int(dm), int(dd) )
		
		if ( fd < basedate ) :
			fd = fd.replace( year = datetime.date.today().year + 1 )
			td = td.replace( year = datetime.date.today().year + 1 )
		
		while fd <= td :
			if fd.weekday() < 5 : # 5 : Saturday			
				#print ( u'insert into tbAcademicCalendar values ( "'+ str( fd.year) + '/' + str( fd.month) + '/' + str( fd.day) + '", ' + str(school_id) + ', "' + content[i] + '" , "00","" ) '  )
				cur.execute( u'insert into tbAcademicCalendar values ( "'+ str( fd.year) + '/' + str( fd.month) + '/' + str( fd.day) + '", ' + str(school_id) + ', "' + content[i] + '" , "00","" ) '  )
			fd = fd + tdelta
				
conn.commit()
			
cur.close()
conn.close()