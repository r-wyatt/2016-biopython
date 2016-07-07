#-----------------------------------------------------------------------------
# Set-up section
#-----------------------------------------------------------------------------
from Bio import Entrez
import time
import sys
import csv
Entrez.email ="someemail@gmail.com"

#-----------------------------------------------------------------------------
# Dummy data to work with in testing
#-----------------------------------------------------------------------------
acc = "XP_001345507"
accList = ["AAQ07962", "XP_009303831", "XP_009290029", "NP_919397"]

with open("test.txt","w") as testFile:
	writer = csv.writer(testFile)
	for each in accList:
		writer.writerow([each])
testFile.close()

#-----------------------------------------------------------------------------
# Read data from a csv file into a list
#-----------------------------------------------------------------------------
def csv_to_list(filename):
	with open(filename,"r") as read:
		reader = csv.reader(read)
		tempList = list(reader)
	inputList = []
	for i in range(0,(len(tempList))):
		inputList.append(tempList[i][0])
	return inputList

#-----------------------------------------------------------------------------
# Fetch data can take either the list of accessions or name of csv (one entry per line)
#-----------------------------------------------------------------------------
db = "protein"
def fetch_data(datatype, input, db=db, ids=accList):
	if isinstance(input, str):
		inputList = csv_to_list(input)
	else:
		inputList = input
	temp = sys.stdout
	sys.stdout = open("results\\" + datatype + "_outfile.txt", "w")
	handle = Entrez.efetch(db="protein", id=inputList, rettype=datatype, retmode="text")
	print handle.read()

fetch_data("gb", "test.txt")


'''
with open("genbankFile.csv",'a') as csvoutfile:
	output = csv.writer(csvoutfile)
	output.write(handle.read())
'''
'''
request = Entrez.epost("nucleotide",id=",".join(map(str,gis)))
result = Entrez.read(request)
webEnv = result["WebEnv"]
queryKey = result["QueryKey"]
handle = Entrez.efetch(db="nucleotide",retmode="xml", webenv=webEnv, query_key=queryKey)
for r in Entrez.parse(handle):
    # Grab the GI 
    try:
        gi=int([x for x in r['GBSeq_other-seqids'] if "gi" in x][0].split("|")[1])
    except ValueError:
        gi=None
    print ">GI ",gi," "+r["GBSeq_primary-accession"]+" "+r["GBSeq_definition"]+"\n"+r["GBSeq_sequence"][0:20]
		
'''