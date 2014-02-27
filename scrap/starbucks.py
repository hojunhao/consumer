# -*- coding: ISO-8859-1 -*-
import requests
import re
from bs4 import BeautifulSoup as BS
import csv
import os

#starting URL
url = 'http://www.starbucks.com.sg/store-locator.html'
#where to save csv
datadir= os.path.dirname(os.getcwd())+"\data"


def getAreaPage(url):
    r = requests.get(url)
    html = r.text
    soup = BS(html)
    
    content = soup.find('div', id="content")
    links = content.findAll('a', href=True)
    areas =[]
    for l in links:
        l = l['href']
        if not re.match(r'^stores-24h*', l):
            name = re.search(r'-(.*?)\.', l).group(1)
            areas.append((name, l))
    return areas 
#print getAreaPage(links)
#[('cbd', 'stores-cbd.html'), ('east', 'stores-east.html'), ('orchard', 'stores-orchard.html'),  ......

def getPageContent(url):
    r = requests.get(url)
    html = r.text
    soup = BS(html)
    
    tbody = soup.find('tbody')
    trows = tbody.findAll('tr', valign="top")
    
    rows=[]
    for row in trows:
        content = row.findAll('td')
        rows.append(content)
    return rows #output in list of BS tags not formatted



testcell = getPageContent('http://www.starbucks.com.sg/stores-east.html')[0][0]
#print testcell

def formatCell(cell):
    breaks = cell.findAll('br')
    if len(breaks)>0:
        [b.extract() for b in breaks]
    return cell.getText(separator ="\n", strip=True)
# 80, Airport Boulevard Unit No: #01-06 Terminal 1 Arrival hall Central Singapore 819642 Tel: 6546 7696

# address = formatCell(testcell)
# print address

def getPostal(str):
    result = re.search(r'Singapore.*?([0-9]{6})', str)
    if result:
        return result.group(1)
    else:
        return ""
#819642
#print getPostal(formatCell(getPageContent('http://www.starbucks.com.sg/stores-east.html')[0][1]))

#get a list of tuples of pages to scrap in accordance to areas
pages = getAreaPage(url)

info =[]
for p in pages:
    area, link = p
    url = "http://www.starbucks.com.sg/" + link
    content = getPageContent(url)
    for row in content:
        info.append([area, formatCell(row[0]), getPostal(formatCell(row[1])),formatCell(row[1]), formatCell(row[2]), formatCell(row[3]) ])

csvfilepath = datadir+'\starbucks.csv'
with open(csvfilepath, 'wb') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL, delimiter=",")
    writer.writerows(info)