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

test: sanity units

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./exceptions.py

units:
	${PYTHON} ./one.py
	${PYTHON} ./algebra.py
	${PYTHON} ./formatting.py


# end of file 
