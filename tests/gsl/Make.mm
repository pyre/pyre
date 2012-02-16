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
	${PYTHON} ./vector_fill.py
	${PYTHON} ./vector_set.py
	${PYTHON} ./vector_contains.py
	${PYTHON} ./vector_add.py
	${PYTHON} ./vector_sub.py
	${PYTHON} ./vector_mul.py
	${PYTHON} ./vector_div.py
	${PYTHON} ./vector_shift.py
	${PYTHON} ./vector_scale.py


# end of file 
