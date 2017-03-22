import subprocess,datetime,time,sys,os,re
from Bio import AlignIO
#-----------------------------------------------------------------------------
# Presets
#-----------------------------------------------------------------------------
input = sys.argv[1] # first argument is the input alignment

base = 'strippedalign'

rates = [0.6,0.8,0.9,0.92,0.94,0.96,0.98]
alignments = []

#-----------------------------------------------------------------------------
# Alignments
#-----------------------------------------------------------------------------
starttime = time.time()
print "\nStarted: ",datetime.datetime.now().time(),"\n"

for each in rates:
	outname = base+re.sub(r'\..*','',str(each*100))+".fas"
	cmd = ['trimal','-in',input,'-out',outname,'-fasta','-gt',str(each)]
	process = subprocess.Popen(cmd)
	process.wait()

	alignment=AlignIO.read(open(outname),"fasta")	
	print ("Alignment length: %i for %i percent" % (alignment.get_alignment_length(),each*100))
	phyname = re.sub(r'fas','phy',outname)
	output = open(phyname,"w")
	alignments.append(phyname)
	AlignIO.write(alignment,output,"phylip-relaxed")
	output.close()

	
#-----------------------------------------------------------------------------
# Calls to raxML
#-----------------------------------------------------------------------------

for each in alignments:
	time1 = time.time()
	print "\n***** Building tree for ",each," *****"
	name = "T"+re.match(r'.*?([0-9]*)\..*',each).group(1)
	raxMLcmd = ['raxmlHPC.exe', '-m', 'PROTGAMMAJTTF', '-p', '56845', '-s', each, '-n', name,">","stdout."+name]
	process = subprocess.Popen(raxMLcmd,shell=True)
	process.wait()
	time2 = time.time()-time1
	div = divmod(time2,86400)
	days = div[0]
	elapsed = div[1]
	print "Finished  tree for",each," tree. Time: ",str(days)," days, ",str(datetime.timedelta(seconds=elapsed-0))

endtime = datetime.datetime.now().time()
elapsed = time.time()-starttime
div = divmod(elapsed,86400)
days = div[0]
secs = div[1]
print "\nFinished: ",datetime.datetime.now().time()
print "Total elapsed time: ",days, " days, ",str(datetime.timedelta(seconds=elapsed-0)),"\n"


