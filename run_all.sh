#! /bin/bash

# usage:
# $ ./run_all.sh <input string>

SCRIPTS_DIR=/home/katya/Projects/KIT_LU_pipeline
LEX_KB=$SCRIPTS_DIR/KBs/lexicalKB.txt

if [ $# -eq 0 ]; then
	echo "No input string provided."
else
	echo $1 |
	$SCRIPTS_DIR/run_Boxer_client_pipeline_EN.sh |
	python $SCRIPTS_DIR/Boxer_output_parsing.py  |
	$SCRIPTS_DIR/run_Henry.sh $LEX_KB |
	python $SCRIPTS_DIR/GoalAndSOWgenerator.py > /dev/stdout 
	#python $SCRIPTS_DIR/ClassifyHenryOutput.py > /dev/stdout
fi