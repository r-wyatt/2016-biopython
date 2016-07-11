from Bio import SeqIO
import sys
import re


def find_species(desc):
	mobj = re.match(r'.*\[([A-Z|a-z])\S* ([A-Z|a-z]{3}).*', desc)
	name = mobj.group(1) + mobj.group(2)
	print name
	return name.title()

gbk_filename = "results\\gb_outfile.txt"
faa_filename = "results\\gb_outfile_converted.fna"
input_handle  = open(gbk_filename, "r")
output_handle = open(faa_filename, "w")

for seq_record in SeqIO.parse(input_handle, "genbank") :
	print "Dealing with GenBank record %s" % seq_record.id
	output_handle.write(">%s %s\n%s\n" % (
												find_species(seq_record.description),
												seq_record.id,
												seq_record.seq))	

output_handle.close()
input_handle.close()