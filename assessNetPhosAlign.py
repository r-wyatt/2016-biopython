import os, re, sys

intro = '''
This script will analyze the gap map transformed
NetPhos output to produce a table of phosphorylated
residues, their position and percent conservation.

Arguments:
	1 Filename of netPhos output file
	2: Filename for output\n'''

print intro

try:
	infile = sys.argv[1]
	netPhos = sys.argv[2]
	outfile = sys.argv[3]
except:
	print "Can't parse arguments.\n"
	quit()

conservedSites = {}

for line in open(infile,"r"):
	if re.search(">",line):
		name = re.match(r'([^ |^\t]*).*',line).group(1).strip(">").strip("\n")
		if len(name)>20:
			name = name[:20]
		gapDict[name]={}
		seqLength = 0
		gapsize = 0
		gap = False
		gapCumulative = 0
	else:
		for i in range(0,len(line)):
			if line[i] == " ":
				continue
			seqLength += 1 # Position in sequence
			if line[i] == "-" and gap == False: # Gap open
				gap = True
				pos = seqLength-1-gapCumulative
				gapsize += 1
				gapCumulative += 1

			elif line[i] == "-" and gap == True:
				gapsize += 1
				gapCumulative += 1

			elif line[i] != "-" and gap == True: # Gap close
				gap = False
				gapDict[name][pos]=gapsize
				#print "Gap at: ",pos," of length ",gapsize
				gapsize = 0