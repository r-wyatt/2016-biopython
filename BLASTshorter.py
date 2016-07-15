#-----------------------------------------------------------------------------
# Automated BLAST searching
#-----------------------------------------------------------------------------
''' Script to run a series of BLAST searches
Written by R. A. Wyatt in July, 2016 with the help of many forum questions
and answers. Especially those on stackoverflow.

This script requires version 2.5 of python (syntax breaks with 3.5, sadly). 
It takes an input file with directions for what BLAST searches to accomplish.

Input file must have the following format:
Genus species,queryAccession
Genus species,queryAccession
Genus species,queryAccession

Where each line is a separate BLAST instruction. This can be edited in excel and saved
as a .csv if need be.
'''
#-----------------------------------------------------------------------------
# Set-up section
#-----------------------------------------------------------------------------
from Bio.Blast import NCBIWWW
from Bio import SeqIO
from Bio import Seq
from Bio import Entrez
from Bio.Blast import NCBIXML
from os import listdir
from os.path import isfile
from shutil import rmtree
import os.path
import errno
import time
import csv
import sys
import re
Entrez.email ="someemail@gmail.com"

#=============================================================================
#-------- Utility Functions --------------------------------------------------
#=============================================================================

#-----------------------------------------------------------------------------
# Directory utilities
#-----------------------------------------------------------------------------
def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc:  # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise

def rmdir_p(path):
	if os.path.isdir(path):
		rmtree(path)

def cleanup(dir):
	directories = [dir,dir+'\\BLAST',dir+'\\accs',dir+'\\fasta']

	for folder in directories:
		rmdir_p(folder)
		mkdir_p(folder)
#-----------------------------------------------------------------------------
# Takes a string and finds the species if in format [Genus species]
#-----------------------------------------------------------------------------
def find_species(desc):
	mobj = re.match(r'.*\[([A-Z|a-z])\S* ([A-Z|a-z]{3}).*', desc)
	name = mobj.group(1) + mobj.group(2)
	return name.title()
#-----------------------------------------------------------------------------
# Strip filename of extension
#-----------------------------------------------------------------------------
def record_name(filename):
	rnam = re.match(r'(\S*).[A-Z|a-z]{3}',filename)
	return rnam.group(1)
#-----------------------------------------------------------------------------
# Read data from a csv file into a list 
#-----------------------------------------------------------------------------
# required for fetch_data()

def csv_to_list(filename):
	with open(filename,"r") as read:
		reader = csv.reader(read)
		tempList = list(reader)
		print tempList
	inputList = []
	for i in range(0,(len(tempList))):
		inputList.append(tempList[i][0])

	return inputList
	
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
# Consolidate species files
#-----------------------------------------------------------------------------
def consolidate_species(dir):
	files = [f for f in listdir(dir) if isfile(dir+f)]
# TODO unfinished script here




#=============================================================================
#-------- Basic Functionality ------------------------------------------------
#=============================================================================

#-----------------------------------------------------------------------------
# Basic BLAST Functionality (searching database given gi and species query)
#-----------------------------------------------------------------------------
def search_NCBI(species, seqQuery, out):
	print("\n\nNot an operational search just yet, but good job anyway")
	print("\n\nSearching: "+species+" for "+seqQuery)
	
	# NCBI query
	'''
	eQ = species + '\[Organism\]'
	gi = seqQuery
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
# Given input file, give a csv of IDs
#-----------------------------------------------------------------------------
# First argument is the path to the XML file from a remote BLAST search, second
# is an e value threshold below which results from the BLAST search will be discarded,
# third is the name of the file to write the accessions to, and fourth is the name of the
# file to send the file names of processed BLAST searches to.

def get_ids(filename, dir, ethresh = 0.01):
	eValueThresh = ethresh
	result = open(dir+"\\BLAST\\"+filename) # mode omitted defaults to read only
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
	spec = filename[0:4]
	print "filtering for: " + spec
	filteredHits = filter_species(hits,spec)
	# Saving results
	# Save as separate files for each species~!
	name = record_name(filename)
	with open(dir+"\\accs\\"+name+".csv",'w') as csvfile:
		blasthits = csv.writer(csvfile)
		for each in filteredHits:
			blasthits.writerow([each[0]])
	csvfile.close()

#-----------------------------------------------------------------------------
# Fetch data can take either the list of accessions or name of csv (one entry per line)
#-----------------------------------------------------------------------------
def fetch_data(datatype, rname, dir):
	accs = csv_to_list(dir+"\\accs\\"+rname+".csv")
	save_stdout = sys.stdout 
	sys.stdout = open(dir+"\\fasta\\"+rname+".txt", "w")
	handle = Entrez.efetch(db="protein", id=accs, rettype=datatype, retmode="text")
	print handle.read()
	sys.stdout = save_stdout
	
#=============================================================================
#-------- Flow Control -------------------------------------------------------
#=============================================================================

#-----------------------------------------------------------------------------
# BLAST controller
#-----------------------------------------------------------------------------	
def run_blasts(dir):
	indexfile = raw_input("Enter name of csv file with species and gi numbers: ")
	if os.path.isfile(indexfile):
		with open(indexfile,'rb') as directions:
			index = csv.reader(directions)
			setDirections = []
			for row in index:
				setDirections.append(row)
			count = len(setDirections)	
			with open(dir+"\\filenames.csv",'w') as csvfile:
				filenames = csv.writer(csvfile)
				for i in range(0,count-1):
					if setDirections[i] != None:
						query = str(setDirections[i][1])
						species = str(setDirections[i][0])
						matchSpecies = re.match(r'([A-Z|a-z])[A-Z|a-z]* ([A-Z|a-z]{3}).*', species)
						shortSpecies = matchSpecies.group(1).upper() + matchSpecies.group(2).lower()
						if not os.path.exists(dir+"\BLAST\\"):
							mkdir_p(dir+"\\BLAST\\")
						out = dir+"\\BLAST\\" + shortSpecies + "_" + query + ".xml"
						search_NCBI(species,query,out)
						filenames.writerow((species, out))
			csvfile.close()	
	else:
		print("\n\nThis file doesn't exist")
		run_blasts()	
		
#-----------------------------------------------------------------------------
# Parse a series of xml BLAST output files to return accession lists
#-----------------------------------------------------------------------------
def parse_files(dir):
	files = [f for f in listdir(dir) if isfile(dir+f)]
	for file in files:
		get_ids(file)
		masterName = record_name(file)
		fetch_data("gb",masterName)

#-----------------------------------------------------------------------------
# Run BLAST searches
#-----------------------------------------------------------------------------
directoryName = raw_input("Enter directory name to write results to: ")
print "\n\n Clearing/creating new directory..."
cleanup(directoryName)
run_blasts(directoryName)

#-----------------------------------------------------------------------------
# Run parser and data fetch
#-----------------------------------------------------------------------------
print "\n\nFetching genbank data and saving..."	
parse_files(directoryName+"\\BLAST\\")

#-----------------------------------------------------------------------------
# Reformat genbank file to FASTA
#-----------------------------------------------------------------------------
print "\n\nFormatting genbank data to FASTA..."

gbk_filename = directoryName+"\\gb_outfile.txt"
faa_filename = directoryName+"\\fasta_outfile.txt"
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
