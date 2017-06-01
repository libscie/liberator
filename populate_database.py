#!/usr/bin/env python
import os, sys
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "liberator.settings")
import django
django.setup()
import argparse
import json
from django.db.utils import IntegrityError
from doi.models import *

def parse_arguments():
    '''Parse command line arguments and return argparse object'''
    parser = argparse.ArgumentParser(description='Populate the database')
    parser.add_argument('-d', '--datadir', metavar='<path to data directory>', required=True)
    return parser.parse_args()

def add_article(dir, doi_prefix, doi_suffix):
    '''Adds the given article to the database'''

    print('Processing {}/{}...'.format(doi_prefix, doi_suffix))
    path = os.path.join(dir, doi_prefix, doi_suffix)
    if not os.path.isdir(path):
        raise IOError('Article directory {} does not exist'.format(path))

    # Simple data structure for NoSQL data
    nosql = {
        'crossref': {
            'filename': os.path.join(path, 'crossref.json'),
            'data': {},
        },
        'oadoi': {
            'filename': os.path.join(path, 'oadoi.json'),
            'data': {},
        },
        'zenodo': {
            'filename': os.path.join(path, 'zenodo-access.json'),
            'data': {},
        },
    }

    # Parse .json files and update the data structure
    for source in nosql:
        filename = nosql[source]['filename']
        if os.path.isfile(filename):
            with open(filename,'r') as f:

                # Note that the .json file's content is evaluated as Python code!
                try:
                    nosql[source]['data'] = eval(f.read())
                except SyntaxError:
                    pass

    # Create and save the Article object
    try:
        Article(
            doi_prefix = doi_prefix,
            doi_suffix = doi_suffix,
            crossref = nosql['crossref']['data'],
            oadoi = nosql['oadoi']['data'],
            zenodo = nosql['zenodo']['data'],
        ).save()
    except IntegrityError:
        print('WARNING: Article {}/{} is already in the database'.format(doi_prefix, doi_suffix), file=sys.stderr)

if __name__ == "__main__":
    args = parse_arguments()
    dir = args.datadir

    # Traverse the data directory two levels deep
    for prefix in os.listdir(dir):
        curdir = os.path.join(dir, prefix)
        if os.path.isdir(curdir):
            for suffix in os.listdir(curdir):
                curdir = os.path.join(dir, prefix, suffix)
                if os.path.isdir(curdir):
                    add_article(dir, prefix, suffix)
        else:
            print('WARNING: Ignoring file {}'.format(prefix), file=sys.stderr)
