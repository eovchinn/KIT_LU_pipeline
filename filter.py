#!/usr/bin/python
# -*- coding: utf-8 -*-

# Contributors:
#   * Katya Ovchinnikova <e.ovchinnikova@gmail.com> (2015)

import argparse
import sys

def main():

	# parse arguments
	parser = argparse.ArgumentParser(description="C&C output fixer.")
	parser.add_argument("-i", help="Input line. Default is stdin.", default=None)
	parser.add_argument("-o", help="Output line. Default is stdout.", default=None)
	
	pa = parser.parse_args()

	ifile = open(pa.i, "r") if pa.i else sys.stdin
	ofile = open(pa.o, "w") if pa.o else sys.stdout

	counter = 0
	for line in ifile:
		line = line.rstrip(' \t\n\r')
		if line.endswith(" with"): 
			line = line[:-5]
		if "Could" in line: line = line.replace("Could","Can")
		if "could" in line: line = line.replace("could","can")
		ofile.write(line)


if __name__ == "__main__":
	main()