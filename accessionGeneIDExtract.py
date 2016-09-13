#-----------------------------------------------------------------------------
# From a genbank file, retrieve accessions and geneIDs
#-----------------------------------------------------------------------------
'''
Usage:
'''
#-----------------------------------------------------------------------------
# Automated BLAST searching
#-----------------------------------------------------------------------------
from Bio import SeqIO
import sys

#-----------------------------------------------------------------------------
# Automated BLAST searching
#-----------------------------------------------------------------------------
gb_file = sys.argv[1]
for gb_record in SeqIO.parse(open(gb_file,"r"), "genbank") :
    # now do something with the record
    print "Name %s, %i features" % (gb_record.name, gb_record.geneid)
    print repr(gb_record.seq)