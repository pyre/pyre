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

test: sanity algebra structural

sanity:
	${PYTHON} ./sanity.py

algebra:
	${PYTHON} ./number.py
	${PYTHON} ./ordering.py
	${PYTHON} ./boolean.py

structural:
	${PYTHON} ./dependencies.py
	${PYTHON} ./patch.py

# end of file 
