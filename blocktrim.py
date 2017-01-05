#-----------------------------------------------------------------------------
# Clustalw run and read
#-----------------------------------------------------------------------------
''' This code requires that biopython is installed (as well as, obviously, python). 
Not tested for version 3 of python, so it will probably break.

Cite trimal:


Edit the filenames below:			'''

infile = "align.aln"
outfile = "trimAlign.aln"

#-----------------------------------------------------------------------------
# Set-up section
#-----------------------------------------------------------------------------
from Bio import AlignIO
import sys, os, re

#-----------------------------------------------------------------------------
# Function to use Gblocks to trim alignment
#-----------------------------------------------------------------------------
def blocktrim(input):
	os.system("Gblocks.exe "+input)
#-----------------------------------------------------------------------------
# Reformat alignment
#-----------------------------------------------------------------------------
def trim_fasta_names(alignpath, input):
	no_ext = re.sub(r'\.[A-Za-z]{3}', "", input)
	print no_ext
	outname = no_ext + "Rename.aln"
	stdout_bak = sys.stdout
	sys.stdout = open(os.path.join(alignpath, outname),"w")
	for line in open(os.path.join(alignpath, input)):
		line = re.sub(r'\>([A-Za-z]{4}) (\S*)', r'>\1\2', line)
		s = line[0] + line[1].lower() + line[2:]
		print s,
	sys.stdout = stdout_bak
	format_converter(sys.argv[1],outname,"phylip-relaxed")
	
def format_converter(alignpath, input, output_style):
	alignment = AlignIO.read(os.path.join(alignpath,input), "fasta")
	AlignIO.write(alignment,os.path.join(alignpath,"transfomed.phy"),output_style)
#-----------------------------------------------------------------------------
# Flow control
#-----------------------------------------------------------------------------
dir = sys.argv[1] # First argument is the master directory name

blocktrim(os.path.join(dir,"align.aln"))
trim_fasta_names(dir,"align.aln-gb")




