# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

all: test

test: sanity partition

sanity:
	${PYTHON} ./sanity.py

partition:
	${PYTHON} ./partition.py
	${MPI_EXECUTIVE} -np 8 ${PYTHON} ./partition.py

# end of file 
