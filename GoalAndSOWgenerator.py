#!/usr/bin/python
# -*- coding: utf-8 -*-

# Contributors:
# * Katya Ovchinnikova <e.ovchinnikova@gmail.com> (2014)
# Generator of pks goals and SOW from Henry output.
# The script takes the output of Henry, parses it, and generates pks goals and SOWs.

import sys
import argparse
import json

from Henry import HenryReader
from PKS import PKSGenerator

def main():

	# parse arguments
	parser = argparse.ArgumentParser(description="Henry output classifier.")
	parser.add_argument("-i", help="The input Henry file to be processed. Default is stdin.", default=None)
	parser.add_argument("-o", help="Output file. Default is stdout.", default=None)
	
	pa = parser.parse_args()

	ifile = open(pa.i, "r") if pa.i else sys.stdin
	ofile = open(pa.o, "w") if pa.o else sys.stdout

	hr = HenryReader(ifile)
	pks = PKSGenerator(hr.Hypo)

	# write classifier output into stdout or output file
	ofile.write(json.dumps(pks.data))

if __name__ == "__main__":
	main()