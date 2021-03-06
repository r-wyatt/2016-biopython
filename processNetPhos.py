import os, re, sys, string

intro = '''
This script will produce a gap map of an alignment and
apply that map to the output from a NetPhos file to
produce an aligned NetPhos output. This allows easy
visualization of the conservation of predicted phos
sites in a protein family, for example.

Arguments:
	1: Filename of input alignment
	2: Filename of netPhos output file
	3: Filename for alignment output
	4: Filename for site sums\n'''

print intro

try:
	infile = sys.argv[1]
	netPhos = sys.argv[2]
	outfile = sys.argv[3]
	outfile2 = sys.argv[4]
except:
	print "Can't parse arguments.\n"
	quit()

gapDict = {}

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
				gapsize = 0


# account for EOF gap:
if gap == True:
	gapDict[name][pos]=gapsize


netPhosSeq = {}
sequence = False
for line in open(netPhos,"r"):
	if re.search(">", line):
		if sequence: # avoid trying to write before first case
			sequence = string.replace(sequence,' ','')
			netPhosSeq[name] = sequence
		name = re.match(r'([^ |^\t]*).*',line).group(1).strip(">")
		sequence = ""
		if name == '337179_NP_932333.1':
			print "Found danio rerio" # use this to catch the scores
	if name and re.search("%1",line):
		sequence = sequence + line.strip("%1  ")[0:50]

sequence = string.replace(sequence,' ','')
netPhosSeq[name] = sequence # deal with final entry


def makegap(num,string = ""): 
	if num == 0:
		return string
	string = string + "-"
	return makegap(num-1, string)

alignPhos = {}

for key in netPhosSeq.keys():
	if key not in gapDict:
		print "Sequence "+key+" from netPhos doesn't have a gapMap, skip to next hit"
		continue
	map = gapDict[key]
	result = ""
	length = len(netPhosSeq[key])
	for i in range(0,length): # Doesn't include a final gap if there is one		
		if i in map:
			result = result+makegap(map[i])+netPhosSeq[key][i]
		else:
			result = result + netPhosSeq[key][i]
	

	alignPhos[key] = result

stdout_bk = sys.stdout
sys.stdout = open(outfile,"w+")

for name in alignPhos.keys():
	print ">",name
	print alignPhos[name]

sys.stdout = stdout_bk

print "\nFinished writing aligned NetPhos file"

longest = 0
for key in alignPhos.keys():
	if len(alignPhos[key]) > longest:
		longest = len(alignPhos[key])

for key in alignPhos.keys():
	seqLen = len(alignPhos[key])
	if seqLen < longest:
		alignPhos[key] = alignPhos[key] + makegap(longest - seqLen)


# Iterate through length:
phosSites = ['T','Y','S']
print "\nNumber of sequences: ", len(alignPhos),"\n"

stdout_bk = sys.stdout
sys.stdout = open(outfile2,"w+")
print "pos, char, count"
for i in range(0,longest):
	for residue in phosSites:
		count = 0
		for key in alignPhos.keys():
			if alignPhos[key][i] == residue:
				count +=1
		if count > 0:
			print i,", ",residue,", ",count

sys.stdout = stdout_bk

print "Finished site sums, all done!"



