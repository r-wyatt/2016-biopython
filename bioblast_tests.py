#-----------------------------------------------------------------------------
# Set-up section
#-----------------------------------------------------------------------------
from Bio.Blast import NCBIWWW
from Bio import SeqIO
from Bio import Seq
from Bio.Blast import NCBIXML
import os.path
import time
import csv
import re
# Testing gi = '225543094'

#-----------------------------------------------------------------------------
# Basic Functionality (searching database given gi and species query)
#-----------------------------------------------------------------------------

def search_a_database(species, seqQuery, out):
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
# Search database repeatedly (input is csv with {species, gi} in each row)
#-----------------------------------------------------------------------------
def parse_a_set(queryList):
	print("Made it to parse a set")
	print(queryList)
	count = len(queryList)	
	with open("results\\filenames.txt",'a') as csvfile:
		filenames = csv.writer(csvfile)
		for i in range(0,count-1):
			if queryList[i] != None:
				query = str(queryList[i][1])
				species = str(queryList[i][0])
				matchSpecies = re.match(r'([A-Z|a-z])[A-Z|a-z]* ([A-Z|a-z]{3}).*', species)
				shortSpecies = matchSpecies.group(1).upper() + matchSpecies.group(2).lower()
				out = "results\\BLAST_" + shortSpecies + "_" + query + ".xml"
				search_a_database(species,query,out)
				filenames.writerow((species, out))
			else:
				print("That's all folks!")
	csvfile.close()	

#-----------------------------------------------------------------------------
# Flow control
#-----------------------------------------------------------------------------	
def decide_what_to_do():
	decision = raw_input("Run a blast search (r), a series of blast searches (s) or quit (q)? ")
	if decision == "s":
		indexfile = raw_input("Enter name of csv file with species and gi numbers: ")
		if os.path.isfile(indexfile):
			with open(indexfile,'rb') as directions:
				index = csv.reader(directions)
				setDirections = []
				for row in index:
					setDirections.append(row)
					print(setDirections)
				parse_a_set(setDirections)
				
		else:
			print("\n\nThis file doesn't exist")
			decide_what_to_do()
	elif decision == "r":
		species = raw_input("Please enter the species query to limit results: ")
		seqQuery = raw_input("Please enter the protein gi number to use as sequence query: ")
		search_a_database(species, seqQuery)
	elif decision == "q":
		print("\n\nThanks for playing!")
	else:
		print("\n\nNot a valid selection.\n\n")
		decide_what_to_do()

#-----------------------------------------------------------------------------
# Actually run the shit
#-----------------------------------------------------------------------------
decide_what_to_do()






