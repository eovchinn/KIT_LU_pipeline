#! /bin/bash

# usage:
# $ ./run_server_test.sh

CANDC_CLIENT_BIN=$BOXER_DIR/bin/soap_client
CANDC_CLIENT_OPT="--url localhost:9000"

check_str() {
	read s
	if [ ! -z "$s" ]; then
		echo "0"
	else
		echo "1"
	fi
}

echo "Test" |
$CANDC_CLIENT_BIN $CANDC_CLIENT_OPT  2>&1 |
grep "Connection refused" |
check_str > /dev/stdout
