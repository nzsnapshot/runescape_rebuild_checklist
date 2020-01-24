import json
import collections
import os
import csv

filename = 'readable_eq_data.json'
with open(filename) as f:
    alldicts = json.load(f)




names = []

for key in alldicts.items():
    names.append(key[1]['name'])

for name in names:
    print(name)





