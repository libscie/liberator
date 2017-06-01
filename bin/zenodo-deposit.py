import requests

headers = {"Content-Type": "application/json"}
r = requests.post('https://zenodo.org/api/deposit/depositions',
                  params={'access_token': ZENODO_KEY}, json={},
                  headers=headers)
# Get the deposition id from the previous response
deposition_id = r.json()['id']
# Upload file
data = {'filename': 'fulltext.pdf'}
files = {'file': open('/path/to/myfirstfile.csv', 'rb')}
r = requests.post('https://zenodo.org/api/deposit/depositions/%s/files' % deposition_id,
                  params={'access_token': ZENODO_KEY}, data=data,
                  files=files)
# Add metadata
data = {
    'metadata': {
        'title': 'My first upload',
        'upload_type': 'poster',
        'description': 'This is my first upload',
        'creators': [{'name': 'Doe, John',
                      'affiliation': 'Zenodo'}]
    }
}
r = requests.put('https://zenodo.org/api/deposit/depositions/%s' % deposition_id,
                 params={'access_token': ZENODO_KEY}, data=json.dumps(data),
                 headers=headers)
# Deposit
r = requests.post('https://zenodo.org/api/deposit/depositions/%s/actions/publish' % deposition_id,
    params={'access_token': ZENODO_KEY} )
r.status_code