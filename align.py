#-----------------------------------------------------------------------------
# Clustalw run and read
#-----------------------------------------------------------------------------
''' This code requires that Clustalw be installed under the directory
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
import sys
import os

#-----------------------------------------------------------------------------
# Clustal run
#-----------------------------------------------------------------------------
'''# Todo build code to run clustal (install also)
clustalw_exe = r"C:\Program Files\ClustalW2\clustalw2.exe"
clustalw_cline = ClustalwCommandline(clustalw_exe, infile="results\\opuntia.fasta")

assert os.path.isfile(clustalw_exe), "Clustal W executable missing"
save_stdout = sys.stdout
save_stderr = sys.stderr
stdout, stderr = clustalw_cline()

tree = Phylo.read("results\\opuntia.dnd","newick")
Phylo.draw_ascii(tree)
'''
#-----------------------------------------------------------------------------
# USE MUSCLE!!! Put code in here:
#-----------------------------------------------------------------------------
muscle_cline = MuscleCommandline(input="opuntia.fasta")
save_stdout = sys.stdout
save_stderr = sys.stderr

stdout,stderr = muscle_cline()
align = AlignIO.read(StringIO(stdout), "fasta")
print(align)

