#!/usr/bin/python3

import configparser
import getopt
import os
import sys
import uuid

import flickrapi

print('FlickrSync')

if len(sys.argv) == 1:
    print('\nUsage:')
    print('./sync.py <directory-to-upload>')
    print('\nArguments:')
    print('--tags, -t:      "tag1, tag2, multi word tag, tag3"')
    exit()

config = configparser.ConfigParser()
config.read('conf.ini')

API_KEY = config['auth']['key']
API_SECRET = config['auth']['secret']

UPLOAD_DIR = sys.argv[1]
UPLOAD_UUID = str(uuid.uuid1())
UPLOAD_ALBUM = os.path.basename(UPLOAD_DIR)

UPLOAD_TAGS = [
    "FlickrSync",
    UPLOAD_UUID,
    UPLOAD_ALBUM,
]

opts, args = getopt.getopt(sys.argv[2:], "t:", ["tags="])
for o, a in opts:
    if o in ("-t", "--tags"):
        UPLOAD_TAGS += a.split(',')

UPLOAD_TAGS = ["\"" + tag.strip() + "\"" for tag in UPLOAD_TAGS]
UPLOAD_TAGS = ' '.join(UPLOAD_TAGS)

flickr = flickrapi.FlickrAPI(API_KEY, API_SECRET)
flickr.authenticate_console(perms='write')

directory = os.walk(UPLOAD_DIR)
files = []

for r, d, f in directory:
    for name in f:
        files.append(os.path.join(r, name))

counter = 0
total = len(files)

print('UUID: ' + UPLOAD_UUID)

for name in files:
    counter += 1
    print('Uploading %d of %d: %s' % (counter, total, name))
    flickr.upload(
        filename=name,
        tags=UPLOAD_TAGS,
        is_public=0,
        is_family=0
    )

print('\nCompleted.')
