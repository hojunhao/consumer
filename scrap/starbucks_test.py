# -*- coding: ISO-8859-1 -*-
import requests
import re
from bs4 import BeautifulSoup as BS

url = 'http://www.starbucks.com.sg/stores-cbd.html'

r = requests.get(url)
html = r.text
soup = BS(html)

tbody = soup.find('tbody')
trows = tbody.findAll('tr', valign="top")

rows=[]
for row in trows:
    content = row.findAll('td')
    rows.append(content)

# for r in rows:
#     for c in r:
#         breaks = c.findAll('br')
#         if len(breaks)>0:
#             print len(breaks)
#             [b.replaceWith("\n") for b in breaks]
#         print c

cell= rows[0][1]
print cell.text

def formatCell(cell):
    breaks = cell.findAll('br')
    if len(breaks)>0:
        [b.extract() for b in breaks]
    return cell.getText(separator ="\n", strip=True)
#     output = ""
#     for c in clean:
#         c = c.strip()
#         output = output + " " + c
#     return output.strip()

print formatCell(cell)