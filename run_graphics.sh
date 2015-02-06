#! /bin/bash

# usage:
# $ ./run_graphics.sh <id>
# or
# $ ./run_graphics.sh

PROOFGRAPH=/home/katya/Software/henry-n700/tools/proofgraph.py

if [ -z "$1" ]; then
	GRAPH_OPT="--graph 1"	
else
	GRAPH_OPT="--graph $1"
fi

python $PROOFGRAPH $GRAPH_OPT | dot -T pdf > /dev/stdout