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

This code breaks if the save directory you specify already exists. If you want to uoverwrite
a directory, you need to delete it before running this code. I tried, but failed, as windows
throws access denied errors.
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
import glob
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

def init(dir):
	directories = [dir]
	lst = ["BLAST","accs","gb","fasta"]
	for string in lst:
		directories.append(os.path.join(dir,string))
	print directories
	for folder in directories:
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
	wdir = os.path.join(dir, "gb")
	ids = []
	files = [f for f in listdir(wdir) if isfile(wdir+f)]
	for file in files:
		ids.append(file[0:4])
	specs = list(set(ids))
	for spec in specs:
		read_files = glob.glob(wdir+spec+"*")
		with open(wdir+"master"+spec+".txt", "wb") as outfile: # Change to write to upper level?
			for f in read_files:
				with open(f, "rb") as infile:
					outfile.write(infile.read())
				infile.close()
		outfile.close()
		
def merge_all_fasta(dir):
	wdir = os.path.join(dir + "fasta")
	files = [f for f in listdir(wdir) if isfile(wdir+f)]
	for file in files:
		print file
		with open(os.path.join(dir,"master"+".txt"), "a") as outfile:
			for f in read_files:
				with open(f, "r") as infile:
					outfile.write(infile.read())
				infile.close()
		outfile.close()

#=============================================================================
#-------- Basic Functionality ------------------------------------------------
#=============================================================================

#-----------------------------------------------------------------------------
# Basic BLAST Functionality (searching database given gi and species query)
#-----------------------------------------------------------------------------
def search_NCBI(species, seqQuery, out):
	#print("\n\nNot an operational search just yet, but good job anyway")
	print("\n\nSearching: "+species+" for "+seqQuery)
	
	# NCBI query

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


#-----------------------------------------------------------------------------
# Given input file, give a csv of IDs
#-----------------------------------------------------------------------------
# First argument is the path to the XML file from a remote BLAST search, second
# is an e value threshold below which results from the BLAST search will be discarded,
# third is the name of the file to write the accessions to, and fourth is the name of the
# file to send the file names of processed BLAST searches to.

def get_ids(filename, dir, ethresh = 0.01):
	eValueThresh = ethresh
	result = open(os.path.join(dir,"BLAST",filename)) # mode omitted defaults to read only
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
	with open(os.path.join(dir,"accs",name+".csv"),'w') as csvfile:
		blasthits = csv.writer(csvfile)
		for each in filteredHits:
			blasthits.writerow([each[0]])
	csvfile.close()

#-----------------------------------------------------------------------------
# Fetch data can take either the list of accessions or name of csv (one entry per line)
#-----------------------------------------------------------------------------
def fetch_data(datatype, rname, dir):
	accs = csv_to_list(os.path.join(dir,"accs",rname+".csv"))
	save_stdout = sys.stdout 
	# Save concatenated genbank records
	sys.stdout = open(os.path.join(dir,"gb",+rname+".txt"), "w")
	handle = Entrez.efetch(db="protein", id=accs, rettype=datatype, retmode="text")
	print handle.read()
	sys.stdout = save_stdout

#-----------------------------------------------------------------------------
# Reformat genbank file to FASTA
#-----------------------------------------------------------------------------
def process_gbk(dir):
	print "\n\nFormatting genbank data to FASTA..."
	wdir = os.path.join(dir,"gb")
	read_files = glob.glob(wdir+"master"+"*")
	for file in read_files:
		mobj = re.match(r'\S*master([A-Z|a-z]{4})\S*',file)
		spec = mobj.group(1)
		input_handle = open(file,"r")
		output_handle = open(os.path.join(dir,"fasta","master"+spec+".txt"),"w")
		for seq_record in SeqIO.parse(input_handle, "genbank"):
			#print "Dealing with GenBank record %s" % seq_record.id
			output_handle.write(">%s %s\n%s\n" % (
														find_species(seq_record.description),
														seq_record.id,
														seq_record.seq))	
		output_handle.close()
		input_handle.close()
	
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
			for i in range(0,count-1):
				if setDirections[i] != None:
					query = str(setDirections[i][1])
					species = str(setDirections[i][0])
					matchSpecies = re.match(r'([A-Z|a-z])[A-Z|a-z]* ([A-Z|a-z]{3}).*', species)
					shortSpecies = matchSpecies.group(1).upper() + matchSpecies.group(2).lower()
					out = os.path.join(dir,"BLAST", + shortSpecies + "_" + query + ".xml")
					search_NCBI(species,query,out)
	else:
		print("\n\nThis file doesn't exist")
		run_blasts()	
		
#-----------------------------------------------------------------------------
# Parse a series of xml BLAST output files to return accession lists
#-----------------------------------------------------------------------------
def parse_files(dir):
	wdir = os.path.join(dir,"BLAST")
	files = [f for f in listdir(wdir) if isfile(wdir+f)]
	for file in files:
		get_ids(file,dir)
		masterName = record_name(file)
		fetch_data("gb",masterName,dir)

#-----------------------------------------------------------------------------
# Run BLAST searches
#-----------------------------------------------------------------------------
directoryName = raw_input("Enter directory name to write results to: ")
print "\n\n Clearing/creating new directory...\n\n"
init(directoryName)

run_blasts(directoryName)

#-----------------------------------------------------------------------------
# Run parser and data fetch
#-----------------------------------------------------------------------------
print "\n\nFetching genbank data and saving..."	
parse_files(directoryName)

consolidate_species(directoryName)

process_gbk(directoryName)

print "\n\n* * Run Success * *"
