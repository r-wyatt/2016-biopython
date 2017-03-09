import re, sys, os
from Bio import Entrez

Entrez.email = 'someuser@mail.com'

handle = Entrez.efetch(db="protein", id="XP_522163.1", rettype="gb", retmode="text")
result=handle.read().split('\n')

for line in result:
	if 'ORGANISM' in line:
		print '_'.join(line.split()[1:]) 
