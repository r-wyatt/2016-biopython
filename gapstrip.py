import subprocess,sys,os,re
from Bio import AlignIO

input = sys.argv[1] # first argument is the input alignment
dir = sys.argv[2]   # second argument is the directory for the output files

if not os.path.exists(dir):
	os.makedirs(dir)

base = 'strippedalign'

rates = [0.4,0.6,0.7,0.8,0.9,0.95,0.99,1]
alignments = []


for each in rates:
	outname = os.path.join(dir,base+re.sub(r'\..*','',str(each*100))+".fas")
	cmd = ['trimal','-in',input,'-out',outname,'-fasta','-gt',str(each)]
	process = subprocess.Popen(cmd)
	process.wait()

	alignment=AlignIO.read(open(outname),"fasta")	
	print ("Alignment length: %i for %i percent" % (alignment.get_alignment_length(),each*100))
	phyname = re.sub(r'fas','phy',outname)
	output = open(phyname,"w")
	alignments.append(output)
	AlignIO.write(alignment,output,"phylip-relaxed")
	output.close()

print alignments
	
#raxml

for each in alignments:
	print each
	name = "T"+re.match(r'.*?([0-9]*)\..*',each).group(1)
	raxMLcmd = ["raxml -m PROTGAMMAJTTF -p 56845 -s", each, "-n", name]
	print raxMLcmd
	print name



	

