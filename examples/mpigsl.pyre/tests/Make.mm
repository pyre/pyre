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

test: sanity distribute

sanity:
	${PYTHON} ./sanity.py

distribute:
	${PYTHON} ./collect.py
	${MPI_EXECUTIVE} -np 8 ${PYTHON} ./collect.py
	${PYTHON} ./partition.py
	${MPI_EXECUTIVE} -np 8 ${PYTHON} ./partition.py


# end of file 
