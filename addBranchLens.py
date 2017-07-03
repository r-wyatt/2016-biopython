import sys, os,re

file = sys.argv[1]

with open(file,"r") as newick:
	tree = newick.readlines()

tree = re.sub(r',',':1,',tree[0])
tree = re.sub(r'\)','):1',tree)
with open("BL_"+file,"w") as output:
	output.write(tree)

print(tree)