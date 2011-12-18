# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

all: test clean

test: sanity framework

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./exceptions.py
	${PYTHON} ./fileserver.py
	${PYTHON} ./binder.py
	${PYTHON} ./executive.py

framework:
	${PYTHON} ./fileserver_uri.py
	${PYTHON} ./fileserver_mount.py
	${PYTHON} ./executive_registrar.py
	${PYTHON} ./executive_uri.py
	${PYTHON} ./executive_codecs.py
	${PYTHON} ./executive_shelves.py
	${PYTHON} ./executive_configuration.py
	${PYTHON} ./executive_retrieveComponentDescriptor.py
	${PYTHON} ./executive_retrieveComponentDescriptor_duplicate.py
	${PYTHON} ./executive_retrieveComponentDescriptor_badImport.py
	${PYTHON} ./executive_retrieveComponentDescriptor_syntaxError.py


# end of file 
