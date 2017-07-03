import os, re, sys, csv

intro = '''\nThis script will take a csv with bibliographic information
and parse it into RIS format. Bibliographic info needs to be 
formatted as from scopus output to tab delimited spreadsheet. 
For more info use: 
	CSVtoRIS.py -format
	
Arguments:
		1: Input filename
		2: Output format
'''

format = '''
Format requirements: 15 columns
Authors / Title / Year / Source Title / Volume /
Issue / ... / Page start / Page end / ... /
... / DOI / ... / Abstract / Document Type /
Source / ... / Notes
'''

if sys.argv[1] =="-format":
	print format
	sys.exit()

print intro

infile = sys.argv[1]
outfile = infile[:-3]+"ris"

parse = infile.split("\\")
print parse

def printNames(string):
	names = string.split(".,")
	print "AU - "+names.pop(0)
	count = 2
	for name in names:
		print "AU - "+name[1:]
		count += 1

def printType(string):
	if string in ("Article","Article in Press","Review","Letter"):
		print "TY - JOUR"
	elif string == "Book Chapter":
		print "TY - CHAP"
	else:
		raise ValueError("This script can't handle the type; "+string)
		

stdout_bk = sys.stdout
sys.stdout = open(outfile,"w")

with open(infile, 'rb') as f:
	reader = csv.reader(f,delimiter='\t')
	headers = True
	for entry in reader:
		if headers == True:
			headers = False
		else:
			printType(entry[14])
			print("TI - "+entry[1])
			printNames(entry[0])
			print("AB - "+entry[13])
			print("JF - "+entry[3])
			print("SP - "+entry[7])
			print("EP - "+ entry[8])
			print("Y1 - "+entry[2])
			print("VL - "+entry[4])
			print("DO - "+entry[11])
			print("DB - "+entry[15])
			print("N1 - "+entry[19])
			print("ER - ")
f.close()

