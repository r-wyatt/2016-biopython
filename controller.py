#=============================================================================
#-------- Controller ---------------------------------------------------------
#=============================================================================
import sys import os

"""Naval Fate.

Usage:
  controller.py BLAST inputfile newdirectory
  controller.py ALIGN inputdirectory
  controller.py TRIM inputdirectory


Options:
  -h --help     Show this screen.


"""
from docopt import docopt


if __name__ == '__main__':
    arguments = docopt(__doc__, version='Naval Fate 2.0')
    print(arguments)