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
Entrez.email ="r.a.wyatt@unb.ca"

#-----------------------------------------------------------------------------
# Read data from a csv file into a list 
#-----------------------------------------------------------------------------
# required for fetch_data()

def csv_to_list(filename):
	print "Ran csv_to_list"
	with open(filename,"r") as read:
		reader = csv.reader(read)
		tempList = list(reader)
	inputList = []
	for i in range(0,(len(tempList))):
		inputList.append(tempList[i][0])
	
	print inputList
	return inputList

#-----------------------------------------------------------------------------
# Fetch data can take either the list of accessions or name of csv (one entry per line)
#-----------------------------------------------------------------------------
def fetch_data(datatype, input):
	if isinstance(input, str):
		inputList = csv_to_list(input)
	else:
		inputList = input
	temp = sys.stdout
	sys.stdout = open("results\\" + datatype + "_outfile.txt", "w")
	handle = Entrez.efetch(db="protein", id=inputList, rettype=datatype, retmode="text")
	print handle.read()

#-----------------------------------------------------------------------------
# Filter accession list
#-----------------------------------------------------------------------------
def filter_species(listOfTuples, shortSpecies):
	filtered = []
	for each in listOfTuples:
		if each[1] == shortSpecies:
			filtered.append(each)
	output = list(set(filtered))
	return output

#-----------------------------------------------------------------------------
# Given input file, give a csv of IDs
#-----------------------------------------------------------------------------
# First argument is the path to the XML file from a remote BLAST search, second
# is an e value threshold below which results from the BLAST search will be discarded,
# third is the name of the file to write the accessions to, and fourth is the name of the
# file to send the file names of processed BLAST searches to.

def get_ids(input, ethresh = 0.01, outfile1 = "outfile.csv"):
	eValueThresh = 0.01
	result = open(input) # mode omitted defaults to read only
	blast_record = NCBIXML.parse(result)
	blast_records = list(blast_record)
	record = blast_records[0]
	hits = []
	for alignment in record.alignments:
		for hsp in alignment.hsps:
			if hsp.expect < eValueThresh:
				title = alignment.title
				mdata = re.match( r'.*[A-Z|a-z]{2,3}\|(.*?)\|.*?\[([A-Z])\S* ([A-Z|a-z]{3}).*\].*?', title)
				if mdata is not None:
					accession = re.match(r'([A-Z|a-z|_|0-9]*)\..*', mdata.group(1))
					acc = str(accession.group(1))
					genus = str(mdata.group(2)[0])
					species = str(mdata.group(3)[:3])
					shortSpecies = (genus + species)
					hits.append((acc, shortSpecies))
	spec = input[14:18]
	filteredHits = filter_species(hits,spec)
	# Saving results
	with open("outfile.csv",'a') as csvfile:
		blasthits = csv.writer(csvfile)
		for each in filteredHits:
			blasthits.writerow([each[0]])
	csvfile.close()

#-----------------------------------------------------------------------------
# Parse a series of files
#-----------------------------------------------------------------------------
def parse_files():
		with open("results\\filenames.csv",'r') as csvfile:
			reader = csv.reader(csvfile)
			files = list(reader)
			for filename in files:
				get_ids(filename[1])
		csvfile.close()
		with open("outfile.csv",'r') as csvfile2:
			read = csv.reader(csvfile2)
			bam = list(read)
			cord =[]
			for i in range(0,len(bam)):
				cord.append(bam[i][0])
			accs = list(set(cord))
		csvfile2.close()
		return bam

#-----------------------------------------------------------------------------
# Takes a string and finds the species if in format [Genus species]
#-----------------------------------------------------------------------------
def find_species(desc):
	mobj = re.match(r'.*\[([A-Z|a-z])\S* ([A-Z|a-z]{3}).*', desc)
	name = mobj.group(1) + mobj.group(2)
	return name.title()
	
#-----------------------------------------------------------------------------
# Run parser and data fetch
#-----------------------------------------------------------------------------
# This bit clears output files so they are clean on initializing this program
with open("outfile.csv","w") as csvfile:
	csvfile.truncate()
	
parse_files()
fetch_data("gb", "outfile.csv")

#-----------------------------------------------------------------------------
# Reformat genbank file to FASTA
#-----------------------------------------------------------------------------
gbk_filename = "results\\gb_outfile.txt"
faa_filename = "results\\fasta_outfile.txt"
input_handle  = open(gbk_filename, "r")
output_handle = open(faa_filename, "w")

for seq_record in SeqIO.parse(input_handle, "genbank") :
	print "Dealing with GenBank record %s" % seq_record.id
	output_handle.write(">%s %s\n%s\n" % (
												find_species(seq_record.description),
												seq_record.id,
												seq_record.seq))	

output_handle.close()
input_handle.close()
