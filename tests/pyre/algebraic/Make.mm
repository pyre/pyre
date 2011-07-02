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

test: sanity algebra logic

sanity:
	${PYTHON} ./sanity.py

algebra:
	${PYTHON} ./algebra.py
	${PYTHON} ./dependencies.py
	${PYTHON} ./patch.py

logic:
	${PYTHON} ./logic.py

# end of file 
