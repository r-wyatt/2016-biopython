import time, sys, csv, re, os
from Bio import Entrez

intro = '''\nThis script will 
Arguments:
		1: Filename
		2: \n'''

print intro
Entrez.email = raw_input("Email: ")

with open(sys.argv[1]) as names:
	reader = csv.reader(names)
	stdout_bk = sys.stdout
	sys.stdout = open("output1","w")
	for name in reader:
		accM = re.match(r'(.*\.[0-9])_.*',name[0])
		acc = accM.group(1)
		handle = Entrez.efetch(db="protein", id=acc, rettype="gb", retmode="text")
		print handle.read()
		time.sleep(3)
	sys.stdout = stdout_bk

print "Done collecting Genbank files"
