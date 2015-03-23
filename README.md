# KIT_LU_pipeline
Language understanding pipeline for KIT.

**Requirements:**
* Python
* SWI-Prolog
* [Boxer](http://svn.ask.it.usyd.edu.au/trac/candc/wiki/boxer) ([subversion](http://svn.ask.it.usyd.edu.au/trac/candc/wiki/Subversion), [SOAP server](http://svn.ask.it.usyd.edu.au/trac/candc/wiki/InstallSOAP))
* [Gurobi Optimizer](http://www.gurobi.com/) (with Free Academic License)
* [Henry](https://github.com/naoya-i/henry-n700) or [Phillip](https://github.com/kazeto/phillip) abductive reasoning engine

=======

**Installation for KIT lab PCs:**

a) Run the following commands in terminal:
- `git clone https://github.com/eovchinn/KIT_LU_pipeline`
- `cd KIT_LU_pipeline`
- `source ./deploy_all.sh`

b) Obtain Gurobi license key
- Go to [http://www.gurobi.com/](http://www.gurobi.com/)
- Login or register your account and login
- Go to DOWNLOADS->LICENSES->UNIVERSITY LICENSE
- Accept license conditions and push REQUEST LICENSE
- run `grbgetkey LICENSE_KEY` (shown on the Gurobi web page) in terminal, make sure that you store the key (gurobi.lic) in KIT_LU_pipeline/gurobi/

c) Add to your .bashrc: 
- `KIT_LU_DIR=PATH_TO_KIT_LU_pipeline`
- `source PATH_TO_KIT_LU_pipeline/lupipeline.setenv.sh`

d) If you use SSH, make sure that your .bash_profile starts .bashrc, otherwise env variables won't be exportet. It can be done by adding the following lines to .bash_profile:
```
if [ -f ~/.bashrc ]; then
  . ~/.bashrc
fi
```

=======

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
