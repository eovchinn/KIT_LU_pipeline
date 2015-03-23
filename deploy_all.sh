#!/bin/bash

./lupipeline.setenv.sh

source ./lupipeline.setenv.sh

cd boxer
./installation/install_boxer.sh
