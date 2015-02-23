# KIT_LU_pipeline
Language understanding pipeline for KIT.

**Requirements:**
* Python
* SWI-Prolog
* [Boxer](http://svn.ask.it.usyd.edu.au/trac/candc/wiki/boxer) ([subversion](http://svn.ask.it.usyd.edu.au/trac/candc/wiki/Subversion), [SOAP server](http://svn.ask.it.usyd.edu.au/trac/candc/wiki/InstallSOAP))
* [Gurobi](http://www.gurobi.com/)
* [Henry](https://github.com/naoya-i/henry-n700) or [Phillip](https://github.com/kazeto/phillip) abductive reasoning engine

=======

**Installation:**

a) Export env variables:
* export KIT_LU_DIR
* export BOXER_DIR
* export HENRY_DIR
* export PHILLIP_DIR
* export GUROBI_HOME
* export GRB_LICENSE_FILE

b) Export paths and libs:
* export PATH=$PATH:$HOME/bin:$GUROBI_HOME/bin
* export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$GUROBI_HOME/lib
* export LIBRARY_PATH=$LIBRARY_PATH:$GUROBI_HOME/lib
* export CPLUS_INCLUDE_PATH=$CPLUS_INCLUDE_PATH:$GUROBI_HOME/include

=======

**Running:**
* start server by running `./run_Boxer_server.sh`
* process test sentences by running `./process_test_sentences.sh`
* process input text by running `./run_all.sh "INPUT TEXT"`
