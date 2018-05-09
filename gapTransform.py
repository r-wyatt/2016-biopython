import sys, csv, re, os

intro = '''
This script will .

Arguments:
	1: Alignment input
	2: netPhos input (same sequences present as alignment)
	3: Filename for output\n'''

print intro

try:
	alnfile = sys.argv[1]
	phosfile = sys.argv[2]
	#outfile = sys.argv[3]
except:
	print "Can't parse arguments.\n"
	quit()

gapMap = {}

for line in open(alnfile,"r"):
	if re.search(">",line):
		try:
			gapMap[name] = gaps
		except:
		name = re.match(r'>([0-9]*).*',line).group(1)
		print name
		#sys.stdout.write(">"+name+"\n")
		gaps = []
		pos = 0
		length = 0
		offset = 0
		gapMap[name] = []
	else:
		for char in line:
			pos += 1
			if char == "-":
				length += 1
			else:
				if length != 0:
					gaps.append([pos-(length+1+offset),length])
					#print gaps[-1]
					offset += length
				length = 0

print gapMap
test = []

for line in open(phosfile,"r"):
	if re.search(">", line):
		name = re.match(r'>([0-9]*).*',line).group(1)
		if name in gapMap:
			currentMap = gapMap[name]
		else:
			print name, "not found in alignemnt"
	if re.search("# "+name,line):
		pos = re.match(r'')
		print line
print test






