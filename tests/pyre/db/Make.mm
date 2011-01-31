# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2011 all rights reserved
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

all: test

test: sanity pyrepg

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./sanity-pyrepg.py

pyrepg:
	${PYTHON} ./pyrepg-exceptions.py

# end of file 
