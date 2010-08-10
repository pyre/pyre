# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2010 all rights reserved
#
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

all: test

test: sanity types

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./exceptions.py

types:
	${PYTHON} ./array.py
	${PYTHON} ./boolean.py
	${PYTHON} ./dimensional.py
	${PYTHON} ./float.py
	${PYTHON} ./int.py


# end of file 
