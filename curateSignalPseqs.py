import sys, csv, re, os

intro = '''\nThis script will 
Arguments:
		1: Filename
		2: \n'''

print intro

dir = sys.argv[1]

with open(guidefile, 'rb') as f:
    reader = csv.reader(f)
    guide = list(reader)
f.close()