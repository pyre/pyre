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

test: sanity

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./exceptions.py


# end of file 
