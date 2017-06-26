#-*- coding: utf-8 -*-
import telepot
import time
import sys
from bs4 import BeautifulSoup

from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By

reload(sys)
sys.setdefaultencoding('utf-8')

YOUR_ACCESS_TOKEN = ""

bot = telepot.Bot(YOUR_ACCESS_TOKEN)

#print bot.getMe()["username"]
#print bot.getMe()["first_name"]

while True :

	browser = webdriver.Firefox()
	#browser.implicitly_wait(10)
	#browser.get("https://www.sblib.seoul.kr/MachinePossible.do")
	browser.get("https://www.sblib.seoul.kr/library/menu/10030/contents/40002/contents.do")
	
	try :
		elem =  WebDriverWait(browser, 10).until( EC.presence_of_element_located((By.TAG_NAME,"tbody")) ) 
	finally :
		pass

	soup = BeautifulSoup(browser.page_source, "html.parser")

	#cols  = soup.findAll( 'tr')
	
	print time.strftime('%X %x %Z')
	
	cols_th = soup.find('th', text="길음역예약대출기").parent.findAll('th')
	cols_td = soup.find('th', text="길음역예약대출기").parent.findAll('td')
	
	for i in range(len(cols_th)):
		print cols_th[i].text, cols_td[i].text
		if cols_th[i].text.strip() == "길음역예약대출기" and cols_td[i].text.strip() =="예약가능" :
			bot.sendMessage( 0, u"길음역 예약대출기 예약가능")
			browser.quit()
			sys.exit()
	
	'''	
		for col in cols:
			if col.th.text != "위치" :	
				print col.th.text , col.td.text			
				if col.th.text == "길음역예약대출기" and col.td.text =="예약가능" :
					bot.sendMessage( 0, u"길음역 예약대출기 예약가능")
					browser.quit()
					sys.exit()
	'''
	browser.quit()

	time.sleep (60)
