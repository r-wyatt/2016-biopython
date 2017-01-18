from Bio.Blast import NCBIWWW
from Bio import SeqIO
from Bio import Seq
from Bio import Entrez
from Bio.Blast import NCBIXML
from stat import S_IWRITE, S_IREAD
import sys, os, re, csv

#-----------------------------------------------------------------------------
# Presets
#-----------------------------------------------------------------------------
numhits = 200
eThresh = 0.05
minlength = 200 # Minimum length of sequences (shorter will be trimmed)
Entrez.email = raw_input("Enter email: ")

#-----------------------------------------------------------------------------
# Parse arguments
#-----------------------------------------------------------------------------
with open(sys.argv[1], 'rb') as f: 					# input path to species list (csv file)
    reader = csv.reader(f)
    species = list(reader)[0]
print species

cF = SeqIO.parse(sys.argv[2], "fasta")	# fasta formatted consensus sequence file
consensus = cF.next().seq
dir = sys.argv[3] 									# outdirectory (path)

if not os.path.exists(dir):							# initialize master directory
	os.makedirs(dir)
	
for string in ["gb","fasta","XML"]:					# initialize folder structure
	folder = os.path.join(dir,string)
	if not os.path.exists(folder):
		os.makedirs(folder)
		
#-----------------------------------------------------------------------------
# Return filename without extension
#-----------------------------------------------------------------------------
def stripext(filename):
	filename = re.match(r'([\S\s]*)\.[\S\s]',filename)
	return filename.group(1)
	
#-----------------------------------------------------------------------------
# Takes a string and finds the species if in format [Genus species]
#-----------------------------------------------------------------------------
def find_species(string):
	mobj = re.match(r'.*\[([A-Z|a-z])\S* ([A-Z|a-z]{3}).*', string)
	name = mobj.group(1) + mobj.group(2)
	return name.title()
	
#-----------------------------------------------------------------------------
# BLAST
#-----------------------------------------------------------------------------
for eQ in species:
	print " BLAST for", eQ,"\n"
	result = NCBIWWW.qblast("blastp","nr",consensus, entrez_query= eQ, expect=0.050, hitlist_size=numhits)
	save_file = open(os.path.join(dir,"XML",eQ+".xml"), "w")
	save_file.write(result.read())
	save_file.close()
	result.close()
	print(" Saving file...\n")

#-----------------------------------------------------------------------------
# Process xml files
#-----------------------------------------------------------------------------
files = os.listdir(os.path.join(dir,"XML",""))
print files

for file in files:
	os.chmod(os.path.join(dir,"XML",file),S_IREAD)
	result = open(os.path.join(dir,"XML",file),"r") # mode omitted defaults to read only
	blast_record = NCBIXML.parse(result)
	blast_records = list(blast_record)
	record = blast_records[0]
	hits = []
	specm = re.match( r'(\S{1})\S* (\S{3})[\S\s]*', file)
	specCode = specm.group(1)+specm.group(2)
	for alignment in record.alignments:
		for hsp in alignment.hsps:
			if hsp.expect < eThresh:
				title = alignment.title
				print title
				mdata = re.match( r'.*[A-Z|a-z]{2,3}\|\S*\|(.*?)\|.*', title)
				if mdata is not None:
					accession = re.match(r'([A-Z|a-z|_|0-9]*)\..*', mdata.group(1))
					acc = str(accession.group(1))
					species = find_species(title)
					print acc,shortSpecies,specCode
					hits.append((acc, species))
	filtered = []
	for each in hits:
		if each[1] == specCode:
			filtered.append(each)
	output = list(set(filtered))
	print output
	
	# Saving results as gb
	save_stdout = sys.stdout
	sys.stdout = open(os.path.join(dir,"gb",stripext(file)+".gb"), "w")
	for each in output:
		handle = Entrez.efetch(db="protein", id=each[0], rettype="gb", retmode="text")
		print handle.read()
	sys.stdout = save_stdout

#-----------------------------------------------------------------------------
# Parse fasta format sequences!
#-----------------------------------------------------------------------------
gbfiles = os.listdir(os.path.join(dir,"gb",""))

print "\n\n Formatting genbank data to FASTA..."

for file in gbfiles:
	input_handle = open(os.path.join(dir,"gb",file),"r")
	output_handle = open(os.path.join(dir,"fasta",stripext(file)+".fa"),"w")
	for seq_record in SeqIO.parse(input_handle, "genbank"):
		output_handle.write(">%s %s\n%s\n" % (find_species(seq_record.description),
												seq_record.id,
												seq_record.seq))	
	output_handle.close()
	input_handle.close()

#-----------------------------------------------------------------------------
# Make one big fasta file
#-----------------------------------------------------------------------------	
fastafiles = os.listdir(os.path.join(dir,"fasta",""))

save_stdout = sys.stdout
sys.stdout = open(os.path.join(dir,"master.fa"), "w")
for file in fastafiles:
	with open(os.path.join(dir,"fasta",file)) as fin:
		print fin.read()

sys.stdout = save_stdout

#-----------------------------------------------------------------------------
# Remove spaces in fasta names
#-----------------------------------------------------------------------------
masterfasta = os.path.join(dir,"master.fa")
nsmasterfasta = os.path.join(dir,"master_ns.fa")

stdout_bk = sys.stdout
sys.stdout = open(nsmasterfasta,"w+")
with open(masterfasta,"r") as f:
	for line in f:
		if re.search(r'>',line):
			line = re.sub(r' ',"_",line)
		sys.stdout.write(line)
sys.stdout = stdout_bk

#-----------------------------------------------------------------------------
# Clean duplicate and short sequences
#-----------------------------------------------------------------------------
fastafile = nsmasterfasta
cleanfasta = os.path.join(dir,"master_clean.fa")
sequences={}

for seq_record in SeqIO.parse(fastafile, "fasta"):
	sequence = str(seq_record.seq).upper()
	if len(sequence) >= minlength:
		if sequence not in sequences:
			sequences[sequence] = seq_record.id
   # If it is already in the hash table, we're just gonna concatenate the ID
   # of the current sequence to another one that is already in the hash table
		else:
			if not re.search(seq_record.id,sequences[sequence]):
				sequences[sequence] += "_" + seq_record.id

# Write the clean sequences
output_file = open(cleanfasta, "w+")
# Just read the hash table and write on the file as a fasta format
for sequence in sequences:
	output_file.write(">" + sequences[sequence] + "\n" + sequence + "\n")
output_file.close()

print("CLEAN!!!")




