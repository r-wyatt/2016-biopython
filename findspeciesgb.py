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
				mdata = re.match( r'.*[\|[A-Z|a-z]{2,3}\|(\S*)\|]{2}.*', title)
				if mdata is not None:
					accession = re.match(r'([A-Z|a-z|_|0-9]*)\..*', mdata.group(2))
					acc = str(accession.group(2))
					species = find_species(title)
					hits.append(acc)

	
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
print gbfiles
print "\n\n Formatting genbank data to FASTA..."

for file in gbfiles:
	specm = re.match( r'(\S{1})\S* (\S{3})[\S\s]*', file)
	specCode = specm.group(1)+specm.group(2)
	input_handle = open(os.path.join(dir,"gb",file),"r")
	for seq_record in SeqIO.parse(input_handle, "genbank"):
		print(seq_record.id, seq_record.seq)	
	input_handle.close()


	
