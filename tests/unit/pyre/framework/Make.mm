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

managers: curator

curator:
	${PYTHON} ./curator.py
	${PYTHON} ./curator_uri.py

framework:
	${PYTHON} ./executive.py
	${PYTHON} ./executive_fileserver.py
	${PYTHON} ./executive_codecs.py
	${PYTHON} ./executive_configuration.py


# end of file 
