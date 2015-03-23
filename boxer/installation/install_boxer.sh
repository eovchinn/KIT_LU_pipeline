#!/bin/bash

echo installing BOXER ...

boxer_username=e.ovchinnikova@gmail.com
boxer_password=6llm4HpL
boxer_models=models-1.02.tgz

svn co http://svn.ask.it.usyd.edu.au/candc/trunk $BOXER_DIR --username $boxer_username --password $boxer_password

tar -xzf $BOXER_DIR/installation/$boxer_models -C $BOXER_DIR

cd $BOXER_DIR

mkdir -p ext/bin
ln -s `which soapcpp2` ext/bin || true
make -f Makefile.unix
make -f Makefile.unix soap
make -f Makefile.unix bin/boxer
make -f Makefile.unix bin/tokkie

cd $KIT_LU_DIR
