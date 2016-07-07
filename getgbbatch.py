from Bio import Entrez
import time
import sys
import csv
Entrez.email ="someemail@gmail.com"

## We instead upload the list of ID beforehand 
gis=[166706892,431822405,431822402]
acc = "XP_001345507"
db = "protein"

accList = ["AAQ07962", "XP_009303831", "XP_009290029", "NP_919397"]
print accList

with open("test.txt","w") as testFile:
	writer = csv.writer(testFile)
	for each in accList:
		writer.writerow([each])
testFile.close()

def fetch_data(datatype, filename, db=db, ids=accList):
	with open(filename,"r") as read:
		reader = csv.reader(read)
		tempList = list(reader)
	inputList = []
	for i in range(0,(len(tempList))):
		inputList.append(tempList[i][0])
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