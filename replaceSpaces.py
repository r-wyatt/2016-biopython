# Remove spaces in fasta file sequence names
# Functionally this will replace all spaces with underscores
# for any line that includes ">"

'''
Usage:
	replaceSpaces.py directoryOfFastaFiles

Options:
	-h --help	Show this screen.
	--filext	Transform only files with the given file extension.
'''

from docopt import docopt
print(docopt(__doc__, version='Replace Spaces 1.0')

import re, sys

def rem_spaces(file):
	stdout_bk = sys.stdout
	sys.stdout = open("ns_"+file,"w+")
	with open(file) as f:
		for line in f:
			if re.search(r'>',line):
				line = re.sub(r' ',"_",line)
			sys.stdout.write(line)
		print "file finished"
	sys.stdout = stdout_bk
	

def do_all_files(directory):
	files = [f for f in listdir(wdir) if isfile(wdir+f)]
	for file in files:
		rem_spaces(file)
	
do_all_files(sys.argv[1])
