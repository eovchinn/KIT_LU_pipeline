#!/bin/bash

export KIT_LU_DIR=${PWD}
source ${PWD}/lupipeline.setenv.sh

read -p "Are you ok with adding LU pipeline env variables to your .bashrc? [yn]" answer
if [[ $answer = y ]] ; then
  echo "export KIT_LU_DIR=${PWD}" >> ~/.bashrc
  echo "source $KIT_LU_DIR/lupipeline.setenv.sh" >> ~/.bashrc
fi

source ./boxer/installation/install_boxer.sh
