import time, sys, csv, re, os
from Bio import Entrez, SeqIO

intro = '''
This script will take a list of fasta names (as
outputted for instance from BLAST), and return a
csv file with their associated locations, gene
information, etc. Takes two arguments, a csv input
with a single column of names starting with their
accession numbers (no carat).

Arguments:
		1: Input filename
		2: Output filename\n'''

print intro
Entrez.email = raw_input("Email: ")


def get_gb(acc,name):
	handle = Entrez.efetch(db="protein", id=acc, rettype="gb", retmode="text")
	locus = ["NA","NA","NA","NA"]
	geneID = "NA"
	chr = "NA"
	nt = "NA"
	while True:
		line = handle.readline()
		if re.search("DBSOURCE",line):
			sys.stdout.write(line)
			mo = re.match(r'.*accession (\S*).*',line)
			nt = mo.group(1)
		elif re.search("GeneID",line):
			sys.stdout.write(line)
			mo = re.match(r'.*GeneID:([0-9]*).*',line)
			geneID = mo.group(1)
			locus = get_locus(geneID)
		elif re.search("chromosome=",line):
			sys.stdout.write(line)
			mo = re.match(r'.*chromosome="([A-Z|a-z|0-9]*).*',line)
			chr = mo.group(1)
		elif re.search("//",line):
			sys.stdout.write(line)
			output = [name,acc,nt,geneID,chr]#
			for element in locus:
				output.append(element)
			print output
			return output



def get_locus(geneID):
	handle = Entrez.efetch(db="gene", id=geneID)
	locus = False
	while True:
		line = handle.readline()
		#sys.stdout.write(line)
		if line == "  locus {\n":
			locus = True
			print "found locus!"
		elif re.search("accession",line) and locus:
			sys.stdout.write(line)
			m1 = re.match(r'.*"(.*)".*',line)
			acc = m1.group(1)
		elif re.search("version",line) and locus:
			sys.stdout.write(line)
			m2 = re.match(r'.* ([0-9]*),.*',line)
			acc = acc + "." + m2.group(1)
		elif re.search("from",line) and locus:
			sys.stdout.write(line)
			m3 = re.match(r'.*from ([0-9]*).*',line)
			start = m3.group(1)
		elif re.search("to",line) and locus:
			sys.stdout.write(line)
			m4 = re.match(r'.*to ([0-9]*).*',line)
			end = m4.group(1)
		elif re.search("strand",line) and locus:
			sys.stdout.write(line)
			m5 = re.match(r'.*(strand [A-Z|a-z]*).*',line)
			strand = m5.group(1)
			break
		elif re.search("properties",line):
			break
	output = [acc,start,end,strand]
	return output


with open(sys.argv[1]) as names:
	starttime = time.clock()
	seqInfo = []
	reader = csv.reader(names)
	#reader = [["NP_998288.1"]]
	
	for name in reader:
		#print name
		if re.search(r'(.*?\.[0-9]) .*',name[0]) is not None:
			accM = re.match(r'(.*?\.[0-9]) .*',name[0])
			acc = accM.group(1)
		else:
			seqInfo.append(name)
			continue
		#acc = name
		print acc
		seqInfo.append(get_gb(acc,name))
		time.sleep(3)


print "\nDone collecting Genbank protein files\n\nWriting to file...\n"

with open(sys.argv[2],"w") as outfile:
	writer = csv.writer(outfile)
	writer.writerows(seqInfo)
endtime = time.clock()

print str(endtime-starttime)



