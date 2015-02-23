#! /bin/bash

# usage:
# $ ./run_all.sh <input string>

LEX_KB=$KIT_LU_DIR/KBs/lexicalKB.txt

if [ $# -eq 0 ]; then
	echo "No input string provided."
else
	echo $1 |
	$KIT_LU_DIR/run_Boxer_client_pipeline_EN.sh |
	python $KIT_LU_DIR/Boxer_output_parsing.py  |
	$KIT_LU_DIR/run_Henry.sh $LEX_KB |
	python $KIT_LU_DIR/GoalAndSOWgenerator.py > /dev/stdout 
	#python $SCRIPTS_DIR/ClassifyHenryOutput.py > /dev/stdout
fi