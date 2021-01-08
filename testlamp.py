from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import sys
import requests
import os
from PIL import Image

# путь к драйверу chrome
chrome_options = webdriver.ChromeOptions()
#chrome_options.add_argument('--headless')
chrome_options.add_argument('--no-sandbox')
chrome_options.add_argument('--disable-dev-shm-usage')
wd = webdriver.Chrome('C:\Program Files (x86)\chromedriver_win32\chromedriver', options=chrome_options)
Visited = []


def visited(url):
	
	wd.get(url)
	elems = wd.find_elements_by_xpath("//a[@href]")
	for elem in elems:
		if elem.get_attribute("href") in Visited or elem.get_attribute("href")[:25] !='https://www.lampatron.ru/':
			continue
		else:
			Visited.append(elem.get_attribute("href"))



#url = "https://www.lampatron.ru/cat/bytype/design-lamps/"
directory = os.getcwd()
files_in_directory = os.listdir(directory)
if 'content' in files_in_directory:
	#print(files_in_directory)
	directory = directory + "\content\\"
else:
	os.mkdir('content')
	directory = directory + "\content\\"
	os.mkdir(directory+"\empty")
#print(directory)
#urls = ["spider", "dekorativnielampi"]
urls = ["design-lamps", "dekorativnielampi", "magnetrack", "lampholders", "constructor", "lampyedisona", "lededison", "xxl", "spider"] 
HeadURL = "https://www.lampatron.ru/cat/bytype/"
for url in urls:
	ref = HeadURL + url
	visited(ref)
print(len(Visited))
#Visited = ['https://www.lampatron.ru/cat/item/sborka001/', 'https://www.lampatron.ru/cat/item/design-lamps-kemma/', 'https://www.lampatron.ru/cat/item/design-lamps-rissa-b/']
with open("output.csv", 'w', encoding='utf-8') as f:
	sys.stdout = f
	for ref in Visited:
		site = "https://www.lampatron.ru"
		wd.get(ref)
		requiredHtml = wd.page_source
		soup = BeautifulSoup(requiredHtml, 'html5lib')
		name = soup.find_all(itemprop="name")
		imgs = soup.find_all(class_ = "prod-pix1")

		try:
			lamp = name[0].text
		except:
			continue

		price = soup.find_all(itemprop="price")
			
		options = soup.find_all("option")
		try:
		
			lampdir = name[0].text
			#print(lampdir)
			#print(os.listdir(directory))
			if lampdir in os.listdir(directory):
				#print(os.listdir(directory))
				lampdir = directory + lampdir + "\\"
			else:
				os.mkdir(directory + lampdir + "\\")
				lampdir = directory + lampdir + "\\"
			#print(lampdir)


			myimages = []
			for img in imgs:
				if 'data-lazy' in img.attrs:
					myimages.append(img.attrs['data-lazy'])
			newimgdir = []
			for img in myimages:
				imgurl = site + img
				#print(imgurl)
				wd.get(imgurl)

				image = Image.open(requests.get(imgurl, stream = True).raw)
				#print(lampdir + list(img.split('/'))[-1] + '.jpg')
				image.save(lampdir + list(img.split('/'))[-1] )
				newimgdir.append(lampdir + list(img.split('/'))[-1])
				#image.save(list(img.split('/'))[-1] )
			#print(myimages)
			
			if len(options) != 0:
				for opt in options:
					print(ref, name[0].text, opt.text, str(int(opt.attrs['data-price'].replace(u'\xa0', u''))), str(int(opt.attrs['data-price'].replace(u'\xa0', u''))/2), newimgdir , sep = ';')
			else:
				if len(price) != 0:
					#print(price[0].content)
					#str(int(price[0].text.replace(u'\xa0', u'')))
					#print(name[0].text)
					#print(newimgdir)
					#print(str(int(price[0].text.replace(u'\xa0', u''))))
					print(ref, name[0].text, "1 вариант", str(int(price[0].text.replace(u'\xa0', u''))), str(int(price[0].text.replace(u'\xa0', u''))/2), newimgdir , sep = ';')
				else:
					continue
		except:
			print(ref,0,0,0,0,0)

#sys.stdout = stdout_fileno