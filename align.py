#-----------------------------------------------------------------------------
# Clustalw run and read
#-----------------------------------------------------------------------------
''' This code requires that muscle.exe be added to the PATH
'''
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
'''
To use this command, on the command line enter:
python align.py
'''
#-----------------------------------------------------------------------------
# Function to use trimal to trim alignment
#-----------------------------------------------------------------------------
def trim_align(alignpath,out):
	cmd = ['trimal', '-in', alignpath, '-out', out, "-automated1"]
	process = subprocess.Popen(cmd)
	process.wait()
	print('Done')

#-----------------------------------------------------------------------------
# USE MUSCLE!!! Put code in here:
#-----------------------------------------------------------------------------
dir = raw_input("Enter directory master name: ")

out_file = os.path.join(dir,"fasta","mast.txt")
in_file = os.path.join(dir,"opuntia.fasta")
muscle_cline = MuscleCommandline(input=in_file,out=out_file)

directoryName = raw_input("Enter directory name to write results to: ")

trim_align(out_file,os.path.join("results","outfile.aln")



