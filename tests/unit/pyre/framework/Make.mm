# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

all: test

test: sanity managers framework

sanity:
	${PYTHON} ./sanity.py

managers: binder fileserver

binder:
	${PYTHON} ./binder.py

fileserver:
	${PYTHON} ./fileserver.py
	${PYTHON} ./fileserver_uri.py
	${PYTHON} ./fileserver_mount.py

framework:
	${PYTHON} ./executive.py
	${PYTHON} ./executive_registrar.py
	${PYTHON} ./executive_codecs.py
	${PYTHON} ./executive_configuration.py


# end of file 
