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
# Basic BLAST Functionality (searching database given gi and species query)
#-----------------------------------------------------------------------------
def search_NCBI(species, seqQuery, out):
	print("\n\nNot an operational search just yet, but good job anyway")
	print("\n\nSearching: "+species+" for gi"+seqQuery)
'''
	# NCBI query
	
	eQ = species + '\[Organism\]'
	gi = int(seqQuery)
	result = NCBIWWW.qblast("blastp","nr", gi, entrez_query= eQ, expect=0.001, hitlist_size=100, ncbi_gi=True)
	print("Saving file as: " + out)

	# Save file
	save_file = open(out, "w")
	save_file.write(result.read())
	save_file.close()
	result.close()
	time.sleep(120) # Pause 2min between database queries
'''	
#-----------------------------------------------------------------------------
# BLAST controller
#-----------------------------------------------------------------------------	
''' Input file must have the following format:
Genus species,queryAccession
Genus species,queryAccession
Genus species,queryAccession

Where each line is a separate BLAST instruction. This can be edited in excel and saved
as a .csv if need be.
'''
def run_blasts():
	indexfile = raw_input("Enter name of csv file with species and gi numbers: ")
	if os.path.isfile(indexfile):
		with open(indexfile,'rb') as directions:
			index = csv.reader(directions)
			setDirections = []
			for row in index:
				setDirections.append(row)
			count = len(setDirections)	
			with open("results\\filenames.csv",'w') as csvfile:
				filenames = csv.writer(csvfile)
				for i in range(0,count-1):
					if setDirections[i] != None:
						query = str(setDirections[i][1])
						species = str(setDirections[i][0])
						matchSpecies = re.match(r'([A-Z|a-z])[A-Z|a-z]* ([A-Z|a-z]{3}).*', species)
						shortSpecies = matchSpecies.group(1).upper() + matchSpecies.group(2).lower()
						out = "results\\BLAST_" + shortSpecies + "_" + query + ".xml"
						search_NCBI(species,query,out)
						filenames.writerow((species, out))
			csvfile.close()	
	else:
		print("\n\nThis file doesn't exist")
		run_blasts()

#-----------------------------------------------------------------------------
# Read data from a csv file into a list 
#-----------------------------------------------------------------------------
# required for fetch_data()

def csv_to_list(filename):
	with open(filename,"r") as read:
		reader = csv.reader(read)
		tempList = list(reader)
	inputList = []
	for i in range(0,(len(tempList))):
		inputList.append(tempList[i][0])

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
	save_stdout = sys.stdout 
	sys.stdout = open("results\\" + datatype + "_outfile.txt", "w")
	handle = Entrez.efetch(db="protein", id=inputList, rettype=datatype, retmode="text")
	print handle.read()
	sys.stdout = save_stdout
	
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
		os.remove("results\\filenames.csv")

#-----------------------------------------------------------------------------
# Takes a string and finds the species if in format [Genus species]
#-----------------------------------------------------------------------------
def find_species(desc):
	mobj = re.match(r'.*\[([A-Z|a-z])\S* ([A-Z|a-z]{3}).*', desc)
	name = mobj.group(1) + mobj.group(2)
	return name.title()

#-----------------------------------------------------------------------------
# Run BLAST searches
#-----------------------------------------------------------------------------
run_blasts()

#-----------------------------------------------------------------------------
# Run parser and data fetch
#-----------------------------------------------------------------------------
# This bit initializes output files 
bin = open("outfile.csv","w")
bin.close()

print "\n\nFetching genbank data and saving..."	
parse_files()
fetch_data("gb", "outfile.csv")
os.remove("outfile.csv")

#-----------------------------------------------------------------------------
# Reformat genbank file to FASTA
#-----------------------------------------------------------------------------
print "\n\nFormatting genbank data to FASTA..."
gbk_filename = "results\\gb_outfile.txt"
faa_filename = "results\\fasta_outfile.txt"
input_handle  = open(gbk_filename, "r")
output_handle = open(faa_filename, "w")

for seq_record in SeqIO.parse(input_handle, "genbank") :
	#print "Dealing with GenBank record %s" % seq_record.id
	output_handle.write(">%s %s\n%s\n" % (
												find_species(seq_record.description),
												seq_record.id,
												seq_record.seq))	

output_handle.close()
input_handle.close()

print "\n\n* * Run Success * *"
