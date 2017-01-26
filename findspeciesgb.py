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

dir = sys.argv[1]

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

print("CLEAN!!!")

	
