# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


PROJECT = gsl

#--------------------------------------------------------------------------
#

all: test

test: sanity vectors

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./vector.py

vectors:
	${PYTHON} ./vector_allocate.py
	${PYTHON} ./vector_zero.py

# end of file 
