# -*- Makefile -*-
#
# michael a.g. aïvázis
# california institute of technology
# (c) 1998-2012 all rights reserved
#


PROJECT = pyre
PROJ_TIDY += __pycache__

#--------------------------------------------------------------------------
#

all: test clean

test:
	${PYTHON} ./run.py


# end of file 
