#! /bin/bash

TEST_BOXER_SERVER=`./run_server_test.sh`

if [[ $TEST_BOXER_SERVER == 1* ]];
then 
	echo "Killing Boxer server";
	fuser -k -n tcp ${BOXER_SOAP_SERVER:10:5}
else 
	echo "Boxer server is not running.";
fi