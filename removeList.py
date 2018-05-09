import os, re, sys

intro = '''
This script will take a file with a blacklist of fasta names,
and remove sequences that are associated to that species, giveb
in the form [Genus species] in the fasta name, from the specified
file of fasta sequences.

Arguments:
		1: Text file of blacklist entries
		2: Fasta file to trim
		3: Name of output file\n'''

print intro

blacklist = sys.argv[1]
fasta = sys.argv[2]
output = sys.argv[3]

species = []
with open(blacklist,"r") as f:
	for line in f:
		mobj = re.match(r'.*\[([A-Z|a-z]* [a-z]*)\].*',line)
		try:
			species.append(mobj.group(1))
		except:
			continue

with open(output,"w+") as h:
	stdout_bk = sys.stdout
	sys.stdout = h
	with open(fasta, "r") as g:
		keep = False
		for line in g:
			if re.search('>',line):
				mobj = re.match(r'.*\[([A-Z|a-z]* [a-z]*)\].*',line)
				try:
					spec = mobj.group(1)
				except:
					continue
				if spec in species:
					keep = False
					continue
				else:
					sys.stdout.write(line.strip("\n"))
					keep = True
			elif keep == True:
				sys.stdout.write(line.strip("\n"))
			else:
				continue
	sys.stdout = stdout_bk





