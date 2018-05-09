#-----------------------------------------------------------------------------
# Set-up section
#-----------------------------------------------------------------------------
from Bio import Entrez
import sys, csv, os, re

intro = '''\nThis script will take a csv with alternate names in columns
	
Arguments:
		1: Input filename
		2: Output format
'''
print intro
jobName = raw_input("Job name: ")
Entrez.email = raw_input("Enter email: ")

years = [2000,2001,2002,2003,2004,2005,2006,2007,2008,2009,2010,2011,2012,2013,2014,2015,2016,2017,2018]

def searchHitNum(query,sdate,edate):
	
	handle = Entrez.esearch(db="pubmed", retmax=1, term=query,mindate=sdate,maxdate=edate)
	results = Entrez.read(handle)
	results = str(results)

	obj = re.match(r'\{u\'Count\': \'([0-9]*)\'.*',results,flags=re.DOTALL)
	return obj.group(1)

with open("MMPnames.csv") as file:
	input = csv.reader(file)
	temp = list(input)
	names = []
	for name in temp:
		names.append(filter(None,name))

#print names

counts = [["Nick","Query","Year","Count"]]
queries = []
for mmp in names:
	for year in years:
		year = str(year)
		query = '"[Title/Abstract] OR "'.join(mmp)
		query = '"'+query+'"[Title/Abstract]'
		counts.append([re.sub('"','',query[4:6]),query,year,searchHitNum(query,year,year)])
		queries.append(query)


with open("output2.csv","w") as f:
	writer = csv.writer(f)
	writer.writerows(counts)

stdout_bk = sys.stdout
sys.stdout = open("queries2.txt","w")
print queries
sys.stdout = stdout_bk

print "done file"
