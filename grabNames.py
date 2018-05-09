import sys, os, re

intro = '''\nThis script will put all of the sequence names from
a fasta file specified by the first argument into the new file 
specified by the second argument. It will create several different
iterations of names for different purposes (ex: no special charac-
ters/spaces for tree building or full accession for fact checking
or species codes for display).\n'''

print intro

nicknames = [["72 kDa","2"],["interstitial","1"],[r'stromelysin[- ]1',"3"],
			[r'stromelysin[- ]2',"10"],["metalloelastase","12"],["collagenase 3","13"],
			["interstitial collagenase B","1b"],["neutrophil","8"],
			["matrilysin","7"],[r'stromelysin[- ]3',"11"]]

stdout_bk = sys.stdout
sys.stdout = open(os.path.join(sys.argv[2]),"w+")

with open(os.path.join(sys.argv[1]),"r") as f:
	for line in f:
		sys.stdout
		if re.search(r'>',line):
			line = line.replace(",","")
			accm = re.match(r'\>([0-9]*)_([A-Z|a-z]{2,3}_[0-9]*.[0-9]*) .*',line)
			if accm is not None:
				acc = accm.group(2)
				gID = accm.group(1)
			else:
				acc = ""
			specmatch = re.match(r'.*\[([A-Z|a-z]* [A-Z|a-z]*)\].*',line)
			if specmatch is not None:
				species = re.sub(r' ',"_",specmatch.group(1))
				gs = re.match(r'(.).*_(.).*',species)
				scode = gs.group(1)+gs.group(2)
			elif specmatch is None and accm is not None:
				handle = Entrez.efetch(db="protein", id=acc, rettype="gb", retmode="text")
				result=handle.read().split('\n')
				for i in result:
					if 'ORGANISM' in i:
						species = '_'.join(i.split()[1:])
						species = re.sub(r'\(.*\)','',species)
				gs = re.match(r'(.).*_(.).*',species)
				scode = gs.group(1)+gs.group(2)
			else:
				species = ""
				scode = ""
			number = re.match(r'.*matri[xc] metallop[roteinpd]{5,6}ase[- ]([0-9]*) .*',line)
			if number is not None:
				code = number.group(1)
			else:
				code = ""
				for nick in nicknames:
					if re.search(nick[0],line):
						code = nick[1]
			nospace = line.strip(">").split(" ")
			figName = species+"_MMP"+code
			raxmlName = scode+code+acc
			phyName = scode+acc.replace("_","")[:-2]
			shortName = scode[0:1]+phyName[-9:]
			firstName = line.replace("\n","")[1:].replace("\r","")
			longName = figName+"_"+acc
			geneIDname = scode+gID[-8:]
			sys.stdout.write((firstName+","+raxmlName+","+figName+","+geneIDname+"," +
			                 phyName+","+shortName+","+longName+","+nospace[0]+","+species+"\n"))
sys.stdout = stdout_bk			
			

print "\nFinished file"

