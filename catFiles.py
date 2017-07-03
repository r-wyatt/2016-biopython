import sys, os, re

intro = '''\nThis script will put all of the files in a directory 
specified by the first argument into one file specified 
by the second argument.\n'''

print intro

stdout_bk = sys.stdout
sys.stdout = open(sys.argv[2],"w+")

files = os.listdir(sys.argv[1])

for file in files:
	with open(os.path.join(sys.argv[1],file),"r") as f:
		for line in f:
			sys.stdout.write(line)

sys.stdout = stdout_bk			
			
print "\nFinished file"