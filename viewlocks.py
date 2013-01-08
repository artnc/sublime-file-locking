#!/usr/bin/env python

# This script recursively scans its containing directory for .sublimelock files and
# prints information about each lock file.
#
# The first optional command-line argument specifies which locks to show.
# Only lock display entries containing the argument will be shown.
# Default is all.
#
# An optional second argument, "-r" will delete those locks.
#
# Example: python viewlocks.py art -r
#          This will remove all locks set by art and also all
#          locks whose filepaths contain "art"

import os, sys, time
from collections import defaultdict

maxname = 15 # Maximum username length in characters

arg1 = sys.argv[1] if len(sys.argv) > 1 else "" # Which locks to show
arg2 = sys.argv[2] if len(sys.argv) > 2 else "" # Remove locks if "-r"
d = defaultdict(list)
sep = "-" * 75
print(sep + "\nLocked\t\tAge\tUser" + " " * (maxname - 4) + "File\n" + sep)
startdir = os.path.dirname(os.path.realpath(__file__))
removed = 0
for root, dirs, files in os.walk(startdir):
  for fname in files:
    fpath = os.path.join(root, fname)
    if os.path.splitext(fpath)[1] == ".sublimelock":
      try:
        f = open(fpath, 'rU')
      except IOError:
        print("Error opening " + fpath)
      else:
        with f:
          lockinfo = f.read().splitlines()
          locker = lockinfo[0]
          locktime = int(os.path.getmtime(fpath))
          minutesago = (int(time.time()) - locktime) // 60
          fuzzymsg = (str(minutesago) + " min" if minutesago < 60 else str(minutesago // 60) + " hrs")
          rowmessage = time.strftime("%b %d, %H:%M", time.localtime(locktime)) + "\t" + fuzzymsg + "\t" + locker + " " * (maxname - len(locker)) + fpath.split(startdir)[1][1:-12]
          if arg1 in rowmessage:
            d[locktime].append(rowmessage)
            if arg2 == "-r":
              os.remove(fpath)
              removed += 1
if len(d):
  for key in sorted(d.iterkeys()):
    for entry in d[key]:
      print(entry)
else:
  print("No locks found.")
if arg2 == "-r":
  print(sep + "\nRemoved " + str(removed) + " locks.")
