# Phylogenetic Tree Building from BLAST to TreeVIEW
## BLAST searching
The process for building a tree. Note there's an optional third argument, mock, to sidestep the BLAST searches, which take long and have a delay built into them. Here it is, needs to be executed from the directory where fastBLAST.py occurs, and directory name is the path to a directory that will be created by fastBLAST:
> python fastBLAST.py queryList.csv directoryName

From here we need to take the result in directoryName\master.txt and run it through alignment and trimming algorithm. To do this use the following command (also from the main scripts directory as fastBLAST.py):
> python align.py directoryName



