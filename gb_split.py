from Bio import SeqIO
import sys

for rec in SeqIO.parse(sys.stdin, "genbank"):
   SeqIO.write([rec], open("results\\genbank\\" + rec.id + ".gbk", "w"), "genbank")