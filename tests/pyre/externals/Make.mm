# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2013 all rights reserved
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

working: manager

all: test

test: sanity manager

sanity:
	${PYTHON} ./sanity.py

manager:
	${PYTHON} ./locate.py


# end of file 
