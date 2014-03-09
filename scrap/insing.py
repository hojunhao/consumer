import requests
import re
from bs4 import BeautifulSoup as BS
import csv
import time
import os

datadir= os.path.dirname(os.getcwd())+"\data"


url = "http://search.insing.com/categories"
def getMainCategories(url):
    # Get all main categories from start url - Return a list of main categories
    r = requests.get(url)
    html = r.text
    soup = BS(html)

    categories = soup.find('div', class_="business-category-list")
    header2 = soup.findAll('h2')

    maincategories =[]
    for h in header2:
        link = h.find('a')
        if link:
            maincategories.append(link['href'])
    return maincategories

        

def getSubCategories(url):
    # Get all subcategories for each main categories
    r = requests.get(url)
    html = r.text
    soup = BS(html)
    subcat = soup.find('div', class_="subcat-single clearfix")
    li_items = subcat.findAll('a')
    
    subcategories = []
    for l in li_items:
        subcategories.append(l['href'])
    return subcategories

def moreCategories(url):
    check = re.search(r'subcat', url)
    if check:
        return True
    else:
        return False

def changeSubCatToListing(url):
    match = re.search(r'subcat/(.*)', url)
    front = "http://search.insing.com/ts/"
    return front+ match.group(1)


def getBizListingHTML(url, pagecount):
    # Get the biz listing HTML in each page, input url = subcat url
    result_url = url + "?page=" + str(pagecount)
    r = requests.get(result_url)
    html = r.text
    return html
    

def getBizListingfromHTML(html):
    # Get biz listing from HTML, return a list of name, address, postal code
    # need to specific html parser as lxml returned broken results
    soup = BS(html, "html.parser")
    resultlist = soup.findAll('li', title=re.compile(r"Click here"))
    output = []
    for result in resultlist:
        row=[]
        
        # contiune to next iteration if the shop is closed
        closed = result.find('h4')
        if closed:
            continue
        
        BizName = result.find('h3')
        BizName = BizName.text.strip()
        splits = BizName.split()
        BizNameFormatted =" ".join(splits)
        row.append(BizNameFormatted.encode("ascii", "ignore"))
        
        Address = result.find('p', class_="address")
        AddressFormatted = re.search(r'>(.*?)<', str(Address).replace('<br/>', " "))
        if not AddressFormatted: AddressFormatted ="NA"
        else: AddressFormatted = AddressFormatted.group(1)
        row.append(AddressFormatted)
        
        postal =  re.search(r'S([0-9]{6})', AddressFormatted)
        if not postal: postal ="NA"
        else: postal = postal.group(1)
        row.append(postal)
        output.append(row)
        
    return output
    
    
def checkResultHTML(html):
    # check if there results on the page, return True/False
    result_present = re.search(r'div class\="results"', html, re.DOTALL)
    if not result_present: return False
    else: return True

def addCat(bizlist, maincat, subcat):
    # add main and subcat each element in list
    for l in bizlist:
        l.append(maincat)
        l.append(subcat)
    return bizlist

def appendCSV(inputlist, fname):
    #append the CSV file
    with open(fname, "ab+") as f:
        writer = csv.writer(f, quoting=csv.QUOTE_MINIMAL, delimiter=",")
        writer.writerows(inputlist)

def getAllSubCat(maincat):
    output = []
    for cat in maincat:
        SubcatWithinMaincat = getSubCategories(cat)
        for subcat in SubcatWithinMaincat:
            output.append(subcat)
    return output
    
def getCatName(url):
    searchResult = re.search(r'http.*/(.*)', url)
    return searchResult.group(1)
        

#======== Main ===============
allmaincat =  getMainCategories(url)
# allmaincat = ["http://search.insing.com/categories/subcat/food-drink"]
csvfilepath = datadir+'\insing.csv'

for m in allmaincat:
    MainCatName = getCatName(m)
    Subcategories = getSubCategories(m)
    
    for sub in Subcategories:
        if moreCategories(sub):
            sub=changeSubCatToListing(sub)
        SubCatName = getCatName(sub)
        pagecount =1
        startime=time.time()
        while True:
            html = getBizListingHTML(sub, pagecount)
            if not checkResultHTML(html):
                break
            resultlist = getBizListingfromHTML(html)
            resultlist = addCat(resultlist, MainCatName, SubCatName)
            appendCSV(resultlist, csvfilepath)
            pagecount +=1
        endtime=time.time()
        print "Completed: " + MainCatName + "\t\t" + SubCatName + "\nTime taken: " + "{0:.3f}".format(endtime-startime) +'\n'
                





