#!/usr/bin/env python3

import requests
import os, sys
import json
import itertools
import time

if len(sys.argv) != 3:
  sys.exit("Please specify\n[1] CrossRef filter (see API docs)\n[2] output dir")

crossref_filter = str(sys.argv[1])
out_dir = sys.argv[2]

# Initial call
r = requests.get("http://api.crossref.org/works?filter=%s&cursor=*&rows=1000" % crossref_filter)

if r.status_code != 200:
    sys.exit("CrossRef call failed. Please check filter.")

# Parse the data
data = r.json()['message']
items = data['items']
cursor = data['next-cursor']

print(data['total-results'])

closer = 0

while closer < 2:
    for i in range(0, len(items)):
        doi = items[i]['DOI']
        os.makedirs('%s/%s' % (out_dir, doi), exist_ok = True)
        filename = '%s/%s/crossref.json' % (out_dir, doi)
        new_file = open(filename, "w")
        new_file.write(str(items[i]))
        new_file.close()

    time.sleep(5)
    r = requests.get("http://api.crossref.org/works?filter=%s&cursor=%s&rows=1000" % (crossref_filter, cursor))
    data = r.json()['message']
    items = data['items']
    cursor = data['next-cursor']
    """
    This one ensures that while loop stops after the first page
    with less items than rows (the first still contains hits!)
    """
    if len(items) != 1000:
        closer += 1


