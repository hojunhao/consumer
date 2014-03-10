# -*- coding: utf-8 -*-
import re
import requests

# ==== data for testing ====
address = "25 Serangoon North Ave 5 #06-00 Keppel Digihub  S554914"
address2 = "25 Serangoon North Ave 5"
address3 = "114 Bukit Merah View #01-578  S150114"

address_testlist = ["25 Serangoon North Ave 5 #06-00 Keppel Digihub  S554914",
                    "1A Thomson Ridge  S574633",
                    "221 Boon Lay Place #02-138 Boon Lay Shopping Centre  S640221",
                    "419 Sembawang Road  S758390",
                    "1018 East Coast Parkway #02-02 Leisure Court  S449877",
                    "9A Trengganu Street  S058463",
                    "Blk 210 Lorong 8 Toa Payoh #01-231 Lorong 8 Toa Payoh Market and Food Centre  S310210",
                    "Blk 226H Ang Mo Kio Street 22 #01-08 Kebun Baru Food Centre  S568226",
                    "Blk 226H Ang Mo Kio Street 22 #01-10 Kebun Baru Food Centre  S568226",
                    "AT Ubi Road 3  S408858"]


#=== actual functions ===
def rmUnitandPostal(address):
    #change Ave to Avenue - for onemap search to work
    address = address.replace("Ave", "Avenue")
    
    regexRmUnitandPostal= re.compile(r'(.*?)(#|S[0-9]{5,6})')
    match = regexRmUnitandPostal.search(address)
    if match:
        return match.group(1)
    else:
        return address

def getSearchResult(searchaddress):
    params = {'token': "qo/s2TnSUmfLz+32CvLC4RMVkzEFYjxqyti1KhByvEacEdMWBpCuSSQ+IFRT84QjGPBCuz/cBom8PfSm3GjEsGc8PkdEEOEr",
          'searchVal' : "",
          'returnGeom': 1}
    params['searchVal'] = str(searchaddress)
    url = "http://www.onemap.sg/API/services.svc/basicSearch"
    r = requests.get(url, params=params)
    return r.json()

def getXYCoordFromAddress(address):
    formatted_address = rmUnitandPostal(address)
    results = getSearchResult(formatted_address)

    if "ErrorMessage" in results["SearchResults"][0]:
        address_split = formatted_address.split()
        if (len(address_split)==3):
            return 0 , 0
        else:
            new_address = " ".join(address_split[1:])
            return getXYCoordFromAddress(new_address)
    else:
        x = results["SearchResults"][1]["X"]
        y = results["SearchResults"][1]["Y"]
        return x, y
    


# ==== test list ====
for a in address_testlist:
    print getXYCoordFromAddress(a)
    
print "\n"
print getSearchResult("226H Ang Mo Kio Street 22")



