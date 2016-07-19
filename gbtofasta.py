from Bio import SeqIO
import glob
import re
def find_species(desc):
	mobj = re.match(r'.*\[([A-Z|a-z])\S* ([A-Z|a-z]{3}).*', desc)
	name = mobj.group(1) + mobj.group(2)
	return name.title()
def process_gbk(dir):
	wdir = dir + "\\gb\\"
	read_files = glob.glob(wdir+"master"+"*")
	for file in read_files:
		mobj = re.match(r'\S*master([A-Z|a-z]{4})\S*',file)
		spec = mobj.group(1)
		input_handle = open(file,"r")
		output_handle = open(dir+"\\fasta\\"+"master"+spec+".txt","w")
		for seq_record in SeqIO.parse(input_handle, "genbank") :
			#print "Dealing with GenBank record %s" % seq_record.id
			output_handle.write(">%s %s\n%s\n" % (
														find_species(seq_record.description),
														seq_record.id,
														seq_record.seq))	

		output_handle.close()
		input_handle.close()
		
process_gbk("m")