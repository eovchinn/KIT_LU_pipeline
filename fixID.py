#!/usr/bin/python
# -*- coding: utf-8 -*-

# Contributors:
#   * Katya Ovchinnikova <e.ovchinnikova@gmail.com> (2015)

import re

import sys
import argparse

from Henry import HenryReader
from PropClass import Classifier

def main():

	# parse arguments
	parser = argparse.ArgumentParser(description="C&C output fixer.")
	parser.add_argument("-i", help="The C&C output file to be processed. Default is stdin.", default=None)
	parser.add_argument("-o", help="Output file. Default is stdout.", default=None)
	
	pa = parser.parse_args()

	ifile = open(pa.i, "r") if pa.i else sys.stdin
	ofile = open(pa.o, "w") if pa.o else sys.stdout

	counter = 0
	for line in ifile:
		if line.startswith("ccg("):
			id = line[4:-2]
			if counter>0:
				newid = str(500*counter+int(id))
				ofile.write("ccg("+newid+",\n")
			else: ofile.write(line)
			if id=='500':
				counter+=1
		else: ofile.write(line)

if __name__ == "__main__":
	main()