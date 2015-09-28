#! /bin/bash

# usage:
# $ ./run_Phillip.sh <KB>
# or
# $ ./run_Phillip.sh

PHILLIP_BIN=$PHILLIP_DIR/bin/phil
PHILLIP_OPT="-m inference -c lhs=depth -c ilp=weighted -c sol=gurobi -p max_depth=4 -T 60"

if [ "$1" ]; then
	$PHILLIP_BIN $PHILLIP_OPT -k $1 < /dev/stdin  > /dev/stdout
else
	echo "No compiled knowledge base specified."
fi