#!/usr/bin/env python3

import requests
import os, sys
import json
import itertools
import time, math#, progressbar

if len(sys.argv) != 2:
  sys.exit("Please specify\n[1] CrossRef filter (see API docs)\n")

crossref_filter = str(sys.argv[1])

# Initial call
r = requests.get("http://api.crossref.org/works?filter=%s&cursor=*&rows=1000" % crossref_filter)

if r.status_code != 200:
    sys.exit("CrossRef call failed. Please check filter.")

# Parse the data
data = r.json()['message']
items = data['items']
cursor = data['next-cursor']

pages = math.ceil(data['total-results'] / 1000)

row = 1000
closer = 0

#bar = progressbar.ProgressBar()

#for page in bar(range(0,pages)):
for page in range(0,pages):
    for i in range(0, len(items)):
        doi = items[i]['DOI']
        os.makedirs('db/doi/%s' % doi, exist_ok = True)
        filename = 'db/doi/%s/crossref.json' % doi
        new_file = open(filename, "w")
        new_file.write(str(items[i]))
        new_file.close()
    try:
        r = requests.get("http://api.crossref.org/works?filter=%s&cursor=%s&rows=1000" % (crossref_filter, cursor))
        data = r.json()['message']
        items = data['items']
        cursor = data['next-cursor']
    except (ValueError, KeyError):
        print("Timing-out for 5 minutes")
        time.sleep(300)

