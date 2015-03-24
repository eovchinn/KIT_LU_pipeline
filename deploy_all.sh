#!/bin/bash

echo -e "#!/bin/bash\n\n" > lupipeline.setenv.sh

export KIT_LU_DIR=${PWD}
echo -e "export KIT_LU_DIR=${PWD}\n" >> lupipeline.setenv.sh

export BOXER_DIR=$KIT_LU_DIR/boxer
echo -e "BOXER_DIR=$KIT_LU_DIR/boxer\n" >> lupipeline.setenv.sh

export BOXER_SOAP_SERVER=localhost:9000
echo -e "BOXER_SOAP_SERVER=localhost:9000\n" >> lupipeline.setenv.sh

export HENRY_DIR=/usr/share/henry
echo -e "HENRY_DIR=/usr/share/henry\n" >> lupipeline.setenv.sh

export GRB_LICENSE_FILE=$KIT_LU_DIR/gurobi/gurobi.lic
echo -e "GRB_LICENSE_FILE=$KIT_LU_DIR/gurobi/gurobi.lic" >> lupipeline.setenv.sh

read -p "Are you ok with adding LU pipeline env variables to your .bashrc? [yn]" answer
if [[ $answer = y ]] ; then
  echo "source $KIT_LU_DIR/lupipeline.setenv.sh" >> ~/.bashrc
fi

chmod 755 *.sh

source ./boxer/installation/install_boxer.sh
