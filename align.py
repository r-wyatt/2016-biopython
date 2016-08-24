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
python align.py directoryName

Note that muscle and trimAlign must be installed and added to path. If script doesn't work, test that they are accessible from the command line.
'''
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
# Flow control
#-----------------------------------------------------------------------------
dir = sys.argv[1] # First argument is the master directory name

out_file = os.path.join(dir,"align.aln")
in_file = os.path.join(dir,"master.txt")

align(in_file,out_file)

trim_align(os.path.join(dir,"align.aln"), os.path.join(dir,"trimAlign.aln"))



