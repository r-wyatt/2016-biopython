import sys, csv, re, os

intro = '''
This script will replace names using a guiding csv: Each row consists
of variations for a given record. You can use grabNames.py to create 
an appropriate csv with a selection of name variations from a file of
fasta sequences.

Arguments:
	1: Filename of file to replace names
	2: Filename to save replaced file as
	3: Guide file for names (csv)
	4: Index of new names as int (default is second column)
	5: Index of original names as int (default is first column)\n'''

print intro

try:
	infile = sys.argv[1]
	outfile = sys.argv[2]
	guidefile = sys.argv[3] # This is a file of FASTA headers (all names include '>')
	index = int(sys.argv[4])-1 if len(sys.argv) > 4 else 2
	prior = int(sys.argv[5])-1 if len(sys.argv) > 5 else 1
except:
	print "Can't parse arguments.\n"
	quit()

			
with open(guidefile, 'rb') as f:
    reader = csv.reader(f)
    guide = list(reader)
f.close()
	
stdout_bk = sys.stdout
sys.stdout = open(outfile,"w+")

with open(infile,"r") as f:
	for line in f:
		if not re.search(r'[0-9|A-Z|a-z]*',line):
			continue
		for i in guide:
			if i[prior] in line:
				line = line.replace(i[prior],i[index])
		sys.stdout.write(line)


f.close()

sys.stdout = stdout_bk

print "\nFinished process"




