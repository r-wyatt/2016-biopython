from Bio.Blast import NCBIWWW
from Bio import SeqIO
from Bio import Seq
from Bio import Entrez
from Bio.Blast import NCBIXML
from stat import S_IWRITE, S_IREAD
import sys, glob, os, re, csv

#-----------------------------------------------------------------------------
# Presets
#-----------------------------------------------------------------------------
numhits = 200
ethresh = 0.05
Entrez.email = raw_input("Enter email: ")

#-----------------------------------------------------------------------------
# Return filename without extension
#-----------------------------------------------------------------------------
def remove_ext(filename):
	filename = re.match(r'([\S\s]*)\.[\S\s]',filename)
	return filename.group(1)
	
#-----------------------------------------------------------------------------
# Filter accession list by species
#-----------------------------------------------------------------------------
def filter_species(listOfTuples, shortSpecies):
	filtered = []
	for each in listOfTuples:
		if each[1] == shortSpecies:
			filtered.append(each)
	output = list(set(filtered))
	return output

#-----------------------------------------------------------------------------
# Parse arguments
#-----------------------------------------------------------------------------
with open(sys.argv[1], 'rb') as f: # input path to species list (csv file)
    reader = csv.reader(f)
    species = list(reader)[0]
print species	
consensus = open(sys.argv[2]).read() # fasta file containing consensus sequence
dir = sys.argv[3] # path to outdirectory

for str in ["gb","fasta","XML"]:
	folder = os.path.join(dir,str)
	if not os.path.exists(folder):
		os.makedirs(folder)
'''	
#-----------------------------------------------------------------------------
# BLAST
#-----------------------------------------------------------------------------
for eQ in species:
	print eQ
	print consensus
	result = NCBIWWW.qblast("blastp","nr",consensus, entrez_query= eQ, expect=0.050, hitlist_size=numhits)
	save_file = open(os.path.join(dir,"XML",eQ), "w")
	save_file.write(result.read())
	save_file.close()
	result.close()
	print(" Saving file as: " + out)
#-----------------------------------------------------------------------------
# Process xml files
#-----------------------------------------------------------------------------
'''
files = glob.glob(os.path.join(dir,"XML"))
print files

for file in files:
	os.chmod(os.path.join(dir,"XML",file),S_IREAD)
	result = open(os.path.join(dir,file),"r") # mode omitted defaults to read only
	blast_record = NCBIXML.parse(result)
	blast_records = list(blast_record)
	record = blast_records[0]
	hits = []
	for alignment in record.alignments:
		for hsp in alignment.hsps:
			if hsp.expect < eThresh:
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
	hits = filter_species(hits,spec)
	
	# Saving results as gb
	save_stdout = sys.stdout
	sys.stdout = open(os.path.join(dir,"gb",remove_ext(file)+".gb"), "w")
	for each in hits:
		handle = Entrez.efetch(db="protein", id=each[1], rettype="gb", retmode="text")
			print handle.read()
	sys.stdout = save_stdout
	csvfile.close()
	
#-----------------------------------------------------------------------------
# Fetch fasta format sequences!
#-----------------------------------------------------------------------------

gbfiles = glob.glob(os.path.join(dir,"gb")

print "\n\n Formatting genbank data to FASTA..."

for file in gbfiles:
	input_handle = open(os.path.join(wdir,file),"r")
	output_handle = open(os.path.join(dir,"fasta",spec+".txt"),"w")
	for seq_record in SeqIO.parse(input_handle, "genbank"):
		output_handle.write(">%s %s\n%s\n" % (find_species(seq_record.description),
												seq_record.id,
												seq_record.seq))	
	output_handle.close()
	input_handle.close()

	
