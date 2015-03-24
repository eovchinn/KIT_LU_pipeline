#! /bin/bash

# usage:
# $ ./run_Boxer_server.sh

TEST_BOXER_SERVER=`./run_server_test.sh`

if [[ $TEST_BOXER_SERVER == 1* ]];
then 
	echo "Boxer server is already running on $BOXER_SOAP_SERVER";
else 
	TEST_PORT=`netstat -an |grep $BOXER_SOAP_SERVER |grep LISTEN`

	if [ -z "$TEST_PORT" ]; then
		CANDC_SERVER_BIN=$BOXER_DIR/bin/soap_server
		CANDC_SERVER_OPT="--models $BOXER_DIR/models/boxer --server $BOXER_SOAP_SERVER --candc-printer boxer"
		$CANDC_SERVER_BIN $CANDC_SERVER_OPT > /dev/stdout
	else echo "Port $BOXER_SOAP_SERVER is occupied";
	fi
fi


