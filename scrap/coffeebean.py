# -*- coding: ISO-8859-1 -*-
import requests
import re
from bs4 import BeautifulSoup as BS
import csv
import os

#where to save csv
datadir= os.path.dirname(os.getcwd())+"\data"

url = 'http://www.coffeebean.com.sg/coffeebean/store.cfm'

def getRows(url):
    r = requests.get(url)
    html = r.text
    soup = BS(html)
    rows=[]
    table = soup.findAll('div', class_="tabset_content")
    for t in table:
        trows = t.findAll('tr')
        for d in trows:
            td = d.findAll('td', class_=True)
            rows.append(td)
    return rows
    
def getPostal(str):
    result = re.search(r'Singapore.*?([0-9]{6})', str, re.DOTALL)
    if result:
        return result.group(1)
    else:
        return ""

def formatRows(rows):
    frows=[]
    for r in rows:
        if len(r):
            frow=[]
            for d in r:
                breaks = d.findAll('br')
                if len(breaks)>0:
                    [b.extract() for b in breaks]
                frow.append(d.getText(separator ="\n", strip=True))
            frows.append(frow)
    return frows

rows= getRows(url)
frows= formatRows(rows)

info=[]
for f in frows:
    postal = getPostal(f[0])
    if postal !="":
        f.append(postal)
        info.append(f)
    
csvfilepath = datadir+'\coffeebean.csv'
with open(csvfilepath, 'wb') as f:
    writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL, delimiter=",")
    writer.writerows(info)
