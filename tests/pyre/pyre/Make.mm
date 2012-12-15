# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

all: test clean

test: sanity api

sanity:
	${PYTHON} ./sanity.py

api:
	${PYTHON} ./loadConfiguration.py
	${PYTHON} ./resolve.py

# end of file 
