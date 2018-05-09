import sys, csv, re, os

intro = '''
This script will .

Arguments:
	1: Filename of alignment input
	2: Filename for output\n'''

print intro

try:
	infile = sys.argv[1]
	#outfile = sys.argv[2]
except:
	print "Can't parse arguments.\n"
	quit()

gapMap = {}

for line in open(infile,"r"):
	if re.search(">",line):
		try:
			gapMap[name] = gaps
		name = re.match(r'([^ |^\t]*).*',line).group(1).strip(">")
		sys.stdout.write(">"+name+"\n")
		gaps = []
		pos = 0
		length = 0
	else:
		for char in line:
			pos += 1
			if char == "-":
				length += 1
			else:
				if length != 0:
					gaps.append([pos-length-1,length])
					print pos - length -1, length
				length = 0

