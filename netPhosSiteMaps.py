import os, re, sys

intro = '''
This script will pull 'fasta' maps of phosphorylation
from the NetPhos file specified by the first argument.

Arguments:
	1: Filename of NetPhos output
	2: Output file\n'''

print intro
try:
	netPhos = sys.argv[1]
	stdout_bk = sys.stdout
	sys.stdout = open(sys.argv[2],"w+")
except:
	print "Can't parse arguments.\n"
	quit()


for line in open(netPhos,"r"):
	if re.search(">", line):
		name = re.match(r'([^ |^\t]*).*',line).group(1).strip(">")
		sys.stdout.write(">"+name+"\n")
	if name and re.search("%1",line):
		sys.stdout.write(line.strip("%1  ")[0:50]+"\n")

sys.stdout = stdout_bk
print "Finished file"