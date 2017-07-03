import os, re, sys

intro = '''\nThis script will strip a file (arg1) of exact duplicate FASTA 
sequences. It will not compare sequences, only remove sequences
with the exact same name. File to write to specified by arg2.\n'''

print intro

stdout_bk = sys.stdout

sys.stdout = open(sys.argv[2],"w+")

with open(sys.argv[1],"r") as f:
	names = []
	dup = False
	for line in f:
		if re.search(r'>',line):
			dup = False
			if line in names:
				dup = True
			names.append(line)
		if dup == False:
			sys.stdout.write(line)
					

f.close()

print "\nDone file\n"
