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

types:
	${PYTHON} ./float.py


# end of file 
