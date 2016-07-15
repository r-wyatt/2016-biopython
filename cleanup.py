from shutil import rmtree
import os


def mkdir_p(path):
	try:
		os.makedirs(path)
	except OSError as exc:  # Python >2.5
		if exc.errno == errno.EEXIST and os.path.isdir(path):
			pass
		else:
			raise

def rmdir_p(path):
	if os.path.isdir(path):
		rmtree(path)
		
def cleanup():
	directories = ['results\\BLAST','results\\accs','results\\fasta']

	for folder in directories:
		rmdir_p(folder)
		mkdir_p(folder)

cleanup()