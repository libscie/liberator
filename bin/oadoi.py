#!/usr/bin/env python3

import os
import re as r
import requests
import time

dirs = [x[0] for x in os.walk('db/doi')]

i = 1

for dir in dirs:
    if i % 500000 == 0:
        time.sleep(50000)
    doi = dir[7:]
    if doi != '' or len(doi) > 7:
        try:
            if not os.path.isfile('%s/oadoi.json' % dir):
                r = requests.get("http://api.oadoi.org/%s?email=info@libscie.org" % doi)
                data = r.json()
                filename = '%s/oadoi.json' % dir
                new_file = open(filename, "w")
                new_file.write(str(data))
                new_file.close()
        except:
            with open("db/tmp-oadoi", "a") as myfile:
                myfile.write("%s" % doi)
        print('Just parsed %d of %d dois through oaDOI' % (i, len(dirs)))
        i += 1
