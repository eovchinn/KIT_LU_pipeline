**Full installation instructions for KIT lab PCs:**

1) Install packages:

`sudo apt-get install python2.7-dev libsqlite3-dev libpcre3-dev swi-prolog`

2) Install Gurobi

a) Download Guribi
- Go to [http://www.gurobi.com/](http://www.gurobi.com/)
- Login or register your account and login
- Go to DOWNLOADS->Gurobi Software->Gurobi Optimizer
- Download Guribi *version 5.6.*
- Unpack Gurobi
`tar xvfz gurobi*...`

b) Obtain Gurobi license key
- Go to [http://www.gurobi.com/](http://www.gurobi.com/)
- Login or register your account and login
- Go to DOWNLOADS->LICENSES->UNIVERSITY LICENSE
- Accept license conditions and push REQUEST LICENSE
- run `grbgetkey LICENSE_KEY` (shown on the Gurobi web page) in terminal, make sure that you store the key (gurobi.lic) in KIT_LU_pipeline/gurobi/

3) Install Henry:

```
git clone https://github.com/naoya-i/henry-n700
make
```

4) Install KIT_LU_pipeline

- `git clone https://github.com/eovchinn/KIT_LU_pipeline`
- `cd KIT_LU_pipeline`
- `source ./deploy_all.sh` (*DON'T* allow the script to export env variables)

5) Set enviroment variables

a) Export env variables:
* export KIT_LU_DIR
* export BOXER_DIR
* export BOXER_SOAP_SERVER (for example, `export BOXER_SOAP_SERVER=localhost:9000`)
* export HENRY_DIR
* export GUROBI_HOME
* export GRB_LICENSE_FILE

b) Export paths and libs:
* `export PATH=$PATH:$HOME/bin:$GUROBI_HOME/bin`
* `export LD_LIBRARY_PATH=$LD_LIBRARY_PATH:$GUROBI_HOME/lib`
* `export LIBRARY_PATH=$LIBRARY_PATH:$GUROBI_HOME/lib`
* `export CPLUS_INCLUDE_PATH=$CPLUS_INCLUDE_PATH:$GUROBI_HOME/include`

If you use SSH, make sure that your .bash_profile starts .bashrc, otherwise env variables won't be exportet. It can be done by adding the following lines to .bash_profile:
```
if [ -f ~/.bashrc ]; then
  . ~/.bashrc
fi
```
=======

**Running standalone:**

a) start server 

`./run_Boxer_server.sh`

b) process text

 `./process_test_sentences.sh`
 
 or 
 
 `./run_all.sh "INPUT TEXT"`
 
c) stop server

 `./kill_Boxer_server.sh`
