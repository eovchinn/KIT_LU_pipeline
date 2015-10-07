#! /bin/bash

# usage:
# $ ./run_client_pipeline_EN.sh <input_file> <output_dir>
# or
# $ ./run_client_pipeline_EN.sh <input_file>
# or
# $ ./run_client_pipeline_EN.sh

TOKENIZER_BIN=$BOXER_DIR/bin/tokkie
CANDC_CLIENT_BIN=/usr/share/boxer/bin/soap_client
BOXER_BIN=$BOXER_DIR/bin/boxer

TOKENIZER_OPT="--stdin"
CANDC_CLIENT_OPT="--url $BOXER_SOAP_SERVER"
BOXER_OPT="--semantics tacitus --resolve false --stdin --elimeq true --mwe yes"


if [ -d "$2" ]; then
	$TOKENIZER_BIN $TOKENIZER_OPT < "${1:-/dev/stdin}" |
	tee $2/tmp.tok |
	$CANDC_CLIENT_BIN $CANDC_CLIENT_OPT |
	tee $2/tmp.candc |
	$BOXER_BIN $BOXER_OPT > /dev/stdout
else
	$TOKENIZER_BIN $TOKENIZER_OPT < "${1:-/dev/stdin}" |
	$CANDC_CLIENT_BIN $CANDC_CLIENT_OPT |
	$BOXER_BIN $BOXER_OPT > "${2:-/dev/stdout}"
fi
