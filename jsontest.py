import csv
import json
import requests
import re



params = {'token': "qo/s2TnSUmfLz+32CvLC4RMVkzEFYjxqyti1KhByvEacEdMWBpCuSSQ+IFRT84QjGPBCuz/cBom8PfSm3GjEsGc8PkdEEOEr",
          'searchVal' : 543201,
          'returnGeom': 1}
params['searchVal'] = "548 Woodlands Drive 44"
url = "http://www.onemap.sg/API/services.svc/basicSearch"
r = requests.get(url, params=params)
print r.url

data = r.json()
headers =r.headers
encoding = r.encoding

print data["SearchResults"][1]



