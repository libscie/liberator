#!/usr/bin/env python3

import os
import re as r
import requests

dirs = [x[0] for x in os.walk('db/doi')]

i = 1

for dir in dirs:
    doi = dir[7:]
    if doi != '' or len(doi) > 7:
        r = requests.get("http://api.oadoi.org/%s?email=info@libscie.org" % doi)
        data = r.json()
        filename = '%s/oadoi.json' % dir
        new_file = open(filename, "w")
        new_file.write(str(data))
        new_file.close()
    print('Just parsed %d of %d dois through oaDOI' % (i, len(dirs)))
    i += 1
