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
with open(sys.argv[1], 'rb') as f: 		# Argument 1: input path to species list (csv file)
    reader = csv.reader(f)
    species = list(reader)[0]

cF = SeqIO.parse(sys.argv[2], "fasta")	# Argument 2: fasta formatted consensus sequence file
consensus = cF.next().seq

dir = sys.argv[3] 						# Argument 3: outdirectory (path)

if not os.path.exists(dir):				# initialize master directory
	os.makedirs(dir)
	
for string in ["gb","fasta","XML"]:		# initialize folder structure
	folder = os.path.join(dir,string)
	if not os.path.exists(folder):
		os.makedirs(folder)
		
#-----------------------------------------------------------------------------
# Print some useful run headers
#-----------------------------------------------------------------------------
print "\nSpecies selected:",
for sp in species:
	print sp+",",
print "\n"

print "Consensus:",consensus
print ""	
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

for file in files:
	os.chmod(os.path.join(dir,"XML",file),S_IREAD)
	result = open(os.path.join(dir,"XML",file),"r") # mode omitted defaults to read only
	blast_record = NCBIXML.parse(result)
	blast_records = list(blast_record)
	record = blast_records[0]
	hits = []
	for alignment in record.alignments:
		for hsp in alignment.hsps:
			if hsp.expect < eThresh:
				title = alignment.title
				mdata = re.match( r'[A-Z|a-z]{2,3}\|[0-9]*\|[A-Z|a-z]{2,3}\|(\S*)\|.*', title)
				if mdata is not None:
					acc = mdata.group(1)
					name = re.match(r'.*(\[[A-Z|a-z]* [A-Z|a-z]*\]).*',title)
					if name is None:
						print "\nNo species name found for", "<"+title+">: ","Removed\n"
						continue
					species = find_species(name.group(1))
					hits.append(acc)
				else :
					print "Can't parse title:",title

	
	# Saving results as gb
	save_stdout = sys.stdout
	sys.stdout = open(os.path.join(dir,"gb",stripext(file)+".gb"), "w")
	for each in hits:
		handle = Entrez.efetch(db="protein", id=each, rettype="gb", retmode="text")
		print handle.read()
	sys.stdout = save_stdout

#-----------------------------------------------------------------------------
# Parse fasta format sequences!
#-----------------------------------------------------------------------------
gbfiles = os.listdir(os.path.join(dir,"gb",""))
print "\n\n Formatting genbank data to FASTA..."

for file in gbfiles:
	newfile = os.path.join(dir,"fasta",stripext(file)+".fa")
	SeqIO.convert(os.path.join(dir,"gb",file), "genbank",newfile,"fasta")

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
# Add species code
#-----------------------------------------------------------------------------
masterfasta = os.path.join(dir,"master.fa")
nsmasterfasta = os.path.join(dir,"master_ns.fa")

stdout_bk = sys.stdout
sys.stdout = open(nsmasterfasta,"w+")
with open(masterfasta,"r") as f:
	for line in f:
		if re.search(r'>',line):
			species = re.match(r'.*\[([A-Z|a-z]* [A-Z|a-z]*)\].*',line).group(1)
			species = re.sub(r' ',"_",species)
			acc = re.match(r'>(\S*) .*',line).group(1)
			line = ">"+acc+"_"+species+"\n"
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
				print "sequence duplicate found: <%s> merged with <%s>" % (seq_record.id,sequences[sequence])
				sequences[sequence] += "_" + seq_record.id

# Write the clean sequences
output_file = open(cleanfasta, "w+")
# Just read the hash table and write on the file as a fasta format
for sequence in sequences:
	output_file.write(">" + sequences[sequence] + "\n" + sequence + "\n")
output_file.close()




