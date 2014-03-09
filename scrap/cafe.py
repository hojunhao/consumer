# -*- coding: utf-8 -*-
import requests
import re
from bs4 import BeautifulSoup as BS
import csv
import os

#where to save csv
datadir= os.path.dirname(os.getcwd())+"\data"

url = 'http://joeyasher.com/2014/01/03/cafes-in-singapore-sorted-by-location/'

r = requests.get(url)
html = r.text
soup = BS(html)


# blog content
content = soup.find('div', class_="entry clear-block")
# list of cafe resides with divs without any classes
content_filtered = content.findAll('div', class_=False)

cafelist=[]
for c in content_filtered:
    list = c.findAll('li')
    for l in list:
        cafelist.append(l.text)

info=[]
for i in cafelist:
    result=re.search(r'^(.*?)@.*? (.*)', i)
    info.append([result.group(1), result.group(2)])

csvfilepath = datadir+'\cafe.csv'
with open(csvfilepath, 'wb') as f:
    for i in info:
        line = i[0].encode('ascii', 'ignore')+',"'+i[1].encode('ascii', 'ignore')+'"\n'
        f.write(line)
        
print "Completed"