%:
	make -f Makefile.unix $@

all:
	mkdir -p ext/bin
	ln -s `which soapcpp2` ext/bin || true
	make -f Makefile.unix
	make -f Makefile.unix soap
	make -f Makefile.unix bin/boxer
	make -f Makefile.unix bin/tokkie
