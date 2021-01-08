from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import sys
import requests
import os

# путь к драйверу chrome
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome('C:\Program Files (x86)\chromedriver_win32\chromedriver', options=chrome_options)

def visited(url):
	Visited = []
	wd.get(url)
	elems = wd.find_elements_by_xpath("//a[@href]")
	for elem in elems:
		if elem.get_attribute("href") in Visited or elem.get_attribute("href")[:25] !='https://www.lampatron.ru/':
			continue
		else:
			Visited.append(elem.get_attribute("href"))
	return Visited

urls = ["design-lamps", "dekorativnielampi", "magnetrack", "lampholders", "constructor", "lampyedisona", "lededison", "xxl", "spider"] 
HeadURL = "https://www.lampatron.ru/cat/bytype/"
Refs = []
for url in urls:
	ref = HeadURL + url
	Refs.append(visited(ref))
os.mkdir('content')
stdout_fileno = sys.stdout
i = 0
for refs in Refs:
	i+=1
	with open(urls[i] + ".csv", 'w', encoding='utf-8') as f:
		sys.stdout = f
		for ref in refs:
			url = ref
			wd.get(url)
			requiredHtml = wd.page_source
			soup = BeautifulSoup(requiredHtml, 'html5lib')
			name = soup.find_all(itemprop="name")
			imgs = soup.find_all(class_ = "prod-pix1")
			images = []
			try:
				os.mkdir('content/' + name[0].text)
				option = soup.find_all("option")
				
			except:
				continue
			
			for img in imgs:
					try:
						imgurl = site+img.attrs['data-lazy']
						filename= img.attrs['data-lazy'].split('/')[-1]
						images.append(imgurl)
						response = requests.get(imgurl, stream=True)
						with open('content/'+name[0].text+'/'+filename+'.jpg', 'wb') as f:
							f.write(response.content)
						del response
					except:
						continue
			for opt in option:
				print(url, name[0].text, opt.text, opt.attrs['data-price'], str(int(opt.attrs['data-price'].replace(u'\xa0', u''))/2), images, "/content/"+name[0].text, sep=';')

wd.close()
wd.quit()
