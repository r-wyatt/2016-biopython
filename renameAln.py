from Bio import AlignIO
import sys
import os.path
import re

def trim_fasta_names(alignpath, input):
	no_ext = re.sub(r'\.[A-Za-z]{3}', "", input)
	print no_ext
	outname = no_ext + "Rename.aln"
	stdout_bak = sys.stdout
	sys.stdout = open(os.path.join(alignpath, outname),"w")
	for line in open(os.path.join(alignpath, input)):
		line = re.sub(r'\>([A-Za-z]{1})[A-Za-z]{3} (\S*)', r'>\1\2', line)
		s = line[0] + line[1].lower() + line[2:]
		print s,
	sys.stdout = stdout_bak
	format_converter(sys.argv[1],outname,"phylip-relaxed")
	
def format_converter(alignpath, input, output_style):
	alignment = AlignIO.read(os.path.join(alignpath,input), "fasta")
	AlignIO.write(alignment,os.path.join(alignpath,"transfomed.phy"),output_style)

	
trim_fasta_names(sys.argv[1],sys.argv[2]) # directory, alignment name

print "all done"

