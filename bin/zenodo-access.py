#!/usr/bin/env python3

import os
import re as r
import requests
import time

dirs = [x[0] for x in os.walk('db/doi')]

i = 1

for dir in dirs:
    doi = dir[7:]
    if doi != '' or len(doi) > 7:
        try:
            r = requests.get(
    		  'https://zenodo.org/api/records',
    		  params={'q': 'doi:"%s"' % dir})
        # except (ConnectionError, TimeoutError, MaxRetryError):
        #     time.sleep(5000)
            data = r.json()
            if data['hits']['total'] > 0:
            	filename = '%s/zenodo-access.json' % dir
            	new_file = open(filename, "w")
            	new_file.write(str(data))
            	new_file.close()
            elif data['hits']['total'] == 0:
                filename = '%s/zenodo-access.json' % dir
                new_file = open(filename, "w")
                new_file.write('')
                new_file.close()
            elif r.status_code != 200:
                time.sleep(5000)
        except:
            with open("db/tmp-zenodo", "a") as myfile:
                myfile.write("%s" % doi)
    print('Just parsed %d of %d dois through Zenodoo' % (i, len(dirs)))
    i += 1