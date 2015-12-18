# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


PROJECT = pyre

#--------------------------------------------------------------------------
#

all: test

test: sanity manager applications

sanity:
	${PYTHON} ./sanity.py

manager:
	${PYTHON} ./locate.py

applications:
	${PYTHON} ./simple.py
	${PYTHON} ./configure.py
	${PYTHON} ./configure.py --mpi=openmpi
	${PYTHON} ./configure.py --mpi=mpich


# end of file
