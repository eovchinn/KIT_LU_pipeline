#! /bin/bash

# usage:
# $ ./run_Henry.sh <KB>
# or
# $ ./run_Henry.sh

HENRY_BIN=/home/katya/Software/henry-n700/bin/henry
BOXER2HENRY=/home/katya/Projects/ADP-pipeline/pipelines/English/Boxer2Henry.py

HENRY_MODEL=/home/katya/Software/henry-n700/models/h93.py
HENRY_OPT="-m infer -e $HENRY_MODEL -d 3 -t 4 -O proofgraph,statistics -T 60"
#HENRY_OPT="-m infer -e $HENRY_MODEL -d 3 -t 4 -T 60"

if [ -f "$1" ]; then
	#python $BOXER2HENRY < /dev/stdin |
	#cat $1 - | 
	cat $1 - < /dev/stdin |
	$HENRY_BIN $HENRY_OPT > /dev/stdout
else
	#python $BOXER2HENRY < /dev/stdin |
	#$HENRY_BIN $HENRY_OPT > /dev/stdout
	$HENRY_BIN $HENRY_OPT < /dev/stdin > /dev/stdout
fi