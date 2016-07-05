from Bio import Entrez
import time
import csv
Entrez.email ="someemail@gmail.com"

## We instead upload the list of ID beforehand 
gis=[166706892,431822405,431822402]
acc = "XP_001345507"
db = "nuccore"

handle = Entrez.efetch(db=db, rettype="gb", id=acc)
#print output to stdout
with open("genbankFile.csv",'a') as csvoutfile:
	output = csv.writer(csvoutfile)
	output.write(handle.read())

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