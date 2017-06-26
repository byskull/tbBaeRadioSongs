#-*- coding: utf-8 -*-

import re
import mechanize
import urllib2
import cookielib
from bs4 import BeautifulSoup
import pymysql

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

conn = pymysql.connect(host='127.0.0.1', port=3307, user='root', passwd='0000', db='mysql', charset='utf8')
cur = conn.cursor()

cj = cookielib.CookieJar()
br = mechanize.Browser()
br.set_cookiejar(cj)
br.open("http://mini.imbc.com/manager/SelectList.asp?PROG_CD=RAMFM300");

for i in range(10) :
	br.open("http://mini.imbc.com/manager/SelectList.asp?PG="+str(i+1)+"&WH=&PROG_CD=RAMFM300&txtstart=&txtend=&searchType=&reSearch=&criteria=&Key=");
	
	soup = BeautifulSoup( br.response().read() , "html5lib" )

	cols = soup.findAll( 'a', attrs={ 'href' : re.compile("SeqNo*")} )

	for col in cols :				
		br.open("http://mini.imbc.com/manager/" + col.attrs[u'href']);

		soup = BeautifulSoup( br.response().read() , "html5lib" )
		
		artists = []
		songs = []

		ns = soup.findAll('caption')
		
		for ars in ns :			
			#print ars.string.decode('utf-8')	
			year, month, day = re.findall( "\d+", ars.string) [0:3]		
			
		cur.execute( "delete from tbBaeRadioSongs where RefDate = '" + year + "/" + month + "/" + day + "' "	)
		
		ns = soup.findAll('td', attrs={"class" : "td_artist" })
		for ars in ns :					
			artists.append ( ars.string.strip().replace('"','') )	
			
		ns = soup.findAll('p')
		
		for ars in ns :			
			if ( ars.string != None ) :
				songs.append( ars.string.strip() )	

		for i in range( len( artists ) ) :
			#print "[" + artists[i].encode('utf-8').decode('utf-8') + "] " + songs[i].decode('utf-8').encode('utf-8') + '\n'						
			cur.execute( u'insert into tbBaeRadioSongs values ( "'+ year + '/' + month + '/' + day + '", ' + unicode( str(i) ) + ', "' + artists[i][0:100] + '" , "' + songs[i][0:255].replace('"', '\\"' ) + '" ) '  )
		
	conn.commit()
				
cur.close()
conn.close()