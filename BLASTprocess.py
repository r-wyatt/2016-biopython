#-----------------------------------------------------------------------------
# Set-up section
#-----------------------------------------------------------------------------
from Bio.Blast import NCBIWWW
from Bio import SeqIO
from Bio import Seq
from Bio import Entrez
from Bio.Blast import NCBIXML
import os.path
import time
import csv
import sys
import re

#-----------------------------------------------------------------------------
# 
#-----------------------------------------------------------------------------