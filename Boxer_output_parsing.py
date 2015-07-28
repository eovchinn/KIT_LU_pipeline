#!/usr/bin/python
# -*- coding: utf-8 -*-

# Contributors:
# * Katya Ovchinnikova <e.ovchinnikova@gmail.com> (2014)
# Boxer output parser.
# The script takes the output of the Boxer Parser, parses it, and puts into a json structure.

import sys
import argparse

from Boxer import BoxerReader
from Henry import HenryWriter

def main():

	# parse arguments
	parser = argparse.ArgumentParser(description="Boxer output parser.")
	parser.add_argument("-i", help="The input Boxer file to be processed. Default is stdin.", default=None)
	parser.add_argument("-o", help="Output file. Default is stdout.", default=None)
	parser.add_argument("-a", help="Appendix to be added to the observation.", default="")

	
	pa = parser.parse_args()

	ifile = open(pa.i, "r") if pa.i else sys.stdin
	ofile = open(pa.o, "w") if pa.o else sys.stdout

	appendix_obs = pa.a if pa.a else ""

	# read Boxer file, parse it, convert into Henry input
	br = BoxerReader(ifile)
	hw = HenryWriter(br.texts,appendix_obs)

	# write Henry input into stdout or output file
	ofile.write(hw.Hobs)

	ifile.close()
	ofile.close()

if __name__ == "__main__":
	main()
