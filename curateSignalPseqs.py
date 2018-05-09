import sys, csv, re, os

intro = '''
This script will organize a directory containing
three files of NCBI gene search results into files 
that contain only species entries for which there is 
an existing entry in each file.

Arguments:
		1: Directory of input files
		2: Directory for output \n'''

print intro

dir = sys.argv[1]
outdir = sys.argv[2]

files = []
for filename in os.listdir(dir):
	files.append(filename)

def add_file (filename):
	with open(os.path.join(dir,filename),"r") as f:
		temp = {}
		for line in f.readlines():
			data = line.split("\t")
			if data[1] in temp:
				print "Duplicates, overwriting " + data[1]+": "+temp[data[1]][0]+" for "+data[0]
			temp[data[1]]=data
	return temp

arrays = {}
for file in files:
	arrays[file]=add_file(file)

# for array in arrays:
	# print array[1]["Homo sapiens"]

count = 0
count2 = 0
species = []
print arrays.keys()
print files[0]+"\n"
for key in arrays[files[0]]:
	if all(key in arrays[i] for i in arrays.keys()):
		count += 1
		species.append(str(key))
	count2 +=1

print count2,count, len(species)

for file in files:
	f = open(os.path.join(outdir,file),"w+")
	stdoutBk = sys.stdout
	sys.stdout = f
	for s in species:
		if s == "Org_name":
			continue
		sys.stdout.write("\t".join(arrays[file][s]))
	sys.stdout = stdoutBk
	f.close()
