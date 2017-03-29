#!/usr/bin/env python3

import requests
import os, sys
import json
import itertools
import time

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

print(data['total-results'])

closer = 0

while closer < 2:
    for i in range(0, len(items)):
        doi = items[i]['DOI']
        os.makedirs('db/doi/%s' % doi, exist_ok = True)
        filename = 'db/doi/%s/crossref.json' % doi
        new_file = open(filename, "w")
        new_file.write(str(items[i]))
        new_file.close()

    time.sleep(5)
    try:
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
    except (ValueError, KeyError):
        print("Timing-out for 5 minutes")
        time.sleep(300)


