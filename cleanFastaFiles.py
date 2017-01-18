#!/usr/bin/env
#-----------------------------------------------------------------------------
# Automated BLAST searching
#-----------------------------------------------------------------------------
''' Script to clean up fasta files
Written by R. A. Wyatt in Jan, 2017. sequence_cleaner function from
<biopython.org/wiki/Sequence_Cleaner>, author unknown.


Remove spaces in fasta file sequence names
Functionally this will replace all spaces with underscores
for any line that includes ">"

Settings here:
'''
minlength = 200 # Minimum length of sequences (shorter will be trimmed)

#-----------------------------------------------------------------------------
# Set-up section
#-----------------------------------------------------------------------------
import re, sys, glob, os
from Bio import SeqIO
from glob import glob

def rem_spaces(dir, file):
	stdout_bk = sys.stdout
	sys.stdout = open(os.path.join(dir,"ns"+file),"w+")
	with open(os.path.join(dir,file),"r") as f:
		for line in f:
			if re.search(r'>',line):
				line = re.sub(r' ',"_",line)
			sys.stdout.write(line)
	sys.stdout = stdout_bk
	return("ns"+file)
	

def sequence_cleaner(dir, fasta_file, min_length=0, por_n=100):
	# Create our hash table to add the sequences
	sequences={}
	# Using the Biopython fasta parse we can read our fasta input
	for seq_record in SeqIO.parse(os.path.join(dir,fasta_file), "fasta"):
		# Take the current sequence
		sequence = str(seq_record.seq).upper()
		# Check if the current sequence is according to the user parameters
		if (len(sequence) >= min_length and
			(float(sequence.count("N"))/float(len(sequence)))*100 <= por_n):
		# If the sequence passed in the test "is it clean?" and it isn't in the
		# hash table, the sequence and its id are going to be in the hash
			if sequence not in sequences:
				sequences[sequence] = seq_record.id
	   # If it is already in the hash table, we're just gonna concatenate the ID
	   # of the current sequence to another one that is already in the hash table
			else:
				if not re.search(seq_record.id,sequences[sequence]):
					sequences[sequence] += "_" + seq_record.id

	# Write the clean sequences

	# Create a file in the same directory where you ran this script
	output_file = open(os.path.join(dir,"clear_" + fasta_file), "w+")
	# Just read the hash table and write on the file as a fasta format
	for sequence in sequences:
		output_file.write(">" + sequences[sequence] + "\n" + sequence + "\n")
	output_file.close()

def do_all_files(directory):
	dir = os.path.join(directory,"fasta")
	files = [f for f in os.listdir(dir) if os.path.isfile(os.path.join(dir,f))]
	for file in files:
		newfile = rem_spaces(dir,file)
		sequence_cleaner(dir,newfile,minlength)


newfile = rem_spaces(sys.argv[1],"master.txt")
sequence_cleaner(sys.argv[1],newfile,minlength)

os.remove(os.path.join(sys.argv[1],"master.txt"))
os.remove(os.path.join(sys.argv[1],"nsmaster.txt"))
os.rename(os.path.join(sys.argv[1],"clear_nsmaster.txt"),os.path.join(sys.argv[1],"master.txt"))


