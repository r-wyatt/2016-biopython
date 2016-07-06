#-----------------------------------------------------------------------------
# Set-up section
#-----------------------------------------------------------------------------
from Bio.Blast import NCBIWWW
from Bio import SeqIO
from Bio import Seq
from Bio.Blast import NCBIXML
import re
import csv
import sys

#-----------------------------------------------------------------------------
# Given input file, give a csv of IDs
#-----------------------------------------------------------------------------
# First argument is the path to the XML file from a remote BLAST search, second
# is an e value threshold below which results from the BLAST search will be discarded,
# third is the name of the file to write the accesions to, and fourth is the name of the
# file to send the file names of processed BLAST searches to.

def get_ids(input, ethresh = 0.01, outfile1 = "outfile.csv", outfile2 = "outfile2.csv"):
	eValueThresh = 0.01
	n = 1
	result = open(input)
	blast_record = NCBIXML.parse(result)
	blast_records = list(blast_record)
	record = blast_records[0]
	with open(outfile1,'wb') as csvfile, open(outfile2,'wb') as csvfile2:
		blasthits = csv.writer(csvfile)
		tracker = csv.writer(csvfile2)
		for alignment in record.alignments:
			for hsp in alignment.hsps:
				if hsp.expect < eValueThresh:
					stamp = '\n[[ * * * * Record No.' + str(n) + ' * * * * ]]'
					print stamp
					n += 1
					title = alignment.title
					#print title
					mdata = re.match( r'.*([A-Z|a-z]{2,3})\|(.*?)\|.*?\[([A-Z])\S* ([A-Z|a-z]{3}).*\].*?', title)
					if mdata is not None:
						accessiontyp = mdata.group(1)
						accession = re.match(r'([A-Z|a-z|_|0-9]*)\..*', mdata.group(2))
						species = mdata.group(3) + mdata.group(4)
						print "//all matches made for " + species + " //"
						blasthits.writerow([accessiontyp, accession, species])
						tracker.writerow([stamp, title])
					#print('sequence:', title)
					#print('e value:', hsp.expect)
			print ".\n.\n.\n."
		
	print blasthits
	print tracker
	csvfile.close()
	csvfile2.close()

#-----------------------------------------------------------------------------
# Actually run the shit
#-----------------------------------------------------------------------------
# When running this script from the console, one argument is required: the name
# of the BLAST search output file

get_ids(sys.argv[1])