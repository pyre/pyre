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

configurations: blas cython gcc gsl hdf5 mpi postgres python vtk

blas:
	${PYTHON} ./blas.py
	${PYTHON} ./blas.py --blas=gsl
	${PYTHON} ./blas.py --blas=atlas
	${PYTHON} ./blas.py --blas=openblas

cython:
	${PYTHON} ./cython.py

gcc:
	${PYTHON} ./gcc.py

gsl:
	${PYTHON} ./gsl.py

hdf5:
	${PYTHON} ./hdf5.py

mpi:
	${PYTHON} ./mpi.py
	${PYTHON} ./mpi.py --mpi=openmpi
	${PYTHON} ./mpi.py --mpi=mpich

postgres:
	${PYTHON} ./postgres.py

python:
	${PYTHON} ./python.py
	${PYTHON} ./python.py --python=python3
	${PYTHON} ./python.py --python=python2
	${PYTHON} ./python.py --python=python2#python27

vtk:
	${PYTHON} ./vtk.py


# end of file
