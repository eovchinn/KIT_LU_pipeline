# KIT_LU_pipeline
Language understanding pipeline for KIT.

**Requirements:**
* Python
* SWI-Prolog
* [Boxer](http://svn.ask.it.usyd.edu.au/trac/candc/wiki/boxer) ([subversion](http://svn.ask.it.usyd.edu.au/trac/candc/wiki/Subversion), [SOAP server](http://svn.ask.it.usyd.edu.au/trac/candc/wiki/InstallSOAP))
* [Gurobi Optimizer](http://www.gurobi.com/) (with Free Academic License)
* [Henry](https://github.com/naoya-i/henry-n700) or [Phillip](https://github.com/kazeto/phillip) abductive reasoning engine

=======

**Installation for KIT lap PCs:**

a) Run the following commands in terminal:
`git clone https://github.com/eovchinn/KIT_LU_pipeline`
`cd KIT_LU_pipeline`
`./deploy_all.sh`

b) Obtain Gurobi licence key
- Go to (http://www.gurobi.com/)(http://www.gurobi.com/)
- Login using login/password `kit.user@inbox.com/lupipeline` or register your own account
- Go to DOWNLOADS->LINCENCES->UNIVERSITY LICENSE
- Accept licence conditions and push REQUEST LICENSE
- run `grbgetkey LICENSE_KEY` in terminal, make sure that you store the key under KIT_LU_pipelin/gurobi/gurobi.lic

**Installation (general):**

a) Export env variables:
* export KIT_LU_DIR
* export BOXER_DIR
* export BOXER_SOAP_SERVER (for example, `export BOXER_SOAP_SERVER=localhost:9000`)
* export HENRY_DIR
* export PHILLIP_DIR
* export GUROBI_HOME
* export GRB_LICENSE_FILE

b) Export paths and libs:
* `export PATH=$PATH:$HOME/bin:$GUROBI_HOME/bin`
* `export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$GUROBI_HOME/lib`
* `export LIBRARY_PATH=$LIBRARY_PATH:$GUROBI_HOME/lib`
* `export CPLUS_INCLUDE_PATH=$CPLUS_INCLUDE_PATH:$GUROBI_HOME/include`
=======

**Running:**
* start server by running `./run_Boxer_server.sh`
* process test sentences by running `./process_test_sentences.sh`
* process input text by running `./run_all.sh "INPUT TEXT"`
