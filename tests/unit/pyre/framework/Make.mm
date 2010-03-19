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

test: sanity framework

sanity:
	${PYTHON} ./sanity.py

framework:
	${PYTHON} ./executive.py
	${PYTHON} ./executive_fileserver.py


# end of file 
