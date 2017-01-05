# Remove spaces in fasta file sequence names
# Functionally this will replace all spaces with underscores
# for any line that includes ">"

import re, sys, glob, os

def rem_spaces(dir, file):
	stdout_bk = sys.stdout
	sys.stdout = open(file,"w+")
	with open(os.path.join(dir,"ns"+file),"w+") as f:
		for line in f:
			if re.search(r'>',line):
				line = re.sub(r' ',"_",line)
			print(line)
		print "file finished"
	sys.stdout = stdout_bk
	

def do_all_files(directory):
	dir = os.path.join(directory,"fasta")
	files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir,f))]
	for file in files:
		rem_spaces(dir,file)
	
do_all_files(sys.argv[1])
