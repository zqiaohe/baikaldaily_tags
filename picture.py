from selenium import webdriver
from bs4 import BeautifulSoup
import pandas as pd
import sys
import requests
import os
import shutil
url = "https://www.lampatron.ru/media/design-lamps/design-lamps-fire-b467.jpg"
response = requests.get(url, stream=True)
with open('pic.jpg', 'wb') as f:
	f.write(response.content)
del response
