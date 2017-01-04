#-----------------------------------------------------------------------------
# Clustalw run and read
#-----------------------------------------------------------------------------
''' This code requires that muscle.exe be added to the PATH, and that biopython
is installed (as well as, obviously, python). Not tested for version 3 of python,
so it will probably break.

To use this script, on the command line enter:
python align.py directoryName_from_fastBLAST_results

Download muscle_version.exe from http://www.drive5.com/muscle/downloads.htm
Put file into an accessible directory (ex programs/muscle)
Add to PATH

Cite MUSCLE:

Edgar, R.C. (2004) MUSCLE: multiple sequence alignment with high accuracy and high throughput.Nucleic Acids Res. 32(5):1792-1797.
doi:10.1093/nar/gkh340

Edgar, R.C. (2004) MUSCLE: a multiple sequence alignment method with reduced time and space complexity BMC Bioinformatics, (5) 113.
doi:10.1186/1471-2105-5-113

Cite trimal:

Edit the filenames below:			'''

infile = "master.txt"
outfile1 = "align.aln"
outfile2 = "trimAlign.aln"


#-----------------------------------------------------------------------------
# Set-up section
#-----------------------------------------------------------------------------
from Bio.Align.Applications import ClustalwCommandline

from Bio import AlignIO
from Bio import Phylo
from StringIO import StringIO
import subprocess
import os.path
import sys
import os
import re

#-----------------------------------------------------------------------------
# MUSCLE through command line call
#-----------------------------------------------------------------------------
def align(fasta,out):
	open(out,"w+")
	cmd = ['muscle', '-in', fasta, '-out', out]
	process = subprocess.Popen(cmd)
	process.wait()
	print('\nDone align\n')
	
#-----------------------------------------------------------------------------
# Function to use trimal to trim alignment
#-----------------------------------------------------------------------------
def trim_align(alignpath,out):
	cmd = ['trimal', '-in', alignpath, '-out', out, "-automated1"]
	process = subprocess.Popen(cmd)
	process.wait()
	print('\nDone trim\n')
#-----------------------------------------------------------------------------
# Functions to condense fasta names before saving as phylip
#-----------------------------------------------------------------------------
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
	


#-----------------------------------------------------------------------------
# Flow control
#-----------------------------------------------------------------------------
dir = sys.argv[1] # First argument is the master directory name

out_file = os.path.join(dir,outfile1)
in_file = os.path.join(dir,infile)
print(out_file,in_file)

align(in_file,out_file)

trim_align(out_file, os.path.join(dir,outfile2))
trim_fasta_names(dir,"align.phy")



