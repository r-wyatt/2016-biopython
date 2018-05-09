import os, re, sys, string

intro = '''
This script will produce a gap map of an alignment and
apply that map to the output from a NetPhos file to
produce an aligned NetPhos output. This allows easy
visualization of the conservation of predicted phos
sites in a protein family, for example.

Example input:
PhosSites_v2.py final_mmp2.aln final_mmp2_netPhos.txt mmp2_NetPhos-align.txt mmp2_netPhos-sites.csv "Danio rerio"

Arguments:
	1: Filename of input alignment
	2: Filename of netPhos output file
	3: Filename for alignment output
	4: Filename for site outputs and scores
	5: Species of interest\n'''
# edit this code to process differently
# want a better way to maintain scores

print intro

try:
	infile = sys.argv[1]
	netPhos = sys.argv[2]
	outfile = sys.argv[3]
	outfile2 = sys.argv[4]
	species = sys.argv[5]
except:
	print "Can't parse arguments.\n"
	quit()

gapDict = {}

for line in open(infile,"r"):
	if re.search(">",line):
		name = re.match(r'([^ |^\t]*).*',line).group(1).strip(">").strip("\n")
		if len(name)>20:
			name = name[:20]
		if re.search(species, line):
			refSeq = name
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

def makegap(num,string = ""): 
	if num == 0:
		return string
	string = string + "-"
	return makegap(num-1, string)

def gaptransform(number, gapMap):
	for i in gapMap.keys():
		number+= gapMap[i]
	return number

sites = []
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
	if re.search("# "+name,line):
		score = line[45:50]
		pos = line[24:28].replace(' ','')
		char = line[29]
		enzyme = line[53:64].replace(' ','')
		addition = [name,pos,char,score,enzyme]
		sites.append(addition)
	if name and re.search("%1",line):
		sequence = sequence + line.strip("%1  ")[0:50]

#print sites[1:10]
stdout_bk = sys.stdout

sequence = string.replace(sequence,' ','')
netPhosSeq[name] = sequence # deal with final entry

alignPhos = {}

for key in netPhosSeq.keys():
	if key not in gapDict:
		print "Sequence "+key+" from NetPhos isn't in alignment, skip to next hit"
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

print "\nNumber of sequences: ", len(alignPhos),"\n"

# Error handling in the case of no reference species:
if not refSeq:
	print "Selected species of interest not found." 
	print "Ensure entry is in alignment file.\n"
	sys.stdout = open(outfile2,"w+")
	for entry in sites:
		print ",".join(entry)
	sys.stdout = stdout_bk
	print "Untransformed NetPhos output written."
	quit()

# Apply gap maps to sequences
for i in range(0,len(sites)):
	sites[i].append(sites[i][1])
	seqName = sites[i][0]
	pos = int(sites[i][1])
	newpos = pos
	for gap in gapDict[seqName].keys():
		if gap < pos:
			newpos += gapDict[seqName][gap]
	sites[i][1] = newpos

# Translate gap-mapped sequences to reference sequence coordinates
outputMap = gapDict[refSeq]
newSites = []

sums = []
print "Number of Sites: ",len(sites),"\n"
for site in sites:
	if refSeq == site[0]:
		align_pos = int(site[1])
		new_pos = align_pos
		curr_char = site[2]
		for gap in outputMap.keys():
			if gap + outputMap[gap] < new_pos:
				new_pos -= outputMap[gap]
		site[1] = new_pos
		site.append(str(align_pos))
		newSites.append(site)
		count = 0
		matches = 0
		references = 0
		for othersite in sites:
			count += 1
			if int(othersite[1]) == align_pos and othersite[2] == site[2]:
				if refSeq in othersite[0]:
					references += 1
					print "woot"
				matches += 1
				#print "found a match"
				othersite[1] = new_pos
				othersite.append(str(align_pos))
				newSites.append(othersite)
		sums.append([new_pos,matches+1])
		#print "Matches: ",matches,"/",count," References = ",blebs,references

for i in range(0, len(newSites)):
	for sum in sums:
		if sum[0] == newSites[i][1]:
			newSites[i].append (str(sum[1]))
			break

for i in range(0,len(newSites)):
	newSites[i][1] = str(newSites[i][1])

sys.stdout = open(outfile2,"w+")
print "name, pos, residue, score, enzyme, orignal_pos, align_pos, sum"
for entry in newSites:
	print ",".join(entry)
sys.stdout = stdout_bk

print "Finished translating locations, all done!"



