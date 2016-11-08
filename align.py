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
from Bio.Align.Applications import MuscleCommandline
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
def align(alignpath,out):
	cmd = ['muscle.exe', '-in', alignpath, '-out', out]
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
# Function to save alignment as relaxed phylip
#-----------------------------------------------------------------------------
def save_phylip(input, output):
	AlignIO.read(os.path.join("2016-11-02","align.aln"),"fasta")


#-----------------------------------------------------------------------------
# Flow control
#-----------------------------------------------------------------------------
dir = sys.argv[1] # First argument is the master directory name

out_file = os.path.join(dir,outfile1)
in_file = os.path.join(dir,infile)

align(in_file,out_file)

trim_align(out_file, os.path.join(dir,outfile2))



