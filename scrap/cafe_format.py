# -*- coding: utf-8 -*-
import re
cafelist=["Jimmy Monkey Cafe @ 9 one-north Gateway #01-51 (one-north residences) | C/D/F/$6-$18/$5",
"MU Parlour @ 16A Lorong Mambong",
"Park Cafe Bar @ 281 Holland Avenue #01-01",
"Park Cafe Bar @ 281 Holland Avenue #01-01",
"Food For Thought Cafe @ 1 Cluny Road #B1-00 (Singapore Botanic Gardens)",
"Relish @ 501 Bukit Timah Road #02-01 (Cluny Court)"]

list=[]
for i in cafelist:
    list.append(i.decode('utf-8', 'ignore'))

print repr(list[3])

result = re.search(r'^(.*?)@.*? (.*)#?', list[3])
print result.group(1), result.group(2)

print list[1]
result = re.search(r'^(.*?)@.*? (.*)#?', list[4])
print result.group(1), result.group(2)