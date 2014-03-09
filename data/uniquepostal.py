import csv
import json
import requests

filename = 'insing.csv'

set_postal = set()
with open(filename, "rb") as f:
    reader = csv.reader(f)
    for row in reader:
        set_postal.add(row[2])

sorted_postal = sorted(set_postal)

def getSVY21coord(postal):
    url = "http://www.onemap.sg/API/services.svc/basicSearch?token=qo/s2TnSUmfLz+32CvLC4RMVkzEFYjxqyti1KhByvEacEdMWBpCuSSQ+IFRT84QjGPBCuz/cBom8PfSm3GjEsGc8PkdEEOEr&searchVal="+str(postal)+"&returnGeom=1"
    r = requests.get(url)
    data = r.text
    results = json.loads(data)
    if "ErrorMessage" in results["SearchResults"][0]:
        return "NA", "NA"
    else:
        x = results["SearchResults"][1]["X"]
        y = results["SearchResults"][1]["Y"]
        return x, y

counter = 0
with open("list_of_postal.csv", 'ab') as w:
    for item in sorted_postal:
        print counter
        print item
        x, y = getSVY21coord(item)
        print x, y
        w.write(item + ',' + x + ',' + y +','+ '\n')
        counter+=1
           
