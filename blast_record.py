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

dummyList = [("cp102", "Mmus"),("spd901", "Hsap"),("cp102", "Mmus"),("cp984", "Mmus")]

print dummyList
#-----------------------------------------------------------------------------
# Actually run the shit
#-----------------------------------------------------------------------------
def filter_results(listOfTuples, shortSpecies):
	noDups = list(set(listOfTuples))

	filtered = []
	for each in noDups:
		if each[1] == shortSpecies:
			filtered.append(each)
	return filtered

#-----------------------------------------------------------------------------
# Given input file, give a csv of IDs
#-----------------------------------------------------------------------------
# First argument is the path to the XML file from a remote BLAST search, second
# is an e value threshold below which results from the BLAST search will be discarded,
# third is the name of the file to write the accessions to, and fourth is the name of the
# file to send the file names of processed BLAST searches to.

def get_ids(input, ethresh = 0.01, outfile1 = "outfile.csv"):
	eValueThresh = 0.01
	n = 1
	result = open(input) # mode omitted defaults to read only
	blast_record = NCBIXML.parse(result)
	blast_records = list(blast_record)
	record = blast_records[0]
	hits = []
	for alignment in record.alignments:
		for hsp in alignment.hsps:
			if hsp.expect < eValueThresh:
				stamp = '\n[[ * * * * Record No.' + str(n) + ' * * * * ]]'
				print stamp
				n += 1
				title = alignment.title
				#print title
				mdata = re.match( r'.*[A-Z|a-z]{2,3}\|(.*?)\|.*?\[([A-Z])\S* ([A-Z|a-z]{3}).*\].*?', title)
				if mdata is not None:
					accession = re.match(r'([A-Z|a-z|_|0-9]*)\..*', mdata.group(1))
					acc = str(accession.group(1))
					genus = str(mdata.group(2)[0])
					species = str(mdata.group(3)[:3])
					shortSpecies = (genus + species)
					hits.append((acc, shortSpecies))
				#print('sequence:', title)
				#print('e value:', hsp.expect)
		print ".\n.\n.\n."
	spec = input[15:19]
	print "\n\n\nFiltering for: " + spec + "\n\n\n"
	filteredHits = filter_results(hits,spec)
	# Saving results
	with open("compare.csv","w") as compare:
		writer = csv.writer(compare)
		for each in hits:
			writer.writerow([each[0]])	
	with open(outfile1,'wb') as csvfile:
		blasthits = csv.writer(csvfile)
		for each in filteredHits:
			blasthits.writerow([each[0]])
			
	csvfile.close()

#-----------------------------------------------------------------------------
# Actually run the shit
#-----------------------------------------------------------------------------
# When running this script from the console, one argument is required: the name
# of the BLAST search output file

get_ids(sys.argv[1])

with open("outfile.csv") as outfile, open("compare.csv") as compare:
	old = csv.reader(compare)
	oldTemp = list(old)
	new = csv.reader(outfile)
	newTemp = list(new)
	print "Length of old: " + str(len(oldTemp))
	print "Length of new: " + str(len(newTemp))
	


