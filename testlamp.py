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
	print(url)
	elems = wd.find_elements_by_xpath("//a[@href]")
	for elem in elems:
		if elem.get_attribute("href") in Visited or elem.get_attribute("href")[:25] !='https://www.lampatron.ru/':
			continue
		else:
			Visited.append(elem.get_attribute("href"))
	print(Visited)
	return Visited

url = "https://www.lampatron.ru/cat/bytype/design-lamps/"
print(visited(url))