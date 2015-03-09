#! /bin/bash

# usage:
# $ ./run_Boxer_server.sh

CANDC_SERVER_BIN=$BOXER_DIR/bin/soap_server
CANDC_SERVER_OPT="--models $BOXER_DIR/models/boxer --server $BOXER_SOAP_SERVER --candc-printer boxer"

$CANDC_SERVER_BIN $CANDC_SERVER_OPT > /dev/stdout
