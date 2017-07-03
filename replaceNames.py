import sys, csv, re, os

intro = '''\nThis script will replace names using a guiding csv:
the first column needs to contain the original name
and the other columns need to contain the new names.
Arguments:
		1: Filename of file to replace names
		2: Filename to save replaced file as
		3: Guide file for names (csv)
		4: Index of new names as int (default is column one)
		5: Index of original names as int (default is column two)\n'''

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
		for i in guide:
			if i[prior] in line:
				line = line.replace(i[prior],i[index])
		print line


f.close()

sys.stdout = stdout_bk

print "\nFinished process"




