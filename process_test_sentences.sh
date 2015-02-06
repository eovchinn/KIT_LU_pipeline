cat /dev/null > output/kitchen_test_output.txt
while read line; 
do echo -e "$line\n"$(./run_all.sh "$line")"\n">>output/kitchen_test_output.txt; 
done < input/kitchen_test_sentences.txt