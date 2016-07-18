from os import listdir
from os.path import isfile
import glob

#-----------------------------------------------------------------------------
# Consolidate species files
#-----------------------------------------------------------------------------
def consolidate_species(dir):
	wdir = dir + "\\gb\\"
	ids = []
	files = [f for f in listdir(wdir) if isfile(wdir+f)]
	for file in files:
		ids.append(file[0:4])
	specs = list(set(ids))
	for spec in specs:
		print spec
		read_files = glob.glob(wdir+spec+"*")
		print read_files
		with open(wdir+"master"+spec+".txt", "wb") as outfile:
			for f in read_files:
				print f
				with open(f, "rb") as infile:
					outfile.write(infile.read())
				infile.close()
		outfile.close()
	
consolidate_species("m")