from Bio.Blast import NCBIWWW
from Bio import SeqIO
from Bio import Seq
from Bio.Blast import NCBIXML
import re
import csv


filename = raw_input("Please enter the file name to examine: ")
result = open("results\\" + filename)
blast_record = NCBIXML.parse(result)

blast_records = list(blast_record)
record = blast_records[0]

# Code adapted from biopython tutorials:

E_VALUE_THRESH = 0.01
n = 1

with open('outfile.csv','wb') as csvfile, open('outfile2.csv','wb') as csvfile2:
	blasthits = csv.writer(csvfile)
	tracker = csv.writer(csvfile2)
	for alignment in record.alignments:
		for hsp in alignment.hsps:
			if hsp.expect < E_VALUE_THRESH:
				stamp = '\n[[ * * * * Record No.' + str(n) + ' * * * * ]]'
				print stamp
				n += 1
				title = alignment.title
				#print title
				mdata = re.match( r'.*([A-Z|a-z]{2,3})\|(.*?)\|.*?\[([A-Z])\S* ([A-Z|a-z]{3}).*\].*?', title)
				if mdata is not None:
					accessiontyp = mdata.group(1)
					accession = mdata.group(2)
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
