#!/usr/bin/python

import os

status_file='/tmp/status.up'
status_file_exists=False

try:
    if os.path.exists(status_file):
        print "File exists, everything is ok."
        status_file_exists=True
    else:
        print "File not found, app is bad."

except Exception as e:
    print "Error Occured: %s" % e

if status_file_exists:
    exit(0)
else:
    exit(1)
