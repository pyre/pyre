# -*- Makefile -*-
#
# michael a.g. aïvázis
# orthologue
# (c) 1998-2015 all rights reserved
#


PROJECT = pyre

all: test

test: sanity manager configurations

sanity:
	${PYTHON} ./sanity.py

manager:
	${PYTHON} ./locate.py

configurations: gcc gsl mpi python

gcc:
	${PYTHON} ./gcc.py

gsl:
	${PYTHON} ./gsl.py

mpi:
	${PYTHON} ./mpi.py
	${PYTHON} ./mpi.py --mpi=openmpi
	${PYTHON} ./mpi.py --mpi=mpich

python:
	${PYTHON} ./python.py


# end of file
