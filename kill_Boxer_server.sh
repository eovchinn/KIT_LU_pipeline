#! /bin/bash

fuser -k -n tcp ${BOXER_SOAP_SERVER:10:5}