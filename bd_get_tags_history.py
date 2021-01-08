from selenium import webdriver
import time
from bs4 import BeautifulSoup
import sys
#import pandas as pd
#from tabulate import tabulate
from datetime import date, time, datetime
from tabulate import tabulate

chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
chrome_options.add_experimental_option( "prefs",{'profile.managed_default_content_settings.javascript': 2,'profile.managed_default_content_settings.images':2})
# chrome_options.add_experimental_option("excludeSwitches", ['enable-logging'])
chrome_options.add_argument('--log-level=3')

wd = webdriver.Chrome('C:\Program Files (x86)\chromedriver_win32\chromedriver',options=chrome_options)

#d = {'datetime': [], 'headline': [], 'tags': [], 'section':[]}
#df = pd.DataFrame(data=d)

stdout_fileno = sys.stdout
with open("output.csv", 'w', encoding='utf-8') as f:
	sys.stdout = f

	for i in range(403200, 403309):
		url = 'https://www.baikal-daily.ru/news/19/'+str(i)


		try:	
			wd.get(url)
			requiredHtml = wd.page_source

			soup = BeautifulSoup(requiredHtml, 'html5lib')
		
			pub_time = soup.find_all(itemprop="datePublished")
			
			if len(pub_time) == 0:
				continue;

			headline = soup.find_all(itemprop="headline")
			tags = soup.find_all(class_="news-tags")
			tags = tags[0].text.strip().split('\n')
			section = soup.find_all(class_="news-section")
			for tag in tags:
				#row = [time[0].text, headline[0].text, tag, section[0].text]
				#print(time[0].text, headline[0].text, tag, section[0].text)
				#df.loc[len(df)] = row
				pub_date = datetime.strptime(pub_time[0].text,"%d.%m.%Y %H:%M").date()
				pub_tm = datetime.strptime(pub_time[0].text,"%d.%m.%Y %H:%M").time()
				#print(pub_tm)
				print(str(i)+';'+str(pub_date) + ';' + str(pub_tm) + ';' + headline[0].text.strip() + ';' + tag.strip() + ';' + section[0].text.replace(',', ''))
		except:
			print(str(i)+';None; None; None; None; None')

wd.close()
wd.quit()

sys.stdout = stdout_fileno

with open("output2.txt", 'w', encoding='utf-8') as f2:
	sys.stdout = f2

sys.stdout = stdout_fileno
