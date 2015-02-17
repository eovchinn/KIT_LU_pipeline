# KIT_LU_pipeline
Language understanding pipeline for KIT.

Requirements:
* Python
* SWI-Prolog
* [Boxer](http://svn.ask.it.usyd.edu.au/trac/candc/wiki/boxer) ([subversion](http://svn.ask.it.usyd.edu.au/trac/candc/wiki/Subversion), [SOAP server](http://svn.ask.it.usyd.edu.au/trac/candc/wiki/InstallSOAP))
* [Gurobi](http://www.gurobi.com/)
* [Henry](https://github.com/naoya-i/henry-n700) or [Phillip](https://github.com/kazeto/phillip) abductive reasoning engine

Installation:
* Set the correct paths in the run_*.sh files

Running:
* start server by running `./run_Boxer_server.sh`
* process test sentences by running `./process_test_sentences.sh`
* process input text by running `./run_all.sh "INPUT TEXT"`
