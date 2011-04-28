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

test: sanity package

sanity:
	${PYTHON} ./sanity.py
	${PYTHON} ./extension.py
	${MPI_EXECUTIVE} -np 8 ${PYTHON} ./extension.py
	${PYTHON} ./world.py
	${MPI_EXECUTIVE} -np 8 ${PYTHON} ./world.py

package:
	${MPI_EXECUTIVE} -np 8 ${PYTHON} ./group.py
	${MPI_EXECUTIVE} -np 7 ${PYTHON} ./group_include.py
	${MPI_EXECUTIVE} -np 7 ${PYTHON} ./group_exclude.py



# end of file 
