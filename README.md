# Phylogenetic Tree Building from BLAST to TreeVIEW
## BLAST searching

The code under the name fastBLAST.py (not known for its fast-ness but its direct data manipulation) uses the following function to search a series fo BLASTs (defined in a user input .csv file)

``` python
def search_NCBI(species, seqQuery, out):	
	print("\n\nSearching: "+species+" for "+seqQuery)
	# NCBI query
	run = True
	if len(sys.argv) > 3:
		if sys.argv[3] == "mock":
			run = False
	if run == True:
		eQ = species + '\[Organism\]'
		gi = seqQuery
		result = NCBIWWW.qblast("blastp","nr", gi, entrez_query= eQ, expect=0.001, hitlist_size=100, ncbi_gi=True)

		# Save file
		save_file = open(out, "w")
		save_file.write(result.read())
		save_file.close()
		result.close()
		time.sleep(120) # Pause 2min between database queries
		print("Saving file as: " + out)
	else:
		print("\n\nMock Search")
```