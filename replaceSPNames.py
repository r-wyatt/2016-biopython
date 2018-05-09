import sys, csv, re, os

intro = '''
This script will replace names using a guiding csv:
the first column needs to contain the original name
and the other columns need to contain the new names.

This modification of this script will take as the
name to be replaced the first column entries up to
their first spaces (to deal with truncation).

Arguments:
		1: Filename of file to replace names
		2: Filename to save replaced file as
		3: Guide file for names (csv)
		4: Index of new names as int (default is column two)\n'''

print intro

infile = sys.argv[1]
outfile = sys.argv[2]
guidefile = sys.argv[3] # This is a file of FASTA headers (all names include '>')
index = int(sys.argv[4])-1 if len(sys.argv) > 4 else 2
prior = int(sys.argv[5])-1 if len(sys.argv) > 5 else 1

			
with open(guidefile, 'rb') as f:
    reader = csv.reader(f)
    guide = list(reader)
f.close()
	
stdout_bk = sys.stdout
sys.stdout = open(outfile,"w+")

with open(infile,"r") as f:
	for line in f:
		line = line.replace(",","")
		if not re.search(r'[0-9|A-Z|a-z]*',line):
			continue
		for i in guide:
			mobj = re.match(r'([^ ]*).*',i[prior])
			truncat = mobj.group(1)
			if truncat in line:
				line = line.replace(truncat,i[index])
		line = line.replace('\n','')
		sys.stdout.write(line)


f.close()

sys.stdout = stdout_bk

print "\nFinished process"
