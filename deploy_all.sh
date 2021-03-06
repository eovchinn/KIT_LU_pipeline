#!/bin/bash

echo -e "#!/bin/bash\n" > lupipeline.setenv.sh

export KIT_LU_DIR=${PWD}
echo "export KIT_LU_DIR=${PWD}" >> lupipeline.setenv.sh

export BOXER_DIR=/usr/share/boxer
echo "export BOXER_DIR=/usr/share/boxer" >> lupipeline.setenv.sh

export BOXER_SOAP_SERVER=localhost:38900
echo "export BOXER_SOAP_SERVER=localhost:38900" >> lupipeline.setenv.sh

export HENRY_DIR=/usr/share/henry
echo "export HENRY_DIR=/usr/share/henry" >> lupipeline.setenv.sh

export PHILLIP_DIR=/usr
echo "export PHILLIP_DIR=/usr" >> lupipeline.setenv.sh

export GRB_LICENSE_FILE=$KIT_LU_DIR/gurobi/gurobi.lic
echo "export GRB_LICENSE_FILE=$KIT_LU_DIR/gurobi/gurobi.lic" >> lupipeline.setenv.sh

read -p "Are you ok with adding LU pipeline env variables to your .bashrc? [yn]" answer
if [[ $answer = y ]] ; then
  echo "source $KIT_LU_DIR/lupipeline.setenv.sh" >> ~/.bashrc
fi

chmod 755 *.sh
