import re, sys, os

intro = '''\nThis little script will rename NCBI refseq fasta entries in a file
using the first accession, a species tag in the form [Species genus]
and the name of the file before the extension to rename all sequences
with cognate names that have no spaces.\n'''

print intro

infile = raw_input("  Enter name of input file: ")
outfile = raw_input( "  Enter name of file to save to: ")
dir = raw_input("  Specify directory (leave blank to indicate current directory): ")

stdout_bk = sys.stdout
sys.stdout = open(os.path.join(dir,outfile),"w+")
with open(os.path.join(dir,infile),"r") as f:
	for line in f:
		sys.stdout
		if re.search(r'>',line):
			species = re.match(r'.*\[([A-Z|a-z]* [A-Z|a-z]*)\].*',line)
			if species is not None:
				species = re.sub(r' ',"_",species.group(1))
			else:
				species = ""
			number = re.match(r'.*matrix metalloproteinase-([0-9]*) .*',line)
			if number is not None:
				code = number.group(1)
			else:
				code = ""
			acc = re.match(r'>(\S*) .*',line).group(1)
			line = ">"+code+acc+"_"+species+"\n"
		sys.stdout.write(line)
sys.stdout = stdout_bk

print "\nFinished file"