#! /bin/bash

# usage:
# $ ./run_all.sh <input string>

LEX_KB=$KIT_LU_DIR/KBs/lexicalKB.txt
LEX_KB_COMPILED=$KIT_LU_DIR/KBs/phil_kb/kitchen

if [ $# -eq 3 ]; then
	LEX_KB_COMPILED=$KIT_LU_DIR/KBs/phil_kb/kitchen_atomic
fi

if [ $# -eq 0 ]; then
	echo "No input string provided."
else
	if [ $# -eq 1 ]; then
		echo $1 |
		$KIT_LU_DIR/run_Boxer_client_pipeline_EN.sh |
		python $KIT_LU_DIR/Boxer_output_parsing.py|
		#$KIT_LU_DIR/run_Henry.sh $LEX_KB |
		#python $KIT_LU_DIR/GoalAndSOWgenerator.py > /dev/stdout 
		$KIT_LU_DIR/run_Phillip.sh $LEX_KB_COMPILED |
		python $KIT_LU_DIR/GoalAndSOWgenerator.py -m p > /dev/stdout 
	else
		echo $1 |
		$KIT_LU_DIR/run_Boxer_client_pipeline_EN.sh |
		python $KIT_LU_DIR/Boxer_output_parsing.py -a "$2" |
		#$KIT_LU_DIR/run_Henry.sh $LEX_KB |
		#python $KIT_LU_DIR/GoalAndSOWgenerator.py > /dev/stdout 
		$KIT_LU_DIR/run_Phillip.sh $LEX_KB_COMPILED |
		python $KIT_LU_DIR/GoalAndSOWgenerator.py -m p > /dev/stdout
	fi
fi