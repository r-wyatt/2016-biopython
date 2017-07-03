import csv, sys, os

contents = []
with open(sys.argv[1], "r") as file:
	reader = csv.reader(file)
	for line in reader:
		contents.append(line)

names = []	
for line in contents:
	names.append(line[0])
names = set(names)	
for name in names:
	sys.stdout.write('"'+name+'"'+", ")
