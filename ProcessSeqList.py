import xml.etree.cElementTree as etree
from Bio import Entrez, SeqIO
import urllib
import sys, re, time

intro = '''
This script will take a list of GeneIDs in a text file
and retrieve the longest associated protein sequence for
each, then save them to a file.

Arguments:
		1: Text file of GeneIDs
		2: File to save fasta sequences\n'''

print intro
Entrez.email = raw_input("Email: ")
GeneIDs = sys.argv[1]
fastafile = sys.argv[2]

def progress(goal, curr):
	x = 1

def fetch(acc):
	try:
		handle = Entrez.efetch(db="protein", id=acc, rettype="fasta",retmode="text")
	except:
		sys.stdout = stdout_bk
		print "Entered first error level with "+acc
		sys.stdout = open(fastafile,"a")
		time.sleep(3)
		try:
			handle = Entrez.efetch(db="protein", id=acc, rettype="fasta",retmode="text")
		except:
			sys.stdout = stdout_bk
			print "Entered second error level with "+acc
			sys.stdout = open(fastafile,"a")
			time.sleep(10)
			handle = Entrez.efetch(db="protein", id=acc, rettype="fasta",retmode="text")
	return handle

def get_length(acc):
	handle = fetch(acc)
	record = "".join(handle.readlines())
	#record = Entrez.read(handle)
	record = record.split("\n")
	length = 0
	name = record[0].split(" ")[0][1:]
	seq = "".join(record[1:])
	for line in record[1:len(record)-1]:
		length += len(line)
	return [length,name,record]


def get_longest_ID(gID):
	if gID == "":
		return ["",""]
	beg = 'https://biodbnet-abcc.ncifcrf.gov/webServices/rest.php/biodbnetRestApi.xml?method=db2db&format=row&'
	cus = 'input=geneID&inputValues='+gID+'&outputs=RefSeqProteinAccession'
	url =beg+cus
	u = urllib.urlopen(url)
	response = u.read()
	obj = etree.fromstring(response)

	for box in obj[0]:
		if box.tag == 'RefSeqProteinAccession':
			accs = box.text
	accs = accs.split("//")
	max = 0
	for acc in accs:
		aa = get_length(acc)
		if aa[0] > max:
			max = aa[0]
			output = [aa[1],aa[2]]
	return output

start = time.clock()

stdout_bk = sys.stdout
sys.stdout = open(fastafile,"w")
with open(GeneIDs,"r") as genes:
	for gene in genes:
		gene = re.sub("\n","",re.sub(" ","",gene))
		record = get_longest_ID(gene)
		for line in record[1]:
			if re.search(">",line):
				line = re.sub(">",">"+gene+"_",line)
			sys.stdout.write(line)
			sys.stdout.write("\r\n")

sys.stdout = stdout_bk
end = time.clock()
time = divmod(end,60)
minutes = time[0]
seconds = time[1]
print 'Script end at: {:02.0f} min {:02.0f} sec'.format(minutes,seconds)